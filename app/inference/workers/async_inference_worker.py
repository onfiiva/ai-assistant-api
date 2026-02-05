import asyncio
import json
import traceback
import aiohttp
from uuid import UUID
from datetime import datetime, timedelta

import redis.asyncio as aioredis

from app.core.config import settings
from app.llm.factory import LLMClientFactory
from app.inference.inference_repository import InferenceJobRepository

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
        job_id = UUID(job["job_id"])
        provider = job.get("model", settings.DEFAULT_PROVIDER)

        try:
            await self.repo.update_status(job_id, "running")
            hb_task = asyncio.create_task(self.heartbeat(job_id))

            llm_client = self.llm_factory.get(provider)

            gen_config = {
                "temperature": job.get("temperature", 0.7),
                "top_p": job.get("top_p", 1.0),
                "max_tokens": job.get("max_tokens", 512),
                "instruction": job.get("instruction"),  # optional
            }

            instruction = job.get("instruction") or ""

            result = await asyncio.wait_for(
                asyncio.to_thread(
                    llm_client.generate,
                    prompt=job["prompt"],
                    gen_config=gen_config,
                    instruction=instruction
                ),
                timeout=60
            )

            job = await self.repo.update_status(job_id, "finished", result=result)

            if callback_url := job.get("callback_url"):
                async with aiohttp.ClientSession() as session:
                    await session.post(callback_url, json=job)

        except asyncio.TimeoutError:
            ...
        finally:
            hb_task.cancel()

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
