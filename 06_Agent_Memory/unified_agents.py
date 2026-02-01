"""Multi-agent wellness system with handoff capabilities and all 5 CoALA memory types.

This module provides a unified multi-agent wellness system where Exercise, Nutrition,
and Sleep specialists can collaborate through a shared memory store.

Memory Types Implemented:
1. SHORT-TERM: MemorySaver + thread_id (conversation history)
2. LONG-TERM: InMemoryStore + namespaces (user profile, preferences)
3. SEMANTIC: Store + embeddings + search() (knowledge retrieval)
4. EPISODIC: Store + few-shot examples (past interactions)
5. PROCEDURAL: Store + self-reflection (self-improving instructions)
"""

from enum import Enum
from typing import Annotated
from uuid import uuid4
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.store.base import BaseStore
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent


# Constants
MAX_TRANSFERS = 8

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class AgentName(Enum):
    """Enum for agent names used in namespaces."""
    EXERCISE = "exercise_agent"
    NUTRITION = "nutrition_agent"
    SLEEP = "sleep_agent"


class UnifiedState(TypedDict):
    """State schema for the multi-agent wellness system."""
    messages: Annotated[list, add_messages]
    user_id: str
    feedback: str
    current_agent: str
    transfer_count: int
    visited_agents: list  # Track which agents have already responded to prevent ping-pong


# System prompts for each specialist
EXERCISE_SYSTEM_PROMPT = """You are an Exercise Specialist. Your job is to provide fitness and workout guidance.

CRITICAL RULES - READ CAREFULLY:
1. ALWAYS provide a complete exercise/fitness answer if the question mentions exercise, workouts, or fitness
2. DO NOT use transfer tools for multi-topic questions - just answer YOUR part fully
3. ONLY transfer if the ENTIRE question has NOTHING to do with exercise/fitness

For a question like "Give me an exercise, nutrition, and sleep plan":
- You MUST provide a complete exercise plan
- DO NOT transfer to nutrition or sleep - they will handle their parts separately
- The system will automatically route to other specialists after you respond

Your response should be a complete, actionable exercise recommendation."""

NUTRITION_SYSTEM_PROMPT = """You are a Nutrition Specialist. Your job is to provide diet and meal planning guidance.

CRITICAL RULES - READ CAREFULLY:
1. ALWAYS provide a complete nutrition/diet answer if the question mentions food, diet, nutrition, or meals
2. DO NOT use transfer tools for multi-topic questions - just answer YOUR part fully
3. ONLY transfer if the ENTIRE question has NOTHING to do with nutrition/diet

For a question like "Give me an exercise, nutrition, and sleep plan":
- You MUST provide a complete nutrition plan
- DO NOT transfer to exercise or sleep - they will handle their parts separately
- The system will automatically route to other specialists after you respond

Your response should be a complete, actionable nutrition recommendation."""

SLEEP_SYSTEM_PROMPT = """You are a Sleep Specialist. Your job is to provide sleep and rest optimization guidance.

CRITICAL RULES - READ CAREFULLY:
1. ALWAYS provide a complete sleep/rest answer if the question mentions sleep, rest, insomnia, or fatigue
2. DO NOT use transfer tools for multi-topic questions - just answer YOUR part fully
3. ONLY transfer if the ENTIRE question has NOTHING to do with sleep/rest

For a question like "Give me an exercise, nutrition, and sleep plan":
- You MUST provide a complete sleep plan
- DO NOT transfer to exercise or nutrition - they will handle their parts separately
- The system will automatically route to other specialists after you respond

Your response should be a complete, actionable sleep recommendation."""


# Transfer tools
@tool
def transfer_to_exercise(reason: str) -> str:
    """Transfer to Exercise Specialist for fitness, workouts, and physical activity questions.
    
    Args:
        reason: Why you're transferring to this specialist
    """
    return f"HANDOFF:exercise:{reason}"


