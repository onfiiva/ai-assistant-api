from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# DTO for req
class InferenceRequest(BaseModel):
    prompt: str
    model: str = "gemini"
    temperature: float = 0.7
    callback_url: Optional[str] = None


# DTO for res
class InferenceResponse(BaseModel):
    job_id: UUID


class InferenceResult(BaseModel):
    text: str
    finish_reason: Optional[str]
    usage: dict
    provider: str


# DTO for status res
class InferenceStatusResponse(BaseModel):
    job_id: UUID
    status: str
    result: Optional[InferenceResult]
    error: str | None = None
