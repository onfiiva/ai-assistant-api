from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AgentMemory(ABC):
    @abstractmethod
    def load(self, agent_id: str) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def save(self, agent_id: str, history: List[Dict[str, Any]]) -> None:
        ...

    @abstractmethod
    def clear(self, agent_id: str) -> None:
        ...

    @abstractmethod
    def store_observation(self, agent_id: str, text: str) -> None:
        pass

    @abstractmethod
    def retrieve(self, agent_id: str, query: str, k: int = 3) -> List[str]:
        pass
