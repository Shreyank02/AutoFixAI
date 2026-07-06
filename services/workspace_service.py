from pathlib import Path
import shutil

from utils.logger import logger

JOB_ROOT = Path("workspace/jobs")

JOB_ROOT.mkdir(
    parents=True,
    exist_ok=True,
)


class WorkspaceService:

    @staticmethod
    def workspace_path(
        issue_number: int,
    ):

        return JOB_ROOT / f"issue-{issue_number}"
    
    @staticmethod
    def workspace_exists(
        issue_number: int,
    ):

        return WorkspaceService.workspace_path(
            issue_number
        ).exists()
    
    @staticmethod
    def create_workspace(
        repo_name: str,
        issue_number: int,
    ):

        source = (
            Path("workspace/repositories")
            / repo_name
        )

        destination = WorkspaceService.workspace_path(
            issue_number
        )

        if destination.exists():

            shutil.rmtree(destination)

        shutil.copytree(
            source,
            destination,
        )

        logger.info(
            f"Workspace created for issue {issue_number}"
        )

        return destination
    
    @staticmethod
    def delete_workspace(
        issue_number: int,
    ):

        workspace = WorkspaceService.workspace_path(
            issue_number
        )

        if workspace.exists():

            shutil.rmtree(workspace)

            logger.info(
                f"Workspace deleted: {issue_number}"
            )
    
    @staticmethod
    def list_workspaces():

        return [
            folder.name
            for folder in JOB_ROOT.iterdir()
            if folder.is_dir()
        ]
    
