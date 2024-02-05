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


if __name__ == "__main__":
    unittest.main()
