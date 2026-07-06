from services.auth_service import get_installation_token
from services.github_client import GitHubClient
from services.repository_service import RepositoryService

INSTALLATIONS = {}


class InstallationService:

    @staticmethod
    def handle_webhook(payload: dict):

        installation_id = payload["installation"]["id"]

        repositories = payload.get("repositories", [])

        for repo in repositories:

            full_name = repo["full_name"]

            owner = full_name.split("/")[0]

            repo_name = full_name.split("/")[1]

            InstallationService.register(
                installation_id,
                full_name,
            )

            InstallationService.clone_repository(
                owner,
                repo_name,
                installation_id,
            )

        print(INSTALLATIONS)

    @staticmethod
    def register(
        installation_id,
        repo_name,
    ):

        INSTALLATIONS[repo_name] = installation_id

    @staticmethod
    def get_installation(
        repo_name,
    ):

        return INSTALLATIONS.get(repo_name)
    
    @staticmethod
    def clone_repository(
        owner: str,
        repo_name: str,
        installation_id: int,
    ):
        """
        Clone a repository using the GitHub App installation token.
        """

        token = get_installation_token(installation_id)

        clone_url = (
            f"https://x-access-token:{token}"
            f"@github.com/{owner}/{repo_name}.git"
        )

        RepositoryService.clone_repository(
            clone_url,
            repo_name,
        )

        print("Generating installation token...")

        token = get_installation_token(installation_id)

        print(token[:20])

        print("Clone URL")

        print(clone_url)

    @staticmethod
    def handle_repository_event(payload: dict):

        installation_id = payload["installation"]["id"]

        repositories = payload.get("repositories_added", [])

        for repo in repositories:

            full_name = repo["full_name"]

            owner, repo_name = full_name.split("/")

            InstallationService.register(
                installation_id,
                full_name
            )

            InstallationService.clone_repository(
                owner,
                repo_name,
                installation_id
            )