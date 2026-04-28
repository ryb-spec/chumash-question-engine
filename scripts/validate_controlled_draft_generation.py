from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "controlled_draft_generation"
REPORTS = BASE / "reports"
README = BASE / "README.md"
TSV = BASE / "bereishis_perek_1_first_controlled_draft.tsv"
PACKET = REPORTS / "bereishis_perek_1_first_controlled_draft_teacher_review_packet.md"
GEN_REPORT = REPORTS / "bereishis_perek_1_first_controlled_draft_generation_report.md"
SKIP_REPORT = REPORTS / "bereishis_perek_1_first_controlled_draft_skipped_revision_required_report.md"
APPLIED_REPORT = REPORTS / "bereishis_perek_1_first_controlled_draft_yossi_review_applied.md"
READINESS_REPORT = REPORTS / "bereishis_perek_1_first_controlled_draft_preview_planning_readiness_report.md"
REVISION_REPORT = REPORTS / "bereishis_perek_1_first_controlled_draft_revision_resolution_report.md"
PREGEN_TSV = ROOT / "data" / "pre_generation_review" / "bereishis_perek_1_first_batch_pre_generation_review.tsv"

DIRECT_PREGEN_IDS = {
    "preg_b1_002", "preg_b1_003", "preg_b1_004", "preg_b1_005", "preg_b1_006", "preg_b1_007", "preg_b1_008", "preg_b1_009", "preg_b1_011", "preg_b1_012", "preg_b1_013", "preg_b1_014", "preg_b1_015", "preg_b1_016", "preg_b1_017", "preg_b1_018", "preg_b1_019", "preg_b1_020", "preg_b1_023",
}
SKIPPED_PREGEN_IDS = {"preg_b1_001", "preg_b1_010", "preg_b1_021", "preg_b1_022", "preg_b1_024"}
REVISED_DRAFT_IDS = {"cdraft_b1_001", "cdraft_b1_004", "cdraft_b1_006", "cdraft_b1_008"}
SOURCE_ONLY_DRAFT_ID = "cdraft_b1_016"
EXPECTED_DECISION_COUNTS = {"approve_draft_item": 18, "approve_with_revision": 0, "needs_follow_up": 0, "reject_item": 0, "source_only": 1}
REQUIRED_COLUMNS = {
    "draft_item_id", "pre_generation_review_id", "exact_template_candidate_id", "input_candidate_id", "audit_id", "ref", "approved_family", "hebrew_token", "hebrew_phrase", "draft_prompt", "expected_answer", "answer_choices", "correct_answer", "distractor_notes", "explanation", "source_evidence_note", "draft_review_status", "answer_key_review_status", "distractor_review_status", "hebrew_rendering_review_status", "protected_preview_gate_review_status", "protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed", "cautions", "yossi_draft_decision", "yossi_draft_notes",
}
REMAINING_REVIEW_STATUS_FIELDS = {"answer_key_review_status", "distractor_review_status", "hebrew_rendering_review_status", "protected_preview_gate_review_status"}
SAFETY_FIELDS = {"protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed"}
FORBIDDEN_PHRASES = {"protected_preview_ready", "reviewed_bank_ready", "runtime_ready", "student_facing", "approved_for_preview", "approved_for_reviewed_bank", "approved_for_runtime"}
ET = "\u05d0\u05ea"
HIBDIL = "\u05d4\u05d1\u05d3\u05d9\u05dc"
BDL = "\u05d1\u05d3\u05dc"
HAMAYIM = "\u05d4\u05de\u05d9\u05dd"
HAADAMAH = "\u05d4\u05d0\u05d3\u05de\u05d4"
RAKIA = "\u05e8\u05e7\u05d9\u05e2"
MEOROT = "\u05de\u05d0\u05d5\u05e8\u05d5\u05ea"
SHERETZ = "\u05e9\u05e8\u05e5"
BEHEMAH = "\u05d1\u05d4\u05de\u05d4"
CHAYAH = "\u05d7\u05d9\u05d4"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return reader.fieldnames or [], list(reader)


