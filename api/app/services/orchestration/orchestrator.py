from app.agents.memory.redis import RedisAgentMemory
from app.agents.react.agent import ReActAgent
from app.services.chat_service import ChatService
from app.services.orchestration.classifier import QueryClassifier
from app.core.logging import logger


class SmartOrchestrator:
    def __init__(
        self
    ):
        pass

    async def run(
        self,
        query: str,
        provider: str,
        gen_config: dict | None = None,
        agent_id: str | None = None
    ):
        classifier = QueryClassifier(
            provider=provider,
            generation_config=gen_config
        )

        complexity = await classifier.classify(query)

        logger.info(f"Request complexity is: {complexity}")

        if complexity == "SIMPLE":
            logger.info("Calling single-shot service...")
            chat_service = ChatService()

            return await chat_service.chat(
                prompt=query,
                provider=provider,
                gen_config=gen_config
            )

        memory = RedisAgentMemory()

        agent = ReActAgent(
            memory=memory,
            provider=provider,
            generation_config=gen_config
        )

        logger.info("Calling agent service...")
        return await agent.run(
            agent_id=agent_id or "default",
            goal=query
        )
