
from pydantic import BaseModel, Field


class WebResearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)
    max_results: int = Field(default=5, ge=1, le=10)


class WebResearchResult(BaseModel):
    title: str
    url: str
    snippet: str


class WebResearchResponse(BaseModel):
    query: str
    result_count: int
    results: list[WebResearchResult]
