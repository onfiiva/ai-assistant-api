from pydantic import BaseModel
from typing import Optional, Dict, Any

# United contract
# Able to validate
# Able to extend

class Usage(BaseModel):
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]

class GenerationConfig(BaseModel):
    temperature: float
    top_p: float
    max_tokens: int

class LLMResult(BaseModel):
    text: str
    finish_reason: Optional[str]

class LLMResponse(BaseModel):
    model: str
    prompt: str
    generation_config: GenerationConfig
    usage: Optional[Usage]
    result: LLMResult
    meta: Dict[str, Any] = {}