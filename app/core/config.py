from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str | None = None
    gemini_api_key: str | None = None

    default_provider: str = "gemini"
    llm_timeout: int = 30
    max_retries: int = 3

    class Config:
        env_file = ".env"


settings = Settings()
