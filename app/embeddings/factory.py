from app.embeddings.clients.openai_client import OpenAIEmbeddingClient
from app.embeddings.clients.gemini_client import GeminiEmbeddedClient


def get_embedding_client(provider: str):
    if provider == "openai":
        return OpenAIEmbeddingClient()
    if provider == "gemini":
        return GeminiEmbeddedClient()
    else:
        raise ValueError(f"Unknown embedding provider: '{provider}'")
