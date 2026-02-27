from uuid import uuid4, UUID

from app.inference.inference_repository import InferenceJobRepository


class InferenceService:
    def __init__(
        self,
        repo: InferenceJobRepository
    ):
        self.repo = repo

    async def create_job(
        self,
        prompt: str,
        model: str,
        temperature: float,
        job_type: str,
        user_id: int | None = None,
        callback_url: str | None = None
    ) -> UUID:
        job_id = uuid4()

        payload = {
            "prompt": prompt,
            "model": model,
            "temperature": temperature,
            "user_id": user_id,
            "callback_url": callback_url,
            "job_type": job_type
        }

        await self.repo.enqueue_job(job_id=job_id, payload=payload)

        return job_id

    async def get_job_status(
        self,
        job_id: UUID
    ) -> dict | None:
        return await self.repo.get_job(job_id)