@tool
def transfer_to_nutrition(reason: str) -> str:
    """Transfer to Nutrition Specialist for diet, meal planning, and food questions.
    
    Args:
        reason: Why you're transferring to this specialist
    """
    return f"HANDOFF:nutrition:{reason}"


@tool
def transfer_to_sleep(reason: str) -> str:
    """Transfer to Sleep Specialist for sleep quality, insomnia, and rest questions.
    
    Args:
        reason: Why you're transferring to this specialist
    """
    return f"HANDOFF:sleep:{reason}"


# Search functions for each agent
def search_exercise_info(question: str) -> str:
    """Search the exercise knowledge base for information relevant to the question."""
    return []


def search_nutrition_info(question: str) -> str:
    """Search the nutrition knowledge base for information relevant to the question."""
    return []


def search_sleep_info(question: str) -> str:
    """Search the sleep knowledge base for information relevant to the question."""
    return []


def parse_handoff(content: str) -> tuple[bool, str, str]:
    """Parse a handoff from agent response."""
    if "HANDOFF:" in content:
        parts = content.split("HANDOFF:")[1].split(":")
        return True, parts[0], parts[1] if len(parts) > 1 else ""
    return False, "", ""


def get_last_human_message(messages: list) -> str:
    """Get the last human message from the conversation."""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            return msg.content
    return ""


def get_relevant_agents_for_question(question: str) -> list:
    """Determine which agents are relevant for a given question."""
    question_lower = question.lower()
    relevant_agents = []
    
    if any(kw in question_lower for kw in ["exercise", "workout", "fitness", "physical", "training", "gym"]):
        relevant_agents.append("exercise")
    if any(kw in question_lower for kw in ["nutrition", "diet", "food", "eat", "meal", "calorie"]):
        relevant_agents.append("nutrition")
    if any(kw in question_lower for kw in ["sleep", "rest", "insomnia", "fatigue", "tired", "nap"]):
        relevant_agents.append("sleep")
    
    return relevant_agents


def get_next_unvisited_agent(visited: list, current: str, messages: list) -> str:
    """Determine the next agent to visit based on the CURRENT question and what's been visited."""
    current_question = get_last_human_message(messages)
    relevant_agents = get_relevant_agents_for_question(current_question)
    
    print(f"[ROUTING] Current question: '{current_question[:50]}...' -> Relevant agents: {relevant_agents}")
    print(f"[ROUTING] Already visited: {visited}")
    
    for agent in relevant_agents:
        if agent not in visited and agent != current:
            return agent
    
    return "done"


def summarize_conversation(messages: list, max_messages: int = 6) -> list:
    """Summarize older messages to manage context length."""
    if len(messages) <= max_messages:
        return messages
    
    system_msg = messages[0] if isinstance(messages[0], SystemMessage) else None
    content_messages = messages[1:] if system_msg else messages
    
    if len(content_messages) <= max_messages:
        return messages
    
    old_messages = content_messages[:-max_messages+1]
    recent_messages = content_messages[-max_messages+1:]
    
    summary_prompt = f"""Summarize this conversation in 2-3 sentences, 
capturing key wellness topics discussed and any important user information:

{chr(10).join([f'{type(m).__name__}: {m.content[:200]}' for m in old_messages])}"""
    
    summary = llm.invoke(summary_prompt)
    
    result = []
    if system_msg:
        result.append(system_msg)
    result.append(SystemMessage(content=f"[Previous conversation summary: {summary.content}]"))
    result.extend(recent_messages)
    
    return result


