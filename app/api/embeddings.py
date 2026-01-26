from fastapi import APIRouter, Query
from typing import List
from app.embeddings.service import EmbeddingService
from app.embeddings.schemas import SimilarityResult
from app.embeddings.factory import get_embedding_client

router = APIRouter(prefix="/embeddings", tags=["embeddings"])

# Docs example
DOCUMENTS = [
    "FastAPI — is a serious web-framework for Python",
    "Python — is a public use programming language",
    "OpenAI GPT — is a stong LLM",
    "Docker allows to containerize apps",
]


@router.post("/search", response_model=List[SimilarityResult])
async def search(
    query: str,
    top_k: int = Query(3, ge=1),
    provider: str = Query("gemini")
):
    client = get_embedding_client(provider)
    service = EmbeddingService(client)
    return await service.most_similar(query, DOCUMENTS, top_k=top_k)
