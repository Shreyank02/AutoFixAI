from langgraph.graph import StateGraph
from langgraph.graph import END

from agents.state import WorkflowState
from agents.supervisor import SupervisorAgent
from agents.analyzer import AnalyzerAgent
from agents.developer import DeveloperAgent
from agents.reviewer import ReviewAgent
from agents.llm import LLMService


llm = LLMService()

supervisor = SupervisorAgent()
analyzer = AnalyzerAgent(llm)
developer = DeveloperAgent(llm)
reviewer = ReviewAgent()
builder = StateGraph(WorkflowState)


def supervisor_node(state):
    return supervisor.run(state)

def analyzer_node(state):
    return analyzer.run(state)

def developer_node(state):
    return developer.run(state)

def reviewer_node(state):
    return reviewer.run(state)


builder.add_node(
    "Supervisor",
    supervisor_node,
)
builder.add_node(
    "Analyzer",
    analyzer_node,
)
builder.add_node(
    "Developer",
    developer_node,
)
builder.add_node(
    "Reviewer",
    reviewer_node,
)
builder.set_entry_point(
    "Supervisor"
)
builder.add_edge(
    "Supervisor",
    "Analyzer",
)
builder.add_edge(
    "Analyzer",
    "Developer",
)
builder.add_edge(
    "Developer",
    "Reviewer",
)
builder.add_edge(
    "Reviewer",
    END,
)

workflow = builder.compile()