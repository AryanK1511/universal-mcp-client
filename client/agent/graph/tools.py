# client/agent/graph/tools.py

from langchain_tavily import TavilySearch

from client.config import settings

search_tool = TavilySearch(max_results=4, tavily_api_key=settings.TAVILY_API_KEY)

tools = [search_tool]
