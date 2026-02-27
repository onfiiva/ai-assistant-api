import json
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.inference import get_inference_service
from app.llm.sanitizer import sanitize_user_prompt
from app.models.user import UserContext
from app.schemas.chat import ChatRAGRequest, ChatRequest, ChatResponse
from app.schemas.inference import InferenceResponse
from app.inference.inference_service import InferenceService
from app.dependencies.auth import auth_dependency
from app.dependencies.validation import chat_params_dependency
from app.llm.filter import refusal_response
from app.inference.inference_repository import InferenceJobRepository
from app.core.redis import redis_async_client

router = APIRouter(
    prefix="/chat",
    tags=["Async Chats"],
    dependencies=[Depends(auth_dependency)]
)


@router.post("/async", response_model=ChatResponse)
async def chat_async(
    req: ChatRequest,
    user: UserContext = Depends(auth_dependency),
    params=Depends(chat_params_dependency),
    service: InferenceService = Depends(get_inference_service)
):
    """
    Async LLM call: creates job, returns job_id
    """
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    prompt = req.prompt.strip() if req.prompt else ""
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        safe_prompt = sanitize_user_prompt(req.prompt)
    except ValueError as e:
        return refusal_response(str(e))

    safe_prompt = safe_prompt.strip() if safe_prompt else ""
    if not safe_prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    job_id = await service.create_job(
        prompt=safe_prompt,
        model=params["provider"],
        temperature=params["generation_config"].get("temperature", 0.7),
        user_id=user.id,
        callback_url=None,
        job_type=params["job_type"]
    )
    return InferenceResponse(job_id=job_id)


@router.post("/rag/async", response_model=ChatResponse)
async def chat_rag_async(
    req: ChatRAGRequest,
    user: UserContext = Depends(auth_dependency),
    service: InferenceService = Depends(get_inference_service)
):
    """
    Async RAG call: creates job, returns job_id
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        safe_question = sanitize_user_prompt(req.question)
    except ValueError as e:
        return refusal_response(str(e))

    payload = {
        "type": "rag",
        "question": safe_question,
        "llm_provider": req.llm_provider,
        "top_k": req.top_k,
        "user_id": user.id,
        "callback_url": None
    }

    job_id = await service.create_job(
        prompt="",
        model=req.llm_provider,
        temperature=0.7,
        user_id=user.id,
        job_type=req.job_type,
    )

    repo = InferenceJobRepository(redis_async_client)
    await repo.update_status(job_id, status="queued", result=None, error=None)
    await redis_async_client.set(f"inference:job:{job_id}", json.dumps(payload))
    await redis_async_client.lpush("inference:queue", json.dumps(payload))

    return InferenceResponse(job_id=job_id)
