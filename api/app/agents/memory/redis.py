import json
from app.core.redis import redis_client
from .base import AgentMemory


class RedisAgentMemory(AgentMemory):
    PREFIX = "agent:history"

    async def load(self, agent_id: str):
        key = f"{self.PREFIX}:{agent_id}"
        data = redis_client.get(key)
        return json.loads(data) if data else []

    async def save(self, agent_id: str, history):
        key = f"{self.PREFIX}:{agent_id}"
        redis_client.set(key, json.dumps(history), ex=3600)

    async def clear(self, agent_id: str):
        key = f"{self.PREFIX}:{agent_id}"
        redis_client.delete(key)

    async def retrieve(self, agent_id: str, query: str, k: int = 3):
        """
        Returns top-k relevant "memos" for curr agent.
        Simplest variant — find substr query in history.
        """
        history = await self.load(agent_id)
        matches = [
            h.get("observation") or ""
            for h in history
            if query.lower() in (h.get("observation") or "").lower()
        ]
        return matches[:k]

    async def store_observation(self, agent_id: str, observation_text: str):
        """
        Add important info into agent's memory.
        """
        history = await self.load(agent_id)
        history.append({
            "thought": "",
            "action": "STORE",
            "observation": observation_text
        })
        await self.save(agent_id, history)
