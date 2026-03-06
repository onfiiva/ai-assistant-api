from fastapi import HTTPException
from app.core.config import settings


def validate_provider(provider: str | None) -> str:
    if provider is None:
        return settings.DEFAULT_PROVIDER

    provider = provider.lower()

    if provider not in settings.ALLOWED_PROVIDERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported provider: {provider}"
        )

    return provider
