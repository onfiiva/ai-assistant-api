import traceback
from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.rate_limit import rate_limit_dependency
from app.dependencies.validation import chat_params_dependency
from app.services.chat_service import ChatService
from app.services.rag_service import RAGService
from app.llm.factory import get_llm_client
from app.llm.filter import filter_system_commands
from app.llm.schemas import LLMResponse
from app.schemas.chat import ChatRequest, ChatRAGRequest, ChatRAGResponse
from app.llm.config import DEFAULT_GEN_CONFIG
from app.dependencies.auth import auth_dependency

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(auth_dependency)]
)
service = ChatService()


@router.post("/", response_model=LLMResponse)
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


@router.post("/chat/rag", response_model=ChatRAGResponse)
async def chat_rag(req: ChatRAGRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot mbe empty")

    # 1. Init RAG service
    rag = RAGService(
        embedding_provider=req.provider,
        top_k=req.top_k
    )

    # 2. Get LLM client
    llm_client = get_llm_client(req.llm_provider)

    # Generate answer threw RAG
    response = await rag.answer(
        question=req.question,
        llm_client=llm_client,
        gen_config=DEFAULT_GEN_CONFIG
    )

    return response
