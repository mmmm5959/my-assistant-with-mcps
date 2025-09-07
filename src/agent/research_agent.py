# src/agent/research_agent.py
import asyncio
from fastmcp import Client

async def main():
    # Compose 内ではサービス名で接続
    async with Client("http://google-search:8000") as client:
        # サーバー疎通確認
        await client.ping()

        # 利用可能なツールを取得
        tools = await client.list_tools()
        print("Tools:", tools)

        # Google検索ツールを呼び出す
        result = await client.call_tool("search_google", {"query": "LangChain MCP Hub", "num_results": 3})
        print("検索結果:", result)

# 非同期で実行
asyncio.run(main())
