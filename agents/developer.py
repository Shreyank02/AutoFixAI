import json
from pathlib import Path

from agents.schemas import DeveloperResult


class DeveloperAgent:

    def __init__(self, llm):
        self.llm = llm
        self.prompt = Path(
            "prompts/developer.txt"
        ).read_text(
            encoding="utf-8"
        )

    def run(self, state):

        plan = state["implementation_plan"]

        if plan.confidence == "low":
            print("Analyzer confidence is low.")
            return state

        prompt = f"""
Issue Title:
{state["issue_title"]}

Issue Description:
{state["issue_body"]}

Problem:
{plan.problem}

Root Cause:
{plan.root_cause}

Files To Modify:
{", ".join(plan.files_to_modify)}

Implementation Steps:
{chr(10).join(plan.implementation_steps)}

Relevant Code:
{state["retrieved_context"]}
"""

        response = self.llm.invoke(
            self.prompt + "\n\n" + prompt
        )

        print("=" * 80)
        print("RAW LLM RESPONSE")
        print("=" * 80)
        print(response.content)
        print("=" * 80)

        content = response.content.strip()

        if content.startswith("```json"):
            content = content.replace(
                "```json",
                "",
                1,
            )

        if content.startswith("```"):
            content = content.replace(
                "```",
                "",
                1,
            )

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        try:
            patches = json.loads(content)

        except Exception as e:

            print("=" * 80)
            print("FAILED TO PARSE JSON")
            print("=" * 80)
            print(content)
            print("=" * 80)

            raise Exception(
                f"Developer Agent returned invalid JSON.\n{e}"
            )

        if "patches" not in patches:
            raise Exception(
                "Developer response does not contain 'patches'."
            )

        for patch in patches["patches"]:

            patch.setdefault(
                "reason",
                f"Fix {patch.get('symbol', 'code')}"
            )

            patch.setdefault(
                "symbol",
                "unknown"
            )

        print("=" * 80)
        print("PARSED PATCHES")
        print("=" * 80)
        print(
            json.dumps(
                patches,
                indent=4,
            )
        )
        print("=" * 80)

        state["generated_code"] = DeveloperResult(
            **patches
        )

        return state