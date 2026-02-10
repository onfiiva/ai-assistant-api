from enum import Enum
from pydantic import BaseModel
from typing import Optional


class ActionType(str, Enum):
    SEARCH = "search"
    FINISH = "finish"
    VECTOR_SEARCH = "vector_search"
    SUMMARY = "summary"
    EXTERNAL_API = "external_api"
    


class AgentStep(BaseModel):
    thought: str
    action: ActionType
    action_input: Optional[str] = None
