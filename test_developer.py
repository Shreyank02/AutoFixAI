from agents.supervisor import SupervisorAgent
from agents.analyzer import AnalyzerAgent
from agents.developer import DeveloperAgent

from agents.llm import LLMService


state = {

    "issue_title":
        "Database lookup fails",

    "issue_body":
        "Vehicle is detected but database lookup fails.",

    "repository":
        "licence-plate-detection-and-iot-integration",

    "retrieved_context": "",

    "implementation_plan": "",

    "generated_code": "",

}

llm = LLMService()

supervisor = SupervisorAgent()

analyzer = AnalyzerAgent(llm)

developer = DeveloperAgent(llm)

state = supervisor.run(state)

state = analyzer.run(state)

state = developer.run(state)

for patch in state["generated_code"].patches:

    print()

    print("File :", patch.file)

    print()

    print("Replace")

    print("-" * 40)

    print(patch.old_code)

    print()

    print("With")

    print("-" * 40)

    print(patch.new_code)

    print("=" * 80)