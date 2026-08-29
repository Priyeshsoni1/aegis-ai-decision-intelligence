from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class TaskStatus(StrEnum):
    """Status of an individual research task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class EvidenceQuality(StrEnum):
    """Quality classification assigned to evidence."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EvidenceType(StrEnum):
    """Classification of how information is used."""

    FACT = "fact"
    INFERENCE = "inference"
    UNCERTAINTY = "uncertainty"


class ResearchTask(BaseModel):
    """A single research task generated from the user's request."""

    task_id: str
    description: str
    objective: str
    status: TaskStatus = TaskStatus.PENDING
    priority: int = Field(default=1, ge=1)
    required_tools: list[str] = Field(default_factory=list)


class ToolCallRecord(BaseModel):
    """Record of one tool invocation."""

    call_id: str
    tool_name: str
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] | None = None
    success: bool = False
    error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    latency_ms: float | None = Field(default=None, ge=0)


class Evidence(BaseModel):
    """Evidence collected during research."""

    evidence_id: str
    source: str
    title: str | None = None
    content: str
    relevance_score: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )
    quality: EvidenceQuality | None = None
    evidence_type: EvidenceType = EvidenceType.FACT
    collected_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CandidateScore(BaseModel):
    """Score assigned to a decision candidate."""

    candidate: str
    criterion: str
    score: float = Field(ge=0, le=10)
    rationale: str
    evidence_ids: list[str] = Field(default_factory=list)


class DecisionCandidate(BaseModel):
    """A candidate option considered by the decision engine."""

    name: str
    description: str | None = None
    scores: list[CandidateScore] = Field(default_factory=list)


class Recommendation(BaseModel):
    """Final structured recommendation."""

    selected_option: str
    rationale: str
    alternatives: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    uncertainties: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)


class ResearchError(BaseModel):
    """Structured representation of an execution error."""

    error_type: str
    message: str
    component: str
    retryable: bool = False
    occurred_at: datetime | None = None