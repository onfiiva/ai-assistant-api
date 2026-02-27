import json
import logging
from typing import Optional, Dict

from fastapi import Request
from app.core.timing import track_timing
from app.llm.factory import LLMClientFactory
from app.core.config import settings
from app.core.redis import redis_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TTSService:
    CACHE_TTL = 3600  # 1h

    def __init__(self):
        self.llm_factory = LLMClientFactory()

    def _get_tts_key(
        self,
        prompt: str,
        speaker: str,
        language: str,
        gen_config: Optional[Dict] = None
    ) -> str:
        """Генерация ключа для кэша Redis"""
        key = f"tts_cache:v1:prompt={prompt}:speaker={speaker}:lang={language}"
        if gen_config:
            key += f":config={str(sorted(gen_config.items()))}"
        return key

    async def generate(
        self,
        prompt: str,
        provider: str,
        speaker: str = "Vivian",
        language: str = "Auto",
        gen_config: Optional[Dict] = None,
        request: Optional[Request] = None
    ) -> Dict:
        """
        Генерация аудио через Qwen-TTS.
        Возвращает словарь с audio_base64 и provider.
        """
        key = self._get_tts_key(prompt, speaker, language, gen_config)

        provider = provider or settings.DEFAULT_TTS_PROVIDER

        try:
            client = self.llm_factory.get(provider)
        except ValueError:
            raise ValueError(f"Provider '{provider}' is not available")

        # ===== Проверка кэша =====
        if request:
            with track_timing(request, "cache_check"):
                cached = redis_client.get(key)
        else:
            cached = redis_client.get(key)

        if cached:
            logger.info(f"TTSService: Cache hit for speaker '{speaker}'")
            return json.loads(cached)

        logger.info(f"TTSService: Sending prompt to TTS '{prompt[:100]}...'")

        try:
            client = self.llm_factory.get("qwen-tts")

            # ===== Генерация аудио =====
            if request:
                with track_timing(request, "tts_call"):
                    response = await client.generate(
                        prompt=prompt,
                        speaker=speaker,
                        language=language,
                        gen_config=gen_config
                    )
            else:
                response = await client.generate(
                    prompt=prompt,
                    speaker=speaker,
                    language=language,
                    gen_config=gen_config
                )

            # ===== Кэширование =====
            if request:
                with track_timing(request, "cache_write"):
                    redis_client.setex(key, self.CACHE_TTL, json.dumps(response))
            else:
                redis_client.setex(key, self.CACHE_TTL, json.dumps(response))

            logger.info(f"TTSService: Response cached for speaker '{speaker}'")
            return response

        except Exception as e:
            logger.exception(f"TTSService failed for prompt '{prompt}': {e}")
            raise
