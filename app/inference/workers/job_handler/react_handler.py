import json
from uuid import UUID
from app.agents.react.agent import ReActAgent
from app.inference.workers.job_handler.base import JobHandler


class ReActHandler(JobHandler):
    def __init__(self, memory, llm_factory):
        self.memory = memory
        self.llm_factory = llm_factory

    async def can_handle(self, job: dict) -> bool:
        payload = json.loads(job["prompt"])
        return payload.get("agent_type") == "react"

    async def handle(self, job: dict, repo):
        job_id = UUID(job["job_id"])
        payload = json.loads(job["prompt"])
        agent = ReActAgent(
            memory=self.memory,
            provider=payload["provider"],
            max_steps=payload.get("max_steps", 3),
            generation_config=payload.get("generation_config"),
        )
        try:
            result = await agent.run(
                payload["agent_id"],
                payload["goal"]
            )
            await repo.update_status(job_id, "finished", result=result)
            return {"status": "finished", "result": result}
        except Exception as e:
            await repo.update_status(job_id, "failed", error=str(e))
            return {"status": "failed", "error": str(e)}
