from fastapi import APIRouter
from app.container import embedding_service

router = APIRouter(prefix="/search")


@router.get("/")
async def search(q: str, k: int = 5):
    results = await embedding_service.most_similar(query=q, top_k=k)
    return {
        "query": q,
        "k": k,
        "results": [
            {"document": r.document, "score": r.score}
            for r in results
        ]
    }
