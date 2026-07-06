from pathlib import Path

from git import Repo, GitCommandError

from services.auth_service import get_installation_token
from utils.logger import logger


class GitService:

    @staticmethod
    def create_branch(
        repository_path: Path,
        branch_name: str,
    ) -> str:

        repo = Repo(repository_path)

        branches = [branch.name for branch in repo.branches]

        if branch_name in branches:
            repo.git.checkout(branch_name)
            logger.info(f"Checked out existing branch: {branch_name}")
        else:
            repo.git.checkout("-b", branch_name)
            logger.info(f"Created branch: {branch_name}")

        return branch_name

    @staticmethod
    def commit_changes(
        repository_path: Path,
        message: str,
    ):

        repo = Repo(repository_path)

        repo.git.add(A=True)

        if repo.is_dirty(untracked_files=True):
            commit = repo.index.commit(message)
            logger.info(f"Commit created: {commit.hexsha}")
            return commit.hexsha

        logger.info("No changes to commit.")
        return None

    @staticmethod
    def push_branch(
        repository_path: Path,
        owner: str,
        repository: str,
        installation_id: int,
        branch_name: str,
    ):

        token = get_installation_token(installation_id)

        authenticated_remote = (
            f"https://x-access-token:{token}"
            f"@github.com/{owner}/{repository}.git"
        )

        repo = Repo(repository_path)

        origin = repo.remote("origin")

        origin.set_url(authenticated_remote)

        logger.info(f"Pushing branch: {branch_name}")

        origin.push(
            refspec=f"{branch_name}:{branch_name}"
        )

        logger.info("Push successful.")

    @staticmethod
    def checkout_default_branch(
        repository_path: Path,
    ):

        repo = Repo(repository_path)

        for branch in ("main", "master"):

            try:
                repo.git.checkout(branch)
                logger.info(f"Checked out {branch}")
                return branch
            except GitCommandError:
                pass

        raise RuntimeError(
            "Neither 'main' nor 'master' exists."
        )