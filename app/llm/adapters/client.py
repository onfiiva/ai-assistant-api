from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseLLMClient(ABC):
    model_name: str

    @abstractmethod
    def generate(self, prompt: str, gen_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        returns RAW model response
        (text + usage + meta)
        """
        pass
