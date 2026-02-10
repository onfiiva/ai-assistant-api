from pydantic import BaseModel, Field
from typing import List, Optional
from app.agents.schemas import AgentStep


class AgentRunRequest(BaseModel):
    agent_type: str = Field(default="react")
    goal: str
    agent_id: str

    max_steps: int = Field(default=3, ge=1, le=20)

    provider: Optional[str] = None
    generation_config: Optional[dict] = None
    timeout: Optional[int] = None


class AgentRunResponse(BaseModel):
    job_id: str


class AgentStatusResponse(BaseModel):
    job_id: str
    status: str  # pending, completed, error
    history: Optional[List[AgentStep]] = None
    result: Optional[str] = None
    error: Optional[str] = None


class ToolListResponse(BaseModel):
    tools: List[str]
