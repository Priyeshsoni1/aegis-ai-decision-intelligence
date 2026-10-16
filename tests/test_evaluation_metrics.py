
from app.evaluation.metrics import (
    evaluate_report_references,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k():
    assert recall_at_k(
        ["a", "b", "c"],
        ["b", "c", "d"],
        k=2,
    ) == 1 / 3


def test_recall_at_k_returns_zero_when_no_relevant_results():
    assert recall_at_k(["a", "b"], ["x"], k=2) == 0.0


def test_recall_at_k_handles_empty_relevant_set():
    assert recall_at_k(["a", "b"], [], k=2) == 0.0


def test_reciprocal_rank():
    assert reciprocal_rank(
        ["a", "b", "c"],
        ["c"],
    ) == 1 / 3


def test_reciprocal_rank_returns_zero_when_no_match():
    assert reciprocal_rank(["a", "b"], ["x"]) == 0.0


def test_report_reference_integrity():
    report = {
        "findings": [
            {"evidence_refs": ["I1"]},
            {"evidence_refs": ["UNKNOWN"]},
        ],
        "recommendations": [
            {"evidence_refs": []},
        ],
    }
    sources = [{"source_id": "I1"}, {"source_id": "W1"}]

    result = evaluate_report_references(report, sources)

    assert result["reference_integrity_pass"] is False
    assert result["invalid_references"] == ["UNKNOWN"]
    assert result["items_without_references"] == 1
    assert result["finding_count"] == 2
    assert result["recommendation_count"] == 1
