import httpx
from typing import Optional, Dict
from .client import BaseLLMClient


class QwenTTSClient(BaseLLMClient):
    """
    Адаптер для обращения к Qwen-TTS inference контейнеру через HTTP API
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.model_name = "qwen-tts"

    def _sanitize_gen_config(self, gen_config: Optional[Dict] = None) -> Dict:
        """
        Позволяет расширять конфиг TTS (например, pitch, speed, volume)
        """
        return gen_config or {}

    async def generate(
        self,
        prompt: str,
        speaker: str = "Vivian",
        language: str = "Auto",
        gen_config: Optional[Dict] = None
    ) -> Dict:
        """
        Генерация аудио для текста через внешний TTS API.
        Возвращает словарь с audio_base64 и провайдером.
        """
        payload = {
            "text": prompt,
            "speaker": speaker,
            "language": language,
        }
        payload.update(self._sanitize_gen_config(gen_config))

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.base_url}/tts", json=payload)
            if resp.status_code >= 400:
                raise RuntimeError(f"TTS error {resp.status_code}: {resp.text}")
            data = resp.json()

        # Контракт: всегда возвращаем audio_base64 и provider
        return {
            "audio_base64": data.get("audio_base64", ""),
            "provider": "qwen-tts",
            "usage": {
                "prompt_tokens": None,
                "completion_tokens": None,
                "total_tokens": None
            }
        }
