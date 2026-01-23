from pydantic_settings import BaseSettings
from app.core.vault import get_vault_secret, get_vault_list

vault_secrets = get_vault_secret("ai-assistant-api")


class Settings(BaseSettings):
    # ===== Secrets (Vault first) =====
    OPENAI_API_KEY: str | None = vault_secrets.get("OPENAI_API_KEY")
    GEMINI_API_KEY: str | None = vault_secrets.get("GEMINI_API_KEY")

    # ===== App behavior =====
    DEFAULT_PROVIDER: str = "gemini"
    LLM_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

    # ===== Providers =====
    ALLOWED_PROVIDERS: list[str] = get_vault_list(
        vault_secrets,
        "ALLOWED_PROVIDERS",
        default=["gemini"]
    )

    # ===== Forbidden commands =====
    FORBIDDEN_COMMANDS: list[str] = get_vault_list(
        vault_secrets,
        "FORBIDDEN_COMMANDS",
        default=[]
    )

    # ===== Rate limit =====
    RATE_LIMIT_USER_REQUESTS: int = 5
    RATE_LIMIT_ADMIN_REQUESTS: int = 5
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # ===== JWT =====
    JWT_SECRET_KEY: str = vault_secrets.get("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # ===== Infra (env / docker) =====
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = 0

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
