class TTSRequest(BaseModel):
    prompt: str = Field(..., description="Text to synthesize")
    speaker: Optional[str] = Field(default="Vivian", description="Speaker name")
    language: Optional[str] = Field(default="Auto", description="Language code or 'Auto'")
    gen_config: Optional[Dict] = Field(default_factory=dict, description="Optional generation parameters")


class TTSResponse(BaseModel):
    audio_base64: str
    provider: str