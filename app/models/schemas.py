
from pydantic import BaseModel, ConfigDict, Field


class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    sha256: str
    file_size_bytes: int
    character_count: int
    chunk_count: int
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class DocumentUploadResponse(BaseModel):
    message: str
    document: DocumentResponse


class ChunkResponse(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    text: str
    character_count: int
    created_at: str


class ChunkListResponse(BaseModel):
    document_id: str
    total: int = Field(ge=0)
    chunks: list[ChunkResponse]


class DocumentListResponse(BaseModel):
    total: int = Field(ge=0)
    documents: list[DocumentResponse]
