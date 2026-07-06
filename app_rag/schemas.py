from pydantic import BaseModel, Field


class CodeChunk(BaseModel):

    repository: str

    file_path: str

    symbol: str

    symbol_type: str

    language: str | None = None

    framework: str | None = None

    project_type: str | None = None

    imports: list[str] = Field(default_factory=list)

    code: str

    def embedding_text(self):

        return f"""
Repository:
{self.repository}

Language:
{self.language}

Framework:
{self.framework}

Project:
{self.project_type}

File:
{self.file_path}

Type:
{self.symbol_type}

Symbol:
{self.symbol}

Imports:
{", ".join(self.imports)}

Code:

{self.code}
"""