from langchain_ollama import ChatOllama


class LLMService:
    def __init__(self):
        self.model = ChatOllama(
            model="llama3.1:latest",
            temperature=0,
        )

    def invoke(self, prompt):
        return self.model.invoke(prompt)