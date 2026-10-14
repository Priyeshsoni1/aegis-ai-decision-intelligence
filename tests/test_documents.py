
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "AEGIS_DATABASE_PATH",
        str(tmp_path / "test_aegis.db"),
    )

    with TestClient(app) as test_client:
        yield test_client


def test_upload_text_document(client):
    response = client.post(
        "/api/v1/documents",
        files={
            "file": (
                "rules.txt",
                b"Aegis stores evidence and generates decision reports.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["document"]["filename"] == "rules.txt"
    assert body["document"]["chunk_count"] >= 1
    assert body["document"]["character_count"] > 0


def test_list_documents(client):
    client.post(
        "/api/v1/documents",
        files={"file": ("notes.md", b"# Aegis\nProject notes.", "text/markdown")},
    )

    response = client.get("/api/v1/documents")

    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_get_document_chunks(client):
    upload = client.post(
        "/api/v1/documents",
        files={"file": ("notes.txt", b"Evidence-based decisions.", "text/plain")},
    )
    document_id = upload.json()["document"]["id"]

    response = client.get(f"/api/v1/documents/{document_id}/chunks")

    assert response.status_code == 200
    assert response.json()["total"] >= 1
    assert "Evidence-based decisions." in response.json()["chunks"][0]["text"]


def test_duplicate_upload_returns_conflict(client):
    file_data = {
        "file": ("same.txt", b"Same content.", "text/plain"),
    }

    assert client.post("/api/v1/documents", files=file_data).status_code == 201
    response = client.post("/api/v1/documents", files=file_data)

    assert response.status_code == 409


def test_unsupported_file_is_rejected(client):
    response = client.post(
        "/api/v1/documents",
        files={"file": ("program.exe", b"not a document", "application/octet-stream")},
    )

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_missing_document_returns_404(client):
    response = client.get("/api/v1/documents/nonexistent")

    assert response.status_code == 404
