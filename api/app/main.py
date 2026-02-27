from fastapi import Depends, FastAPI
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.ingestion import router as ingest_router
from app.api.search import router as search_router
from app.api.chat_async import router as async_chat_router
from app.api.inference import router as inference_router
from app.api.agents import router as agents_router
from app.api.smart_chat import router as smart_chat_router
from app.api.lmstudio import router as lmstudio_router
from app.api import embeddings
from app.dependencies.auth import auth_dependency
from app.infra.db.qdrant import create_collection
from app.middlewares.body import body_middleware
from app.container import embedding_service, vector_store
from app.middlewares.observability import ObservabilityMiddleware
from app.startup import create_initial_admin

app = FastAPI(title="AI Assistant API")

app.middleware("http")(body_middleware)

app.add_middleware(ObservabilityMiddleware)

app.include_router(agents_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(async_chat_router)
app.include_router(smart_chat_router)
app.include_router(inference_router)
app.include_router(embeddings.router)
app.include_router(ingest_router)
app.include_router(search_router)
app.include_router(lmstudio_router)


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

    create_collection()

    await create_initial_admin()


@app.get("/health", tags=["health"], dependencies=[Depends(auth_dependency)])
async def health():
    return {"status": "ok"}
