"""An agent graph with a post-response spanish check loop.

After the agent responds, a secondary node evaluates spanish.
If spanish is successful, end; otherwise, continue the loop or terminate after a safe limit.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from app.state import MessagesState
from app.models import get_chat_model
from app.tools import get_tool_belt


class SpanishResult(BaseModel):
    spanish_response: str = Field(description="The Spanish translation of the final response")


def _build_model_with_tools():
    """Return a chat model instance bound to the current tool belt."""
    model = get_chat_model()
    return model.bind_tools(get_tool_belt())


def call_model(state: MessagesState) -> dict:
    """Invoke the model with the accumulated messages and append its response."""
    model = _build_model_with_tools()
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


def route_to_action_or_spanish(state: MessagesState):
    """Decide whether to execute tools or run the spanish string translation evaluator."""
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "action"
    return "spanish"


_spanish_prompt = ChatPromptTemplate.from_template(
    "Translate the following response into Spanish: {final_response}"
)


async def spanish_node(state: MessagesState) -> dict:
    """Evaluate spanish translation of the latest response relative to the initial query."""
    print(">>> SPANISH NODE ENTERED WITH STATE:", state, flush=True)
    if len(state["messages"]) > 10:
        return {"messages": [AIMessage(content="SPANISH:END")]}

    initial_query = state["messages"][0]
    final_response = state["messages"][-1]


    structured_model = get_chat_model(model_name="gpt-4.1-mini").with_structured_output(SpanishResult)
 
    try:
        print(">>> ABOUT TO FORMAT PROMPT", flush=True)
        formatted = await _spanish_prompt.ainvoke({
            "initial_query": initial_query.content,
            "final_response": final_response.content
        })
        print(">>> PROMPT FORMATTED:", formatted, flush=True)

        print(">>> ABOUT TO CALL MODEL", flush=True)
        print(">>> TESTING BARE MODEL CALL", flush=True)
        bare_model = get_chat_model(model_name="gpt-4.1-mini")
        print(">>> FORMATTED MESSAGE 1 content:", formatted.messages[0].content, flush=True)
        #print(">>> FORMATTED MESSAGE 2 content:", formatted.messages[0]["content"], flush=True)
        bare_result = await bare_model.ainvoke(formatted.messages[0].content)
        print(">>> BARE MODEL RESULT:", bare_result, flush=True)
        #result = await structured_model.ainvoke(formatted)
    except Exception as e:
        print(">>> SPANISH ERROR:", e, flush=True)
        raise
    return {"messages": [AIMessage(content=bare_result.content)]}


def spanish_decision(state: MessagesState):
    """Terminate on a non-empty spanish response or loop otherwise; guard against infinite loops."""
    last = state["messages"][-1]
    text = getattr(last, "content", "")
    if text:
        return "end"
    return "continue"


def build_graph():
    """Build an agent graph with an auxiliary spanish string translation subgraph."""
    graph = StateGraph(MessagesState)
    tool_node = ToolNode(get_tool_belt())
    graph.add_node("agent", call_model)
    graph.add_node("action", tool_node)
    graph.add_node("spanish", spanish_node)
    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        route_to_action_or_spanish,
        {"action": "action", "spanish": "spanish"},
    )
    graph.add_conditional_edges(
        "spanish",
        spanish_decision,
        {"continue": "spanish", "end": END, END: END},
    )
    graph.add_edge("action", "agent")
    return graph


graph = build_graph().compile()
