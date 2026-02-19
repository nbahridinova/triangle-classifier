import requests
import json

def get_repos_and_commits(user_id):
    repos_url = f"https://api.github.com/users/{user_id}/repos"
    repos_response = requests.get(repos_url, timeout=10)

    if repos_response.status_code != 200:
        raise ValueError(f"Could not fetch the repos for user '{user_id}'")

    repos = json.loads(repos_response.text)

    results = []
    for repo in repos:
        repo_name = repo["name"]
        commits_url = f"https://api.github.com/repos/{user_id}/{repo_name}/commits"
        commits_response = requests.get(commits_url, timeout=10)

        if commits_response.status_code != 200:
            num_commits = 0
        else:
            commits = json.loads(commits_response.text)
            num_commits = len(commits)

        results.append((repo_name, num_commits))

    return results

def print_repos_and_commits(user_id):
    results = get_repos_and_commits(user_id)
    for repo_name, num_commits in results:
        print(f"Repo: {repo_name} Number of commits: {num_commits}")

if __name__ == "__main__":
    user = input("Enter GitHub user ID: ").strip()
    print_repos_and_commits(user)

