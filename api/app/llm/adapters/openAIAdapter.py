from openai import OpenAI
from typing import Dict, Any, List
from .base.base_generation import BaseLLMGenerationClient


class OpenAiClient(BaseLLMGenerationClient):
    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model

    async def generate(
        self,
        prompt: str,
        gen_config: Dict[str, Any],
        instruction: List[str] | None = None
    ) -> Dict[str, Any]:

        messages = []

        if instruction:
            messages.append({
                "role": "system",
                "content": "\n".join(instruction)
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=gen_config["temperature"],
            top_p=gen_config["top_p"],
            max_tokens=gen_config["max_tokens"],
        )

        choice = response.choices[0]

        return {
            "text": choice.message.content,
            "finish_reason": choice.finish_reason,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "provider": "openai"
        }
