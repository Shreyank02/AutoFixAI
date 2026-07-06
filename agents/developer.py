import json

from pathlib import Path

from agents.schemas import DeveloperResult


class DeveloperAgent:

    def __init__(self, llm):

        self.llm = llm

        self.prompt = Path(
            "prompts/developer.txt"
        ).read_text()

    def run(self, state):

        plan = state["implementation_plan"]

        if plan.confidence == "low":

            print("Analyzer confidence is low.")

            return state

        prompt = f"""
            Issue

            Title:
            {state["issue_title"]}

            Description:
            {state["issue_body"]}

            Problem

            {plan.problem}

            Root Cause

            {plan.root_cause}

            Files To Modify

            {", ".join(plan.files_to_modify)}

            Implementation Steps

            {chr(10).join(plan.implementation_steps)}

            Relevant Code

            {state["retrieved_context"]}
            """

        response = self.llm.invoke(

            self.prompt + "\n\n" + prompt

        )

        patches = json.loads(
            response.content
        )

        state["generated_code"] = DeveloperResult(
            **patches
        )

        return state