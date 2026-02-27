from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AgentMemory(ABC):
    @abstractmethod
    async def load(self, agent_id: str) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    async def save(self, agent_id: str, history: List[Dict[str, Any]]) -> None:
        ...

    @abstractmethod
    async def clear(self, agent_id: str) -> None:
        ...

    @abstractmethod
    async def store_observation(self, agent_id: str, text: str) -> None:
        pass

    @abstractmethod
    async def retrieve(self, agent_id: str, query: str, k: int = 3) -> List[str]:
        pass
