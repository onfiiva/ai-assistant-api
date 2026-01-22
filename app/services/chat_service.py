import logging
from app.llm.runner import run_llm
from app.llm.config import DEFAULT_GEN_CONFIG
from app.llm.geminiAdapter import GeminiClient
from app.llm.openAIAdapter import OpenAiClient
from app.core.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ChatService:
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

    def chat(
        self,
        prompt: str,
        provider: str | None = None,
        gen_config: dict | None = None,
        instruction: str | None = None,
        timeout: float | None = None
    ):
        provider = provider or settings.DEFAULT_PROVIDER

        if provider not in self.clients:
            raise ValueError(f"Provider '{provider}' is not available")

        client = self.clients[provider]

        # request log
        logger.info(f"ChatService sending prompt to '{provider}': '{prompt[:100]}...'")
        logger.debug(f"Generation config: {gen_config or DEFAULT_GEN_CONFIG}")
        logger.debug(f"Instruction: {instruction}")

        try:
            response = run_llm(
                prompt=prompt,
                gen_config=gen_config or DEFAULT_GEN_CONFIG,
                client=client,
                instruction=instruction,
                max_retries=settings.MAX_RETRIES,
                timeout=timeout
            )
            logger.info(f"ChatService received response from '{provider}'")
            return response
        except Exception as e:
            logger.exception(f"ChatService failed for prompt: {prompt}, exception: {e}")
            raise
