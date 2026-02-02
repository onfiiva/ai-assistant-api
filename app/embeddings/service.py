from typing import List, Optional
from fastapi import Request
from app.core.timing import track_timing
from app.embeddings.clients.client import EmbeddingClient
from app.embeddings.schemas import SimilarityResult
from app.infra.db.qdrant import search as qdrant_search


class EmbeddingService:
    def __init__(self, client: EmbeddingClient):
        self.client = client

    async def embed(
        self,
        text: str,
        request: Optional[Request] = None,
    ) -> List[float]:
        """Getting embedding for text"""
        if request:
            with track_timing(request, "embedding"):
                vectors = await self.client.embed([text])
        else:
            vectors = await self.client.embed([text])
        return vectors[0]

    async def most_similar(
        self,
        query: str,
        top_k: int = 5,
        request: Optional[Request] = None,
    ) -> List[SimilarityResult]:
        """Finging top-k similar docs via Qdrant"""

        query_vector = await self.embed(query)

        query_vector = await self.embed(query, request=request)

        if request:
            with track_timing(request, "vector_search"):
                hits = qdrant_search(query_vector=query_vector, limit=top_k)
        else:
            hits = qdrant_search(query_vector=query_vector, limit=top_k)

        results = []
        for hit in hits:
            results.append(
                SimilarityResult(
                    document=hit.get("content", ""),
                    score=hit.get("score", 0.0),
                )
            )

        return results
