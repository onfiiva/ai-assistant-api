from typing import Dict, Any
from google import genai
from .client import BaseLLMClient
from google.genai.types import GenerateContentConfig


class GeminiClient(BaseLLMClient):
    def __init__(
        self,
        api_key: str,
        model: str
    ):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model

    def generate(
        self,
        prompt: str,
        gen_config: Dict[str, any],
        instruction: str
    ) -> Dict[str, Any]:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            config=GenerateContentConfig(
                system_instruction=instruction,
                temperature=gen_config["temperature"],
                max_output_tokens=gen_config["max_tokens"],
                top_p=gen_config["top_p"]
            )
        )

        # getting response text & finish reason
        candidate_text = None
        finish_reason = None
        if response.candidates:
            first_candidate = response.candidates[0]
            finish_reason = getattr(first_candidate.content, "content_type", None)
            if first_candidate.content.parts:
                candidate_text = first_candidate.content.parts[0].text

        # collecting metadata
        usage = response.usage_metadata

        return {
            "text": candidate_text,
            "finish_reason": finish_reason,
            "usage": {
                "prompt_tokens": usage.prompt_token_count,
                "completion_tokens": usage.candidates_token_count,
                "total_tokens": usage.total_token_count
            },
            "provider": "gemini"
        }
