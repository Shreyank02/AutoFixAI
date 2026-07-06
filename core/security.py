import hashlib
import hmac

from core.config import settings


def verify_signature(payload: bytes, signature: str | None) -> bool:
    """
    Verify GitHub webhook signature.
    """

    if signature is None:
        return False

    secret = settings.GITHUB_WEBHOOK_SECRET.encode()

    expected = "sha256=" + hmac.new(
        secret,
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)