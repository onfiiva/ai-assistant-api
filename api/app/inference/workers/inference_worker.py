import asyncio
import json
import traceback
from uuid import UUID
from app.core.redis import redis_async_client
from app.llm.factory import LLMClientFactory
from app.inference.inference_repository import InferenceJobRepository
from app.core.logging import logger

QUEUE_KEY = "inference:queue"


class InferenceWorker:
    def __init__(self):
        self.redis = redis_async_client
        self.repo = InferenceJobRepository(self.redis)
        self.llm_factory = LLMClientFactory()

    async def run(self):
        logger.info("InferenceWorker started")
        while True:
            try:
                job_data = await self.redis.rpop(QUEUE_KEY)
                if not job_data:
                    await asyncio.sleep(0.5)
                    continue

                job = json.loads(job_data)
                job_id = UUID(job["job_id"])
                provider = job.get("model")
                prompt = job.get("prompt")
                temperature = job.get("temperature", 0.7)

                logger.info(
                    f"Picked up job {job_id} "
                    f"(model={provider}, prompt='{prompt[:30]}')"
                )

                await self.repo.update_status(job_id, "running")
                logger.info(f"Job {job_id} status updated to RUNNING")

                llm_client = self.llm_factory.get(provider)
                result = await llm_client.generate(
                    prompt=prompt,
                    model=provider,
                    temperature=temperature
                )

                await self.repo.update_status(job_id, "finished", result=result)
                logger.info(f"Job {job_id} finished successfully")

            except Exception as e:
                try:
                    await self.repo.update_status(job_id, "failed", error=str(e))
                except Exception as update_error:
                    logger.error(
                        "Failed to update job status for "
                        f"{job_id}: {update_error}"
                    )

                logger.error(f"Job {job_id} failed: {e}")
                logger.error(traceback.format_exc())
