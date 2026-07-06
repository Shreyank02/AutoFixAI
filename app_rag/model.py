from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field

class FunctionInfo(BaseModel):
    name: str
    start_line: int
    end_line: int


class ClassInfo(BaseModel):
    name: str
    start_line: int
    end_line: int


class CodeStructure(BaseModel):
    imports: list[str] = Field(default_factory=list)

    classes: list[ClassInfo] = Field(default_factory=list)

    functions: list[FunctionInfo] = Field(default_factory=list)

    globals: list[str] = Field(default_factory=list)

    line_count: int = 0
    
class FileInfo(BaseModel):
    path: Path
    extension: str
    language: Optional[str] = None
    size: int
    structure: CodeStructure = Field(
        default_factory=CodeStructure
    )


class DependencyInfo(BaseModel):
    name: str
    version: Optional[str] = None
    manager: str


class RepositoryContext(BaseModel):

    name: str

    root_path: Path

    language: Optional[str] = None

    framework: Optional[str] = None

    project_type: Optional[str] = None

    entry_points: List[Path] = Field(default_factory=list)

    libraries: List[str] = Field(default_factory=list)

    dependencies: List[DependencyInfo] = Field(default_factory=list)

    files: List[FileInfo] = Field(default_factory=list)

    features: List[str] = Field(default_factory=list)

