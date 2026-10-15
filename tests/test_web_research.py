
from fastapi.testclient import TestClient

from app.api.routes import research as research_route
from app.main import app

client = TestClient(app)


def test_web_research_returns_sources(monkeypatch):
    def fake_search_web(query: str, max_results: int = 5):
        assert query == "major technology risks"
        assert max_results == 3
        return [
            {
                "title": "Technology Risk Report",
                "url": "https://example.com/technology-risks",
                "snippet": "An example research snippet.",
            }
        ]

    monkeypatch.setattr(research_route, "search_web", fake_search_web)

    response = client.post(
        "/api/v1/research/web",
        json={
            "query": "major technology risks",
            "max_results": 3,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result_count"] == 1
    assert data["results"][0]["title"] == "Technology Risk Report"
    assert data["results"][0]["url"] == (
        "https://example.com/technology-risks"
    )


def test_web_research_rejects_short_query():
    response = client.post(
        "/api/v1/research/web",
        json={"query": "AI"},
    )

    assert response.status_code == 422


def test_web_research_rejects_too_many_results():
    response = client.post(
        "/api/v1/research/web",
        json={
            "query": "major technology risks",
            "max_results": 11,
        },
    )

    assert response.status_code == 422


def test_web_research_returns_503_on_provider_failure(monkeypatch):
    def fake_search_web(query: str, max_results: int = 5):
        from app.services.web_research import WebResearchError

        raise WebResearchError("External web search is temporarily unavailable.")

    monkeypatch.setattr(research_route, "search_web", fake_search_web)

    response = client.post(
        "/api/v1/research/web",
        json={"query": "major technology risks"},
    )

    assert response.status_code == 503
    assert "temporarily unavailable" in response.json()["detail"]
