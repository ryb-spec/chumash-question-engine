from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RESULTS_MD = ROOT / "data/pipeline_rounds/perek_3_short_repilot_results_2026_04_29.md"
RESULTS_JSON = ROOT / "data/pipeline_rounds/perek_3_short_repilot_results_2026_04_29.json"
LEAK_REPORT = ROOT / "data/pipeline_rounds/perek_3_short_repilot_scope_leak_report_2026_04_29.md"
PEREK_4_GATE_MD = ROOT / "data/pipeline_rounds/perek_3_short_repilot_to_perek_4_ready_gate_2026_04_29.md"
PEREK_4_GATE_JSON = ROOT / "data/pipeline_rounds/perek_3_short_repilot_to_perek_4_ready_gate_2026_04_29.json"

REQUIRED_FILES = (
    RESULTS_MD,
    RESULTS_JSON,
    LEAK_REPORT,
    PEREK_4_GATE_MD,
    PEREK_4_GATE_JSON,
)

FORBIDDEN_PATTERNS = (
    "runtime_allowed=true",
    "runtime_allowed: true",
    "approved_for_runtime",
    "promoted_to_runtime",
    '"perek_4_activated": true',
    '"runtime_scope_widened": true',
    '"fake_data_created": true',
    "Perek 4 is active",
    "Perek 4 is activated",
    "activate Perek 4 now",
    "invented observation",
    "synthetic observation",
)


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path, errors: list[str]) -> dict:
    try:
        payload = json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"{_relative(path)} is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{_relative(path)} must be a JSON object")
        return {}
    return payload


def _require_bool(payload: dict, key: str, expected: bool, errors: list[str], path: Path) -> None:
    if payload.get(key) is not expected:
        errors.append(f"{_relative(path)} must set {key} to {expected}")


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")
    if errors:
        return {"ok": False, "errors": errors}

    results = _load_json(RESULTS_JSON, errors)
    gate = _load_json(PEREK_4_GATE_JSON, errors)

    for key in (
        "raw_logs_used",
        "unverified_phrase_translation_served",
        "old_prefix_prompt_served",
    ):
        _require_bool(results, key, True, errors, RESULTS_JSON)
    for key in (
        "raw_logs_manually_modified",
        "perek_4_content_served",
        "ashis_shis_beginner_shoresh_served",
        "ready_for_clean_short_repilot_closure",
        "ready_for_full_perek_3_closure",
        "ready_for_runtime_expansion",
        "ready_for_reviewed_bank_promotion",
        "perek_4_activated",
        "perek_4_runtime_activation_allowed",
        "perek_4_reviewed_bank_promotion_allowed",
        "perek_4_teacher_review_packet_ready_from_this_evidence",
        "runtime_scope_widened",
        "question_generation_changed",
        "reviewed_bank_promoted",
        "source_truth_changed",
        "fake_data_created",
    ):
        _require_bool(results, key, False, errors, RESULTS_JSON)

    if results.get("answered_attempts_reviewed") != 8:
        errors.append("short re-pilot results must record 8 answered attempts reviewed")
    if results.get("excluded_content_scope_leak_count") != 2:
        errors.append("short re-pilot results must record 2 excluded-content scope leaks")
    if results.get("wording_regression_event_count") != 1:
        errors.append("short re-pilot results must record 1 old-prefix wording event")

    findings = results.get("findings")
    if not isinstance(findings, list):
        errors.append("short re-pilot results JSON must include a findings list")
    else:
        finding_ids = {str(item.get("finding_id")) for item in findings if isinstance(item, dict)}
        for required in (
            "p3_short_repilot_leak_001",
            "p3_short_repilot_leak_002",
            "p3_short_repilot_wording_001",
        ):
            if required not in finding_ids:
                errors.append(f"short re-pilot results missing finding {required}")

    for key in (
        "clean_short_repilot_closure",
        "perek_3_full_closure_go",
        "perek_3_runtime_expansion_go",
        "perek_4_teacher_review_packet_go",
        "perek_4_activated",
        "perek_4_runtime_activation_go",
        "perek_4_reviewed_bank_promotion_go",
        "perek_4_student_facing_go",
        "runtime_scope_widened",
        "reviewed_bank_promoted",
        "source_truth_changed",
        "fake_data_created",
    ):
        _require_bool(gate, key, False, errors, PEREK_4_GATE_JSON)
    _require_bool(gate, "scope_leaks_detected", True, errors, PEREK_4_GATE_JSON)

    results_text = _read_text(RESULTS_MD)
    leak_text = _read_text(LEAK_REPORT)
    gate_text = _read_text(PEREK_4_GATE_MD)
    for required in (
        "raw JSONL files are dirty worktree evidence",
        "Perek 4 content served: no",
        "two phrase_translation items were served",
        "What is the prefix in בְּאִשְׁתּוֹ?",
        "Ready for full Perek 3 closure: no",
    ):
        if required not in results_text:
            errors.append(f"results report missing required phrase: {required}")
    for required in (
        "Manual-only scope control did not produce a fully clean short re-pilot.",
        "phrase_translation",
        "וְאֵיבָה אָשִׁית",
        "Perek 4 content was not observed",
    ):
        if required not in leak_text:
            errors.append(f"scope leak report missing required phrase: {required}")
    for required in (
        "Perek 4 runtime activation",
        "No-go",
        "Yossi should decide",
        "No reviewed-bank promotion",
    ):
        if required not in gate_text:
            errors.append(f"Perek 4 ready gate missing required phrase: {required}")

    for path in REQUIRED_FILES:
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")

    return {"ok": not errors, "errors": errors}


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 3 short re-pilot results validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
