from pathlib import Path

from app_rag.schemas import CodeChunk


class CodeChunker:

    def chunk_repository(
        self,
        context,
    ):

        chunks = []

        for file in context.files:

            if file.extension != ".py":
                continue

            path = context.root_path / file.path

            source = path.read_text(
                encoding="utf-8"
            )

            lines = source.splitlines()

            # ---------- Functions ----------

            for function in file.structure.functions:

                code = "\n".join(

                    lines[
                        function.start_line - 1 :
                        function.end_line
                    ]

                )

                chunks.append(

                    CodeChunk(

                        repository=context.name,

                        file_path=str(file.path),

                        symbol=function.name,

                        symbol_type="function",

                        language=context.language,

                        framework=context.framework,

                        project_type=context.project_type,

                        code=code,

                    )

                )

            # ---------- Classes ----------

            for cls in file.structure.classes:

                code = "\n".join(

                    lines[
                        cls.start_line - 1 :
                        cls.end_line
                    ]

                )

                chunks.append(

                    CodeChunk(

                        repository=context.name,

                        file_path=str(file.path),

                        symbol=function.name,

                        symbol_type="function",

                        language=context.language,

                        framework=context.framework,

                        project_type=context.project_type,

                        imports=file.structure.imports,

                        code=code,

                    )

                )

        return chunks