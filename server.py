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

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)
    return response.json()

@mcp.tool
def get_repository(owner: str, repo: str) -> dict:
    """Get details for a Github repository."""
    data = github_request(f"/repos/{owner}/{repo}")
    return{
        "name": data["name"], 
        "full_name": data["full_name"],
        "description": data["description"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "open_issues": data["open_issues_count"],
        "language": data["language"],
        "default_branch": data["default_branch"],
        "html_url": data["html_url"],

    }

@mcp.tool 
def search_repository(query: str, limit: int = 5) -> list:
    """Search GitHub repositiories."""
    data = github_request(f"/search/repositories?q={query}")
    repositories = []
    for repo in data["items"][:limit]:
        repositories.append({
            "name": repo["full_name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "url": repo["html_url"]
        })
    return repositories

@mcp.tool
def get_user(username: str) -> dict:
    """Get details for a GitHub user."""

    data = github_request(f"/users/{username}")

    return {
        "username": data["login"],
        "name": data["name"],
        "bio": data["bio"],
        "public_repositories": data["public_repos"],
        "followers": data["followers"],
        "following": data["following"],
        "profile_url": data["html_url"]
    }

@mcp.tool
def list_user_repositories(username: str, limit: int = 10) -> list:
    """List public repositories for a GitHub user."""

    data = github_request(f"/users/{username}/repos")

    repositories = []

    for repo in data[:limit]:
        repositories.append({
            "name": repo["name"],
            "description": repo["description"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "url": repo["html_url"]
        })

    return repositories
@mcp.tool
def list_branches(owner: str, repo: str) -> list:
    """List branches in a GitHub repository."""

    data = github_request(f"/repos/{owner}/{repo}/branches")

    branches = []

    for branch in data:
        branches.append({
            "name": branch["name"],
            "protected": branch["protected"]
        })

    return branches
@mcp.tool
def list_commits(owner: str, repo: str, limit: int = 10) -> list:
    """List recent commits for a GitHub repository."""

    data = github_request(f"/repos/{owner}/{repo}/commits")

    commits = []

    for commit in data[:limit]:
        commits.append({
            "sha": commit["sha"][:7],
            "message": commit["commit"]["message"],
            "author": commit["commit"]["author"]["name"],
            "date": commit["commit"]["author"]["date"]
        })

    return commits
@mcp.tool
def list_issues(owner: str, repo: str, limit: int = 10) -> list:
    """List open issues for a GitHub repository."""

    data = github_request(f"/repos/{owner}/{repo}/issues")

    issues = []

    for issue in data[:limit]:
        # Skip pull requests (GitHub returns PRs in the issues endpoint)
        if "pull_request" in issue:
            continue

        issues.append({
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "author": issue["user"]["login"],
            "url": issue["html_url"]
        })

    return issues

if __name__ == "__main__":
    mcp.run()