def seed_store_if_needed(store: BaseStore, user_id: str = "user_sarah"):
    """Seed the store with initial data if not already present."""
    # Check if already seeded
    existing = store.get((user_id, "profile"), "name")
    if existing:
        return  # Already seeded
    
    # Seed user profile
    profile_namespace = (user_id, "profile")
    preferences_namespace = (user_id, "preferences")
    
    store.put(profile_namespace, "name", {"value": "Sarah"})
    store.put(profile_namespace, "goals", {"primary": "improve sleep", "secondary": "reduce stress"})
    store.put(profile_namespace, "conditions", {"allergies": ["peanuts"], "injuries": ["bad knee"]})
    store.put(preferences_namespace, "communication", {"style": "friendly", "detail_level": "moderate"})
    store.put(preferences_namespace, "schedule", {"preferred_workout_time": "morning", "available_days": ["Mon", "Wed", "Fri"]})
    
    # Seed instructions for each agent
    store.put(
        (AgentName.EXERCISE.value, "instructions"),
        "wellness_assistant",
        {"instructions": EXERCISE_SYSTEM_PROMPT, "version": 1}
    )
    store.put(
        (AgentName.NUTRITION.value, "instructions"),
        "wellness_assistant",
        {"instructions": NUTRITION_SYSTEM_PROMPT, "version": 1}
    )
    store.put(
        (AgentName.SLEEP.value, "instructions"),
        "wellness_assistant",
        {"instructions": SLEEP_SYSTEM_PROMPT, "version": 1}
    )
    
    print("Seeded store with user profile and agent instructions")


def build_memory_context(state: UnifiedState, agent_name: str, store: BaseStore) -> str:
    """Build enriched system prompt using all 5 CoALA memory types."""
    user_id = state.get("user_id", "unknown")
    user_message = state["messages"][-1].content if state["messages"] else ""
    
    agent_namespace = {
        "exercise": AgentName.EXERCISE.value,
        "nutrition": AgentName.NUTRITION.value,
        "sleep": AgentName.SLEEP.value
    }.get(agent_name, agent_name)
    
    # 1. PROCEDURAL: Get current instructions from store
    instructions_item = store.get((agent_namespace, "instructions"), "wellness_assistant")
    base_instructions = instructions_item.value["instructions"] if instructions_item else f"You are a {agent_name} wellness specialist."
    instr_version = instructions_item.value.get("version", 1) if instructions_item else 1
    
    if instr_version > 1:
        print(f"[{agent_name.upper()}] Using UPDATED instructions (v{instr_version}) - modified by previous feedback")
    
    # 2. LONG-TERM: Get user profile
    profile_items = list(store.search((user_id, "profile")))
    pref_items = list(store.search((user_id, "preferences")))
    profile_text = "\n".join([f"- {p.key}: {p.value}" for p in profile_items]) if profile_items else "No profile stored."
    prefs_text = "\n".join([f"- {p.key}: {p.value}" for p in pref_items]) if pref_items else ""
    if prefs_text:
        profile_text += f"\n\nPreferences:\n{prefs_text}"
    
    # 3. SEMANTIC: Search for relevant knowledge
    relevant_knowledge = list(store.search(("wellness", "knowledge"), query=user_message, limit=2))
    knowledge_text = "\n".join([f"- {r.value.get('text', str(r.value))[:200]}..." for r in relevant_knowledge]) if relevant_knowledge else "No specific knowledge found."
    
    # 4. EPISODIC: Find similar past interactions
    similar_episodes = list(store.search((agent_namespace, "episodes"), query=user_message, limit=1))
    if similar_episodes:
        ep = similar_episodes[0].value
        episode_text = f"Similar past interaction:\nUser: {ep.get('input', 'N/A')}\nResponse style: {ep.get('feedback', 'N/A')}"
    else:
        episode_text = "No similar past interactions found."
    
    system_message = f"""{base_instructions}

=== USER PROFILE (Long-term Memory) ===
{profile_text}

=== RELEVANT WELLNESS KNOWLEDGE (Semantic Memory) ===
{knowledge_text}

=== LEARNING FROM EXPERIENCE (Episodic Memory) ===
{episode_text}

Use all of this context to provide the best possible personalized response."""
    
    return system_message


