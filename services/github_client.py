import requests

from services.auth_service import get_installation_token


class GitHubClient:

    def __init__(self, installation_id):

        self.base_url = "https://api.github.com"

        self.token = get_installation_token(
            installation_id
        )

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    def get_repository(self, owner, repo):

        response = requests.get(
            f"{self.base_url}/repos/{owner}/{repo}",
            headers=self.headers,
        )

        response.raise_for_status()

        return response.json()