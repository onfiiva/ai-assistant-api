from app.core.config import settings
from app.llm.adapters.geminiAdapter import GeminiClient
from app.llm.adapters.openAIAdapter import OpenAiClient


class LLMClientFactory:
    def __init__(self):
        self.clients = {}
        if settings.GEMINI_API_KEY:
            self.clients["gemini"] = GeminiClient(
                api_key=settings.GEMINI_API_KEY,
                model="gemini-3-flash-preview"
            )
        if settings.OPENAI_API_KEY:
            self.clients["openai"] = OpenAiClient(
                api_key=settings.OPENAI_API_KEY,
                model="gpt-4o-mini"
            )

    def get(self, provider: str):
        client = self.clients.get(provider)
        if not client:
            raise ValueError(f"No LLM client found for provider '{provider}'")
        return client
