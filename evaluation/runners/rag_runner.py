import httpx
from .base.base import BaseRunner


class RAGRunner(BaseRunner):
    def __init__(self, base_url):
        self.url = f"{base_url}/eval/rag"

    async def run(self, question: str) -> str:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(self.url, json={"prompt": question})
            data = resp.json()

            return {
                "text": data.get("text", ""),
                "retrieved_chunks": data.get("retrieved_chunks", []),
                "filtered_chunks": data.get("filtered_chunks", [])
            }
