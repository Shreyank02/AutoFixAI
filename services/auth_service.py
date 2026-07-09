from pathlib import Path
import time
import jwt
import requests

from core.config import settings


def load_private_key() -> str:
    key_path = Path(settings.GITHUB_PRIVATE_KEY)
    if not key_path.exists():
        raise FileNotFoundError(
            f"Private key not found: {key_path}"
        )

    return key_path.read_text()


def generate_app_jwt():
    now = int(time.time())

    payload = {
        "iat": now,
        "exp": now + 600,
        "iss": settings.GITHUB_APP_ID,
    }

    return jwt.encode(
        payload,
        load_private_key(),
        algorithm="RS256",
    )

def get_installation_token(installation_id: int):

    headers = {
        "Authorization": f"Bearer {generate_app_jwt()}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers=headers,
    )

    response.raise_for_status()

    return response.json()["token"]
