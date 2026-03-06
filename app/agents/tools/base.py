from abc import ABC, abstractmethod
from app.agents.schemas import ActionType


class Tool(ABC):
    name: ActionType

    @abstractmethod
    def run(self, input: str) -> str:
        """Execute action"""
        ...
