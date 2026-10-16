
from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import reports as reports_route
from app.services.agent_graph import AgentConfigurationError
from app.services.decision_reports import DecisionReportError

client = TestClient(app)


def sample_response():
    return {
        "report_id": "test-report-001",
        "query": "Assess the technology risks",
        "report": {
            "title": "Technology Risk Assessment",
            "executive_summary": (
                "The available evidence identifies potential "
                "technology risks requiring further assessment."
            ),
            "overall_assessment": (
                "The current evidence is insufficient for a final "
                "go/no-go decision."
            ),
            "findings": [
                {
                    "title": "Access control risk",
                    "description": (
                        "The reviewed material indicates an access "
                        "control concern."
                    ),
                    "severity": "high",
                    "confidence": "moderate",
                    "evidence_refs": ["I1"],
                }
            ],
            "recommendations": [
                {
                    "title": "Review access controls",
                    "action": (
                        "Review permissions and validate the access "
                        "control configuration."
                    ),
                    "priority": "high",
                    "rationale": (
                        "Validation would help determine the extent "
                        "of the identified concern."
                    ),
                    "evidence_refs": ["I1"],
                }
            ],
            "key_uncertainties": [
                "The current evidence does not establish the full impact."
            ],
            "decision_options": [
                "Conduct further validation before making a decision."
            ],
        },
        "evidence_sources": [
            {
                "source_id": "I1",
                "source_type": "internal",
                "title": "risk-policy.pdf",
                "url": "",
                "document_id": "doc-1",
            }
        ],
        "warnings": [],
    }


def test_generate_report_returns_structured_response(monkeypatch):
    monkeypatch.setattr(
        reports_route,
        "generate_decision_report",
        lambda query, top_k=5, web_results=5: sample_response(),
    )

    response = client.post(
        "/api/v1/reports/generate",
        json={"query": "Assess the technology risks"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["report"]["title"] == "Technology Risk Assessment"
    assert data["report"]["findings"][0]["evidence_refs"] == ["I1"]
    assert data["evidence_sources"][0]["source_id"] == "I1"


def test_report_rejects_short_query():
    response = client.post(
        "/api/v1/reports/generate",
        json={"query": "AI"},
    )

    assert response.status_code == 422


def test_report_rejects_invalid_top_k():
    response = client.post(
        "/api/v1/reports/generate",
        json={
            "query": "Assess the technology risks",
            "top_k": 50,
        },
    )

    assert response.status_code == 422


def test_report_configuration_error_returns_503(monkeypatch):
    def fail_generation(query, top_k=5, web_results=5):
        raise AgentConfigurationError("Missing API key")

    monkeypatch.setattr(
        reports_route,
        "generate_decision_report",
        fail_generation,
    )

    response = client.post(
        "/api/v1/reports/generate",
        json={"query": "Assess the technology risks"},
    )

    assert response.status_code == 503


def test_report_generation_error_returns_502(monkeypatch):
    def fail_generation(query, top_k=5, web_results=5):
        raise DecisionReportError("Invalid model output")

    monkeypatch.setattr(
        reports_route,
        "generate_decision_report",
        fail_generation,
    )

    response = client.post(
        "/api/v1/reports/generate",
        json={"query": "Assess the technology risks"},
    )

    assert response.status_code == 502
