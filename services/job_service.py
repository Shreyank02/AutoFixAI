from supabase import create_client

from core.config import settings


supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY,
)


class JobService:

    @staticmethod
    def add_job(job: dict):

        data = {
            "status": "queued",
            "title": job["title"],
            "body": job["body"],
            "issue_number": job["number"],
            "repository": job["repository"],
            "owner": job["owner"],
            "repo_name": job["repo_name"],
            "author": job["author"],
            "installation_id": job["installation_id"],
        }

        response = (
            supabase
            .table("jobs")
            .insert(data)
            .execute()
        )

        print("=" * 60)
        print("JOB INSERTED INTO SUPABASE")
        print(response.data)
        print("=" * 60)

    @staticmethod
    def get_pending_jobs():

        response = (
            supabase
            .table("jobs")
            .select("*")
            .eq("status", "queued")
            .order("id")
            .execute()
        )

        return response.data

    @staticmethod
    def update_status(
        job_id: int,
        status: str,
    ):

        (
            supabase
            .table("jobs")
            .update(
                {
                    "status": status,
                }
            )
            .eq("id", job_id)
            .execute()
        )

    @staticmethod
    def delete_job(
        job_id: int,
    ):

        (
            supabase
            .table("jobs")
            .delete()
            .eq("id", job_id)
            .execute()
        )