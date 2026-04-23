from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from corpus_metrics import evaluate_staged_corpus_readiness


def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Write a staged readiness report with before/after comparison.")
    parser.add_argument("--bundle-dir", required=True, help="Staged bundle directory to evaluate.")
    parser.add_argument("--output", required=True, help="Output JSON path for the readiness report.")
    parser.add_argument("--previous-report", help="Optional previous report JSON to compare against.")
    parser.add_argument("--change-note", action="append", default=[], help="Optional note describing what changed in this pass.")
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir)
    output_path = Path(args.output)
    previous_path = Path(args.previous_report) if args.previous_report else output_path

    previous = load_json(previous_path)
    metrics = evaluate_staged_corpus_readiness(bundle_dir)
    metrics["comparison_to_previous"] = {
        "previous_readiness_recommendation": previous.get("readiness_recommendation"),
        "current_readiness_recommendation": metrics.get("readiness_recommendation"),
        "previous_tokens_with_placeholder_context_count": (
            (previous.get("structural_summary") or {}).get("tokens_with_placeholder_context_count")
        ),
        "current_tokens_with_placeholder_context_count": (
            (metrics.get("structural_summary") or {}).get("tokens_with_placeholder_context_count")
        ),
        "previous_stable_flow_pesukim": (
            (previous.get("generation_summary") or {}).get("stable_flow_pesukim")
        ),
        "current_stable_flow_pesukim": (
            (metrics.get("generation_summary") or {}).get("stable_flow_pesukim")
        ),
        "previous_shoresh_supported_pesukim": (
            ((previous.get("per_skill_support") or {}).get("shoresh") or {}).get("supported_pesukim")
        ),
        "current_shoresh_supported_pesukim": (
            ((metrics.get("per_skill_support") or {}).get("shoresh") or {}).get("supported_pesukim")
        ),
    }
    metrics["change_notes"] = list(args.change_note)
    metrics["remaining_blockers"] = list(
        (metrics.get("diagnostic_summary") or {}).get("blocker_categories") or []
    )
    write_json(output_path, metrics)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
