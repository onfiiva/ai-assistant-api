from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.auth import auth_dependency
from app.dependencies.rate_limit import rate_limit_dependency
from pydantic import BaseModel, validator, Field
from app.services.chat_service import ChatService
from app.llm.schemas import LLMResponse
from app.models.user import UserContext

router = APIRouter()
service = ChatService()


class ChatRequest(BaseModel):
    prompt: str
    provider: str | None = None
    generation_config: dict | None = None
    instruction: str | None = None
    timeout: float | None = None


@router.post("/chat", response_model=LLMResponse)
def chat(
    req: ChatRequest,
    _: None = Depends(rate_limit_dependency)
):
    try:
        return service.chat(
            prompt=req.prompt,
            provider=req.provider,
            gen_config=req.generation_config,
            instruction=req.instruction,
            timeout=req.timeout
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except RuntimeError:
        raise HTTPException(status_code=503, detail="LLM unavailable")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal error")
