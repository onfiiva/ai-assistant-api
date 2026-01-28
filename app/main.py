from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.ingestion import router as ingest_router
from app.api.search import router as search_router
from app.api import embeddings
from app.middlewares.body import body_middleware
from app.container import embedding_service, vector_store

app = FastAPI(title="AI Assistant API")

app.middleware("http")(body_middleware)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(embeddings.router)
app.include_router(ingest_router)
app.include_router(search_router)


@app.on_event("startup")
async def startup():
    texts = [
        "FastAPI tutorial",
        "How to cook pasta",
        "Vector databases and embeddings",
        "Python async programming",
        "Machine learning basics"
    ]

    embeddings = []
    for t in texts:
        vec = await embedding_service.embed(t)
        embeddings.append(vec)

    vector_store.build(embeddings, texts)


@app.get("/health")
async def health():
    return {"status": "ok"}
