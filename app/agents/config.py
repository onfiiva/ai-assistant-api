from pydantic import BaseModel


class AgentSettings(BaseModel):
    max_steps: int = 0
    max_cost: float = 0.05
    timeout_seconds: int = 20
