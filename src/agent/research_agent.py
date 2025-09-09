import os
from dotenv import load_dotenv

load_dotenv()  # .env を読み込む


import asyncio
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.agent.tools.google_mcp_tool import GoogleSearchMCPTool

# LangGraph の状態
class AgentState(dict):
    query: str
    search_results: str
    answer: str

# Google 検索ノード
async def google_search_node(state: AgentState) -> AgentState:
    tool = GoogleSearchMCPTool()
    results = await tool.search(state["query"], num_results=3)
    text = "\n".join([c.text for c in results.content])
    return {"search_results": text}

# AI 要約ノード (OpenAI GPT)
async def summarize_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o-mini")  # 軽量モデルでも可
    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは研究アシスタントです。以下の検索結果を日本語で要約し、ユーザーの質問に答えてください。"),
        ("user", "質問: {query}\n\n検索結果:\n{search_results}")
    ])
    chain = prompt | llm
    response = await chain.ainvoke(state)
    return {"answer": response.content}

# グラフを構築
graph = StateGraph(AgentState)
graph.add_node("google_search", google_search_node)
graph.add_node("summarize", summarize_node)

graph.set_entry_point("google_search")
graph.add_edge("google_search", "summarize")
graph.add_edge("summarize", END)

app = graph.compile()

# 実行関数
async def run_agent(query: str):
    state = {"query": query}
    final_state = await app.ainvoke(state)
    return final_state["answer"]

if __name__ == "__main__":
    query = "FastMCPとは何か？"
    answer = asyncio.run(run_agent(query))
    print("\n=== AI エージェントの回答 ===\n")
    print(answer)
