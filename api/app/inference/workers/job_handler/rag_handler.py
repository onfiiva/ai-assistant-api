import json
from uuid import UUID
from app.inference.workers.job_handler.base import JobHandler
from app.services.rag_service import RAGService
from app.llm.factory import LLMClientFactory
from app.llm.config import DEFAULT_GEN_CONFIG


class RAGHandler(JobHandler):

    async def can_handle(self, job: dict) -> bool:
        return job.get("job_type") == "RAG"

    async def handle(self, job: dict, repo):
        job_id = UUID(job["job_id"])
        await repo.update_status(job_id, "running")

        try:
            payload = json.loads(job["prompt"])

            rag = RAGService(
                embedding_provider=payload["embedding_provider"],
                top_k=payload["top_k"]
            )

            llm_factory = LLMClientFactory()
            llm_client = llm_factory.get(payload["llm_provider"])

            result = await rag.answer(
                question=payload["question"],
                llm_client=llm_client,
                gen_config=payload.get("generation_config", DEFAULT_GEN_CONFIG)
            )

            await repo.update_status(job_id, "finished", result=result)
            return {"status": "finished", "result": result}

        except Exception as e:
            await repo.update_status(job_id, "failed", error=str(e))
            return {"status": "failed", "error": str(e)}
