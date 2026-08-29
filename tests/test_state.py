from datetime import UTC

from app.state.models import (
    CandidateScore,
    DecisionCandidate,
    Evidence,
    EvidenceQuality,
    EvidenceType,
)
from app.state.research import create_research_state


def test_create_research_state():
    state = create_research_state(
        "Which vector database should we use?"
    )

    assert state.user_query == (
        "Which vector database should we use?"
    )
    assert state.task_id
    assert state.status == "pending"
    assert state.retry_count == 0
    assert state.iteration_count == 0
    assert state.created_at.tzinfo == UTC


def test_evidence_model():
    evidence = Evidence(
        evidence_id="ev-001",
        source="official documentation",
        title="Performance",
        content="Example evidence",
        relevance_score=0.95,
        quality=EvidenceQuality.HIGH,
        evidence_type=EvidenceType.FACT,
    )

    assert evidence.relevance_score == 0.95
    assert evidence.quality == EvidenceQuality.HIGH


def test_candidate_score():
    score = CandidateScore(
        candidate="Qdrant",
        criterion="Latency",
        score=8.5,
        rationale="Strong benchmark results.",
        evidence_ids=["ev-001"],
    )

    candidate = DecisionCandidate(
        name="Qdrant",
        scores=[score],
    )

    assert candidate.scores[0].score == 8.5
    assert candidate.scores[0].evidence_ids == ["ev-001"]