import json
from pathlib import Path

from agents.schemas import AnalysisResult


class AnalyzerAgent:

    def __init__(self, llm):
        self.llm = llm
        self.prompt = Path(
            "prompts/analyzer.txt"
        ).read_text(
            encoding="utf-8"
        )

    def run(self, state):

        user_prompt = f"""
Repository Summary:
{state["repository_summary"]}

Issue Title:
{state["issue_title"]}

Issue Description:
{state["issue_body"]}

Relevant Repository Context:
{state["retrieved_context"]}
"""

        response = self.llm.invoke(
            self.prompt + "\n\n" + user_prompt
        )

        print("=" * 80)
        print("RAW ANALYZER RESPONSE")
        print("=" * 80)
        print(response.content)
        print("=" * 80)

        content = response.content.strip()

        # Remove markdown code fences
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

        # Extract JSON if the model added extra text
        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            raise Exception(
                "Analyzer did not return JSON."
            )

        content = content[start:end + 1]

        try:

            data = json.loads(content)

        except Exception as e:

            print("=" * 80)
            print("FAILED TO PARSE ANALYZER JSON")
            print("=" * 80)
            print(content)
            print("=" * 80)

            raise Exception(
                f"Analyzer returned invalid JSON.\n{e}"
            )

        print("=" * 80)
        print("PARSED ANALYZER JSON")
        print("=" * 80)
        print(
            json.dumps(
                data,
                indent=4,
            )
        )
        print("=" * 80)

        # Fallback values in case the model omits fields
        data.setdefault("problem", "")
        data.setdefault("root_cause", "")
        data.setdefault("confidence", "low")
        data.setdefault("evidence", [])
        data.setdefault("missing_information", [])
        data.setdefault("files_to_modify", [])
        data.setdefault("implementation_steps", [])
        data.setdefault("testing_strategy", [])

        state["implementation_plan"] = AnalysisResult(
            **data
        )

        return state