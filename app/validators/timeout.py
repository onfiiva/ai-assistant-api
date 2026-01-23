from app.core.config import settings


def validate_timeout(timeout: int | None) -> int:
    return timeout or settings.LLM_TIMEOUT
