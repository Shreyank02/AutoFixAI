import requests

from services.auth_service import get_installation_token


class GitHubAPIService:

    @staticmethod
    def create_pull_request(
        owner: str,
        repository: str,
        installation_id: int,
        title: str,
        body: str,
        head: str,
        base: str = "main",
    ):

        token = get_installation_token(
            installation_id
        )

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        }

        response = requests.post(
            f"https://api.github.com/repos/{owner}/{repository}/pulls",
            headers=headers,
            json={
                "title": title,
                "body": body,
                "head": head,
                "base": base,
            },
        )

        if response.status_code != 201:
            print(response.status_code)
            print(response.json())
            raise Exception("Failed to create PR")

        return response.json()