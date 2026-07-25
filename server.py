from fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os


load_dotenv()
mcp = FastMCP("GitHub MCP")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found. Please create a .env file.")

def github_request(endpoint: str):
    url = f"https://api.github.com{endpoint}"

if __name__ == "__main__":
    mcp.run()