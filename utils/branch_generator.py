import re
from datetime import datetime


def generate_branch_name(
    issue_title: str,
) -> str:

    slug = issue_title.lower()

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        slug,
    )

    slug = slug.strip("-")

    timestamp = datetime.now().strftime(
        "%Y%m%d-%H%M"
    )

    return f"autofix/{slug}-{timestamp}"