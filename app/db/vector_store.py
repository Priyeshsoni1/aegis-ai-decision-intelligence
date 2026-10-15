
import logging

import psycopg
from pgvector import Vector
from pgvector.psycopg import register_vector

from app.core.config import get_settings

logger = logging.getLogger(__name__)


def get_pg_connection() -> psycopg.Connection:
    settings = get_settings()

    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured. Add your PostgreSQL URL to .env."
        )

    connection = psycopg.connect(settings.database_url)

    try:
        connection.execute("CREATE EXTENSION IF NOT EXISTS vector")
        connection.commit()
        register_vector(connection)
        return connection
    except Exception:
        connection.close()
        raise


def initialize_vector_store() -> None:
    with get_pg_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS aegis_chunks (
                id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                embedding vector(384) NOT NULL,
                search_tsv tsvector GENERATED ALWAYS AS (
                    to_tsvector('english', content)
                ) STORED,
                indexed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE(document_id, chunk_index)
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_aegis_chunks_search_tsv
            ON aegis_chunks USING GIN (search_tsv)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_aegis_chunks_embedding
            ON aegis_chunks USING hnsw (embedding vector_cosine_ops)
            """
        )

    logger.info("PostgreSQL vector store initialized")


def upsert_chunks(records: list[dict]) -> None:
    if not records:
        return

    with get_pg_connection() as connection:
        with connection.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO aegis_chunks (
                    id, document_id, filename, chunk_index, content, embedding
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    document_id = EXCLUDED.document_id,
                    filename = EXCLUDED.filename,
                    chunk_index = EXCLUDED.chunk_index,
                    content = EXCLUDED.content,
                    embedding = EXCLUDED.embedding,
                    indexed_at = NOW()
                """,
                [
                    (
                        record["id"],
                        record["document_id"],
                        record["filename"],
                        record["chunk_index"],
                        record["content"],
                        Vector(record["embedding"]),
                    )
                    for record in records
                ],
            )

    logger.info("Stored %d chunks in PostgreSQL", len(records))
