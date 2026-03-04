from abc import ABC, abstractmethod


class BaseRunner(ABC):
    url: str

    @abstractmethod
    async def run(
        self,
        question: str
    ) -> str:
        pass
