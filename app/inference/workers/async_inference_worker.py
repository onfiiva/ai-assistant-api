import asyncio
import json
from uuid import UUID
from datetime import datetime

import redis.asyncio as aioredis

from app.agents.memory.redis import RedisAgentMemory
from app.core.config import settings
from app.inference.workers.job_handler.llm_handler import LLMHandler
from app.inference.workers.job_handler.react_handler import ReActHandler
from app.inference.workers.job_handler.smart_orchestration_handler import \
    SmartOrchestratorHandler
from app.llm.factory import LLMClientFactory
from app.inference.inference_repository import InferenceJobRepository
from app.core.logging import logger

QUEUE_KEY = "inference:queue"
HEARTBEAT_INTERVAL = 5  # sec
ZOMBIE_TIMEOUT = 300    # sec, if running > 5 min → zombie


class AsyncInferenceWorker:
    def __init__(self):
        self.redis = aioredis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.repo = InferenceJobRepository(self.redis)
        self.llm_factory = LLMClientFactory()
        self.agent_memory = RedisAgentMemory()

        self.handlers = [
            ReActHandler(self.agent_memory, self.llm_factory),
            LLMHandler(self.llm_factory),
            SmartOrchestratorHandler()
        ]

    async def heartbeat(self, job_id: UUID):
        key = f"inference:job:{job_id}"
        while True:
            job = await self.repo.get_job(job_id)
            if not job or job["status"] not in ["running"]:
                break
            job["last_heartbeat_at"] = datetime.utcnow().isoformat()
            await self.redis.set(key, json.dumps(job))
            await asyncio.sleep(HEARTBEAT_INTERVAL)

    async def run_job(self, job: dict):
        for handler in self.handlers:
            if await handler.can_handle(job):
                logger.info(
                    f"Handling job {job['job_id']} "
                    f"with {handler.__class__.__name__}"
                )
                result = await handler.handle(job, self.repo)
                logger.info(f"Job {job['job_id']} result: {result}")
                return
            logger.warning(f"No handler found for job {job['job_id']}")
            await self.repo.update_status(
                UUID(job['job_id']),
                "failed",
                error="No handler found"
            )

    async def handle_zombies(self):
        """
        Check running jobs, if last_heartbeat > ZOMBIE_TIMEOUT → mark failed
        """
        keys = await self.redis.keys("inference:job:*")
        now = datetime.utcnow()
        for key in keys:
            data = await self.redis.get(key)
            if not data:
                continue
            job = json.loads(data)
            if job.get("status") == "running":
                last_hb = job.get("last_heartbeat_at") or job.get("started_at")
                if last_hb:
                    last_hb_dt = datetime.fromisoformat(last_hb)
                    if (now - last_hb_dt).total_seconds() > ZOMBIE_TIMEOUT:
                        await self.repo.update_status(
                            UUID(job["job_id"]),
                            "failed",
                            error="zombie job"
                        )

    async def run(self):
        while True:
            # handle zombies first
            await self.handle_zombies()

            # RPOP queue
            job_data = await self.redis.rpop(QUEUE_KEY)
            if not job_data:
                await asyncio.sleep(0.5)
                continue

            job = json.loads(job_data)
            asyncio.create_task(self.run_job(job))