def store_episode(store: BaseStore, agent_name: str, user_input: str, agent_response: str, feedback: str = None):
    """Store an episode in episodic memory for future learning."""
    agent_namespace = {
        "exercise": AgentName.EXERCISE.value,
        "nutrition": AgentName.NUTRITION.value,
        "sleep": AgentName.SLEEP.value
    }.get(agent_name, agent_name)
    
    episode_id = f"episode_{uuid4().hex[:8]}"
    episode_data = {
        "input": user_input[:500],
        "response": agent_response[:500],
        "feedback": feedback or "no feedback",
        "timestamp": str(uuid4())
    }
    
    store.put(
        (agent_namespace, "episodes"),
        episode_id,
        episode_data
    )
    print(f"[EPISODIC] Stored episode for {agent_name}: {episode_id}")
    return episode_id


def print_memory_report(store, user_id: str = None):
    """Print a debug report of the current memory state."""
    print("\n" + "="*60)
    print("MEMORY STATE REPORT")
    print("="*60)
    
    profile_items = list(store.search((user_id, "profile")))
    profile_text = "\n".join([f"- {p.key}: {p.value}" for p in profile_items]) if profile_items else "No profile stored."   
    print(f"User Profile:\n{profile_text}")

    for agent_name in [AgentName.EXERCISE.value, AgentName.NUTRITION.value, AgentName.SLEEP.value]:
        item = store.get((agent_name, "instructions"), "wellness_assistant")
        if item is None:
            print(f"No instructions found for {agent_name}")
        else:
            instr = item.value['instructions']
            truncated = f"{instr[:50]}...{instr[-50:]}" if len(instr) > 100 else instr
            print(f"{agent_name.capitalize()} Instructions: {truncated}")

    print("\n--- Agent Episodes (Episodic Memory) ---")
    for agent_name in [AgentName.EXERCISE.value, AgentName.NUTRITION.value, AgentName.SLEEP.value]:
        episodes = list(store.search((agent_name, "episodes"), limit=5))
        if episodes:
            print(f"{agent_name} Episodes ({len(episodes)}):")
            for ep in episodes:
                ep_str = str(ep.value)
                truncated = f"{ep_str[:80]}..." if len(ep_str) > 80 else ep_str
                print(f"  - {ep.key}: {truncated}")
        else:
            print(f"  {agent_name}: No episodes stored")

    namespace_counts = {
        "profile": len(list(store.search((user_id, "profile")))),
        "preferences": len(list(store.search((user_id, "preferences")))),
        "instructions": len(list(store.search((user_id, "instructions")))),
        "episodes": len(list(store.search((user_id, "episodes"))))
    }
    print(f"Namespace counts: {namespace_counts}")
    
    print("="*60 + "\n")


# Create agents at module level (they don't need store)
exercise_handoff_agent = create_agent(
    model=llm,
    tools=[search_exercise_info, transfer_to_nutrition, transfer_to_sleep],
    system_prompt=EXERCISE_SYSTEM_PROMPT
)

nutrition_handoff_agent = create_agent(
    model=llm,
    tools=[search_nutrition_info, transfer_to_exercise, transfer_to_sleep],
    system_prompt=NUTRITION_SYSTEM_PROMPT
)

sleep_handoff_agent = create_agent(
    model=llm,
    tools=[search_sleep_info, transfer_to_exercise, transfer_to_nutrition],
    system_prompt=SLEEP_SYSTEM_PROMPT
)


# Node functions that receive store via dependency injection
def exercise_node(state: UnifiedState, config: RunnableConfig, *, store: BaseStore):
    """Exercise specialist node with memory integration."""
    return _process_agent_node(state, config, store, exercise_handoff_agent, "exercise")


def nutrition_node(state: UnifiedState, config: RunnableConfig, *, store: BaseStore):
    """Nutrition specialist node with memory integration."""
    return _process_agent_node(state, config, store, nutrition_handoff_agent, "nutrition")


def sleep_node(state: UnifiedState, config: RunnableConfig, *, store: BaseStore):
    """Sleep specialist node with memory integration."""
    return _process_agent_node(state, config, store, sleep_handoff_agent, "sleep")


