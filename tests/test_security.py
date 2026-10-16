
import pytest
from pydantic import ValidationError

from app.models.agent_schemas import AgentRunRequest
from app.models.report_schemas import (
    DecisionReport,
    ReportGenerationRequest,
)


def test_agent_rejects_excessively_long_query():
    with pytest.raises(ValidationError):
        AgentRunRequest(query="x" * 501)


def test_report_request_rejects_excessively_long_query():
    with pytest.raises(ValidationError):
        ReportGenerationRequest(query="x" * 501)


def test_agent_rejects_excessive_retrieval_limit():
    with pytest.raises(ValidationError):
        AgentRunRequest(
            query="Assess technology risks",
            top_k=11,
        )


def test_report_rejects_unsupported_confidence():
    with pytest.raises(ValidationError):
        DecisionReport.model_validate(
            {
                "title": "Technology risk assessment",
                "executive_summary": (
                    "This is a sufficiently detailed executive summary."
                ),
                "overall_assessment": (
                    "Additional evidence is required before deciding."
                ),
                "findings": [
                    {
                        "title": "Access control risk",
                        "description": (
                            "The evidence indicates a possible access "
                            "control concern."
                        ),
                        "severity": "high",
                        "confidence": "medium",
                        "evidence_refs": [],
                    }
                ],
                "recommendations": [],
                "key_uncertainties": [],
                "decision_options": [],
            }
        )


def test_report_accepts_valid_confidence():
    report = DecisionReport.model_validate(
        {
            "title": "Technology risk assessment",
            "executive_summary": (
                "This is a sufficiently detailed executive summary."
            ),
            "overall_assessment": (
                "Additional evidence is required before deciding."
            ),
            "findings": [
                {
                    "title": "Access control risk",
                    "description": (
                        "The evidence indicates a possible access "
                        "control concern."
                    ),
                    "severity": "high",
                    "confidence": "moderate",
                    "evidence_refs": [],
                }
            ],
            "recommendations": [],
            "key_uncertainties": [],
            "decision_options": [],
        }
    )

    assert report.findings[0].confidence == "moderate"
