import asyncio
from fastmcp import Client

async def main():
    # 起動中の google_search_server に接続
    client = Client("http://localhost:8000/mcp/")

    async with client:
        # サーバー疎通確認
        await client.ping()
        print("✅ MCP server is alive!")

        # 利用可能なツール一覧
        tools = await client.list_tools()
        print("📌 Available tools:", tools)

        # Google検索をテスト
        result = await client.call_tool(
            "search_google", 
            {"query": "Python MCPについて教えて", "num_results": 3}
            )
        print("🔍 Search result:", result)

if __name__ == "__main__":
    asyncio.run(main())
