# Aegis — AI Due Diligence & Decision Intelligence

Aegis is an evidence-driven AI platform for researching business and
technology questions and producing transparent recommendations.

## Current Status

- Phase 1: FastAPI foundation and configuration.
- Phase 2: Document ingestion, extraction, chunking, and SQLite storage.

## Technology Stack

- Python, FastAPI, Pydantic
- PyMuPDF for PDF text extraction
- SQLite for local document metadata and chunks
- pytest, HTTPX, Ruff
- Git and GitHub

## Setup on Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

Copy-Item .env.example .env
```

## Run

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to upload documents and explore the API.

## API Endpoints

- `GET /health` — API health
- `POST /api/v1/documents` — upload PDF, TXT, or Markdown
- `GET /api/v1/documents` — list document metadata
- `GET /api/v1/documents/{document_id}` — document details
- `GET /api/v1/documents/{document_id}/chunks` — inspect text chunks

## Tests

```powershell
python -m pytest
python -m ruff check .
```

## Planned Next Steps

- Local embeddings and hybrid RAG
- External web research
- LangGraph agent orchestration
- Evidence-backed decision reports
- Reliability, evaluation, observability, and deployment

## Security

Never commit `.env` files, credentials, or private documents.
Uploaded documents are stored as extracted text chunks in the local database.
Only upload documents you are authorized to process.

## Phase 3: Embeddings and Hybrid Retrieval

Aegis converts stored document chunks into 384-dimensional embeddings
using `sentence-transformers/all-MiniLM-L6-v2`.

### Retrieval Architecture

- Local embeddings: Sentence Transformers
- Vector database: PostgreSQL + pgvector
- Semantic retrieval: cosine-distance nearest-neighbor search
- Keyword retrieval: PostgreSQL full-text search
- Fusion: Reciprocal Rank Fusion (RRF)

### Index a Document

1. Upload a document using `POST /api/v1/documents`.
2. Copy its returned document ID.
3. Call `POST /api/v1/retrieval/index/{document_id}`.

### Search

Call `POST /api/v1/retrieval/search` with:

```json
{
  "query": "What are the major technology risks?",
  "top_k": 5
}
```

The results contain the source filename, document ID, chunk content,
and fusion score.

### Cost

Embeddings run locally. PostgreSQL uses a free-tier service where
available. Free-tier quotas and availability may change.
