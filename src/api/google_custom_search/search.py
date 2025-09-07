import os
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper

# .env 読み込み
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def google_search(query: str, num_results: int = 5) -> str:
    """
    Google Custom Search APIで検索する関数
    """
    search = GoogleSearchAPIWrapper(
        google_api_key=GOOGLE_API_KEY,
        google_cse_id=GOOGLE_CSE_ID,
        k=num_results,
    )
    return search.run(query)

def get_google_search_tool(num_results: int = 5) -> Tool:
    """
    LangChain Agentに組み込めるGoogle SearchのToolを返す関数
    """
    search = GoogleSearchAPIWrapper(
        google_api_key=GOOGLE_API_KEY,
        google_cse_id=GOOGLE_CSE_ID,
        k=num_results,
    )
    return Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )
