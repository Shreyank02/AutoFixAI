from services.github_client import GitHubClient

INSTALLATION_ID = 144356878

client = GitHubClient(INSTALLATION_ID)

repo = client.get_repository(
    "Shreyank02",
    "Tabby",
)

print(repo["full_name"])