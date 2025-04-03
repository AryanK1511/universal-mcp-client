# client/agent/graph/__init__.py

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from client.agent.graph.nodes import create_assistant_node
from client.agent.graph.state import CustomState


class AgentGraph:
    def __init__(self):
        self.react_graph = None
        self.builder = StateGraph(CustomState)

    def build_graph(self, all_tools):
        # Add all the tools to the tools node
        self.builder.add_node("tools", ToolNode(all_tools))

        # Create the assistant node
        self.builder.add_node("assistant", create_assistant_node(all_tools))

        # Connect Start to Assistant
        self.builder.add_edge(START, "assistant")

        # Connect Assistant to Tools
        self.builder.add_conditional_edges("assistant", tools_condition, "tools", END)

        # Connect Tools to Assistant
        self.builder.add_edge("tools", "assistant")

        # Compile the graph
        self.react_graph = self.builder.compile()

    def get_graph(self):
        return self.react_graph
