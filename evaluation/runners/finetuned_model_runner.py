import requests
from .base.base import BaseRunner


class FineTunedRunner(BaseRunner):
    def __init__(self, base_url):
        self.url = f"{base_url}/eval/finetuned"

    def run(self, question: str) -> str:
        response = requests.post(self.url, json={"prompt": question})
        return response.json().get("text", "")
