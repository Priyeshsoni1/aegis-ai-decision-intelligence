
import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Aegis AI Decision Intelligence"
    app_env: Literal["development", "testing", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    max_upload_size_bytes: int = 10 * 1024 * 1024
    chunk_size: int = 1200
    chunk_overlap: int = 150
    database_path: str = "data/aegis.db"

    database_url: str | None = None
    openrouter_api_key: str | None = None
    openrouter_model: str = "openai/gpt-oss-20b:free"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def get_database_path() -> Path:
    configured_path = os.environ.get("AEGIS_DATABASE_PATH")
    if configured_path:
        return Path(configured_path)
    return Path(get_settings().database_path)
