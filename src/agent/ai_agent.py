import os
import asyncio
from dotenv import load_dotenv
import openai
from fastmcp import Client

# 環境変数読み込み
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# MCP クライアント
client = Client("http://127.0.0.1:8000/mcp/")

async def ask_ai_with_google(prompt: str):
    # まず MCP ツールで情報検索
    async with client:
        search_result = await client.call_tool(
            "search_google",
            {"query": prompt, "num_results": 3}
        )
    
    # 検索結果をまとめて OpenAI に渡す
    content_text = "\n".join([c.text for c in search_result.content])
    
    # GPT へ問い合わせ
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Search results:\n{content_text}\n\nBased on these results, answer the question: {prompt}"}
        ]
    )
    
    return response.choices[0].message.content

async def main():
    query = "FastMCP Pythonとは何か？"
    answer = await ask_ai_with_google(query)
    print("AI回答:\n", answer)

if __name__ == "__main__":
    asyncio.run(main())
