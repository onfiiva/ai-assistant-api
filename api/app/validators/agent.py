from app.core.config import settings
from app.validators.provider import validate_provider


def validate_agent_type(agent_type: str) -> str:
    if agent_type not in ("react",):
        raise ValueError(f"Unsupported agent_type: {agent_type}")
    return agent_type


def resolve_agent_provider(provider: str | None) -> str:
    if provider:
        return validate_provider(provider)
    return settings.DEFAULT_PROVIDER
