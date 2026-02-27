import httpx
from typing import Dict, Any, List, Optional
from PIL import Image
import io
import base64
from .client import BaseLLMClient


class Qwen3VLClient(BaseLLMClient):
    """
    Адаптер для обращения к qwen inference контейнеру
    """

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model_name = model

    def _sanitize_gen_config(self, gen_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Преобразует общий gen_config под Qwen3VL.
        - max_tokens -> max_new_tokens
        - оставляем остальные ключи
        """
        sanitized = {}

        # Rename max_tokens to max_new_tokens
        if "max_tokens" in gen_config and gen_config["max_tokens"] is not None:
            sanitized["max_new_tokens"] = gen_config["max_tokens"]

        # Transfer other keys if got any
        for key in ["temperature", "top_p", "repetition_penalty", "do_sample"]:
            if key in gen_config and gen_config[key] is not None:
                sanitized[key] = gen_config[key]

        return sanitized

    async def generate(
        self,
        prompt: str,
        gen_config: Optional[Dict[str, Any]] = None,
        instruction: Optional[List[str]] = None,
        image: Optional[Image.Image] = None
    ) -> Dict[str, Any]:

        # instruction always a list
        if isinstance(instruction, str):
            instruction = [instruction]
        elif instruction is None:
            instruction = []

        # payload prepare
        payload = {
            "prompt": prompt,
            "instruction": instruction,
            "gen_config": self._sanitize_gen_config(gen_config or {}),
            "image": None
        }

        # Encode image if provided
        if image:
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            payload["image"] = base64.b64encode(buf.getvalue()).decode()

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{self.base_url}/generate",
                json=payload
            )

            if response.status_code >= 400:
                raise RuntimeError(
                    f"LLM error {response.status_code}: {response.text}"
                )

            data = response.json()

        return {
            "text": data.get("text"),
            "finish_reason": data.get("finish_reason", "stop"),
            "usage": data.get("usage", {
                "prompt_tokens": None,
                "completion_tokens": None,
                "total_tokens": None
            }),
            "provider": "qwen3vl"
        }
