"""
Memory Dashboard for Multi-Agent Wellness System

A Streamlit dashboard that shows:
1. Current user profile
2. Recent memories from each agent
3. Cross-agent memory sharing statistics
4. Memory search interface

USAGE:
1. Run your notebook cells to generate memory state
2. Run the last cell to export state: export_store_state(store, "user_sarah")
3. Run: streamlit run memory_dashboard.py
"""

import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
from enum import Enum
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver


# ============================================================
# State File Configuration
# ============================================================
STATE_FILE = Path(__file__).parent / "memory_state.json"


# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="Wellness Memory Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #5A7A9A;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
    }
    .agent-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    .episode-card {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# Agent Configuration
# ============================================================
class AgentName(Enum):
    EXERCISE = "exercise_agent"
    NUTRITION = "nutrition_agent"
    SLEEP = "sleep_agent"


AGENT_COLORS = {
    "exercise_agent": "#FF6B6B",
    "nutrition_agent": "#4ECDC4",
    "sleep_agent": "#9B59B6"
}

AGENT_ICONS = {
    "exercise_agent": "🏃",
    "nutrition_agent": "🥗",
    "sleep_agent": "😴"
}


# ============================================================
# Store Initialization (loads from notebook export)
# ============================================================
def load_store_from_file(file_path: Path) -> tuple[InMemoryStore, dict]:
    """Load store state from exported JSON file."""
    store = InMemoryStore()
    metadata = {}
    
    if file_path.exists():
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Get metadata and include memory access stats
        metadata = data.get("metadata", {})
        metadata["memory_access_stats"] = data.get("memory_access_stats", {})
        
        # Reconstruct store from exported data
        for namespace_key, items in data.get("namespaces", {}).items():
            # Parse namespace tuple from string key
            namespace = tuple(namespace_key.split("::"))
            for key, value in items.items():
                store.put(namespace, key, value)
    
    return store, metadata


def create_demo_store() -> InMemoryStore:
    """Create a demo store with sample data if no export file exists."""
    store = InMemoryStore()
    
    user_id = "user_sarah"
    profile_namespace = (user_id, "profile")
    preferences_namespace = (user_id, "preferences")
    
    store.put(profile_namespace, "name", {"value": "Sarah"})
    store.put(profile_namespace, "goals", {"primary": "improve sleep", "secondary": "reduce stress"})
    store.put(profile_namespace, "conditions", {"allergies": ["peanuts"], "injuries": ["bad knee"]})
    
    store.put(preferences_namespace, "communication", {"style": "friendly", "detail_level": "moderate"})
    store.put(preferences_namespace, "schedule", {"preferred_workout_time": "morning", "available_days": ["Mon", "Wed", "Fri"]})
    
    for agent in AgentName:
        store.put(
            (agent.value, "instructions"),
            "wellness_assistant",
            {"instructions": f"You are a {agent.name.lower()} specialist.", "version": 1}
        )
    
    return store


@st.cache_resource
def get_store():
    """Initialize or get the memory store - loads from exported state if available."""
    if STATE_FILE.exists():
        store, metadata = load_store_from_file(STATE_FILE)
        return store, metadata
    else:
        return create_demo_store(), {"source": "demo", "message": "No exported state found. Showing demo data."}


# ============================================================
# Dashboard Components
# ============================================================

def render_header():
    """Render the dashboard header."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<p class="main-header">🧠 Wellness Memory Dashboard</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Monitor and explore the multi-agent memory system</p>', unsafe_allow_html=True)
    with col2:
        st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
        if st.button("🔄 Refresh"):
            st.rerun()


def render_user_profile(store, user_id: str):
    """Render the current user profile section."""
    st.subheader("👤 Current User Profile")
    
    # Fetch profile data
    profile_items = list(store.search((user_id, "profile")))
    pref_items = list(store.search((user_id, "preferences")))
    
    if not profile_items:
        st.warning("No profile data found for this user.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Profile Information")
        for item in profile_items:
            with st.container():
                key = item.key.replace("_", " ").title()
                value = item.value
                
                if isinstance(value, dict):
                    if "value" in value:
                        st.info(f"**{key}:** {value['value']}")
                    elif "primary" in value:
                        st.info(f"**{key}:** Primary: {value.get('primary', 'N/A')}, Secondary: {value.get('secondary', 'N/A')}")
                    elif "allergies" in value or "injuries" in value:
                        allergies = ", ".join(value.get("allergies", [])) or "None"
                        injuries = ", ".join(value.get("injuries", [])) or "None"
                        st.warning(f"**{key}:**\n- Allergies: {allergies}\n- Injuries: {injuries}")
                    else:
                        st.info(f"**{key}:** {value}")
                else:
                    st.info(f"**{key}:** {value}")
    
    with col2:
        st.markdown("#### Preferences")
        for item in pref_items:
            key = item.key.replace("_", " ").title()
            value = item.value
            
            if isinstance(value, dict):
                details = ", ".join([f"{k}: {v}" for k, v in value.items()])
                st.success(f"**{key}:** {details}")
            else:
                st.success(f"**{key}:** {value}")


def render_agent_memories(store):
    """Render recent memories from each agent."""
    st.subheader("🧠 Agent Memories")
    
    tabs = st.tabs([f"{AGENT_ICONS[agent.value]} {agent.name.title()}" for agent in AgentName])
    
    for tab, agent in zip(tabs, AgentName):
        with tab:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("##### 📋 Current Instructions")
                instr_item = store.get((agent.value, "instructions"), "wellness_assistant")
                if instr_item:
                    instr = instr_item.value.get("instructions", "No instructions")
                    version = instr_item.value.get("version", 1)
                    
                    # Truncate for display
                    display_instr = instr[:300] + "..." if len(instr) > 300 else instr
                    
                    st.markdown(f"""
                    <div style="background: #f0f2f6; padding: 1rem; border-radius: 8px; border-left: 4px solid {AGENT_COLORS[agent.value]};">
                        <strong>Version:</strong> {version}<br>
                        <small>{display_instr}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if version > 1:
                        st.success(f"✅ Instructions updated {version-1} time(s) via feedback")
                else:
                    st.warning("No instructions found")
            
            with col2:
                st.markdown("##### 📝 Recent Episodes")
                episodes = list(store.search((agent.value, "episodes"), limit=5))
                
                if episodes:
                    for ep in episodes:
                        ep_data = ep.value
                        feedback = ep_data.get("feedback", "no feedback")
                        feedback_color = "#4CAF50" if feedback != "no feedback" else "#9E9E9E"
                        
                        st.markdown(f"""
                        <div class="episode-card">
                            <strong>ID:</strong> {ep.key}<br>
                            <strong>Input:</strong> {ep_data.get('input', 'N/A')[:100]}...<br>
                            <strong>Feedback:</strong> <span style="color: {feedback_color};">{feedback}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No episodes stored yet. Chat with the wellness assistant to build episodic memory!")


def render_memory_statistics(store, user_id: str, metadata: dict):
    """Render cross-agent memory sharing statistics."""
    st.subheader("📊 Memory Statistics")
    
    # Calculate stats
    stats = {
        "profile_items": len(list(store.search((user_id, "profile")))),
        "preference_items": len(list(store.search((user_id, "preferences")))),
    }
    
    agent_stats = {}
    total_episodes = 0
    total_instructions_versions = 0
    
    for agent in AgentName:
        episodes = list(store.search((agent.value, "episodes")))
        instr_item = store.get((agent.value, "instructions"), "wellness_assistant")
        version = instr_item.value.get("version", 1) if instr_item else 1
        
        agent_stats[agent.value] = {
            "episodes": len(episodes),
            "instruction_version": version,
            "has_feedback": any(ep.value.get("feedback", "no feedback") != "no feedback" for ep in episodes)
        }
        total_episodes += len(episodes)
        total_instructions_versions += version
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👤 Profile Items", stats["profile_items"])
    with col2:
        st.metric("⚙️ Preferences", stats["preference_items"])
    with col3:
        st.metric("📝 Total Episodes", total_episodes)
    with col4:
        avg_version = total_instructions_versions / len(AgentName)
        st.metric("📈 Avg Instruction Version", f"{avg_version:.1f}")
    
    # Agent comparison chart
    st.markdown("#### Agent Comparison")
    
    chart_data = {
        "Agent": [agent.name.title() for agent in AgentName],
        "Episodes": [agent_stats[agent.value]["episodes"] for agent in AgentName],
        "Instruction Version": [agent_stats[agent.value]["instruction_version"] for agent in AgentName],
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(
            data={agent.name.title(): agent_stats[agent.value]["episodes"] for agent in AgentName},
            use_container_width=True
        )
        st.caption("Episodes per Agent")
    
    with col2:
        st.bar_chart(
            data={agent.name.title(): agent_stats[agent.value]["instruction_version"] for agent in AgentName},
            use_container_width=True
        )
        st.caption("Instruction Version per Agent")
    
    # Cross-Agent Memory Access Statistics (from tracking)
    st.markdown("---")
    st.markdown("#### 🔄 Cross-Agent Memory Access Statistics")
    st.caption("Shows how many times each agent read from / wrote to each memory type")
    
    # Get memory access stats from metadata
    access_stats = metadata.get("memory_access_stats", {})
    reads = access_stats.get("reads", {})
    writes = access_stats.get("writes", {})
    
    if reads or writes:
        memory_types = ["short_term", "long_term", "semantic", "episodic", "procedural"]
        agents = ["router", "exercise", "nutrition", "sleep", "feedback"]
        
        # Create tabs for reads vs writes
        read_tab, write_tab = st.tabs(["📖 Reads", "📝 Writes"])
        
        with read_tab:
            st.markdown("##### Memory Reads by Agent")
            
            # Build table data
            read_data = []
            for agent in agents:
                row = {"Agent": agent.title()}
                agent_reads = reads.get(agent, {})
                for mem_type in memory_types:
                    nice_name = mem_type.replace("_", " ").title()
                    row[nice_name] = agent_reads.get(mem_type, 0)
                read_data.append(row)
            
            # Display as dataframe
            df_reads = pd.DataFrame(read_data)
            df_reads = df_reads.set_index("Agent")
            
            # Display table
            st.dataframe(df_reads, use_container_width=True)
            
            # Total reads per memory type
            st.markdown("**Totals by Memory Type:**")
            totals = {mem_type.replace("_", " ").title(): sum(reads.get(a, {}).get(mem_type, 0) for a in agents) for mem_type in memory_types}
            cols = st.columns(5)
            for i, (mem_type, total) in enumerate(totals.items()):
                cols[i].metric(mem_type, total)
        
        with write_tab:
            st.markdown("##### Memory Writes by Agent")
            
            # Build table data
            write_data = []
            for agent in agents:
                row = {"Agent": agent.title()}
                agent_writes = writes.get(agent, {})
                for mem_type in memory_types:
                    nice_name = mem_type.replace("_", " ").title()
                    row[nice_name] = agent_writes.get(mem_type, 0)
                write_data.append(row)
            
            # Display as dataframe
            df_writes = pd.DataFrame(write_data)
            df_writes = df_writes.set_index("Agent")
            
            # Display table
            st.dataframe(df_writes, use_container_width=True)
            
            # Total writes per memory type
            st.markdown("**Totals by Memory Type:**")
            totals = {mem_type.replace("_", " ").title(): sum(writes.get(a, {}).get(mem_type, 0) for a in agents) for mem_type in memory_types}
            cols = st.columns(5)
            for i, (mem_type, total) in enumerate(totals.items()):
                cols[i].metric(mem_type, total)
    else:
        st.info("No memory access statistics available. Run the notebook tests and export state to see tracking data.")


def render_memory_search(store, user_id: str):
    """Render the memory search interface."""
    st.subheader("🔍 Memory Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search memories",
            placeholder="Enter a search term (e.g., 'exercise', 'sleep', 'knee injury')"
        )
    
    with col2:
        search_scope = st.selectbox(
            "Search in",
            ["All Agents", "Exercise Agent", "Nutrition Agent", "Sleep Agent", "User Profile"]
        )
    
    if search_query:
        st.markdown("---")
        st.markdown(f"#### Results for: *{search_query}*")
        
        results_found = False
        
        if search_scope in ["All Agents", "Exercise Agent"]:
            episodes = list(store.search((AgentName.EXERCISE.value, "episodes"), query=search_query, limit=5))
            if episodes:
                results_found = True
                st.markdown(f"**{AGENT_ICONS['exercise_agent']} Exercise Agent** ({len(episodes)} matches)")
                for ep in episodes:
                    with st.expander(f"Episode: {ep.key}"):
                        st.json(ep.value)
        
        if search_scope in ["All Agents", "Nutrition Agent"]:
            episodes = list(store.search((AgentName.NUTRITION.value, "episodes"), query=search_query, limit=5))
            if episodes:
                results_found = True
                st.markdown(f"**{AGENT_ICONS['nutrition_agent']} Nutrition Agent** ({len(episodes)} matches)")
                for ep in episodes:
                    with st.expander(f"Episode: {ep.key}"):
                        st.json(ep.value)
        
        if search_scope in ["All Agents", "Sleep Agent"]:
            episodes = list(store.search((AgentName.SLEEP.value, "episodes"), query=search_query, limit=5))
            if episodes:
                results_found = True
                st.markdown(f"**{AGENT_ICONS['sleep_agent']} Sleep Agent** ({len(episodes)} matches)")
                for ep in episodes:
                    with st.expander(f"Episode: {ep.key}"):
                        st.json(ep.value)
        
        if search_scope in ["All Agents", "User Profile"]:
            profile_items = list(store.search((user_id, "profile")))
            matching_profile = [p for p in profile_items if search_query.lower() in str(p.value).lower()]
            if matching_profile:
                results_found = True
                st.markdown(f"**👤 User Profile** ({len(matching_profile)} matches)")
                for p in matching_profile:
                    with st.expander(f"Profile: {p.key}"):
                        st.json(p.value)
        
        if not results_found:
            st.info(f"No results found for '{search_query}' in {search_scope}")


def render_chat_interface(store, user_id: str):
    """Render a simple chat interface to interact with the memory system."""
    st.subheader("💬 Chat with Wellness Assistant")
    
    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about exercise, nutrition, or sleep..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response (simplified - in production, use the full graph)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
                    
                    # Build context from memory
                    profile_items = list(store.search((user_id, "profile")))
                    profile_text = "\n".join([f"- {p.key}: {p.value}" for p in profile_items])
                    
                    context = f"""You are a helpful wellness assistant. 
                    
User Profile:
{profile_text}

Respond helpfully to the user's question about wellness."""
                    
                    response = llm.invoke([
                        {"role": "system", "content": context},
                        {"role": "user", "content": prompt}
                    ])
                    
                    st.write(response.content)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.content})
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ============================================================
# Main Dashboard
# ============================================================

