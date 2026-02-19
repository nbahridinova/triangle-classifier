import unittest
from unittest.mock import patch, Mock

from github_api import get_repo_commit_counts, GitHubAPIError

class TestGitHubAPI_Mocked(unittest.TestCase):

    def test_blank_user_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_repo_commit_counts("   ")

    @patch("github_api.requests.get")
    def test_invalid_user_404_raises_github_api_error(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 404
        mock_resp.text = ""
        mock_resp.headers = {}
        mock_get.return_value = mock_resp

        with self.assertRaises(GitHubAPIError):
            get_repo_commit_counts("nonexistent_user")

        args, kwargs = mock_get.call_args
        self.assertIn("https://api.github.com/users/nonexistent_user/repos", args[0])

    @patch("github_api.requests.get")
    def test_rate_limit_403_raises_github_api_error(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 403
        mock_resp.text = ""
        mock_resp.headers = {"X-RateLimit-Remaining": "0"}
        mock_get.return_value = mock_resp

        with self.assertRaises(GitHubAPIError):
            get_repo_commit_counts("anyuser")

    @patch("github_api.requests.get")
    def test_happy_path_two_repos_commit_counts(self, mock_get):
        """
        Mock:
          - /users/<id>/repos returns 2 repos
          - /repos/<id>/<repo>/commits returns lists of commits
        """
        user = "John567"

        repos_resp = Mock()
        repos_resp.status_code = 200
        repos_resp.headers = {}
        repos_resp.text = (
            '[{"name": "Triangle567"}, {"name": "Square567"}]'
        )

        commits_triangle_resp = Mock()
        commits_triangle_resp.status_code = 200
        commits_triangle_resp.headers = {}
        commits_triangle_resp.text = "[" + ",".join(['{}'] * 10) + "]"

        commits_square_resp = Mock()
        commits_square_resp.status_code = 200
        commits_square_resp.headers = {}
        commits_square_resp.text = "[" + ",".join(['{}'] * 27) + "]"

        mock_get.side_effect = [repos_resp, commits_triangle_resp, commits_square_resp]

        lines = get_repo_commit_counts(user)

        self.assertEqual(lines[0], "Repo: Triangle567 Number of commits: 10")
        self.assertEqual(lines[1], "Repo: Square567 Number of commits: 27")

        expected_calls = [
            f"https://api.github.com/users/{user}/repos",
            f"https://api.github.com/repos/{user}/Triangle567/commits",
            f"https://api.github.com/repos/{user}/Square567/commits",
        ]
        actual_calls = [call.args[0] for call in mock_get.call_args_list]
        self.assertEqual(actual_calls, expected_calls)

    @patch("github_api.requests.get")
    def test_repo_list_empty_returns_empty_list(self, mock_get):
        user = "EmptyUser"

        repos_resp = Mock()
        repos_resp.status_code = 200
        repos_resp.headers = {}
        repos_resp.text = "[]"

        mock_get.return_value = repos_resp

        lines = get_repo_commit_counts(user)
        self.assertEqual(lines, [])

    @patch("github_api.requests.get")
    def test_commits_404_skips_repo(self, mock_get):
        """
        If a commits endpoint returns 404 for a repo, our HW3a code skips it.
        """
        user = "UserX"

        repos_resp = Mock()
        repos_resp.status_code = 200
        repos_resp.headers = {}
        repos_resp.text = '[{"name":"RepoA"},{"name":"RepoB"}]'

        commits_404 = Mock()
        commits_404.status_code = 404
        commits_404.headers = {}
        commits_404.text = ""

        commits_ok = Mock()
        commits_ok.status_code = 200
        commits_ok.headers = {}
        commits_ok.text = "[{},{}]"  # 2 commits

        mock_get.side_effect = [repos_resp, commits_404, commits_ok]

        lines = get_repo_commit_counts(user)

        # RepoA skipped, RepoB included
        self.assertEqual(lines, ["Repo: RepoB Number of commits: 2"])

if __name__ == "__main__":
    unittest.main()
