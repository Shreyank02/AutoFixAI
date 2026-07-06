from agents.schemas import (
    AnalysisResult,
    DeveloperResult,
    PatchResult,
)
from typing import TypedDict

class WorkflowState(TypedDict):
    issue_title: str
    issue_body: str
    repository: str
    repository_summary: str
    retrieved_context: str
    implementation_plan: AnalysisResult | None
    generated_code: DeveloperResult | None
    patch_result: PatchResult | None
    review_status: bool
    review_report: str