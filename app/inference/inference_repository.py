import json
from typing import Optional
from uuid import UUID

class InferenceJobRepository:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def enqueue_job(self, job_id: UUID, payload: dict):
        job = {
            "job_id": str(job_id),
            "prompt": payload.get("prompt"),
            "model": payload.get("model"),
            "temperature": payload.get("temperature", 0.7),
            "user_id": payload.get("user_id"),
            "callback_url": payload.get("callback_url"),
            "status": "queued",
            "result": None,
            "error": None
        }
        await self.redis.set(f"inference:job:{job_id}", json.dumps(job))
        await self.redis.lpush("inference:queue", json.dumps(job))

    async def get_job(self, job_id: UUID) -> Optional[dict]:
        data = await self.redis.get(f"inference:job:{job_id}")
        if not data:
            return None
        return json.loads(data)

    async def update_status(
        self, job_id: UUID, status: str, result: str = None, error: str = None
    ):
        key = f"inference:job:{job_id}"
        job = await self.get_job(job_id)
        if not job:
            return
        job["status"] = status
        if result is not None:
            job["result"] = result
        if error is not None:
            job["error"] = error
        await self.redis.set(key, json.dumps(job))
        return job  # return job for callback
