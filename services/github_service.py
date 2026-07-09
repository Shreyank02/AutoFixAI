from utils.logger import logger
from pathlib import Path
from app_rag.indexer import RepositoryIndexer
from services.repository_service import RepositoryService
from services.auth_service import get_installation_token
from services.git_service import GitService
from services.patch_service import PatchService
from services.github_api_services import GitHubAPIService

from utils.pr_generator import (
    create_pr_title,
    create_pr_body,
)

from app_rag.scanner import RepositoryScanner
from app_rag.retriever import RepositoryRetriever

from agents.workflow import workflow


class GitHubService:

    @staticmethod
    def process_issue(issue_data: dict):

        print("=" * 70)
        print("ENTERED process_issue()")
        print(issue_data)
        print("=" * 70)

        logger.info("=" * 70)
        logger.info("AUTOFIX AI STARTED")
        logger.info("=" * 70)

        logger.info(f"Issue : {issue_data['title']}")
        logger.info(f"Repository : {issue_data['repository']}")

        repository_name = issue_data["repository"].split("/")[-1]

        repository_path = RepositoryService.repository_path(
            repository_name
        )
        if not RepositoryService.repository_exists(repository_name):

            logger.info(
                "Repository not found locally. Cloning..."
            )

        installation_id = issue_data["installation_id"]
        owner = issue_data["owner"]
        repo_name = issue_data["repo_name"]

        logger.info("Repository not found locally. Cloning...")

        token = get_installation_token(installation_id)

        clone_url = (
            f"https://x-access-token:{token}"
            f"@github.com/{owner}/{repo_name}.git"
        )

        repository_path = RepositoryService.clone_repository(
            clone_url=clone_url,
            repo_name=repo_name,
        )

        logger.info("Repository cloned successfully.")

        logger.info(
            f"[1/4] Repository Located : {repository_path}"
        )

        scanner = RepositoryScanner(
            repository_path
        )

        context = scanner.scan()

        logger.info(
            "[2/4] Repository Scan Completed"
        )

        # indexer = RepositoryIndexer()

        # indexer.index_repository(context)

        logger.info(
            "[3/4] Repository Indexed"
        )

        retriever = RepositoryRetriever()

        results = retriever.retrieve(
            repository=repository_name,
            issue_text=issue_data["title"],
            top_k=8,
        )

        print(results[0].payload)

        retrieved_context = "\n\n".join(
            [
                f"""
        File: {r.payload.get("file_path")}
        Symbol: {r.payload.get("symbol")}
        Type: {r.payload.get("symbol_type")}
        Language: {r.payload.get("language")}

        Code:
        {r.payload.get("code")}
        """
                for r in results
            ]
        )

        logger.info(
            f"[4/4] Retrieved {len(results)} Code Chunks"
        )

        repository_summary = f"""
            Repository : {context.name}
            Language : {context.language}
            Framework : {context.framework}
            Project Type : {context.project_type}
            Files : {len(context.files)}
            Libraries :
            {", ".join(context.libraries)}
            """

        print("=" * 80)
        print("RETRIEVED CONTEXT")
        print("=" * 80)
        print(retrieved_context)
        print("=" * 80)
        
        state = {
            "issue_title": issue_data["title"],
            "issue_body": issue_data["body"],
            "repository": repository_name,
            "repository_summary": repository_summary,
            "retrieved_context": retrieved_context,
            "implementation_plan": None,
            "generated_code": None,
            "patch_result": None,
            "review_status": False,
            "review_report": "",
        }

        logger.info("=" * 70)
        logger.info("[5/6] Running LangGraph Workflow")
        logger.info("=" * 70)

        result = workflow.invoke(state)

        logger.info("=" * 70)
        logger.info("[6/6] Workflow Completed")
        logger.info("=" * 70)


        analysis = result["implementation_plan"]

        logger.info("ANALYZER RESULT")
        logger.info("-" * 70)

        print(analysis)

        developer = result["generated_code"]

        logger.info("DEVELOPER RESULT")
        logger.info("-" * 70)

        print(developer)
        
        logger.info("=" * 70)
        logger.info("APPLYING PATCH")
        logger.info("=" * 70)

        GitService.checkout_default_branch(
            repository_path
        )

        branch_name = (
            f"autofix/issue-{issue_data['number']}"
        )

        GitService.create_branch(
            repository_path,
            branch_name,
        )

        patch_result = PatchService.apply_patches(
            repository_path,
            developer,
        )

        if not patch_result.success:

            raise Exception(
                "\n".join(
                    patch_result.errors
                )
            )

        logger.info(
            f"Patched Files : {patch_result.modified_files}"
        )

        commit_sha = GitService.commit_changes(
            repository_path,
            f"Fix issue #{issue_data['number']} : {issue_data['title']}"
        )

        if commit_sha is None:

            raise Exception(
                "Nothing was committed."
            )

        logger.info(
            f"Commit Created : {commit_sha}"
        )

        GitService.push_branch(
            repository_path=repository_path,
            owner=owner,
            repository=repo_name,
            installation_id=installation_id,
            branch_name=branch_name,
        )

        logger.info("Branch pushed successfully.")

        pr = GitHubAPIService.create_pull_request(
            owner=owner,
            repository=repo_name,
            installation_id=installation_id,
            title=create_pr_title(analysis),
            body=create_pr_body(analysis),
            head=branch_name,
        )

        logger.info("=" * 70)
        logger.info("PULL REQUEST CREATED")
        logger.info(pr["html_url"])
        logger.info("=" * 70)

        logger.info("=" * 70)
        logger.info("AUTOFIX AI COMPLETED")
        logger.info("=" * 70)

        return {
            "branch": branch_name,
            "commit": commit_sha,
            "pull_request": pr["html_url"],
        }
