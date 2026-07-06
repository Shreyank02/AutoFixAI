from pydantic import BaseModel

class AnalysisResult(BaseModel):
    problem: str
    root_cause: str
    confidence: str
    evidence: list[str]
    missing_information: list[str]
    files_to_modify: list[str]
    implementation_steps: list[str]
    testing_strategy: list[str]


class CodePatch(BaseModel):
    file: str
    symbol: str
    reason: str
    old_code: str
    new_code: str


class DeveloperResult(BaseModel):
    patches: list[CodePatch]

class PatchResult(BaseModel):
    success: bool
    modified_files: list[str]
    errors: list[str]