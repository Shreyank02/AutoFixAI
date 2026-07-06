import json

from pathlib import Path

from agents.schemas import AnalysisResult


class AnalyzerAgent:

    def __init__(self, llm):

        self.llm = llm

        self.prompt = Path(
            "prompts/analyzer.txt"
        ).read_text()

    def run(self, state):

        user_prompt = f"""
            Repository Summary

            {state["repository_summary"]}

            Issue

            Title:
            {state["issue_title"]}

            Description:
            {state["issue_body"]}

            Relevant Repository Context

            {state["retrieved_context"]}
            """

        response = self.llm.invoke(

            self.prompt + "\n\n" + user_prompt

        )

        data = json.loads(
            response.content
        )

        state["implementation_plan"] = AnalysisResult(
            **data
        )

        return state