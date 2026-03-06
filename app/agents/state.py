from dataclasses import dataclass, field
from typing import List, Optional

from app.agents.schemas import AgentStep


@dataclass
class AgentState:
    agent_id: str
    goal: str
    history: List[dict] = field(default_factory=list)
    memory_chunks: List[str] = field(default_factory=list)
    step: int = 0
    finished: bool = False
    final_answer: Optional[str] = None
    last_actions: List[str] = field(default_factory=list)
    next_action: Optional[AgentStep] = None
    total_cost: float = 0.0
