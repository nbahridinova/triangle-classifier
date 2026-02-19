import re
import unittest
import requests
import json

from github_api import get_repo_commit_counts, GitHubAPIError


class TestGitHubAPI_NoMocks(unittest.TestCase):

    def test_blank_user_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_repo_commit_counts("   ")

    def test_invalid_user_raises_github_api_error(self):
        with self.assertRaises(GitHubAPIError):
            get_repo_commit_counts("this_user_should_not_exist_1234567890")

    def test_real_user_output_format(self):

        user = "richkempinski"

        r = requests.get(f"https://api.github.com/users/{user}/repos", timeout=15)
        if r.status_code == 403:
            self.skipTest("Rate limited by GitHub (403) during pre-check.")
        if r.status_code != 200:
            self.skipTest(f"GitHub not reachable / unexpected status: {r.status_code}")

        repos = json.loads(r.text)
        if isinstance(repos, list) and len(repos) > 25:
            self.skipTest("Too many repos for unauthenticated CI testing; skipping to avoid rate limit.")

        lines = get_repo_commit_counts(user)

        self.assertIsInstance(lines, list)
        self.assertGreaterEqual(len(lines), 1)

        pattern = re.compile(r"^Repo: .+ Number of commits: \d+$")
        for line in lines:
            self.assertRegex(line, pattern)


if __name__ == "__main__":
    unittest.main()
