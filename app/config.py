from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Aegis"
    environment: str = Field(default="development", alias="AEGIS_ENV")
    log_level: str = Field(default="INFO", alias="AEGIS_LOG_LEVEL")

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")

    search_api_key: str = Field(default="", alias="SEARCH_API_KEY")

    langsmith_api_key: str = Field(default="", alias="LANGSMITH_API_KEY")
    langsmith_tracing: bool = Field(
        default=False,
        alias="LANGSMITH_TRACING",
    )
    langsmith_project: str = Field(
        default="aegis",
        alias="LANGSMITH_PROJECT",
    )

    postgres_host: str = Field(
        default="localhost",
        alias="POSTGRES_HOST",
    )
    postgres_port: int = Field(
        default=5432,
        alias="POSTGRES_PORT",
    )
    postgres_db: str = Field(
        default="aegis",
        alias="POSTGRES_DB",
    )
    postgres_user: str = Field(
        default="aegis",
        alias="POSTGRES_USER",
    )
    postgres_password: str = Field(
        default="",
        alias="POSTGRES_PASSWORD",
    )

    redis_url: str = Field(
        default="redis://localhost:6379/0",
        alias="REDIS_URL",
    )

    llm_model: str = Field(
    default="gpt-5.6",
    alias="LLM_MODEL",
    )

    llm_timeout_seconds: float = Field(
        default=30.0,
        gt=0,
        alias="LLM_TIMEOUT_SECONDS",
    )


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()