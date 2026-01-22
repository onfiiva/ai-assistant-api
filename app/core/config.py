from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Models API
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    
    # Allowed providers
    # ALLOWED_PROVIDERS: List[str] = ["openai", "gemini"]

    # LLM
    DEFAULT_PROVIDER: str = "gemini"
    LLM_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

    # Rate Limit
    RATE_LIMIT_USER_REQUESTS: int = 5
    RATE_LIMIT_ADMIN_REQUESTS: int = 1
    
    RATE_LIMIT_WINDOW: int = 60 # seconds

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    class Config:
        env_file = ".env"


settings = Settings()
