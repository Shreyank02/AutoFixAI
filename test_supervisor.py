from agents.supervisor import SupervisorAgent

state = {

    "issue_title": "Database lookup fails",

    "issue_body": "Vehicle is detected but database lookup fails.",

    "repository": "licence-plate-detection-and-iot-integration",

    "retrieved_context": "",

    "implementation_plan": "",

    "generated_code": "",

}

agent = SupervisorAgent()

state = agent.run(state)

print(state["retrieved_context"])