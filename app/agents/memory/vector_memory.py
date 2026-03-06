import uuid
from typing import List
from app.agents.memory import AgentMemory
from app.embeddings.factory import EmbeddingFactory
from app.infra.db.qdrant import upsert_embedding, search


class VectorAgentMemory(AgentMemory):
    def __init__(
        self,
        short_term_backend
    ):
        self.short_term = short_term_backend
        self.embedder = EmbeddingFactory().get()

    def load(self, agent_id: str):
        return self.short_term.load(agent_id)

    def save(self, agent_id: str, history):
        self.short_term.save(agent_id, history)

    def store_observation(self, agent_id: str, text: str):
        embedding = self.embedder.embed(text)

        upsert_embedding(
            id=str(uuid.uuid4()),
            vector=embedding,
            content=f"[agent:{agent_id}] {text}"
        )

    def retrieve(self, agent_id: str, query: str, k: int = 3) -> List[str]:
        query_embedding = self.embedder.embed(query)

        results = search(query_embedding, limit=k)

        # Filter only curr agent
        filtered = [
            r["content"]
            for r in results
            if f"[agent:{agent_id}]" in r["content"]
        ]

        return filtered
