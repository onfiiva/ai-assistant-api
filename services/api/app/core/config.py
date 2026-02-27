from pydantic_settings import BaseSettings
from app.core.vault import get_vault_secret, get_vault_list

vault_secrets = get_vault_secret("ai-assistant-api")


class Settings(BaseSettings):
    # ===== Debug =====
    DEBUG_MODE: bool = "True"

    # ===== Secrets (Vault first) =====
    OPENAI_API_KEY: str | None = vault_secrets.get("OPENAI_API_KEY")
    GEMINI_API_KEY: str | None = vault_secrets.get("GEMINI_API_KEY")
    OLLAMA_BASE_URL: str | None = vault_secrets.get("OLLAMA_BASE_URL")
    QWEN3_VL_BASE_URL: str | None = vault_secrets.get("QWEN3_VL_BASE_URL")

    # ===== App behavior =====
    DEFAULT_PROVIDER: str = "gemini"
    EMBEDDING_PROVIDER: str = "gemini"
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
    INSTRUCTION_PATTERNS: list[str] = get_vault_list(
        vault_secrets,
        "INSTRUCTION_PATTERNS",
        default=[]
    )
    EXFILTRATION_PATTERNS: list[str] = get_vault_list(
        vault_secrets,
        "EXFILTRATION_PATTERNS",
        default=[]
    )
    FORBIDDEN_LLM_OUTPUT: list[str] = get_vault_list(
        vault_secrets,
        "FORBIDDEN_LLM_OUTPUT",
        default=[]
    )
    INSTRUCTION_REGEX: list[str] = get_vault_list(
        vault_secrets,
        "INSTRUCTION_REGEX",
        default=[]
    )
    ROLE_OVERRIDE_REGEX: list[str] = get_vault_list(
        vault_secrets,
        "ROLE_OVERRIDE_REGEX",
        default=[]
    )
    META_SYSTEM_REGEX: list[str] = get_vault_list(
        vault_secrets,
        "META_SYSTEM_REGEX",
        default=[]
    )
    MAX_PROMPT_LENGTH: int | None = vault_secrets.get("MAX_PROMPT_LENGTH")
    MAX_RESPONSE_LENGTH: int | None = vault_secrets.get("MAX_RESPONSE_LENGTH")

    ROOT_USR_PASS: str | None = vault_secrets.get("ROOT_USR_PASS")

    # ===== Rate limit =====
    RATE_LIMIT_USER_REQUESTS: int = 5
    RATE_LIMIT_ADMIN_REQUESTS: int = 5
    RATE_LIMIT_WINDOW: int = 60  # seconds
    MAX_EMBED_CHUNKS: int = 50
    MAX_EMBED_TOKENS: int = 30_000
    MAX_CHUNK_TOKENS: int = 512

    # ===== JWT =====
    JWT_SECRET_KEY: str = vault_secrets.get("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # ===== Infra (env / docker) =====
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = 0

    # ===== DB (PG / Qdrant) =====
    DATABASE_URL: str = "postgresql+asyncpg://rag:rag@rag-postgres:5432/rag"
    DB_HOST: str = "localhost"
    DB_USER: str = "rag"
    DB_PASS: str = "rag"
    DB_NAME: str = "rag"
    QDRANT_URL: str = "http://db-qdrant:6333"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
