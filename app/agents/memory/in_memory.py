from .base import AgentMemory


class InMemoryAgentMemory(AgentMemory):
    def __init__(self):
        self.store = {}

    def load(self, agent_id: str):
        return self.store.get(agent_id, [])

    def save(self, agent_id: str, history):
        self.store[agent_id] = history

    def clear(self, agent_id: str):
        self.store.pop(agent_id, None)
