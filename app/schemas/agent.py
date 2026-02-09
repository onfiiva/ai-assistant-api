from pydantic import BaseModel
from typing import List, Optional
from app.agents.schemas import AgentStep


class AgentRunRequest(BaseModel):
    goal: str
    max_steps: Optional[int] = 2


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
