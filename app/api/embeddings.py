from fastapi import APIRouter, Depends, Query
from typing import List
from app.dependencies.auth import auth_dependency
from app.dependencies.rate_limit import rate_limit_dependency
from app.embeddings.service import EmbeddingService
from app.embeddings.schemas import SimilarityResult
from app.embeddings.factory import get_embedding_client

router = APIRouter(
    prefix="/embeddings",
    tags=["embeddings"],
    dependencies=[Depends(auth_dependency)]
)

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
    provider: str = Query("gemini"),
    _: None = Depends(rate_limit_dependency)
):
    client = get_embedding_client(provider)
    service = EmbeddingService(client)
    return await service.most_similar(query, DOCUMENTS, top_k=top_k)
