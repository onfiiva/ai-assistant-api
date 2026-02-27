from app.inference.inference_service import InferenceService
from app.inference.inference_repository import InferenceJobRepository
from app.core.redis import redis_async_client


def get_inference_service() -> InferenceService:
    repo = InferenceJobRepository(redis_async_client)
    return InferenceService(repo)
