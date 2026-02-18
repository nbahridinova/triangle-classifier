import unittest
from unittest.mock import Mock, patch

from github_api import get_repos_and_commits


class TestGitHubAPI(unittest.TestCase):

    @patch("github_api.requests.get")
    def test_two_repos_counts_commits(self, mock_get):

        repos_resp = Mock()
        repos_resp.status_code = 200
        repos_resp.text = '[{"name":"RepoA"},{"name":"RepoB"}]'


        commits_a_resp = Mock()
        commits_a_resp.status_code = 200
        commits_a_resp.text = '[{"sha":"1"},{"sha":"2"},{"sha":"3"}]'


        commits_b_resp = Mock()
        commits_b_resp.status_code = 200
        commits_b_resp.text = '[{"sha":"x"}]'

        mock_get.side_effect = [repos_resp, commits_a_resp, commits_b_resp]

        out = get_repos_and_commits("testuser")
        self.assertEqual(out, [("RepoA", 3), ("RepoB", 1)])

    @patch("github_api.requests.get")
    def test_user_not_found_raises(self, mock_get):
        repos_resp = Mock()
        repos_resp.status_code = 404
        repos_resp.text = '{"message":"Not Found"}'
        mock_get.return_value = repos_resp

        with self.assertRaises(ValueError):
            get_repos_and_commits("no_such_user")

    @patch("github_api.requests.get")
    def test_repo_commits_endpoint_failure_returns_zero(self, mock_get):
      
        repos_resp = Mock()
        repos_resp.status_code = 200
        repos_resp.text = '[{"name":"RepoA"}]'


        commits_resp = Mock()
        commits_resp.status_code = 409
        commits_resp.text = '{"message":"Git Repository is empty."}'

        mock_get.side_effect = [repos_resp, commits_resp]

        out = get_repos_and_commits("testuser")
        self.assertEqual(out, [("RepoA", 0)])


if __name__ == "__main__":
    unittest.main()
