import time

from services.job_service import JobService
from services.github_service import GitHubService

print("=" * 70)
print("AUTOFIX AI WORKER STARTED")
print("=" * 70)

while True:

    jobs = JobService.get_pending_jobs()

    if jobs:

        job = jobs[0]

        print("=" * 70)
        print("NEW JOB FOUND")
        print(job["title"])
        print("=" * 70)

        JobService.update_status(
            job["id"],
            "processing",
        )

        issue = {
            "title": job["title"],
            "body": job["body"],
            "number": job["issue_number"],
            "repository": job["repository"],
            "author": job["author"],
            "owner": job["owner"],
            "repo_name": job["repo_name"],
            "installation_id": job["installation_id"],
        }

        try:

            GitHubService.process_issue(
                issue
            )

            JobService.update_status(
                job["id"],
                "completed",
            )

        except Exception as e:

            print(e)

            JobService.update_status(
                job["id"],
                "failed",
            )

    time.sleep(2)