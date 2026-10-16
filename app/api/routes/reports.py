
import logging

from fastapi import APIRouter, HTTPException

from app.models.report_schemas import (
    ReportGenerationRequest,
    DecisionReportResponse,
)
from app.services.agent_graph import AgentConfigurationError
from app.services.decision_reports import (
    DecisionReportError,
    generate_decision_report,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["decision-reports"],
)


@router.post("/generate", response_model=DecisionReportResponse)
def create_decision_report(
    request: ReportGenerationRequest,
) -> DecisionReportResponse:
    try:
        return generate_decision_report(
            query=request.query,
            top_k=request.top_k,
            web_results=request.web_results,
        )

    except AgentConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except DecisionReportError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Unexpected decision report API error")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while generating the report.",
        ) from exc