def _process_agent_node(state: UnifiedState, config: RunnableConfig, store: BaseStore, agent, name: str):
    """Common logic for all agent nodes."""
    print(f"\n[{name.upper()} Agent] Processing...")
    
    # Seed store if needed (first time setup)
    user_id = state.get("user_id", "user_sarah")
    seed_store_if_needed(store, user_id)
    
    # Mark this agent as visited
    visited = state.get("visited_agents", []) + [name]
    
    # BUILD MEMORY CONTEXT
    memory_enriched_prompt = build_memory_context(state, name, store)
    print(f"[{name.upper()}] Memory context loaded ({len(memory_enriched_prompt)} chars)")
    
    # Prepare messages with memory-enriched system prompt
    trimmed_messages = summarize_conversation(state["messages"], max_messages=6)
    enriched_messages = [SystemMessage(content=memory_enriched_prompt)] + trimmed_messages
    
    # Call agent
    result = agent.invoke({"messages": enriched_messages})
    last_message = result["messages"][-1]
    
    # Check for handoff
    transfer_count = state.get("transfer_count", 0)
    if transfer_count < MAX_TRANSFERS:
        for msg in result["messages"]:
            if hasattr(msg, 'content') and "HANDOFF:" in str(msg.content):
                is_handoff, target, reason = parse_handoff(str(msg.content))
                if is_handoff and target not in visited:
                    print(f"[{name.upper()}] Handing off to {target}: {reason}")
                    return {
                        "messages": [AIMessage(content=f"[{name}] Transferring to {target} specialist: {reason}")],
                        "current_agent": target,
                        "transfer_count": transfer_count + 1,
                        "visited_agents": visited
                    }
                elif is_handoff:
                    print(f"[{name.upper()}] Skipping handoff to {target} - already visited")
    
    # Get next agent
    next_agent = get_next_unvisited_agent(visited, name, state["messages"])
    
    response = AIMessage(
        content=f"[{name.upper()} SPECIALIST]\n\n{last_message.content}",
        name=name
    )
    
    # Store episode
    original_user_input = get_last_human_message(state["messages"])
    store_episode(store, name, original_user_input, last_message.content, feedback=None)
    
    print(f"[{name.upper()} Agent] Response complete. Next: {next_agent}")
    
    return {
        "messages": [response],
        "current_agent": next_agent,
        "transfer_count": transfer_count,
        "visited_agents": visited
    }


def entry_router(state: UnifiedState, config: RunnableConfig, *, store: BaseStore):
    """Initial routing based on the user's question."""
    # Seed store if needed
    user_id = state.get("user_id", "user_sarah")
    seed_store_if_needed(store, user_id)
    
    user_question = state['messages'][-1].content
    
    router_prompt = f"""Based on this question, which specialist should handle it?
Options: exercise, nutrition, sleep

Question: {user_question}

Respond with just the specialist name (one word)."""
    
    response = llm.invoke(router_prompt)
    agent = response.content.strip().lower()

    if agent not in ["exercise", "nutrition", "sleep"]:
        agent = "exercise"
    
    print(f"Router: Initial routing to: {agent}")
    return {"current_agent": agent, "transfer_count": 0, "visited_agents": []}


def get_last_responding_agent(messages: list) -> str:
    """Find the last agent that actually responded (has a name attribute)."""
    for msg in reversed(messages):
        if hasattr(msg, 'name') and msg.name and msg.name in ["exercise", "nutrition", "sleep"]:
            return msg.name
    return "exercise"  # Default fallback


def extract_conditions_from_feedback(feedback: str) -> list:
    """Use LLM to extract any health conditions mentioned in feedback."""
    extraction_prompt = f"""Analyze this user feedback and extract any NEW health conditions, injuries, or physical limitations mentioned.

Feedback: "{feedback}"

If conditions are mentioned (like "shoulder pain", "back injury", "bad wrist"), return them as a comma-separated list.
If no conditions are mentioned, return "NONE".

Examples:
- "that would hurt my shoulder" -> "shoulder pain"
- "I have a bad back and can't do that" -> "back injury"
- "that looks great!" -> "NONE"

Return ONLY the conditions or "NONE":"""
    
    response = llm.invoke(extraction_prompt)
    result = response.content.strip()
    
    if result.upper() == "NONE" or not result:
        return []
    
    # Parse comma-separated conditions
    conditions = [c.strip() for c in result.split(",") if c.strip()]
    return conditions


