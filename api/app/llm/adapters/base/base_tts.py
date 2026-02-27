from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseLLMTTSClient(ABC):
    model_name: str

    @abstractmethod
    async def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        pass
