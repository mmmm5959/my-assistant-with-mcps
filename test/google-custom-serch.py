import sys
import os

# src を import path に追加
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from api.google_custom_search.search import google_search, get_google_search_tool


def test_simple_search():
    print("=== シンプル検索テスト ===")
    result = google_search("LangChainとは何か")
    print(result)


def test_tool():
    print("\n=== Tool経由の検索テスト ===")
    tool = get_google_search_tool()
    result = tool.run("最新の日本のAIニュース")
    print(result)


if __name__ == "__main__":
    test_simple_search()
    test_tool()
