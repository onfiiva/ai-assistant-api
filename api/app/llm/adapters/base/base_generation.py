from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseLLMGenerationClient(ABC):
    model_name: str

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        gen_config: Dict[str, Any],
        instruction: List[str] | None = None
    ) -> Dict[str, Any]:
        """
        returns RAW model response
        (text + usage + meta)
        """
        pass
