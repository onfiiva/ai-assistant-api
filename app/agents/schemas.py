from enum import Enum
from pydantic import BaseModel
from typing import Optional


class ActionType(str, Enum):
    SEARCH = "search"
    FINISH = "finish"


class AgentStep(BaseModel):
    thought: str
    action: ActionType
    action_input: Optional[str] = None
