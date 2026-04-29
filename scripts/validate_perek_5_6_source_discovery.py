from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISCOVERY_DIR = ROOT / "data" / "gate_2_source_discovery"
REPORT_DIR = DISCOVERY_DIR / "reports"
PIPELINE_DIR = ROOT / "data" / "pipeline_rounds"

REPORT = REPORT_DIR / "bereishis_perek_5_6_source_discovery_report.md"
INVENTORY = DISCOVERY_DIR / "bereishis_perek_5_6_review_only_safe_candidate_inventory.tsv"
EXCLUDED = REPORT_DIR / "bereishis_perek_5_6_excluded_risk_lanes.md"
DUPLICATES = REPORT_DIR / "bereishis_perek_5_6_duplicate_session_balance_warnings.md"
STATUS = REPORT_DIR / "bereishis_perek_5_6_source_discovery_status_index.md"
SUMMARY = REPORT_DIR / "bereishis_perek_5_6_source_discovery_summary_2026_04_29.json"
PROMPT = PIPELINE_DIR / "prompts" / "bereishis_perek_5_6_review_checklist_prompt.md"
GATE = PIPELINE_DIR / "bereishis_perek_5_6_source_discovery_gate_2026_04_29.md"

FALSE_COLUMNS = [
    "runtime_allowed",
    "reviewed_bank_allowed",
    "protected_preview_allowed",
    "student_facing_allowed",
    "perek_5_activated",
    "perek_6_activated",
]
FALSE_SUMMARY_FIELDS = [
    "perek_5_activated",
    "perek_6_activated",
    "runtime_scope_widened",
    "reviewed_bank_promoted",
    "protected_preview_packet_created",
    "student_facing_created",
    "source_truth_changed",
]
FORBIDDEN_COMPACT = [
    "runtime_allowed=true",
    "reviewed_bank_allowed=true",
    "protected_preview_allowed=true",
    "student_facing_allowed=true",
]
FORBIDDEN_TEXT = [
    "promoted_to_runtime",
    "approved_for_runtime",
    "Perek 5 is runtime-active",
    "Perek 6 is runtime-active",
    "Perek 5 runtime activation is allowed",
    "Perek 6 runtime activation is allowed",
]


def _fail(message: str) -> None:
    raise SystemExit(message)


def _read(path: Path) -> str:
    if not path.exists():
        _fail(f"Missing required artifact: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict:
    try:
        return json.loads(_read(path))
    except json.JSONDecodeError as exc:
        _fail(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def _read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        _fail(f"Missing required artifact: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _scan_forbidden(paths: list[Path]) -> None:
    for path in paths:
        text = _read(path)
        compact = text.replace(" ", "").lower()
        lowered = text.lower()
        for token in FORBIDDEN_COMPACT:
            if token in compact:
                _fail(f"Forbidden positive gate value in {path.relative_to(ROOT)}: {token}")
        for token in FORBIDDEN_TEXT:
            if token.lower() in lowered:
                _fail(f"Forbidden runtime/promotion claim in {path.relative_to(ROOT)}: {token}")


def validate() -> None:
    required = [REPORT, INVENTORY, EXCLUDED, DUPLICATES, STATUS, SUMMARY, PROMPT, GATE]
    for path in required:
        _read(path)

    rows = _read_tsv(INVENTORY)
    for row in rows:
        candidate_id = row.get("candidate_id", "")
        perek = row.get("perek", "")
        if perek not in {"5", "6"}:
            _fail(f"Candidate {candidate_id} has invalid perek: {perek}")
        if perek == "5" and not candidate_id.startswith("g2srcdisc_p5_"):
            _fail(f"Perek 5 candidate has invalid ID: {candidate_id}")
        if perek == "6" and not candidate_id.startswith("g2srcdisc_p6_"):
            _fail(f"Perek 6 candidate has invalid ID: {candidate_id}")
        if re.search(r"g2srcdisc_p([789]|\d{2,})_", candidate_id):
            _fail(f"No Perek 7+ candidates allowed: {candidate_id}")
        for column in FALSE_COLUMNS:
            if row.get(column) != "false":
                _fail(f"Candidate {candidate_id} must keep {column}=false.")

    summary = _load_json(SUMMARY)
    for field in FALSE_SUMMARY_FIELDS:
        if summary.get(field) is not False:
            _fail(f"Summary JSON must keep {field}=false.")
    if summary.get("candidate_count") != len(rows):
        _fail("Summary candidate_count must match TSV row count.")
    p5_count = sum(1 for row in rows if row.get("perek") == "5")
    p6_count = sum(1 for row in rows if row.get("perek") == "6")
    if summary.get("perek_5_candidate_count") != p5_count:
        _fail("Summary perek_5_candidate_count mismatch.")
    if summary.get("perek_6_candidate_count") != p6_count:
        _fail("Summary perek_6_candidate_count mismatch.")
    if summary.get("protected_preview_packet_created") is not False:
        _fail("Summary must not allow protected-preview packet creation.")

    if not rows:
        report = _read(REPORT)
        status = _read(STATUS)
        if "empty inventory" not in report.lower() or "blocked" not in status.lower():
            _fail("Empty inventory must be explained in report and status index.")

    status_text = _read(STATUS)
    required_status = (
        "Perek 5-6 source discovery only. No runtime activation, no active scope expansion, "
        "no reviewed-bank promotion, no protected-preview packet, and no student-facing content."
    )
    if required_status not in status_text:
        _fail("Status index missing explicit source-discovery-only safety status.")

    prompt = _read(PROMPT)
    for phrase in [
        "compressed teacher-review checklist only",
        "Keep all candidates review-only and all gates false",
        "create a protected-preview packet",
        "create student-facing content",
        "change source truth",
    ]:
        if phrase not in prompt:
            _fail(f"Review-checklist prompt missing required guardrail: {phrase}")

    _scan_forbidden(required)
    print("Perek 5-6 source discovery validation passed.")


if __name__ == "__main__":
    validate()
