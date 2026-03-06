from app.schemas.chat import ChatRequest
from app.validators.generation import validate_generation_config
from app.validators.provider import validate_provider
from app.validators.timeout import validate_timeout


def chat_params_dependency(req: ChatRequest):
    provider = validate_provider(req.provider)
    generation_config = validate_generation_config(
        req.generation_config.model_dump() if req.generation_config else None
    )
    timeout = validate_timeout(req.timeout)
    return {
        "provider": provider,
        "generation_config": generation_config,
        "timeout": timeout,
        "instruction": req.instruction
    }
