from pathlib import Path
from git import Repo, GitCommandError
from services.auth_service import get_installation_token
from utils.logger import logger


class GitService:

    @staticmethod
    def checkout_default_branch(
        repository_path: Path,
    ) -> str:
        repo = Repo(repository_path)
        for branch in ("main", "master"):
            try:
                repo.git.checkout(branch)
                try:
                    repo.remotes.origin.pull(branch)
                except Exception:
                    logger.warning(
                        f"Could not pull latest {branch}."
                    )
                logger.info(f"Checked out {branch}")
                return branch
            except GitCommandError:
                pass
        raise RuntimeError(
            "Neither 'main' nor 'master' exists."
        )

    @staticmethod
    def create_branch(
        repository_path: Path,
        branch_name: str,
    ) -> str:
        repo = Repo(repository_path)
        branches = [b.name for b in repo.branches]
        if branch_name in branches:
            repo.git.checkout(branch_name)
            logger.info(
                f"Checked out existing branch: {branch_name}"
            )

        else:
            repo.git.checkout("-b", branch_name)
            logger.info(
                f"Created branch: {branch_name}"
            )
        return branch_name

    @staticmethod
    def commit_changes(
        repository_path: Path,
        message: str,
    ):
        repo = Repo(repository_path)
        repo.git.add(A=True)
        if not repo.is_dirty(untracked_files=True):
            logger.info(
                "No changes detected. Nothing to commit."
            )

            return None
        commit = repo.index.commit(message)
        logger.info(
            f"Commit created: {commit.hexsha}"
        )
        return commit.hexsha

    @staticmethod
    def push_branch(
        repository_path: Path,
        owner: str,
        repository: str,
        installation_id: int,
        branch_name: str,
    ):
        token = get_installation_token(
            installation_id
        )
        authenticated_remote = (
            f"https://x-access-token:{token}"
            f"@github.com/{owner}/{repository}.git"
        )
        repo = Repo(repository_path)
        origin = repo.remote("origin")
        origin.set_url(authenticated_remote)
        logger.info(
            f"Pushing branch: {branch_name}"
        )
        results = origin.push(
            refspec=f"{branch_name}:{branch_name}"
        )
        for result in results:
            logger.info(result.summary)
            if result.flags & result.ERROR:
                raise RuntimeError(
                    f"Git Push Failed: {result.summary}"
                )

        logger.info("Push successful.")
        return True