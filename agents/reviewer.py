from pathlib import Path

import ast


class ReviewAgent:

    def run(self, state):

        patches = state["generated_code"]

        report = []

        valid = True

        if patches is None:

            state["review_status"] = False

            state["review_report"] = "Developer produced no patches."

            return state

        for patch in patches.patches:

            if not patch.old_code.strip():

                valid = False

                report.append(

                    f"{patch.file}: empty old_code"

                )

            if not patch.new_code.strip():

                valid = False

                report.append(

                    f"{patch.file}: empty new_code"

                )

            if patch.old_code == patch.new_code:

                valid = False

                report.append(

                    f"{patch.file}: patch changes nothing"

                )

            if patch.file.endswith(".py"):

                try:

                    ast.parse(patch.new_code)

                except Exception as e:

                    valid = False

                    report.append(

                        f"{patch.file}: invalid python\n{e}"

                    )

        state["review_status"] = valid

        state["review_report"] = "\n".join(report)

        return state