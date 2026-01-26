from typing import List
from app.embeddings.clients.client import EmbeddingClient
from google import genai
import asyncio


class GeminiEmbeddedClient(EmbeddingClient):
    def __init__(self, model: str = "gemini-embedding-001"):
        self.model = model
        self.client = genai.Client()

    async def embed(self, texts: List[str]) -> List[List[float]]:
        # Gemini SDK is sync -> wrap in thread executor
        return await asyncio.to_thread(self._sync_embed, texts)

    def _sync_embed(self, texts: List[str]) -> List[List[float]]:
        # here we actually call the Gemini SDK
        result = self.client.models.embed_content(
            model=self.model,
            contents=texts
        )

        # unwrap Gemini embeddings
        embeddings: list[list[float]] = []

        for emb in result.embeddings:
            if hasattr(emb, "values"):
                embeddings.append([float(v) for v in emb.values])
            else:
                raise ValueError(f"Unexpected embedding format: {emb}")
        # return list of vectors
        return embeddings
