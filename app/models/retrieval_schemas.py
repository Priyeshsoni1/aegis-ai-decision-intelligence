
from pydantic import BaseModel, Field


class IndexDocumentResponse(BaseModel):
    message: str
    document_id: str
    filename: str
    indexed_chunks: int


class SearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    chunk_index: int
    content: str
    fusion_score: float


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchResult]
