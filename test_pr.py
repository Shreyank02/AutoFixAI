from services.github_api_services import GitHubAPIService

INSTALLATION_ID = 144356878  # Your installation id

response = GitHubAPIService.create_pull_request(

    owner="Shreyank02",

    repository="licence-plate-detection-and-iot-integration",

    installation_id=INSTALLATION_ID,

    title="Test PR from AutoFix AI",

    body="This is an automated pull request created during testing.",

    head="autofix/database-lookup-fails-20260706-1330",

    base="main",

)

print(response["html_url"])