from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME")
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))

    GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
    GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
    GITHUB_PRIVATE_KEY = os.getenv("GITHUB_PRIVATE_KEY")

    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

settings = Settings()