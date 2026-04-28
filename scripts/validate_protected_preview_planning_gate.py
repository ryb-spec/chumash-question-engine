from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "protected_preview_planning_gate"
REPORTS = BASE / "reports"
README = BASE / "README.md"
TSV = BASE / "bereishis_perek_1_first_protected_preview_planning_gate.tsv"
PACKET = REPORTS / "bereishis_perek_1_first_protected_preview_planning_gate_yossi_review_packet.md"
SUMMARY = REPORTS / "bereishis_perek_1_first_protected_preview_planning_gate_report.md"
EXCLUDED = REPORTS / "bereishis_perek_1_first_protected_preview_planning_gate_excluded_report.md"
APPLIED = REPORTS / "bereishis_perek_1_first_protected_preview_planning_gate_yossi_review_applied.md"
READINESS = REPORTS / "bereishis_perek_1_first_protected_preview_candidate_readiness_report.md"
CONTROLLED = ROOT / "data" / "controlled_draft_generation" / "bereishis_perek_1_first_controlled_draft.tsv"

REQUIRED_COLUMNS = {
    "preview_gate_candidate_id", "draft_item_id", "pre_generation_review_id", "ref", "hebrew_token", "hebrew_phrase", "approved_family", "draft_prompt", "answer_choices", "expected_answer", "correct_answer", "explanation", "source_evidence_note", "draft_review_status", "protected_preview_gate_review_status", "hebrew_rendering_review_status", "answer_key_review_status", "distractor_review_status", "context_display_review_status", "preview_gate_candidate_status", "protected_preview_candidate_planning_allowed", "protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed", "yossi_preview_gate_decision", "yossi_preview_gate_notes", "cautions",
}
STATUS_FIELDS = {"protected_preview_gate_review_status", "hebrew_rendering_review_status", "answer_key_review_status", "distractor_review_status", "context_display_review_status"}
SAFETY_FIELDS = {"protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed"}
FORBIDDEN_PHRASES = {"reviewed_bank_ready", "runtime_ready", "student_facing", "approved_for_reviewed_bank", "approved_for_runtime", "approved_for_student_facing", "approved_for_preview", "protected_preview_ready"}
EXCLUDED_DRAFT_IDS = {"cdraft_b1_016"}
ET = "\u05d0\u05ea"
HIBDIL = "\u05d4\u05d1\u05d3\u05d9\u05dc"
BDL = "\u05d1\u05d3\u05dc"
CHAYAH = "\u05d7\u05d9\u05d4"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return reader.fieldnames or [], list(reader)


def has_hebrew(value: str) -> bool:
    return any("\u0590" <= char <= "\u05ff" for char in value)


def contains_forbidden_phrase(text: str, phrase: str) -> bool:
    for line in text.lower().splitlines():
        if phrase not in line:
            continue
        if any(marker in line for marker in ("not ", "no ", "false", "closed", "does not", "before any", "still require")):
            continue
        return True
    return False


