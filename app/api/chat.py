import traceback
from fastapi import APIRouter, HTTPException, Depends, Request
from app.dependencies.rate_limit import rate_limit_dependency
from app.dependencies.security import security_dependency
from app.dependencies.validation import chat_params_dependency
from app.models.user import UserContext
from app.schemas.inference import InferenceResponse
from app.services.chat_service import ChatService
from app.inference.inference_service import InferenceService
from app.services.rag_service import RAGService
from app.llm.factory import LLMClientFactory
from app.llm.filter import filter_system_commands
from app.llm.schemas import LLMResponse
from app.schemas.chat import ChatRequest, ChatRAGRequest, ChatRAGResponse
from app.llm.config import DEFAULT_GEN_CONFIG
from app.dependencies.auth import auth_dependency

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[
        Depends(rate_limit_dependency),
        Depends(security_dependency)
    ]
)
service = ChatService()


@router.post(
    "/",
    response_model=LLMResponse,
)
def chat(
    req: ChatRequest,
    request: Request,
    params=Depends(chat_params_dependency),  # provider, generation_config, timeout
    user: UserContext = Depends(auth_dependency)
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
            timeout=params["timeout"],
            request=request
        )

    except HTTPException:
        raise

    except Exception:
        print("=== Chat endpoint error ===")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/rag",
    response_model=ChatRAGResponse
)
async def chat_rag(
    request: Request,
    req: ChatRAGRequest,
    user: UserContext = Depends(auth_dependency)
):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # 1. Init RAG service
    rag = RAGService(
        embedding_provider=req.provider,
        top_k=req.top_k
    )

    # 2. Get LLM client
    llm_factory = LLMClientFactory()
    llm_client = llm_factory.get(req.llm_provider)

    # Generate answer threw RAG
    response = await rag.answer(
        question=req.question,
        llm_client=llm_client,
        gen_config=DEFAULT_GEN_CONFIG,
        request=request
    )

    return response
