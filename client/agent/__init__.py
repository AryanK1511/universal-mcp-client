# client/agent/__init__.py


from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent

from client.config import settings


class ReactAgent:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
        self.web_search_tool = TavilySearch(
            max_results=2, tavily_api_key=settings.TAVILY_API_KEY
        )
        self.multi_server_client_params = {}

    async def init_agent(self):
        async with MultiServerMCPClient(self.multi_server_client_params) as client:
            tools = [self.web_search_tool]
            client_tools = client.get_tools()
            for tool in client_tools:
                tools.append(tool)
            return create_react_agent(self.model, tools)

    async def get_agent_response(self, prompt):
        agent = await self.init_agent()
        print(f"Agent: {agent}")
        inputs = {"messages": [{"role": "user", "content": prompt}]}
        response = await agent.ainvoke(inputs)
        print(f"Response: {response}")
        return response["messages"][-1].content
