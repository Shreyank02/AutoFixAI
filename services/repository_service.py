from pathlib import Path
from git import Repo, GitCommandError
import shutil

from utils.logger import logger

REPOSITORY_ROOT = Path("workspace/repositories")
REPOSITORY_ROOT.mkdir(parents=True, exist_ok=True)


class RepositoryService:

    @staticmethod
    def repository_path(repo_name: str) -> Path:
        """
        Returns the local path of a repository.
        """
        return REPOSITORY_ROOT / repo_name

    @staticmethod
    def repository_exists(repo_name: str) -> bool:
        return RepositoryService.repository_path(repo_name).exists()

    @staticmethod
    def clone_repository(clone_url: str, repo_name: str) -> Path:

        repo_path = RepositoryService.repository_path(repo_name)

        print("=" * 60)
        print("Repository Path:", repo_path)
        print("Clone URL:", clone_url)
        print("=" * 60)

        if (repo_path / ".git").exists():
            print("Already cloned")
            return repo_path

        if repo_path.exists():
            import shutil
            shutil.rmtree(repo_path)

        try:

            Repo.clone_from(
                clone_url,
                repo_path
            )

            print("Clone successful")

            return repo_path

        except Exception as e:

            print("=" * 60)
            print(type(e))
            print(e)
            print("=" * 60)

            raise
    
    @staticmethod
    def pull_repository(repo_name: str):

        repo_path = RepositoryService.repository_path(repo_name)

        if not repo_path.exists():
            raise FileNotFoundError(repo_name)

        repo = Repo(repo_path)

        logger.info(f"Pulling {repo_name}")

        repo.remotes.origin.pull()

        logger.info(f"{repo_name} updated")

    @staticmethod
    def checkout_branch(
        repo_name: str,
        branch: str,
        create: bool = False,
    ):

        repo = Repo(
            RepositoryService.repository_path(repo_name)
        )

        if create:
            repo.git.checkout("-b", branch)
        else:
            repo.git.checkout(branch)

        logger.info(
            f"Checked out {branch}"
        )

    @staticmethod
    def delete_repository(
        repo_name: str,
    ):

        path = RepositoryService.repository_path(
            repo_name
        )

        if path.exists():

            shutil.rmtree(path)

            logger.info(
                f"Deleted {repo_name}"
            )

            