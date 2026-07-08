from fastapi import APIRouter
from fastapi import Request
from fastapi import HTTPException

from core.security import verify_signature
from services.github_service import GitHubService
from services.installation_service import InstallationService
router = APIRouter()


@router.post("/github")
async def github_webhook(request: Request):

    print("=" * 60)
    print("WEBHOOK HIT")
    print("=" * 60)

    payload = await request.body()

    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_signature(payload, signature):
        raise HTTPException(
            status_code=401,
            detail="Invalid Signature"
        )

    event = request.headers.get("X-GitHub-Event")

    print(f"EVENT = {event}")

    data = await request.json()

    print("=" * 60)
    print("EVENT :", event)
    print("ACTION:", data.get("action"))
    print("=" * 60)

    if event == "issues":

        print("ISSUE ACTION =", data["action"])
        
        if data["action"] == "opened":

            issue = {
                "title": data["issue"]["title"],
                "body": data["issue"]["body"],
                "number": data["issue"]["number"],
                "repository": data["repository"]["full_name"],
                "author": data["issue"]["user"]["login"],
                "owner": data["repository"]["owner"]["login"],
                "repo_name": data["repository"]["name"],
                "installation_id": data["installation"]["id"],
            }
            print("CALLING GitHubService.process_issue()")
            print(issue)
            GitHubService.process_issue(issue)

    elif event == "installation":

        InstallationService.handle_webhook(data)

    elif event == "installation_repositories":

        InstallationService.handle_repository_event(data)
        
    return {
        "status": "ok"
    }