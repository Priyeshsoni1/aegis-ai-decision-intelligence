
import logging

from fastapi import APIRouter, HTTPException

from app.models.agent_schemas import AgentRunRequest, AgentRunResponse
from app.services.agent_graph import (
    AgentConfigurationError,
    run_agent,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])


@router.post("/run", response_model=AgentRunResponse)
def run_research_agent(
    request: AgentRunRequest,
) -> AgentRunResponse:
    try:
        result = run_agent(
            query=request.query,
            top_k=request.top_k,
            web_results=request.web_results,
        )
        return AgentRunResponse(**result)

    except AgentConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Aegis agent execution failed")
        raise HTTPException(
            status_code=503,
            detail="The research agent could not complete the request.",
        ) from exc
