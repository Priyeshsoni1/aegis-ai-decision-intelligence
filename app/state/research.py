from datetime import datetime
from typing import Any
from datetime import UTC, datetime
from uuid import uuid4
from pydantic import BaseModel, Field

from app.state.models import (
    DecisionCandidate,
    Evidence,
    Recommendation,
    ResearchError,
    ResearchTask,
    ToolCallRecord,
)


class ResearchState(BaseModel):
    """Complete state carried through an Aegis research execution."""

    # Request
    task_id: str
    user_query: str

    # Execution metadata
    created_at: datetime
    updated_at: datetime
    status: str = "pending"

    # Requirements extracted from the request
    requirements: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)

    # Research planning
    research_plan: list[ResearchTask] = Field(
        default_factory=list
    )
    current_task_id: str | None = None

    # Research results
    research_results: list[dict[str, Any]] = Field(
        default_factory=list
    )

    # Evidence
    evidence: list[Evidence] = Field(
        default_factory=list
    )

    # Tool execution
    tool_calls: list[ToolCallRecord] = Field(
        default_factory=list
    )

    # Error and recovery information
    errors: list[ResearchError] = Field(
        default_factory=list
    )
    retry_count: int = Field(default=0, ge=0)
    iteration_count: int = Field(default=0, ge=0)

    # Decision
    candidates: list[DecisionCandidate] = Field(
        default_factory=list
    )
    recommendation: Recommendation | None = None

    # Final output
    confidence: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )
    uncertainty: list[str] = Field(
        default_factory=list
    )
    final_report: str | None = None



def create_research_state(
    user_query: str,
) -> ResearchState:
    """Create the initial state for a research execution."""

    now = datetime.now(UTC)

    return ResearchState(
        task_id=str(uuid4()),
        user_query=user_query,
        created_at=now,
        updated_at=now,
    )