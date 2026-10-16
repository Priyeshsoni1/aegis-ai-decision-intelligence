
import json
from pathlib import Path

from app.evaluation.metrics import recall_at_k, reciprocal_rank
from app.services.retrieval import search_chunks


DATASET_PATH = Path("data/evaluation/retrieval_cases.json")
TOP_K = 5


def main() -> None:
    cases = json.loads(DATASET_PATH.read_text(encoding="utf-8"))

    results = []
    recall_scores = []
    reciprocal_ranks = []

    for case in cases:
        relevant_ids = case["relevant_chunk_ids"]

        if any(
            item.startswith("REPLACE_WITH_")
            for item in relevant_ids
        ):
            raise ValueError(
                f"Replace placeholder IDs in case {case['case_id']} "
                "with manually verified chunk IDs before evaluating."
            )

        retrieved = search_chunks(case["query"], top_k=TOP_K)

        retrieved_ids = [
            str(item.get("id") or item.get("chunk_id") or "")
            for item in retrieved
        ]
        retrieved_ids = [item for item in retrieved_ids if item]

        recall = recall_at_k(retrieved_ids, relevant_ids, TOP_K)
        rr = reciprocal_rank(retrieved_ids, relevant_ids)

        recall_scores.append(recall)
        reciprocal_ranks.append(rr)

        results.append(
            {
                "case_id": case["case_id"],
                "query": case["query"],
                "recall_at_k": recall,
                "reciprocal_rank": rr,
                "retrieved_ids": retrieved_ids,
            }
        )

    count = len(results)
    if count == 0:
        raise ValueError("Evaluation dataset contains no cases.")

    report = {
        "case_count": count,
        "k": TOP_K,
        "mean_recall_at_k": sum(recall_scores) / count,
        "mean_reciprocal_rank": sum(reciprocal_ranks) / count,
        "cases": results,
    }

    output_path = Path("data/evaluation/retrieval_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))
    print(f"\nSaved evaluation results to {output_path}")


if __name__ == "__main__":
    main()
