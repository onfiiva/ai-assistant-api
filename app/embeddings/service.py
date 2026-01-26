from typing import List
from app.embeddings.clients.client import EmbeddingClient
from app.embeddings.similarity import cosine_similarity
from app.embeddings.schemas import SimilarityResult


class EmbeddingService:
    def __init__(self, client: EmbeddingClient):
        self.client = client

    async def most_similar(
        self,
        query: str,  # <-- our query to form vecs
        documents: List[str],   # <-- docs to complete text by vecs
        top_k: int = 3  # <-- results limit
    ) -> List[SimilarityResult]:
        vectors = await self.client.embed([query] + documents)

        query_vec = vectors[0]
        doc_vec = vectors[1:]

        scored = [
            SimilarityResult(document=doc, score=cosine_similarity(query_vec, vec))
            for doc, vec in zip(documents, doc_vec)
        ]

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]
