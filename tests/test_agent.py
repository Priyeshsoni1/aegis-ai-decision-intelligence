
from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import agent as agent_route
from app.services.agent_graph import AgentConfigurationError

client = TestClient(app)


def test_agent_endpoint_returns_evidence(monkeypatch):
    def fake_run_agent(query, top_k=5, web_results=5):
        return {
            "query": query,
            "answer": "The evidence identifies two risks. [Internal 1]",
            "internal_sources": [
                {
                    "document_id": "doc-1",
                    "filename": "risk-policy.pdf",
                    "content": "Access control risk",
                }
            ],
            "web_sources": [
                {
                    "title": "Risk guidance",
                    "url": "https://example.com/risks",
                    "snippet": "Example source snippet",
                }
            ],
            "errors": [],
        }

    monkeypatch.setattr(agent_route, "run_agent", fake_run_agent)

    response = client.post(
        "/api/v1/agent/run",
        json={
            "query": "What are the major technology risks?",
            "top_k": 5,
            "web_results": 5,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"].startswith("The evidence identifies")
    assert len(data["internal_sources"]) == 1
    assert len(data["web_sources"]) == 1
    assert data["errors"] == []


def test_agent_rejects_short_query():
    response = client.post(
        "/api/v1/agent/run",
        json={"query": "AI"},
    )

    assert response.status_code == 422


def test_agent_rejects_invalid_result_limit():
    response = client.post(
        "/api/v1/agent/run",
        json={
            "query": "What are the major technology risks?",
            "top_k": 50,
        },
    )

    assert response.status_code == 422


def test_agent_configuration_failure_returns_503(monkeypatch):
    def fake_run_agent(query, top_k=5, web_results=5):
        raise AgentConfigurationError("Missing API key")

    monkeypatch.setattr(agent_route, "run_agent", fake_run_agent)

    response = client.post(
        "/api/v1/agent/run",
        json={"query": "What are the major technology risks?"},
    )

    assert response.status_code == 503
    assert "Missing API key" in response.json()["detail"]
