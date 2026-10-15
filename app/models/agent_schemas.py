
from typing import Any

from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)
    top_k: int = Field(default=5, ge=1, le=10)
    web_results: int = Field(default=5, ge=1, le=10)


class AgentRunResponse(BaseModel):
    query: str
    answer: str
    internal_sources: list[dict[str, Any]]
    web_sources: list[dict[str, str]]
    errors: list[str] = Field(default_factory=list)
