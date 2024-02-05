#!/usr/bin/env python3
""" Unittests for client.py """
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict
from fixtures import TEST_PAYLOAD
from requests import HTTPError


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
        repo: Dict[str, Dict],
        license_key: str,
        expected_result: bool
    ) -> None:
        """ Test has_license method """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected_result
        )


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration tests for GithubOrgClient """
    @classmethod
    def setUpClass(cls):
        """ Set up class """
        payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def mock_get(url):
            """ get mock method """
            if url in payload:
                return Mock(**{'json.return_value': payload[url]})
            return HTTPError
        cls.get_patcher = patch("requests.get", side_effect=mock_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """ Tear down class """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Test public_repos method with expected_repos """
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Tests public_repos method with a license """
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(
            result,
            self.apache2_repos,
        )


if __name__ == "__main__":
    unittest.main()
