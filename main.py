from fastapi import FastAPI

from api.webhook import router
from core.config import settings

app = FastAPI(
    title=settings.APP_NAME
)

app.include_router(
    router,
    prefix="/webhooks"
)


@app.get("/")
def home():
    return {
        "message": "AutoFix AI Running"
    }

@app.get("/")
def health():
    return {
        "status": "running",
        "service": "AutoFix AI"
    }