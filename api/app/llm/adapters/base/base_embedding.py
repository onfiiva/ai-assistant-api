from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseLLMEmbeddingClient(ABC):
    model_name: str

    @abstractmethod
    async def embed(
        self,
        texts: List[str]
    ) -> Dict[str, Any]:
        pass
