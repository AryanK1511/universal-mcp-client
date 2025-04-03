# client/agent/graph/llm.py

from langchain_openai import ChatOpenAI

from client.config import settings

llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
