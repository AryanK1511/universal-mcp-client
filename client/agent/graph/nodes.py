# client/agent/graph/nodes.py

from typing import Any, Callable, Dict

from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState

from client.agent.graph.llm import llm

sys_msg = SystemMessage(content="You are a helpful assistant.")


def create_assistant_node(all_tools) -> Callable[[MessagesState], Dict[str, Any]]:
    def assistant_node(state: MessagesState):
        llm_with_tools = llm.bind_tools(all_tools)
        return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

    return assistant_node
