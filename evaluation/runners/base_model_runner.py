import httpx
from .base.base import BaseRunner


class BaseModelRunner(BaseRunner):
    def __init__(self, base_url):
        self.url = f"{base_url}/eval/base"

    async def run(self, question: str) -> str:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(self.url, json={"prompt": question})
            data = resp.json()
            return data.get("answer", "")
