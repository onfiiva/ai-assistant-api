import httpx
from typing import Dict, Any, List
from .base.base_generation import BaseLLMGenerationClient


class OllamaClient(BaseLLMGenerationClient):
    def __init__(
        self,
        base_url: str,
        model: str
    ):
        self.base_url = base_url.rstrip("/")
        self.model_name = model

    async def generate(
        self,
        prompt,
        gen_config: Dict[str, Any],
        instruction: List[str] | None = None
    ) -> Dict[str, Any]:

        messages = []

        if instruction:
            messages.append({
                "role": "system",
                "content": "\n".join(instruction)
            })

        # user prompt
        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": gen_config["temperature"],
                "top_p": gen_config["top_p"],
                "num_predict": gen_config["max_tokens"],
            }
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )

        response.raise_for_status()
        data = response.json()

        return {
            "text": data["message"]["content"],
            "finish_reason": data.get("done_reason"),
            "usage": {
                # Ollama may not return tokens - may be None
                "prompt_tokens": data.get("prompt_eval_count"),
                "completion_tokens": data.get("eval_count"),
                "total_tokens": (
                    (data.get("prompt_eval_count") or 0) +
                    (data.get("eval_count") or 0)
                )
            },
            "provider": "ollama"
        }
