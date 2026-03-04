import requests
from .base.base import BaseRunner


class RAGRunner(BaseRunner):
    def __init__(self, base_url):
        self.url = f"{base_url}/eval/rag"

    def run(self, question: str) -> str:
        response = requests.post(self.url, json={"question": question})
        return response.json().get("text", "")
