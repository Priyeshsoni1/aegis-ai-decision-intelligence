
from typing import Literal

from pydantic import BaseModel, Field, field_validator


Severity = Literal["low", "moderate", "high", "critical"]
Confidence = Literal["low", "moderate", "high"]
Priority = Literal["low", "medium", "high", "urgent"]


class ReportFinding(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5, max_length=3000)
    severity: Severity
    confidence: Confidence
    evidence_refs: list[str] = Field(default_factory=list)


class ReportRecommendation(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    action: str = Field(min_length=5, max_length=2000)
    priority: Priority
    rationale: str = Field(min_length=5, max_length=2000)
    evidence_refs: list[str] = Field(default_factory=list)


class DecisionReport(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    executive_summary: str = Field(min_length=10, max_length=4000)
    overall_assessment: str = Field(min_length=5, max_length=3000)
    findings: list[ReportFinding] = Field(default_factory=list, max_length=20)
    recommendations: list[ReportRecommendation] = Field(
        default_factory=list,
        max_length=20,
    )
    key_uncertainties: list[str] = Field(default_factory=list, max_length=20)
    decision_options: list[str] = Field(default_factory=list, max_length=10)


class ReportGenerationRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)
    top_k: int = Field(default=5, ge=1, le=10)
    web_results: int = Field(default=5, ge=1, le=10)


class DecisionReportResponse(BaseModel):
    report_id: str
    query: str
    report: DecisionReport
    evidence_sources: list[dict[str, str]]
    warnings: list[str] = Field(default_factory=list)

    @field_validator("report_id")
    @classmethod
    def validate_report_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("report_id cannot be empty")
        return value