def has_hebrew(value: str) -> bool:
    return any("\u0590" <= c <= "\u05ff" for c in value)


def contains_forbidden_phrase(text: str, phrase: str) -> bool:
    for line in text.lower().splitlines():
        if phrase in line and not any(marker in line for marker in ("not ", "no ", "false", "closed", "requires", "teacher-review-only")):
            return True
    return False


def validate_controlled_draft_generation() -> dict[str, object]:
    errors: list[str] = []
    paths = (README, TSV, PACKET, GEN_REPORT, SKIP_REPORT, APPLIED_REPORT, READINESS_REPORT, REVISION_REPORT, PREGEN_TSV)
    for path in paths:
        if not path.exists():
            errors.append(f"missing artifact: {rel(path)}")
    if errors:
        return {"valid": False, "errors": errors}

    fields, rows = read_tsv(TSV)
    if missing := sorted(REQUIRED_COLUMNS - set(fields)):
        errors.append(f"controlled draft TSV missing columns: {missing}")
    if len(rows) != 19:
        errors.append(f"controlled draft TSV must contain exactly 19 rows; found {len(rows)}")

    _, pregen_rows = read_tsv(PREGEN_TSV)
    pregen = {row["pre_generation_review_id"]: row for row in pregen_rows}
    source_ids = {row.get("pre_generation_review_id") for row in rows}
    if source_ids != DIRECT_PREGEN_IDS:
        errors.append("controlled draft rows must link exactly to the 19 controlled-draft-approved pre-generation rows")
    if source_ids & SKIPPED_PREGEN_IDS:
        errors.append("skipped pre-generation revision rows must not appear in controlled draft TSV")

    decision_counts = Counter(row.get("yossi_draft_decision", "") for row in rows)
    status_counts = Counter(row.get("draft_review_status", "") for row in rows)
    family_counts = Counter(row.get("approved_family", "") for row in rows)
    for decision, expected in EXPECTED_DECISION_COUNTS.items():
        if decision_counts.get(decision, 0) != expected:
            errors.append(f"expected {expected} rows with {decision}; found {decision_counts.get(decision, 0)}")
    if set(decision_counts) - set(EXPECTED_DECISION_COUNTS):
        errors.append(f"unexpected Yossi draft decisions: {sorted(set(decision_counts) - set(EXPECTED_DECISION_COUNTS))}")
    if status_counts.get("yossi_draft_approved", 0) + status_counts.get("yossi_draft_approved_after_revision", 0) != 18:
        errors.append("expected 18 rows with approved draft statuses")
    if status_counts.get("source_only_not_for_preview_planning", 0) != 1:
        errors.append("expected 1 source_only_not_for_preview_planning row")
    if status_counts.get("revision_required_before_preview_planning", 0) or status_counts.get("needs_follow_up", 0):
        errors.append("no rows may remain revision-required or needs-follow-up")

    for row in rows:
        row_id = row.get("draft_item_id", "")
        if row.get("approved_family") == "basic_verb_form_recognition":
            errors.append(f"{row_id} must not be verb-form")
        if pregen.get(row.get("pre_generation_review_id", ""), {}).get("yossi_exact_wording_decision") != "approve_for_controlled_draft_generation":
            errors.append(f"{row_id} source row is not controlled-draft approved")
        for field in ("draft_prompt", "expected_answer", "answer_choices", "correct_answer", "explanation", "source_evidence_note"):
            if not row.get(field):
                errors.append(f"{row_id} {field} must be populated")
        if row_id in REVISED_DRAFT_IDS:
            if row.get("yossi_draft_decision") != "approve_draft_item" or row.get("draft_review_status") != "yossi_draft_approved_after_revision":
                errors.append(f"{row_id} must be approved after revision")
        elif row_id == SOURCE_ONLY_DRAFT_ID:
            if row.get("yossi_draft_decision") != "source_only" or row.get("draft_review_status") != "source_only_not_for_preview_planning":
                errors.append(f"{row_id} must be source-only and excluded from preview planning")
        else:
            if row.get("yossi_draft_decision") != "approve_draft_item" or row.get("draft_review_status") != "yossi_draft_approved":
                errors.append(f"{row_id} must remain approved")
        for field in REMAINING_REVIEW_STATUS_FIELDS:
            if row.get(field) != "needs_yossi_review":
                errors.append(f"{row_id} {field} must remain needs_yossi_review")
        for field in SAFETY_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{row_id} {field} must remain false")
        if not has_hebrew(row.get("hebrew_token", "")) or not has_hebrew(row.get("hebrew_phrase", "")):
            errors.append(f"{row_id} must include real Hebrew token and phrase")
        if any("??" in row.get(field, "") for field in REQUIRED_COLUMNS if field in row):
            errors.append(f"{row_id} must not contain placeholder Hebrew corruption")

    by_id = {row["draft_item_id"]: row for row in rows}
    expected_revisions = {
        "cdraft_b1_001": "expanse / firmament",
        "cdraft_b1_004": "lights / luminaries",
        "cdraft_b1_006": "swarming creature / creeping creature",
        "cdraft_b1_008": "animal / beast / domesticated animal",
    }
    for row_id, phrase in expected_revisions.items():
        row = by_id.get(row_id, {})
        if phrase not in row.get("expected_answer", "") or phrase not in row.get("answer_choices", ""):
            errors.append(f"{row_id} must include revised answer-key wording: {phrase}")
    source_row = by_id.get(SOURCE_ONLY_DRAFT_ID, {})
    if CHAYAH not in source_row.get("yossi_draft_notes", "") or "noun/adjective/description" not in source_row.get("yossi_draft_notes", ""):
        errors.append("cdraft_b1_016 must preserve conservative chayah source-only note")

    text = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.suffix in {".md", ""})
    required_text = ("teacher-review", "Generated draft count: 19", "Skipped revision-required count: 5", "Revision-resolution report", "18 draft items", "source-only", ET, HIBDIL, BDL, HAMAYIM, HAADAMAH, RAKIA, "expanse / firmament", MEOROT, "lights / luminaries", SHERETZ, "swarming creature / creeping creature", BEHEMAH, "animal / beast / domesticated animal", CHAYAH, "noun/adjective/description")
    for phrase in required_text:
        if phrase not in text:
            errors.append(f"required controlled draft phrase missing: {phrase!r}")
    if "??" in text or "????" in text:
        errors.append("controlled draft reports must not contain placeholder Hebrew corruption")
    for phrase in FORBIDDEN_PHRASES:
        if contains_forbidden_phrase(text, phrase):
            errors.append(f"forbidden approval phrase appears without clear negation: {phrase}")

    readme_text = README.read_text(encoding="utf-8")
    for path in (TSV, PACKET, GEN_REPORT, SKIP_REPORT, APPLIED_REPORT, READINESS_REPORT, REVISION_REPORT):
        if rel(path) not in readme_text:
            errors.append(f"README must link {rel(path)}")

    return {"valid": not errors, "errors": errors, "row_count": len(rows), "family_counts": dict(family_counts), "decision_counts": dict(decision_counts), "status_counts": dict(status_counts)}


def main() -> int:
    summary = validate_controlled_draft_generation()
    if summary["valid"]:
        print("Controlled draft generation validation passed.")
        print(f"Rows: {summary['row_count']}")
        print(f"Family counts: {summary['family_counts']}")
        print(f"Decision counts: {summary['decision_counts']}")
        print(f"Status counts: {summary['status_counts']}")
        return 0
    print("Controlled draft generation validation failed:")
    for error in summary["errors"]:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
