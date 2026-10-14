
import hashlib
import logging
import sqlite3
from datetime import datetime, timezone
from uuid import uuid4

from app.core.config import get_settings
from app.db.database import get_connection
from app.services.chunker import split_text
from app.services.document_parser import extract_text

logger = logging.getLogger(__name__)


class DuplicateDocumentError(Exception):
    pass


def ingest_document(filename: str, content: bytes) -> dict:
    settings = get_settings()

    if len(content) > settings.max_upload_size_bytes:
        raise ValueError("File exceeds the maximum upload size of 10 MiB.")

    text = extract_text(filename, content)
    chunks = split_text(
        text,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    if not chunks:
        raise ValueError("The document produced no text chunks.")

    digest = hashlib.sha256(content).hexdigest()
    document_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    file_type = filename.rsplit(".", 1)[-1].lower()

    document = {
        "id": document_id,
        "filename": filename,
        "file_type": file_type,
        "sha256": digest,
        "file_size_bytes": len(content),
        "character_count": len(text),
        "chunk_count": len(chunks),
        "created_at": created_at,
    }

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO documents (
                    id, filename, file_type, sha256, file_size_bytes,
                    character_count, chunk_count, created_at
                ) VALUES (
                    :id, :filename, :file_type, :sha256, :file_size_bytes,
                    :character_count, :chunk_count, :created_at
                )
                """,
                document,
            )

            connection.executemany(
                """
                INSERT INTO document_chunks (
                    id, document_id, chunk_index, text,
                    character_count, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        str(uuid4()),
                        document_id,
                        index,
                        chunk,
                        len(chunk),
                        created_at,
                    )
                    for index, chunk in enumerate(chunks)
                ],
            )
    except sqlite3.IntegrityError as exc:
        if "sha256" in str(exc).lower() or "documents.sha256" in str(exc).lower():
            raise DuplicateDocumentError(
                "This exact file has already been ingested."
            ) from exc
        raise

    logger.info(
        "Document ingested: id=%s chunks=%d characters=%d",
        document_id,
        len(chunks),
        len(text),
    )

    return document
