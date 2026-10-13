
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging_config import configure_logging

configure_logging()
settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "An AI platform for evidence-driven due diligence, "
        "hybrid retrieval, and decision intelligence."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", tags=["General"])
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "message": "Welcome to Aegis.",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.app_env,
    }
