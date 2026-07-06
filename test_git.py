from pathlib import Path
from git import Repo

from services.git_service import GitService
from utils.branch_generator import generate_branch_name

repository = Path(
    "workspace/repositories/licence-plate-detection-and-iot-integration"
)

branch = generate_branch_name(
    "Database lookup fails"
)

GitService.create_branch(
    repository,
    branch,
)

GitService.commit_changes(
    repository,
    "Test Commit",
)

GitService.push_branch(
    repository_path=repository,
    owner="Shreyank02",
    repository="licence-plate-detection-and-iot-integration",
    installation_id=144356878,
    branch_name=branch,
)

repo = Repo(repository)

print("\nCurrent Branch:")
print(repo.active_branch.name)

print("\nAll Branches:")

for b in repo.branches:
    print("-", b.name)

print("\nPush completed successfully.")