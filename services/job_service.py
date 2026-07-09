import json
from pathlib import Path
from threading import Lock

JOB_FILE = Path("jobs/jobs.json")
JOB_FILE.parent.mkdir(exist_ok=True)

if not JOB_FILE.exists():
    JOB_FILE.write_text("[]")

_lock = Lock()


class JobService:

    @staticmethod
    def add_job(job):

        with _lock:

            jobs = json.loads(
                JOB_FILE.read_text()
            )

            jobs.append(job)

            JOB_FILE.write_text(
                json.dumps(
                    jobs,
                    indent=4,
                )
            )

    @staticmethod
    def get_jobs():

        with _lock:

            return json.loads(
                JOB_FILE.read_text()
            )

    @staticmethod
    def save_jobs(jobs):

        with _lock:

            JOB_FILE.write_text(
                json.dumps(
                    jobs,
                    indent=4,
                )
            )