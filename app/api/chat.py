import traceback
from fastapi import APIRouter, HTTPException, Depends, Request
from app.dependencies.rate_limit import rate_limit_dependency
from app.dependencies.security import security_dependency
from app.dependencies.validation import chat_params_dependency
from app.llm.sanitizer import sanitize_user_prompt
from app.models.user import UserContext
from app.services.chat_service import ChatService
from app.services.rag_service import RAGService
from app.llm.factory import LLMClientFactory
from app.llm.filter import refusal_response, validate_llm_output
from app.schemas.chat import ChatRequest, ChatRAGRequest, ChatResponse
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
    response_model=ChatResponse,
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

        try:
            safe_prompt = sanitize_user_prompt(req.prompt)
            safe_instruction = sanitize_user_prompt(params["instruction"])
        except ValueError as e:
            return refusal_response(str(e))

        # ===== Call Chat Service =====
        llm_output = service.chat(
            prompt=safe_prompt,
            provider=params["provider"],
            gen_config=params["generation_config"],
            instruction=safe_instruction,
            timeout=params["timeout"],
            request=request
        )

        if not validate_llm_output(llm_output):
            return {
                "status": "fallback",
                "answer": """
                I might be mistaken.
                Please rephrase your question or narrow the scope.
                """,
                "confidence": "low"
            }

        return llm_output

    except HTTPException:
        raise

    except Exception:
        print("=== Chat endpoint error ===")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/rag",
    response_model=ChatResponse
)
async def chat_rag(
    request: Request,
    req: ChatRAGRequest,
    user: UserContext = Depends(auth_dependency)
):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        safe_question = sanitize_user_prompt(req.question)
    except ValueError as e:
        return refusal_response(str(e))

    # 1. Init RAG service
    rag = RAGService(
        embedding_provider=req.provider,
        top_k=req.top_k
    )

    # 2. Get LLM client
    llm_factory = LLMClientFactory()
    llm_client = llm_factory.get(req.llm_provider)

    # Generate answer threw RAG
    llm_output = await rag.answer(
        question=safe_question,
        llm_client=llm_client,
        gen_config=DEFAULT_GEN_CONFIG,
        request=request
    )

    if not validate_llm_output(llm_output):
        return {
            "status": "fallback",
            "answer": """
            I might be mistaken.
            Please rephrase your question or narrow the scope.
            """,
            "confidence": "low"
        }

    return llm_output
