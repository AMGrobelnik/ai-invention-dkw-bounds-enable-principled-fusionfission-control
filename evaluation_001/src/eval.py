"""Evaluation script for DKW Controller."""
import json
import numpy as np

def compute_metrics(results: dict) -> dict:
    """Compute evaluation metrics."""
    metrics = {}

    for method in ["baseline", "proposed"]:
        preds = results[method]

        # Count decisions
        fusion_count = sum(1 for p in preds if p["decision"] == "fusion")
        fission_count = sum(1 for p in preds if p["decision"] == "fission")

        # Compute error rate
        errors = sum(1 for p in preds if p["error"])
        error_rate = errors / len(preds)

        # API calls (fusion=1, fission=2)
        api_calls = fusion_count + 2 * fission_count

        metrics[method] = {
            "fusion_rate": fusion_count / len(preds),
            "fission_rate": fission_count / len(preds),
            "error_rate": error_rate,
            "api_calls": api_calls,
            "avg_calls_per_example": api_calls / len(preds),
        }

    # Compute improvement
    baseline_calls = metrics["baseline"]["avg_calls_per_example"]
    proposed_calls = metrics["proposed"]["avg_calls_per_example"]
    metrics["improvement"] = {
        "api_reduction_pct": (baseline_calls - proposed_calls) / baseline_calls * 100,
        "error_rate_diff": metrics["proposed"]["error_rate"] - metrics["baseline"]["error_rate"],
    }

    return metrics


if __name__ == "__main__":
    with open("../experiment_001/method_out.json") as f:
        results = json.load(f)

    metrics = compute_metrics(results)
    with open("eval_out.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"API reduction: {metrics['improvement']['api_reduction_pct']:.1f}%")
