import traceback
from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.rate_limit import rate_limit_dependency
from app.dependencies.validation import chat_params_dependency
from app.services.chat_service import ChatService
from app.llm.filter import filter_system_commands
from app.llm.schemas import LLMResponse
from app.schemas.chat import ChatRequest

router = APIRouter()
service = ChatService()


@router.post("/chat", response_model=LLMResponse)
def chat(
    req: ChatRequest,
    params=Depends(chat_params_dependency),  # provider, generation_config, timeout
    _: None = Depends(rate_limit_dependency)
):
    try:
        # ===== Prompt validation + system command filter =====
        if not req.prompt or not req.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        safe_prompt = filter_system_commands(req.prompt) or ""

        # ===== Call Chat Service =====
        return service.chat(
            prompt=safe_prompt,
            provider=params["provider"],
            gen_config=params["generation_config"],
            instruction=params["instruction"],
            timeout=params["timeout"]
        )

    except HTTPException:
        raise

    except Exception:
        print("=== Chat endpoint error ===")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")
