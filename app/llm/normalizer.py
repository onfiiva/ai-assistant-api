from .schemas import LLMResponse, Usage, LLMResult, GenerationConfig
from app.core.logging import logger


# normalize to different API's (OpenAI, Claude, Gemini etc.)
def normalize_llm_response(
    *,
    model: str,
    prompt: str,
    gen_config: dict,
    raw_response: dict
) -> LLMResponse:

    usage = raw_response.get("usage")
    logger.info(f"Response to normalize: {raw_response}")
    logger.info(f"Type of response to normalize: {type(raw_response)}")

    return LLMResponse(
        model=model,
        prompt=prompt,
        generation_config=GenerationConfig(**gen_config),
        usage=Usage(**usage) if usage else None,
        result=LLMResult(
            text=raw_response["text"],
            finish_reason=raw_response.get("finish_reason"),
        ),
        meta={
            "provider": raw_response.get("provider"),
            "raw": raw_response,    # <- TODO: should've been removed in PROD
        },
    )
