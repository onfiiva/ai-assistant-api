import json
from app.core.redis import redis_client
from .base import AgentMemory


class RedisAgentMemory(AgentMemory):
    PREFIX = "agent:history"

    def load(self, agent_id: str):
        key = f"{self.PREFIX}:{agent_id}"
        data = redis_client.get(key)
        return json.loads(data) if data else []

    def save(self, agent_id: str, history):
        key = f"{self.PREFIX}:{agent_id}"
        redis_client.set(key, json.dumps(history), ex=3600)

    def clear(self, agent_id: str):
        key = f"{self.PREFIX}:{agent_id}"
        redis_client.delete(key)
