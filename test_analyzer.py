from agents.supervisor import SupervisorAgent
from agents.analyzer import AnalyzerAgent
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

supervisor = SupervisorAgent()

state = supervisor.run(state)

llm = LLMService()

analyzer = AnalyzerAgent(llm)

state = analyzer.run(state)

print(state["implementation_plan"])