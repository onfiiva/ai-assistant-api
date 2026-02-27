from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from pydantic import BaseModel
import json
from app.dependencies.auth import auth_dependency
from app.models.user import UserContext
from app.schemas.inference import InferenceResponse
from app.inference.inference_service import InferenceService
from app.dependencies.inference import get_inference_service
from app.llm.sanitizer import sanitize_user_prompt

router = APIRouter(
    prefix="/instruction/smart",
    tags=["Instruction Tuning Smart"],
    dependencies=[Depends(auth_dependency)]
)


class InstructionExample(BaseModel):
    instruction: str
    input: str
    output: str


@router.post("/add", response_model=InferenceResponse)
async def add_instruction_smart(
    example: InstructionExample,
    user: UserContext = Depends(auth_dependency),
    service: InferenceService = Depends(get_inference_service)
):
    if not (
        example.instruction.strip() and example.input.strip() and example.output.strip()
    ):
        raise HTTPException(status_code=400, detail="All fields must be non-empty")

    try:
        safe_instruction = sanitize_user_prompt(example.instruction)
        safe_input = sanitize_user_prompt(example.input)
        safe_output = sanitize_user_prompt(example.output)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    payload = {
        "type": "instruction_example",
        "instruction": safe_instruction,
        "input": safe_input,
        "output": safe_output,
        "user_id": user.id,
        "example_id": str(uuid4())
    }

    job_id = await service.create_job(
        prompt=json.dumps(payload),
        model="none",  # модель здесь не используется, просто для очереди
        temperature=0.0,
        user_id=user.id,
        job_type="instruction_tuning",
    )

    return InferenceResponse(job_id=job_id)
