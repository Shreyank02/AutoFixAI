from pathlib import Path
from app_rag.scanner import RepositoryScanner
from app_rag.retriever import RepositoryRetriever

class SupervisorAgent:

    def __init__(self):

        self.retriever = RepositoryRetriever()

    def run(self, state):

        repo_path = Path(
            "workspace/repositories"
        ) / state["repository"]

        scanner = RepositoryScanner(repo_path)

        repository_context = scanner.scan()

        issue = f"""
                    Title:
                    {state['issue_title']}

                    Description:
                    {state['issue_body']}
                    """

        results = self.retriever.retrieve(
            repository=state["repository"],
            issue_text=issue,
            top_k=10,
        )

        context = ""

        for result in results:

            payload = result.payload
            context += f"""
                        File:
                        {payload['file_path']}
                        Symbol:
                        {payload['symbol']}
                        Code:
                        {payload['code']}
                        =============================
                        """

        summary = f"""
                Repository
                Name:
                {repository_context.name}
                Language:
                {repository_context.language}
                Framework:
                {repository_context.framework}
                Project Type:
                {repository_context.project_type}
                Files:
                {len(repository_context.files)}
                Dependencies:
                {", ".join(repository_context.dependencies)}
                """
        state["repository_summary"] = summary
        state["retrieved_context"] = context

        return state