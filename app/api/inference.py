from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Path

from app.dependencies.auth import auth_dependency
from app.dependencies.inference import get_inference_service
from app.schemas.inference import \
    InferenceResponse, InferenceRequest, InferenceStatusResponse
from app.inference.inference_service import InferenceService
from app.dependencies.user import get_current_user

router = APIRouter(
    prefix="/inference",
    tags=["inference"],
    dependencies=[Depends(auth_dependency)]
)


@router.post(
    "/",
    response_model=InferenceResponse
)
async def create_inference(
    request: InferenceRequest,
    user=Depends(get_current_user),
    service: InferenceService = Depends(get_inference_service)
):
    """
    Creates async inference job
    """
    job_id = await service.create_job(
        prompt=request.prompt,
        model=request.model,
        temperature=request.temperature,
        user_id=user.id,
        callback_url=request.callback_url
    )
    return InferenceResponse(job_id=job_id)


@router.get(
    "/{job_id}",
    response_model=InferenceStatusResponse
)
async def get_inference_status(
    job_id: UUID = Path(...),
    service: InferenceService = Depends(get_inference_service)
):
    """
    Returns job's state and result/error
    """
    job = await service.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return InferenceStatusResponse(
        job_id=job_id,
        status=job["status"],
        result=job.get("result"),
        error=job.get("error")
    )
