import json
from app.core.redis import redis_async_client
from .base import AgentMemory


class AsyncRedisAgentMemory(AgentMemory):
    PREFIX = "agent:history"

    async def load(self, agent_id: str):
        data = await redis_async_client.get(f"{self.PREFIX}:{agent_id}")
        return json.loads(data) if data else []

    async def save(self, agent_id: str, history):
        await redis_async_client.set(
            f"{self.PREFIX}:{agent_id}",
            json.dumps(history),
            ex=3600
        )

    async def clear(self, agent_id: str):
        await redis_async_client.delete(f"{self.PREFIX}:{agent_id}")
