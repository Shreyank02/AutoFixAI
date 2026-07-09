import time

from services.job_service import JobService
from services.github_service import GitHubService

print("Worker Started")

while True:

    jobs = JobService.get_jobs()

    if jobs:

        job = jobs.pop(0)

        JobService.save_jobs(jobs)

        print(
            f"Processing {job['title']}"
        )

        GitHubService.process_issue(job)

    time.sleep(2)