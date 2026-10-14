
import logging

from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.models.retrieval_schemas import (
    IndexDocumentResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
)
from app.services.retrieval import index_document, search_chunks

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/retrieval", tags=["Retrieval"])


def require_database_url() -> None:
    if not get_settings().database_url:
        raise HTTPException(
            status_code=503,
            detail="PostgreSQL is not configured. Set DATABASE_URL in .env.",
        )


@router.post(
    "/index/{document_id}",
    response_model=IndexDocumentResponse,
)
def index_existing_document(document_id: str) -> IndexDocumentResponse:
    require_database_url()

    try:
        result = index_document(document_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Document indexing failed")
        raise HTTPException(
            status_code=503,
            detail="Document indexing failed. Check database and model configuration.",
        ) from exc

    return IndexDocumentResponse(
        message="Document indexed successfully.",
        **result,
    )


@router.post("/search", response_model=SearchResponse)
def hybrid_search(request: SearchRequest) -> SearchResponse:
    require_database_url()

    try:
        results = search_chunks(request.query, request.top_k)
    except Exception as exc:
        logger.exception("Hybrid search failed")
        raise HTTPException(
            status_code=503,
            detail="Hybrid search failed. Check database and model configuration.",
        ) from exc

    formatted_results = [
        SearchResult(
            chunk_id=row["id"],
            document_id=row["document_id"],
            filename=row["filename"],
            chunk_index=row["chunk_index"],
            content=row["content"],
            fusion_score=float(row["fusion_score"]),
        )
        for row in results
    ]

    return SearchResponse(
        query=request.query,
        total=len(formatted_results),
        results=formatted_results,
    )
