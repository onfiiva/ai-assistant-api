from pydantic import BaseModel, Field
from typing import List, Optional


class GenerationConfig(BaseModel):
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(default=None, ge=1, le=8192)


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=20_000)
    provider: Optional[str] = None
    instruction: Optional[str] = Field(default=None, max_length=5_000)
    generation_config: Optional[GenerationConfig] = None
    timeout: Optional[int] = Field(default=None, ge=1, le=120)


class ChatRAGRequest(BaseModel):
    question: str
    provider: Optional[str] = "gemini"  # embeddings
    llm_provider: Optional[str] = "gemini"  # LLM
    top_k: Optional[int] = 5


class SourceItem(BaseModel):
    index: int
    text: str
    score: float


class ChatRAGResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
