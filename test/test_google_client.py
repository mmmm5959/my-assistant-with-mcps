import asyncio
from src.agent.tools.google_mcp_tool import GoogleSearchMCPTool

async def test_search():
    tool = GoogleSearchMCPTool()
    result = await tool.search(
        "FastMCP Python 使い方　おすすめ", 
        num_results=5
        )
    print("テスト検索結果:", result)

if __name__ == "__main__":
    asyncio.run(test_search())
