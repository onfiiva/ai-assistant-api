import httpx
from typing import Optional, Dict
import io

from app.core.logging import logger
from app.core.config import settings


class TTSService:
    CACHE_TTL = 3600  # 1 час

    def __init__(self):
        self.tts_api_url = settings.TTS_API_URL

    def _get_tts_key(
        self,
        prompt: str,
        speaker: str,
        language: str,
        gen_config: Optional[Dict] = None
    ) -> str:
        key = f"tts_cache:v1:prompt={prompt}:speaker={speaker}:lang={language}"
        if gen_config:
            key += f":config={str(sorted(gen_config.items()))}"
        return key

    async def generate(
        self,
        prompt: str,
        speaker: str = "Vivian",
        language: str = "Auto",
        instruct: str = "Say fast and shortly",
        gen_config: Optional[Dict] = None
    ) -> Dict:
        """
        Генерация аудио через локальный TTS API.
        Возвращает {audio_base64: [...], provider: "qwen-tts"}
        """

        logger.info(f"TTSService: Sending prompt to TTS API '{prompt[:100]}...'")

        payload = {
            "text": prompt,
            "speaker": speaker,
            "language": language,
            "instruct": instruct
        }

        # ===== Скачиваем WAV из StreamingResponse =====
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(f"{self.tts_api_url}/tts/custom_voice", json=payload)
            resp.raise_for_status()
            audio_bytes = await resp.aread()

        return io.BytesIO(audio_bytes)
