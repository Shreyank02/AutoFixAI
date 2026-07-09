from langchain_openai import ChatOpenAI
from core.config import settings

class LLMService:
    def __init__(self):
        self.model = ChatOpenAI(
            model=settings.OPENROUTER_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=0,
            model_kwargs={
                "response_format": {
                    "type": "json_object"
                }
            }
            timeout=120,
        )
    def invoke(self, prompt):
        return self.model.invoke(prompt)