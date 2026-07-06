from pathlib import Path

from agents.schemas import (
    CodePatch,
    DeveloperResult,
)

from services.patch_service import PatchService


repository = Path(
    "workspace/repositories/licence-plate-detection-and-iot-integration"
)

developer = DeveloperResult(

    patches=[
        CodePatch(

            file="check_db.py",

            symbol="check_plate_in_database",

            reason="Testing Patch Service",

            old_code="THIS DOES NOT EXIST",

            new_code="""
# conn.close()
""",
        )
    ]
)

result = PatchService.apply_patches(
    repository,
    developer,
)

print(result)