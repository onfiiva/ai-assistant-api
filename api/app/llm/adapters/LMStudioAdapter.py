from typing import Dict, Any, List, Optional
from .base.base_generation import BaseLLMGenerationClient
from .base.base_embedding import BaseLLMEmbeddingClient
from .base.base_tts import BaseLLMTTSClient
from .base.http_client import BaseHTTPClient

import base64


class LMStudioGenerationClient(BaseLLMGenerationClient, BaseHTTPClient):

    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None):
        BaseHTTPClient.__init__(self, base_url, api_key)
        self.model_name = model

    def _sanitize_config(self, gen_config: Dict[str, Any]) -> Dict[str, Any]:
        allowed = {}
        for key in [
            "temperature",
            "top_p",
            "max_tokens",
            "frequency_penalty",
            "presence_penalty"
        ]:
            if key in gen_config and gen_config[key] is not None:
                allowed[key] = gen_config[key]
        return allowed

    async def generate(
        self,
        prompt: str,
        gen_config: Dict[str, Any],
        instruction: Optional[List[str]] = None,
    ) -> Dict[str, Any]:

        messages = []

        if instruction:
            messages.append({"role": "system", "content": instruction})

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            **self._sanitize_config(gen_config)
        }

        response = await self._post(
            "/v1/chat/completions",
            payload,
            timeout=240.0
        )

        data = response.json()
        choice = data["choices"][0]

        return {
            "text": choice["message"]["content"],
            "finish_reason": choice.get("finish_reason", "stop"),
            "usage": data.get("usage"),
            "provider": "lmstudio"
        }


class LMStudioEmbeddingClient(BaseLLMEmbeddingClient, BaseHTTPClient):

    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None):
        BaseHTTPClient.__init__(self, base_url, api_key)
        self.model_name = model

    async def embed(self, texts: List[str]) -> Dict[str, Any]:

        payload = {
            "model": self.model_name,
            "input": texts
        }

        response = await self._post(
            "/v1/embeddings",
            payload,
            timeout=60.0
        )

        data = response.json()

        return {
            "embeddings": [d["embedding"] for d in data["data"]],
            "provider": "lmstudio",
            "usage": data.get("usage")
        }


class LMStudioTTSClient(BaseLLMTTSClient, BaseHTTPClient):

    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: Optional[str] = None,
        endpoint_type: str = "openai",
    ):
        BaseHTTPClient.__init__(self, base_url, api_key)
        self.model_name = model
        self.endpoint_type = endpoint_type

    def _sanitize_config(self, config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not config:
            return {}

        allowed = {}
        for key in ["speed", "pitch", "volume", "format"]:
            if key in config and config[key] is not None:
                allowed[key] = config[key]

        return allowed

    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        sanitized = self._sanitize_config(config)

        if self.endpoint_type == "openai":
            payload = {
                "model": self.model_name,
                "input": text,
                "voice": voice or "default",
                **sanitized
            }
            endpoint = "/v1/audio/speech"
        else:
            payload = {
                "text": text,
                "voice": voice or "default",
                **sanitized
            }
            endpoint = "/tts"

        response = await self._post(
            endpoint,
            payload,
            timeout=180.0
        )

        content_type = response.headers.get("content-type", "")

        if "application/json" in content_type:
            data = response.json()
            audio_base64 = data.get("audio_base64")
            usage = data.get("usage")
        else:
            audio_base64 = base64.b64encode(response.content).decode()
            usage = None

        return {
            "audio_base64": audio_base64,
            "provider": "lmstudio-tts",
            "usage": usage
        }
