from app.llm.adapters.openAIAdapter import OpenAiClient
from app.llm.adapters.geminiAdapter import GeminiClient


def get_llm_client(provider: str):
    if provider == "openai":
        return OpenAiClient
    elif provider == "gemini":
        return GeminiClient
    else:
        raise ValueError(f"Unknown LLM provider: '{provider}'")
