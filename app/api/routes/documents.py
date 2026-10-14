
import logging

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.db.database import get_connection
from app.models.schemas import (
    ChunkListResponse,
    ChunkResponse,
    DocumentListResponse,
    DocumentResponse,
    DocumentUploadResponse,
)
from app.services.document_ingestion import (
    DuplicateDocumentError,
    ingest_document,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])


@router.post(
    "",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
) -> DocumentUploadResponse:
    filename = (file.filename or "").replace("\\", "/").rsplit("/", 1)[-1]

    if not filename or filename in {".", ".."}:
        raise HTTPException(status_code=400, detail="A valid filename is required.")

    settings = get_settings()

    try:
        content = await file.read(settings.max_upload_size_bytes + 1)
    finally:
        await file.close()

    if len(content) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the maximum upload size of 10 MiB.",
        )

    try:
        document = ingest_document(filename, content)
    except DuplicateDocumentError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected document ingestion failure")
        raise HTTPException(
            status_code=500,
            detail="Document ingestion failed.",
        ) from exc

    return DocumentUploadResponse(
        message="Document ingested successfully.",
        document=DocumentResponse(**document),
    )


@router.get("", response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM documents ORDER BY created_at DESC"
        ).fetchall()

    return DocumentListResponse(
        total=len(rows),
        documents=[DocumentResponse(**dict(row)) for row in rows],
    )


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str) -> DocumentResponse:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM documents WHERE id = ?",
            (document_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    return DocumentResponse(**dict(row))


@router.get("/{document_id}/chunks", response_model=ChunkListResponse)
def get_document_chunks(document_id: str) -> ChunkListResponse:
    with get_connection() as connection:
        exists = connection.execute(
            "SELECT id FROM documents WHERE id = ?",
            (document_id,),
        ).fetchone()

        if exists is None:
            raise HTTPException(status_code=404, detail="Document not found.")

        rows = connection.execute(
            """
            SELECT * FROM document_chunks
            WHERE document_id = ?
            ORDER BY chunk_index
            """,
            (document_id,),
        ).fetchall()

    return ChunkListResponse(
        document_id=document_id,
        total=len(rows),
        chunks=[ChunkResponse(**dict(row)) for row in rows],
    )
