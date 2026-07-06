from pathlib import Path

from agents.schemas import (
    DeveloperResult,
    PatchResult,
)


class PatchService:

    @staticmethod
    def apply_patches(
        repository_path: Path,
        patches: DeveloperResult,
    ) -> PatchResult:

        backups = {}

        modified_files = []

        errors = []

        try:

            for patch in patches.patches:

                file_path = repository_path / patch.file

                if not file_path.exists():

                    raise FileNotFoundError(
                        f"{patch.file} not found."
                    )

                original_text = file_path.read_text(
                    encoding="utf-8"
                )

                backups[file_path] = original_text

                if not patch.old_code.strip():

                    raise ValueError(
                        f"{patch.file}: old_code is empty."
                    )

                if patch.old_code not in original_text:

                    raise ValueError(
                        f"{patch.file}: old_code not found."
                    )

                updated_text = original_text.replace(
                    patch.old_code,
                    patch.new_code,
                    1,
                )

                file_path.write_text(
                    updated_text,
                    encoding="utf-8",
                )

                modified_files.append(
                    patch.file
                )

            return PatchResult(
                success=True,
                modified_files=modified_files,
                errors=[],
            )

        except Exception as e:

            # Rollback every modified file
            for file_path, original_text in backups.items():

                file_path.write_text(
                    original_text,
                    encoding="utf-8",
                )

            errors.append(str(e))

            return PatchResult(
                success=False,
                modified_files=[],
                errors=errors,
            )