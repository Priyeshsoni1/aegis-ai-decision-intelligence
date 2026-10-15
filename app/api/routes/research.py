
from fastapi import APIRouter, HTTPException

from app.models.research_schemas import (
    WebResearchRequest,
    WebResearchResponse,
)
from app.services.web_research import WebResearchError, search_web

router = APIRouter(prefix="/api/v1/research", tags=["research"])


@router.post("/web", response_model=WebResearchResponse)
def web_research(request: WebResearchRequest) -> WebResearchResponse:
    try:
        results = search_web(
            query=request.query,
            max_results=request.max_results,
        )
    except WebResearchError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    return WebResearchResponse(
        query=request.query,
        result_count=len(results),
        results=results,
    )
