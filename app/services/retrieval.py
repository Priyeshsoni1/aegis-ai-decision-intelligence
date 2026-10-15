
import logging

from pgvector import Vector
from psycopg.rows import dict_row

from app.db.database import get_connection
from app.db.vector_store import (
    get_pg_connection,
    initialize_vector_store,
    upsert_chunks,
)
from app.services.embeddings import embed_query, embed_texts

logger = logging.getLogger(__name__)


def index_document(document_id: str) -> dict:
    with get_connection() as connection:
        document = connection.execute(
            "SELECT id, filename FROM documents WHERE id = ?",
            (document_id,),
        ).fetchone()

        if document is None:
            raise LookupError("Document not found.")

        rows = connection.execute(
            """
            SELECT id, document_id, chunk_index, text
            FROM document_chunks
            WHERE document_id = ?
            ORDER BY chunk_index
            """,
            (document_id,),
        ).fetchall()

    if not rows:
        raise ValueError("Document has no chunks to index.")

    chunks = [row["text"] for row in rows]
    vectors = embed_texts(chunks)

    records = [
        {
            "id": row["id"],
            "document_id": row["document_id"],
            "filename": document["filename"],
            "chunk_index": row["chunk_index"],
            "content": row["text"],
            "embedding": vector,
        }
        for row, vector in zip(rows, vectors, strict=True)
    ]

    initialize_vector_store()
    upsert_chunks(records)

    logger.info(
        "Indexed document %s with %d chunks",
        document_id,
        len(records),
    )

    return {
        "document_id": document_id,
        "filename": document["filename"],
        "indexed_chunks": len(records),
    }


def search_chunks(query: str, top_k: int = 5) -> list[dict]:
    query_vector = embed_query(query)

    sql = """
        WITH query_embedding AS (
            SELECT %s::vector AS embedding
        ),
        vector_ranked AS (
            SELECT
                c.id,
                ROW_NUMBER() OVER (
                    ORDER BY c.embedding <=> q.embedding
                ) AS rank
            FROM aegis_chunks c
            CROSS JOIN query_embedding q
            ORDER BY c.embedding <=> q.embedding
            LIMIT %s
        ),
        keyword_scores AS (
            SELECT
                id,
                ts_rank_cd(
                    search_tsv,
                    plainto_tsquery('english', %s)
                ) AS score
            FROM aegis_chunks
            WHERE search_tsv @@ plainto_tsquery('english', %s)
        ),
        keyword_ranked AS (
            SELECT
                id,
                ROW_NUMBER() OVER (ORDER BY score DESC) AS rank
            FROM keyword_scores
            ORDER BY score DESC
            LIMIT %s
        ),
        fused AS (
            SELECT id, 1.0 / (60 + rank) AS score
            FROM vector_ranked
            UNION ALL
            SELECT id, 1.0 / (60 + rank) AS score
            FROM keyword_ranked
        ),
        aggregated AS (
            SELECT id, SUM(score) AS score
            FROM fused
            GROUP BY id
        )
        SELECT
            c.id,
            c.document_id,
            c.filename,
            c.chunk_index,
            c.content,
            a.score AS fusion_score
        FROM aggregated a
        JOIN aegis_chunks c ON c.id = a.id
        ORDER BY a.score DESC
        LIMIT %s
    """

    with get_pg_connection().cursor(row_factory=dict_row) as cursor:
        rows = cursor.execute(
            sql,
            (
                Vector(query_vector),
                top_k,
                query,
                query,
                top_k,
                top_k,
            ),
        ).fetchall()

    return [dict(row) for row in rows]
