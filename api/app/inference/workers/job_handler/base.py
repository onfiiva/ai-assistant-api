from abc import ABC, abstractmethod


class JobHandler(ABC):
    @abstractmethod
    async def can_handle(self, job: dict) -> bool:
        """Checks if it is available to handle current job via worker"""
        pass

    @abstractmethod
    async def handle(self, job: dict, repo) -> dict:
        """Handles job. Returns dict with result"""
        pass
