from typing import List
from app.embeddings.clients.client import EmbeddingClient
from openai import OpenAI
import asyncio


class OpenAIEmbeddingClient(EmbeddingClient):
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.client = OpenAI()  # автоматически берёт OPENAI_API_KEY из env

    async def embed(self, texts: List[str]) -> List[List[float]]:
        # OpenAI SDK сейчас синхронный → оборачиваем в executor
        loop = asyncio.get_event_loop()

        def sync_call():
            resp = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [d.embedding for d in resp.data]

        return await loop.run_in_executor(None, sync_call)
