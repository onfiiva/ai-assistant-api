from .schemas import LLMResponse, Usage, LLMResult, GenerationConfig

# normalize to different API's (OpenAI, Claude, Gemini etc.)

def normalize_llm_response(
    *,
    model: str,
    prompt: str,
    gen_config: dict,
    raw_response: dict
) -> LLMResponse:
    
    usage = raw_response.get("usage")
    
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
            "raw": raw_response, # <- should've been removed in PROD
        },
    )
    