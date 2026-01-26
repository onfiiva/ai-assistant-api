from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api import embeddings
from app.middlewares.body import body_middleware

app = FastAPI(title="AI Assistant API")

app.middleware("http")(body_middleware)

app.include_router(auth_router)

app.include_router(chat_router)

app.include_router(embeddings.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
