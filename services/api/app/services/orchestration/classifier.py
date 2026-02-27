from app.llm.factory import LLMClientFactory
from app.llm.runner import run_llm_async
from app.llm.config import DEFAULT_GEN_CONFIG
from app.services.prompts.classifier_prompt import CLASSIFIER_PROMPT


class QueryClassifier:
    def __init__(
        self,
        provider: str,
        generation_config: str,
    ):
        self.llm_client = LLMClientFactory().get(provider)
        self.gen_config = generation_config or DEFAULT_GEN_CONFIG

    async def classify(self, query: str) -> str:
        response = await run_llm_async(
            query,
            self.gen_config,
            self.llm_client,
            CLASSIFIER_PROMPT
        )

        if response.result.text not in ("SIMPLE", "COMPLEX"):
            # fail-safe - complex default
            return "COMPLEX"

        return response.result.text
