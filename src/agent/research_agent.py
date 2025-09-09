import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.agent.tools.google_mcp_tool import GoogleSearchMCPTool

# .env を読み込む
load_dotenv()


# ==============================
# 状態定義
# ==============================
class AgentState(dict):
    query: str
    search_results: str
    answer: str


# ==============================
# ノード定義
# ==============================
async def google_search_node(state: AgentState) -> AgentState:
    tool = GoogleSearchMCPTool()
    results = await tool.search(state["query"], num_results=3)
    text = "\n".join([c.text for c in results.content])
    return {"search_results": text}


async def summarize_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは研究アシスタントです。以下の検索結果を日本語で要約し、ユーザーの質問に答えてください。"),
        ("user", "質問: {query}\n\n検索結果:\n{search_results}")
    ])
    chain = prompt | llm
    response = await chain.ainvoke(state)
    return {"answer": response.content}


# ==============================
# グラフ関連のユーティリティ
# ==============================
def build_agent_graph():
    """LangGraph を構築して返す"""
    graph = StateGraph(AgentState)
    graph.add_node("google_search", google_search_node)
    graph.add_node("summarize", summarize_node)

    graph.set_entry_point("google_search")
    graph.add_edge("google_search", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()


def export_graph_mermaid(app, filepath: Path):
    """Mermaid 記法でグラフ形状を保存"""
    mermaid_code = app.get_graph().draw_mermaid()
    filepath.write_text(f"```mermaid\n{mermaid_code}\n```", encoding="utf-8")
    print(f"✅ グラフを {filepath} に保存しました")


# ==============================
# 実行関数
# ==============================
async def run_agent(app, query: str) -> str:
    """クエリを実行して最終回答を返す"""
    state = {"query": query}
    final_state = await app.ainvoke(state)
    return final_state["answer"]


# ==============================
# メイン
# ==============================
if __name__ == "__main__":
    query = "FastMCPとは何か？"

    # グラフ構築
    app = build_agent_graph()

    # グラフ形状を Markdown に保存
    export_graph_mermaid(app, Path(__file__).parent / "graph_shape.md")

    # エージェント実行
    answer = asyncio.run(run_agent(app, query))
    print("\n=== AI エージェントの回答 ===\n")
    print(answer)