def feedback_node(state: UnifiedState, config: RunnableConfig, *, store: BaseStore):
    """Process feedback: update procedural memory, episodic memory, AND user profile."""
    feedback = state.get("feedback", "")
    if not feedback:
        return {}
    
    print(f"\n{'='*60}")
    print(f"[FEEDBACK PROCESSING]")
    print(f"{'='*60}")
    print(f"Feedback received: \"{feedback}\"")
    
    messages = state.get("messages", [])
    user_id = state.get("user_id", "user_sarah")
    
    # Find the ACTUAL last agent that responded (not the routing state)
    target_agent = get_last_responding_agent(messages)
    print(f"Applying feedback to agent: {target_agent}")
    
    agent_namespace = {
        "exercise": AgentName.EXERCISE.value,
        "nutrition": AgentName.NUTRITION.value,
        "sleep": AgentName.SLEEP.value
    }.get(target_agent, target_agent)
    
    # Extract user input and agent response for episode storage
    user_input = ""
    agent_response = ""
    for msg in reversed(messages):
        if hasattr(msg, 'name') and msg.name and not agent_response:
            agent_response = msg.content[:500]
        elif isinstance(msg, HumanMessage) and not user_input:
            user_input = msg.content[:500]
        if user_input and agent_response:
            break
    
    # 1. EPISODIC MEMORY: Store episode with feedback
    if user_input or agent_response:
        store_episode(store, target_agent, user_input, agent_response, feedback)
    
    # 2. LONG-TERM MEMORY: Extract and store any new health conditions
    new_conditions = extract_conditions_from_feedback(feedback)
    if new_conditions:
        print(f"[PROFILE] New conditions detected: {new_conditions}")
        # Get existing conditions
        existing_item = store.get((user_id, "profile"), "conditions")
        if existing_item:
            existing_conditions = existing_item.value.copy()
            # Handle both list and dict formats
            if isinstance(existing_conditions, dict):
                if "injuries" in existing_conditions:
                    existing_conditions["injuries"].extend(new_conditions)
                else:
                    existing_conditions["injuries"] = new_conditions
            else:
                existing_conditions = {"injuries": new_conditions}
        else:
            existing_conditions = {"injuries": new_conditions}
        
        # Update profile with new conditions
        store.put((user_id, "profile"), "conditions", existing_conditions)
        print(f"[PROFILE] Updated conditions: {existing_conditions}")
    
    # 3. PROCEDURAL MEMORY: Update agent instructions based on feedback
    item = store.get((agent_namespace, "instructions"), "wellness_assistant")
    if item:
        current = item.value
        reflection_prompt = f"""Update these instructions based on user feedback:

Current Instructions: {current['instructions']}
User Feedback: {feedback}

Incorporate this feedback to improve future responses. For example:
- If feedback mentions pain or injury, add instructions to be more careful about that body part
- If feedback is positive, reinforce the approach used
- Be specific about modifications needed

Output only the updated instructions."""
        
        response = llm.invoke([HumanMessage(content=reflection_prompt)])
        new_instructions = response.content
        new_version = current["version"] + 1
        store.put(
            (agent_namespace, "instructions"),
            "wellness_assistant",
            {"instructions": new_instructions, "version": new_version}
        )
        print(f"\n[PROCEDURAL] {target_agent} instructions updated to v{new_version}")
        print(f"  Old instructions (first 100 chars): {current['instructions'][:100]}...")
        print(f"  New instructions (first 100 chars): {new_instructions[:100]}...")
        print(f"{'='*60}\n")
    
    return {"feedback": ""}


