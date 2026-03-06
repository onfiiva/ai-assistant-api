import json
from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4

from app.dependencies.auth import auth_dependency
from app.llm.config import DEFAULT_GEN_CONFIG
from app.models.user import UserContext
from app.schemas.inference import InferenceResponse
from app.inference.inference_service import InferenceService
from app.dependencies.inference import get_inference_service
from app.llm.sanitizer import sanitize_user_prompt
from app.llm.filter import refusal_response

router = APIRouter(
    prefix="/chat/smart",
    tags=["Smart Orchestration"],
    dependencies=[Depends(auth_dependency)]
)


@router.post("/run", response_model=InferenceResponse)
async def run_smart_orchestrator(
    query: str,
    provider: str | None = None,
    generation_config: dict | None = None,
    agent_id: str | None = None,
    user: UserContext = Depends(auth_dependency),
    service: InferenceService = Depends(get_inference_service),
):
    """
    Create a Smart Orchestrator job and send it to the async worker
    Returns job_id immediately
    """
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        safe_query = sanitize_user_prompt(query)
    except ValueError as e:
        return refusal_response(str(e))

    payload = {
        "query": safe_query,
        "provider": provider or "gemini",
        "generation_config": generation_config or DEFAULT_GEN_CONFIG,
        "agent_id": agent_id or f"smart-{uuid4()}"
    }

    job_id = await service.create_job(
        prompt=json.dumps(payload),
        model=payload["provider"],
        temperature=payload["generation_config"].get("temperature", 0.7),
        user_id=user.id,
        job_type="smart_orchestrator",
    )

    # repo = InferenceJobRepository(redis_async_client)
    # await repo.update_status(job_id, status="queued", result=None, error=None)
    # await redis_async_client.set(f"inference:job:{job_id}", json.dumps(payload))
    # await redis_async_client.lpush("inference:queue", json.dumps(payload))

    return InferenceResponse(job_id=job_id)
