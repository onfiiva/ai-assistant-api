from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router

app = FastAPI(title="AI Assistant API")

app.include_router(auth_router)

app.include_router(chat_router)
