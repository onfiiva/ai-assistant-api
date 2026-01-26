from abc import ABC, abstractmethod
from typing import List


class EmbeddingClient(ABC):
    @abstractmethod
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Accepts a list of str
        Returns a list of embedding vectors
        """
        pass
