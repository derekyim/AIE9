"""A minimal tool-using agent graph.

The graph:
- Calls a chat model bound to the tool belt.
- If the last message requested tool calls, routes to a ToolNode.
- Otherwise, terminates.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.models import get_chat_model, fix_tool_calls
from app.state import MessagesState
from app.tools import get_tool_belt
import os

fireworks_base_url = "https://api.fireworks.ai/inference/v1"
fireworks_api_key = os.environ["FIREWORKS_API_KEY"]
fireworks_chat_model = os.environ["FIREWORKS_CHAT_MODEL_DEREKY"]
fireworks_embedding_model = os.environ["FIREWORKS_EMBEDDING_MODEL_DEREKY"]

def _build_model_with_tools(model_name: str, api_key: str, base_url: str):
    """Return a chat model instance bound to the current tool belt."""
    model = get_chat_model(model_name, api_key, base_url)
    return model.bind_tools(get_tool_belt())


def call_model(state: MessagesState) -> dict:
    """Invoke the model with the accumulated messages and append its response."""
    model = _build_model_with_tools(fireworks_chat_model, fireworks_api_key, fireworks_base_url)
    messages = state["messages"]
    response = fix_tool_calls(model.invoke(messages))
    return {"messages": [response]}


def build_graph():
    """Build an agent graph that interleaves model and tool execution."""
    graph = StateGraph(MessagesState)
    tool_node = ToolNode(get_tool_belt())
    graph.add_node("agent", call_model)
    graph.add_node("action", tool_node)
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition, {"tools": "action", END: END})
    graph.add_edge("action", "agent")
    return graph


# Export compiled graph for LangGraph
graph = build_graph().compile()
