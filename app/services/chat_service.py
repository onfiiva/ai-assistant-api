import json
import logging

from fastapi import Request
from app.core.timing import track_timing
from app.llm.runner import run_llm
from app.llm.config import DEFAULT_GEN_CONFIG
from app.llm.adapters.geminiAdapter import GeminiClient
from app.llm.adapters.openAIAdapter import OpenAiClient
from app.core.config import settings
from app.core.redis import redis_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ChatService:
    CACHE_TTL = 3600  # 1h

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

    def _get_chat_key(
        self,
        prompt: str,
        provider: str,
        gen_config: dict | None = None,
        instruction: str | None = None
    ) -> str:
        """Generating key for Redis Cache"""
        key = f"llm_cache:v1:{provider}:prompt={prompt}"
        if gen_config:
            key += f":config={str(sorted(gen_config.items()))}"
        if instruction:
            key += f":instruction={instruction}"
        return key

    def chat(
        self,
        prompt: str,
        provider: str | None = None,
        gen_config: dict | None = None,
        instruction: str | None = None,
        timeout: float | None = None,
        request: Request | dict | None = None
    ):
        provider = provider or settings.DEFAULT_PROVIDER

        if provider not in self.clients:
            raise ValueError(f"Provider '{provider}' is not available")

        client = self.clients[provider]

        key = self._get_chat_key(prompt, provider, gen_config, instruction)

        # ===== Cache check =====
        if request:
            with track_timing(request, "cache_check"):
                cached = redis_client.get(key)
        else:
            cached = redis_client.get(key)

        if cached:
            logger.info(f"ChatService: Cache hit for provider '{provider}'")
            return json.loads(cached)

        logger.info(f"ChatService sending prompt to '{provider}': '{prompt[:100]}...'")

        try:
            # ===== LLM call =====
            if request:
                with track_timing(request, "llm_call"):
                    response = run_llm(
                        prompt=prompt,
                        gen_config=gen_config or DEFAULT_GEN_CONFIG,
                        client=client,
                        instruction=instruction,
                        max_retries=settings.MAX_RETRIES,
                        timeout=timeout
                    )
            else:
                response = run_llm(
                    prompt=prompt,
                    gen_config=gen_config or DEFAULT_GEN_CONFIG,
                    client=client,
                    instruction=instruction,
                    max_retries=settings.MAX_RETRIES,
                    timeout=timeout
                )

            # ===== REAL TOKEN ACCOUNTING (source of truth) =====
            if request and hasattr(response, "meta"):
                usage = response.meta.get("raw", {}).get("usage")
                if usage:
                    request.state.tokens["prompt_tokens"] = usage.get(
                        "prompt_tokens", 0
                    )
                    request.state.tokens["completion_tokens"] = usage.get(
                        "completion_tokens", 0
                    )
                    request.state.tokens["total_tokens"] = usage.get(
                        "total_tokens", 0
                    )

            # ===== Cache write =====
            response_dict = response.dict()
            if request:
                with track_timing(request, "cache_write"):
                    redis_client.setex(key, self.CACHE_TTL, json.dumps(response_dict))
            else:
                redis_client.setex(key, self.CACHE_TTL, json.dumps(response_dict))

            logger.info(f"ChatService received response from '{provider}' and cached it")
            return response

        except Exception as e:
            logger.exception(f"ChatService failed for prompt: {prompt}, exception: {e}")
            raise
