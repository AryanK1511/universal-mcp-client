# client/agent/__init__.py


from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

from client.agent.graph import AgentGraph
from client.agent.graph.tools import tools
from client.constants import CONSTANT_THREAD_ID


class ReactAgent:
    def __init__(self):
        self.agent_graph = AgentGraph()
        self.multi_server_client_params = {}
        self._initialized = False
        self._graph = None
        self.config = {"configurable": {"thread_id": CONSTANT_THREAD_ID}}

    async def init_agent(self):
        if not self._initialized:
            async with MultiServerMCPClient(self.multi_server_client_params) as client:
                all_tools = tools
                client_tools = client.get_tools()
                for tool in client_tools:
                    all_tools.append(tool)
                self.agent_graph.build_graph(all_tools)
                self._graph = self.agent_graph.get_graph()
                self._initialized = True
        return self._graph

    async def get_agent_response(self, prompt):
        agent = await self.init_agent()
        user_prompt = {"messages": [HumanMessage(content=prompt)]}
        stream = agent.astream(
            input=user_prompt, config=self.config, stream_mode=["values"]
        )
        return stream
