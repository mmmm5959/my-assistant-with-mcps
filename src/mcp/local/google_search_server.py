from fastmcp import FastMCP
from api.google_custom_search.search import google_search

mcp = FastMCP("google-search")

# ツール登録
@mcp.tool()
def search_google(query: str, num_results: int = 5):
    return google_search(query, num_results)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