def validate_protected_preview_planning_gate() -> dict[str, object]:
    errors: list[str] = []
    paths = (README, TSV, PACKET, SUMMARY, EXCLUDED, APPLIED, READINESS, CONTROLLED)
    for path in paths:
        if not path.exists():
            errors.append(f"missing artifact: {rel(path)}")
    if errors:
        return {"valid": False, "errors": errors}

    fields, rows = read_tsv(TSV)
    if missing := sorted(REQUIRED_COLUMNS - set(fields)):
        errors.append(f"planning gate TSV missing columns: {missing}")
    if len(rows) != 18:
        errors.append(f"planning gate TSV must contain exactly 18 rows; found {len(rows)}")

    _, controlled_rows = read_tsv(CONTROLLED)
    controlled = {row["draft_item_id"]: row for row in controlled_rows}
    family_counts = Counter(row.get("approved_family", "") for row in rows)
    decision_counts = Counter(row.get("yossi_preview_gate_decision", "") for row in rows)
    ids = {row.get("draft_item_id", "") for row in rows}
    if ids & EXCLUDED_DRAFT_IDS:
        errors.append("cdraft_b1_016 must not be included")
    if decision_counts.get("approve_for_protected_preview_candidate", 0) != 18:
        errors.append("all 18 rows must be approve_for_protected_preview_candidate")
    if set(decision_counts) - {"approve_for_protected_preview_candidate"}:
        errors.append(f"unexpected preview-gate decisions: {sorted(set(decision_counts) - {'approve_for_protected_preview_candidate'})}")

    for row in rows:
        row_id = row.get("preview_gate_candidate_id", "unknown")
        draft_id = row.get("draft_item_id", "")
        source = controlled.get(draft_id, {})
        if source.get("draft_review_status") not in {"yossi_draft_approved", "yossi_draft_approved_after_revision"}:
            errors.append(f"{row_id} links to non-approved controlled draft row {draft_id}")
        if source.get("yossi_draft_decision") != "approve_draft_item":
            errors.append(f"{row_id} source draft decision must be approve_draft_item")
        if row.get("approved_family") == "basic_verb_form_recognition":
            errors.append(f"{row_id} must not include verb-form row")
        if row.get("hebrew_token") in {ET, HIBDIL, BDL, CHAYAH}:
            errors.append(f"{row_id} includes explicitly excluded Hebrew token")
        if row.get("preview_gate_candidate_status") != "yossi_approved_for_protected_preview_candidate_planning":
            errors.append(f"{row_id} must have planning-only approved status")
        if row.get("protected_preview_candidate_planning_allowed") != "true":
            errors.append(f"{row_id} must allow candidate planning only")
        for field in STATUS_FIELDS:
            if row.get(field) != "needs_yossi_review":
                errors.append(f"{row_id} {field} must be needs_yossi_review")
        for field in SAFETY_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{row_id} {field} must remain false")
        if row.get("yossi_preview_gate_decision") != "approve_for_protected_preview_candidate":
            errors.append(f"{row_id} Yossi decision must be approve_for_protected_preview_candidate")
        if "not protected-preview release approval" not in row.get("yossi_preview_gate_notes", ""):
            errors.append(f"{row_id} notes must negate protected-preview release approval")
        if not has_hebrew(row.get("hebrew_token", "")) or not has_hebrew(row.get("hebrew_phrase", "")):
            errors.append(f"{row_id} must include real Hebrew token and phrase")
        if any("??" in row.get(field, "") for field in REQUIRED_COLUMNS if field in row):
            errors.append(f"{row_id} must not contain placeholder Hebrew corruption")

    text = "\n".join(path.read_text(encoding="utf-8") for path in (README, PACKET, SUMMARY, EXCLUDED, APPLIED, READINESS))
    for phrase in ("does not approve protected-preview use", "not protected-preview release approval", "18", "candidate-readiness", "source-only", ET, HIBDIL, BDL, CHAYAH):
        if phrase not in text:
            errors.append(f"required planning-gate phrase missing: {phrase!r}")
    if "??" in text or "????" in text:
        errors.append("planning-gate reports must not contain placeholder Hebrew corruption")
    for phrase in FORBIDDEN_PHRASES:
        if contains_forbidden_phrase(text, phrase):
            errors.append(f"forbidden release approval phrase appears without clear negation: {phrase}")
    readme = README.read_text(encoding="utf-8")
    for path in (TSV, PACKET, SUMMARY, EXCLUDED, APPLIED, READINESS):
        if rel(path) not in readme:
            errors.append(f"README must link {rel(path)}")

    return {"valid": not errors, "errors": errors, "row_count": len(rows), "family_counts": dict(family_counts), "decision_counts": dict(decision_counts)}


def main() -> int:
    summary = validate_protected_preview_planning_gate()
    if summary["valid"]:
        print("Protected-preview planning gate validation passed.")
        print(f"Rows: {summary['row_count']}")
        print(f"Family counts: {summary['family_counts']}")
        print(f"Decision counts: {summary['decision_counts']}")
        return 0
    print("Protected-preview planning gate validation failed:")
    for error in summary["errors"]:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
