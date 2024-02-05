#!/usr/bin/env python3
""" Unittests for client.py """
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """ a class that tests GithubOrgClient """
    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch('client.get_json')
    def test_org(
        self,
        org_name: str,
        response: Dict,
        mock_get_json: Mock
    ) -> None:
        """ Test org method """
        mock_get_json.return_value = response
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, response)
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org_name)
        )

    def test_public_repos_url(self) -> None:
        """ Test _public_repos_url method """
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_payload

            client = GithubOrgClient("google")
            result = client._public_repos_url
            self.assertEqual(result, mock_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """ Test public_repos method """
        url = "https://api.github.com/orgs/google/repos"
        repos = [
            {"id": 1, "name": "repo1"},
            {"id": 2, "name": "repo2"},
            {"id": 3, "name": "repo3"}
        ]
        mock_get_json.return_value = repos
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = url
            org_client: GithubOrgClient = GithubOrgClient("google")
            self.assertEqual(
                org_client.public_repos(),
                ["repo1", "repo2", "repo3"]
            )
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: Dict,
        license_key: str,
        expected_result: bool
    ) -> None:
        """ Test has_license method """
        org_client = GithubOrgClient("testorg")
        result = org_client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
