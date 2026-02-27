from typing import Optional
from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="Text to synthesize"
    )
    speaker: Optional[str] = Field(
        default="Vivian",
        description="Speaker name"
    )
    language: Optional[str] = Field(
        default="Auto",
        description="Language code or 'Auto'"
    )
    instruct: Optional[str] = Field(
        default="Say fast and shortly",
        description="Instruction for TTS"
    )


class TTSResponse(BaseModel):
    audio_base64: str
    provider: str
