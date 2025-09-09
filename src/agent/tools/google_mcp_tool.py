import asyncio
from fastmcp import Client

class GoogleSearchMCPTool:
    def __init__(self, base_url: str = "http://localhost:8000/mcp/"):
        self.client = Client(base_url)

    async def search(self, query: str, num_results: int = 5):
        async with self.client:
            result = await self.client.call_tool(
                "search_google",
                {"query": query, "num_results": num_results}
            )
            return result

# 動作テスト用
if __name__ == "__main__":
    async def main():
        tool = GoogleSearchMCPTool()
        res = await tool.search("FastMCP Python")
        print(res)

    asyncio.run(main())
