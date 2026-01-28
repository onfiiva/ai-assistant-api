from typing import List
from app.embeddings.clients.client import EmbeddingClient
from app.embeddings.schemas import SimilarityResult
from app.infra.db.qdrant import search as qdrant_search


class EmbeddingService:
    def __init__(self, client: EmbeddingClient):
        self.client = client

    async def embed(self, text: str) -> List[float]:
        """Получаем embedding для текста"""
        vectors = await self.client.embed([text])
        return vectors[0]

    async def most_similar(
        self,
        query: str,
        top_k: int = 5
    ) -> List[SimilarityResult]:
        """Ищем top-k похожих документов через Qdrant"""
        query_vector = await self.embed(query)

        # search возвращает список Qdrant Hit объектов
        hits = qdrant_search(query_vector=query_vector, limit=top_k)

        results = []
        for hit in hits:
            results.append(SimilarityResult(
                document=hit.payload.get("content", ""),
                score=hit.score
            ))

        return results
