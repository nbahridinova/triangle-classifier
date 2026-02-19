import os
import requests
import json


class GitHubAPIError(Exception):
    """Raised when a GitHub API call fails (404, 403 rate limit, etc.)."""
    pass


def get_repo_commit_counts(user_id: str) -> list:
    """
    Input: GitHub user ID (string)
    Output: list of strings in the format:
        "Repo: <repo_name> Number of commits: <count>"
    """
    if user_id is None or str(user_id).strip() == "":
        raise ValueError("GitHub user ID must be a non-empty string.")

    user_id = str(user_id).strip()

    headers = {
        "User-Agent": "HW4a-GitHubAPI",
        "Accept": "application/vnd.github+json",
    }

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    repos_url = f"https://api.github.com/users/{user_id}/repos"
    try:
        repos_resp = requests.get(repos_url, headers=headers, timeout=15)
    except requests.RequestException as e:
        raise GitHubAPIError(f"Network error contacting GitHub: {e}")

    if repos_resp.status_code == 404:
        raise GitHubAPIError(f"User '{user_id}' not found (404).")
    if repos_resp.status_code == 403:
        remaining = repos_resp.headers.get("X-RateLimit-Remaining", "?")
        raise GitHubAPIError(f"Rate limit hit (403). Remaining={remaining}")
    if repos_resp.status_code != 200:
        raise GitHubAPIError(f"GitHub error: {repos_resp.status_code} {repos_resp.text[:200]}")

    try:
        repos_data = json.loads(repos_resp.text)
    except json.JSONDecodeError:
        raise GitHubAPIError("Could not parse JSON from repos response.")

    if not isinstance(repos_data, list):
        raise GitHubAPIError("Unexpected repos response format (expected a list).")

    output_lines = []

    for repo_obj in repos_data:
        repo_name = repo_obj.get("name")
        if not repo_name:
            continue

        commits_url = f"https://api.github.com/repos/{user_id}/{repo_name}/commits"
        try:
            commits_resp = requests.get(commits_url, headers=headers, timeout=15)
        except requests.RequestException as e:
            raise GitHubAPIError(f"Network error contacting GitHub: {e}")

        if commits_resp.status_code == 403:
            remaining = commits_resp.headers.get("X-RateLimit-Remaini_
