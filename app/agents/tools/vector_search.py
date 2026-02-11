from app.embeddings.factory import get_embedding_client
from app.embeddings.service import EmbeddingService
from app.core.config import settings
from app.infra.db import qdrant
from .base import Tool
from app.agents.schemas import ActionType


class VectorSearchTool(Tool):
    name = ActionType.VECTOR_SEARCH

    def __init__(self):
        embedding_client = get_embedding_client(settings.EMBEDDING_PROVIDER)
        self.embedding_service = EmbeddingService(
            client=embedding_client
        )
        self.use_qdrant = True  # switch between Qdrant & FAISS

        # Lazy initialization for FAISS
        self.faiss_index = None

    def run(self, input: str, top_k: int = 5) -> str:
        # 1. Get embedding
        embedding = self.embedding_service.embed_text(input)

        # 2. Choose the base for search
        if self.use_qdrant:
            results = qdrant.search(query_vector=embedding, limit=top_k)
            return "\n".join(
                [
                    f"{r['content']} (score: {r['score']:.3f})"
                    for r in results
                ]
            )
        else:
            if self.faiss_index is None:
                raise ValueError("FAISS index is not built")
            results = self.faiss_index.search(query_embedding=embedding, k=top_k)
            return "\n".join(
                [
                    f"{doc} (score: {score:.3f})"
                    for doc, score in results
                ]
            )
