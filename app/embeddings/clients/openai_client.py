from typing import List
from app.embeddings.clients.client import EmbeddingClient
import openai


class OpenAIEmbeddingClient(EmbeddingClient):
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model

    async def embed(self, texts: List[str]) -> List[List[float]]:
        # Using OpenAI API to get embeddings
        response = openai.Embedding.create(
            model=self.model,
            input=texts
        )
        # In OpenAI response.data[i].embedding - vector itselfs
        return [item["embedding"] for item in response["data"]]
