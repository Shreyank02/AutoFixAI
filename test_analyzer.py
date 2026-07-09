from agents.llm import LLMService
from pathlib import Path

llm = LLMService()

prompt = Path("prompts/analyzer.txt").read_text()

user_prompt = """
Repository Summary:
Repository Name: autofix_testing_repo

Issue:
subtract() function is not working

Relevant Code:

def subtract(a, b):
    return a + b
"""

response = llm.invoke(prompt + "\n\n" + user_prompt)

print(response)
print("=" * 80)
print(repr(response.content))