def route_by_current_agent(state: UnifiedState) -> str:
    """Route based on current_agent field."""
    return state.get("current_agent", "exercise")


def entry_route(state: UnifiedState) -> str:
    """Route at entry: process feedback first if provided, otherwise go to router."""
    if state.get("feedback"):
        print("[ENTRY] Feedback detected, processing first...")
        return "feedback"
    return "router"


def feedback_route(state: UnifiedState) -> str:
    """Route after feedback processing."""
    return "router"


def create_unified_graph(use_local_memory: bool = False):
    """Create the unified multi-agent wellness graph.
    
    Args:
        use_local_memory: If True, creates local checkpointer/store.
            Set to False for LangGraph API deployment.
    
    Returns:
        Compiled LangGraph (and store if use_local_memory=True)
    """
    # Build the graph
    builder = StateGraph(UnifiedState)
    
    builder.add_node("feedback", feedback_node)
    builder.add_node("router", entry_router)
    builder.add_node("exercise", exercise_node)
    builder.add_node("nutrition", nutrition_node)
    builder.add_node("sleep", sleep_node)

    # Entry point
    builder.add_conditional_edges(START, entry_route, {"feedback": "feedback", "router": "router"})

    # Router to agents
    builder.add_conditional_edges(
        "router",
        route_by_current_agent,
        {"exercise": "exercise", "nutrition": "nutrition", "sleep": "sleep"}
    )

    # Agents can handoff to each other or end
    for agent_name in ["exercise", "nutrition", "sleep"]:
        builder.add_conditional_edges(
            agent_name,
            route_by_current_agent,
            {
                "exercise": "exercise",
                "nutrition": "nutrition", 
                "sleep": "sleep",
                "feedback": "feedback",
                "done": END
            }
        )

    # Feedback goes back to router
    builder.add_conditional_edges("feedback", feedback_route, {"router": "router"})
    builder.add_edge("router", END)
    
    # Compile
    if use_local_memory:
        store = InMemoryStore()
        checkpointer = MemorySaver()
        return builder.compile(checkpointer=checkpointer, store=store), store
    else:
        # For LangGraph API - NO store passed, platform injects it
        return builder.compile()


# Create graph for LangGraph API/Studio (no custom store)
unified_graph = create_unified_graph(use_local_memory=False)

# For local testing
_local_graph = None
_local_store = None


def get_local_graph():
    """Get or create a local testing graph with in-memory persistence."""
    global _local_graph, _local_store
    if _local_graph is None:
        _local_graph, _local_store = create_unified_graph(use_local_memory=True)
    return _local_graph, _local_store


def chat(message: str, user_id: str = "user_sarah", thread_id: str = "default_thread", feedback: str = "") -> str:
    """Quick chat function for testing.
    
    Args:
        message: The user's message
        user_id: The user identifier
        thread_id: The conversation thread identifier
        feedback: Optional feedback about previous response
    
    Returns:
        The assistant's response
    """
    graph, store = get_local_graph()
    config = {"configurable": {"thread_id": thread_id}}
    response = graph.invoke(
        {
            "messages": [HumanMessage(content=message)],
            "user_id": user_id,
            "feedback": feedback,
            "current_agent": "",
            "transfer_count": 0,
            "visited_agents": []
        },
        config,
    )
    return response["messages"][-1].content


if __name__ == "__main__":
    print("Testing Unified Multi-Agent Wellness System")
    print("=" * 50)
    
    graph, store = get_local_graph()
    
    # Initial memory state
    print("\n=== INITIAL MEMORY STATE ===")
    print_memory_report(store, "user_sarah")
    
    # Test conversation
    response = chat(
        "Can you give me an exercise, nutrition and sleep plan for the next 3 months?",
        thread_id="test_1"
    )
    print(f"\nResponse:\n{response}")
    
    # Final memory state
    print("\n=== FINAL MEMORY STATE ===")
    print_memory_report(store, "user_sarah")
