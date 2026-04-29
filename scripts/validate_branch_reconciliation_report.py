from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_MD = ROOT / "data/pipeline_rounds/branch_reconciliation_perek_3_4_baseline_report.md"
REPORT_JSON = ROOT / "data/pipeline_rounds/branch_reconciliation_perek_3_4_baseline_report.json"

REQUIRED_TOP_LEVEL_FIELDS = {
    "schema_version",
    "current_branch",
    "main_branch",
    "branches",
    "artifact_presence",
    "source_integrity",
    "validators",
    "proposed_merge_order",
    "go_no_go",
    "safety_boundaries",
    "next_commands",
}


def validate_branch_reconciliation_report() -> dict:
    errors: list[str] = []
    if not REPORT_MD.exists():
        errors.append(f"missing markdown report: {REPORT_MD.relative_to(ROOT).as_posix()}")
    if not REPORT_JSON.exists():
        errors.append(f"missing JSON report: {REPORT_JSON.relative_to(ROOT).as_posix()}")

    payload = {}
    if REPORT_JSON.exists():
        try:
            payload = json.loads(REPORT_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"JSON report is invalid: {error}")
        else:
            missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(payload))
            if missing:
                errors.append(f"JSON report missing top-level fields: {missing}")
            if not payload.get("proposed_merge_order"):
                errors.append("JSON report must include proposed merge order")
            if payload.get("safety_boundaries", {}).get("no_runtime_activation") is not True:
                errors.append("JSON report must confirm no runtime activation")

    if REPORT_MD.exists():
        text = REPORT_MD.read_text(encoding="utf-8")
        for phrase in [
            "Source integrity result",
            "Proposed merge-forward order",
            "No runtime activation",
            "No reviewed-bank promotion",
            "No student-facing content",
        ]:
            if phrase not in text:
                errors.append(f"Markdown report missing phrase: {phrase}")
        if "all branches are merged" in text.lower():
            errors.append("Markdown report must not claim branches are merged when this is only planned")

    return {"valid": not errors, "errors": errors}


def main() -> int:
    summary = validate_branch_reconciliation_report()
    if summary["valid"]:
        print("Branch reconciliation report validation passed.")
        return 0
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
