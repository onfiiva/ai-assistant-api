from app.embeddings.clients.openai_client import OpenAIEmbeddingClient
from app.embeddings.clients.gemini_client import GeminiEmbeddedClient
from app.embeddings.clients.lmstudio_client import LMStudioEmbeddingClient


def get_embedding_client(provider: str):
    if provider == "openai":
        return OpenAIEmbeddingClient()
    if provider == "gemini":
        return GeminiEmbeddedClient()
    if provider == "lmstudio":
        return LMStudioEmbeddingClient()
    else:
        raise ValueError(f"Unknown embedding provider: '{provider}'")