def main():
    """Main dashboard entry point."""
    # Initialize store
    store, metadata = get_store()
    user_id = "user_sarah"
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        selected_user = st.text_input("User ID", value=user_id)
        
        # Show state file status
        st.markdown("---")
        st.markdown("### 📁 Data Source")
        
        if STATE_FILE.exists():
            mod_time = datetime.fromtimestamp(STATE_FILE.stat().st_mtime)
            st.success(f"✅ Loaded from notebook export")
            st.caption(f"Last updated: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            if st.button("🔄 Reload State"):
                st.cache_resource.clear()
                st.rerun()
        else:
            st.warning("⚠️ No exported state found")
            st.caption("Run `export_store_state(store, 'user_sarah')` in your notebook to export state.")
        
        st.markdown("---")
        st.markdown("### 📚 About")
        st.markdown("""
        This dashboard visualizes the **5 CoALA Memory Types**:
        
        1. **Short-term**: Conversation history
        2. **Long-term**: User profile & preferences
        3. **Semantic**: Knowledge retrieval
        4. **Episodic**: Past interactions
        5. **Procedural**: Self-improving instructions
        """)
        
        st.markdown("---")
        st.markdown("### 🔗 Quick Links")
        st.markdown("""
        - [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
        - [CoALA Paper](https://arxiv.org/abs/2309.02427)
        """)
    
    # Header
    render_header()
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 User Profile",
        "🧠 Agent Memories", 
        "📊 Statistics",
        "🔍 Search",
        "💬 Chat"
    ])
    
    with tab1:
        render_user_profile(store, selected_user)
    
    with tab2:
        render_agent_memories(store)
    
    with tab3:
        render_memory_statistics(store, selected_user, metadata)
    
    with tab4:
        render_memory_search(store, selected_user)
    
    with tab5:
        render_chat_interface(store, selected_user)


if __name__ == "__main__":
    main()
