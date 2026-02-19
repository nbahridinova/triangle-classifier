import unittest
from unittest.mock import patch, Mock

from github_api import get_repo_commit_counts, GitHubAPIError


def _mock_response(status_code=200, json_data=None, headers=None):
    r = Mock()
    r.status_code = status_code
    r.json.return_value = json_data if json_data is not None else []
    r.headers = headers if headers is not None else {}
    return r


def mocked_requests_get(url, timeout=15):
    if url == "https://api.github.com/users/richkempinski/repos":
        return _mock_response(
            200,
            json_data=[
                {"name": "hellogitworld"},
                {"name": "helloworld"},
            ],
        )

    if url == "https://api.github.com/repos/richkempinski/hellogitworld/commits":
        return _mock_response(200, json_data=[{}, {}, {}])  

    if url == "https://api.github.com/repos/richkempinski/helloworld/commits":
        return _mock_response(200, json_data=[{}])  

    return _mock_response(404, json_data={"message": "Not Found"})


class TestGitHubAPI_WithMocks(unittest.TestCase):

    @patch("github_api.requests.get", side_effect=mocked_requests_get)
    def test_output_format_is_correct(self, mock_get):
        results = get_repo_commit_counts("richkempinski")


        if results and isinstance(results[0], str):
            self.assertIn("Repo: hellogitworld", results[0])
            self.assertIn("Number of commits: 3", results[0])
        else:
            self.assertIn(("hellogitworld", 3), results)
            self.assertIn(("helloworld", 1), results)

        self.assertTrue(mock_get.called)

    @patch("github_api.requests.get", side_effect=lambda url, timeout=15: _mock_response(404, {"message": "Not Found"}))
    def test_user_not_found_raises(self, mock_get):
        with self.assertRaises(GitHubAPIError):
            get_repo_commit_counts("this_user_does_not_exist_12345")
