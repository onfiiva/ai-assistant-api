from app.core.config import settings
from app.llm.adapters.geminiAdapter import GeminiClient
from app.llm.adapters.openAIAdapter import OpenAiClient
from app.llm.adapters.ollamaAdapter import OllamaClient
from app.llm.adapters.qwen3vlAdapter import Qwen3VLClient


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
        if settings.OLLAMA_BASE_URL:
            self.clients["ollama"] = OllamaClient(
                base_url=settings.OLLAMA_BASE_URL,
                model="mistral"
            )
        if settings.QWEN3_VL_BASE_URL:
            self.clients["qwen3vl"] = Qwen3VLClient(
                base_url=settings.QWEN3_VL_BASE_URL,
                model="qwen3-vl-4b-instruct"
            )

    def get(self, provider: str):
        client = self.clients.get(provider)
        if not client:
            raise ValueError(f"No LLM client found for provider '{provider}'")
        return client
