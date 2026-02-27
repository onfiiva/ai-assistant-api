import json
from uuid import UUID

from app.inference.workers.job_handler.base import JobHandler
from app.services.orchestration.orchestrator import SmartOrchestrator


class SmartOrchestratorHandler(JobHandler):
    def __init__(self):
        self.orchestrator = SmartOrchestrator()

    async def can_handle(self, job: dict) -> bool:
        """Any job with job_type 'smart_orchestrator'"""
        return job.get("job_type") == "smart_orchestrator"

    async def handle(self, job: dict, repo):
        job_id = UUID(job["job_id"])
        await repo.update_status(job_id, "running")

        payload = json.loads(job["prompt"])
        query = payload["query"]
        provider = payload.get("provider")
        gen_config = payload.get("generation_config")
        agent_id = payload.get("agent_id", f"smart-{job_id}")

        try:
            result = await self.orchestrator.run(
                query=query,
                provider=provider,
                gen_config=gen_config,
                agent_id=agent_id
            )

            # If result is pydantic model
            if hasattr(result, "dict"):
                result = result.dict()

            await repo.update_status(job_id, "finished", result=result)
            return {"status": "finished", "result": result}
        except Exception as e:
            await repo.update_status(job_id, "failed", error=str(e))
            return {"status": "failed", "error": str(e)}
