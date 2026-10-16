
from typing import Any


def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int = 5,
) -> float:
    """Fraction of known relevant items retrieved within the top k."""
    if not relevant_ids:
        return 0.0

    retrieved = set(retrieved_ids[:k])
    relevant = set(relevant_ids)

    return len(retrieved & relevant) / len(relevant)


def reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: list[str],
) -> float:
    """Reciprocal rank of the first relevant result."""
    relevant = set(relevant_ids)

    for rank, item_id in enumerate(retrieved_ids, start=1):
        if item_id in relevant:
            return 1.0 / rank

    return 0.0


def evaluate_report_references(
    report: dict[str, Any],
    evidence_sources: list[dict[str, Any]],
) -> dict[str, Any]:
    """Check report structure and evidence-reference integrity."""
    valid_ids = {
        str(source["source_id"])
        for source in evidence_sources
        if source.get("source_id")
    }

    all_references: list[str] = []
    findings = report.get("findings", [])
    recommendations = report.get("recommendations", [])

    for item in findings + recommendations:
        all_references.extend(
            str(ref) for ref in item.get("evidence_refs", [])
        )

    invalid_references = sorted(set(all_references) - valid_ids)
    unsupported_items = sum(
        1
        for item in findings + recommendations
        if not item.get("evidence_refs")
    )

    return {
        "finding_count": len(findings),
        "recommendation_count": len(recommendations),
        "source_count": len(valid_ids),
        "reference_count": len(all_references),
        "invalid_references": invalid_references,
        "items_without_references": unsupported_items,
        "reference_integrity_pass": not invalid_references,
    }
