
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_rejects_short_query() -> None:
    response = client.post(
        "/api/v1/retrieval/search",
        json={"query": "AI"},
    )

    assert response.status_code == 422


def test_search_rejects_invalid_top_k() -> None:
    response = client.post(
        "/api/v1/retrieval/search",
        json={"query": "technology risk assessment", "top_k": 21},
    )

    assert response.status_code == 422
