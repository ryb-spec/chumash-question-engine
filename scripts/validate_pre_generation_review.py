from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "data" / "pre_generation_review"
REPORTS_DIR = BASE_DIR / "reports"
README_PATH = BASE_DIR / "README.md"
REVIEW_TSV_PATH = BASE_DIR / "bereishis_perek_1_first_batch_pre_generation_review.tsv"
REVIEW_MD_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_pre_generation_yossi_review_sheet.md"
REVIEW_CSV_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_pre_generation_yossi_review_sheet.csv"
REPORT_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_pre_generation_review_report.md"
APPLIED_REPORT_PATH = REPORTS_DIR / "bereishis_perek_1_first_batch_pre_generation_yossi_review_applied.md"
CONTROLLED_DRAFT_TSV_PATH = ROOT / "data" / "controlled_draft_generation" / "bereishis_perek_1_first_controlled_draft.tsv"
SOURCE_TSV_PATH = ROOT / "data" / "template_skeleton_planning" / "bereishis_perek_1_first_batch_exact_template_wording_planning.tsv"

REQUIRED_COLUMNS = {
    "pre_generation_review_id", "exact_template_candidate_id", "skeleton_candidate_id", "input_candidate_id", "audit_id", "ref", "hebrew_token", "hebrew_phrase", "approved_family", "non_student_facing_wording_pattern", "required_placeholders", "family_policy_status", "exact_wording_review_status", "answer_key_language_review_status", "distractor_constraints_review_status", "context_display_review_status", "hebrew_rendering_review_status", "protected_preview_gate_review_status", "row_level_generation_status", "final_question_allowed", "answer_choices_allowed", "answer_key_allowed", "distractors_allowed", "protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed", "row_level_cautions", "yossi_exact_wording_decision", "yossi_answer_key_decision", "yossi_distractor_decision", "yossi_context_display_decision", "yossi_hebrew_rendering_decision", "yossi_protected_preview_gate_decision", "yossi_notes",
}
REVIEW_STATUS_FIELDS = {"exact_wording_review_status", "answer_key_language_review_status", "distractor_constraints_review_status", "context_display_review_status", "hebrew_rendering_review_status", "protected_preview_gate_review_status"}
SAFETY_FIELDS = {"final_question_allowed", "answer_choices_allowed", "answer_key_allowed", "distractors_allowed", "protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed"}
YOSSI_DECISION_FIELDS = {"yossi_exact_wording_decision", "yossi_answer_key_decision", "yossi_distractor_decision", "yossi_context_display_decision", "yossi_hebrew_rendering_decision", "yossi_protected_preview_gate_decision"}
FORBIDDEN_CONTENT_COLUMNS = {"question_text", "prompt", "prompt_text", "student_prompt", "answer_options", "correct_answer", "distractor_options", "protected_preview_content"}
FORBIDDEN_PHRASES = {"question_ready", "protected_preview_ready", "reviewed_bank_ready", "runtime_ready", "student_facing", "approved_for_questions", "approved_for_preview"}
ALLOWED_FAMILIES = {"vocabulary_meaning", "basic_noun_recognition", "direct_object_marker_recognition", "shoresh_identification"}
DIRECT_APPROVAL_IDS = {
    "preg_b1_002", "preg_b1_003", "preg_b1_004", "preg_b1_005", "preg_b1_006", "preg_b1_007", "preg_b1_008", "preg_b1_009", "preg_b1_011", "preg_b1_012", "preg_b1_013", "preg_b1_014", "preg_b1_015", "preg_b1_016", "preg_b1_017", "preg_b1_018", "preg_b1_019", "preg_b1_020", "preg_b1_023",
}
REVISION_IDS = {"preg_b1_001", "preg_b1_010", "preg_b1_021", "preg_b1_022", "preg_b1_024"}
ET = "\u05d0\u05ea"
HIBDIL = "\u05d4\u05d1\u05d3\u05d9\u05dc"
BDL = "\u05d1\u05d3\u05dc"
HAMAYIM = "\u05d4\u05de\u05d9\u05dd"
HAADAMAH = "\u05d4\u05d0\u05d3\u05de\u05d4"
HAARETZ = "\u05d4\u05d0\u05e8\u05e5"


def repo_relative(path: Path) -> str:
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
        if any(marker in line for marker in ("forbidden", "not ", "no ", "nothing marked", "does not", "must not", "remain closed", "remain blocked", "blocked", "false", "not protected-preview")):
            continue
        return True
    return False


def validate_pre_generation_review() -> dict[str, object]:
    errors: list[str] = []
    required_paths = (README_PATH, REVIEW_TSV_PATH, REVIEW_MD_PATH, REVIEW_CSV_PATH, REPORT_PATH, APPLIED_REPORT_PATH, SOURCE_TSV_PATH, CONTROLLED_DRAFT_TSV_PATH)
    for path in required_paths:
        if not path.exists():
            errors.append(f"required pre-generation review artifact missing: {repo_relative(path)}")
    if errors:
        return {"valid": False, "errors": errors}

    fields, rows = read_tsv(REVIEW_TSV_PATH)
    missing = sorted(REQUIRED_COLUMNS - set(fields))
    if missing:
        errors.append(f"pre-generation review TSV missing columns: {missing}")
    forbidden_columns = sorted(FORBIDDEN_CONTENT_COLUMNS & set(fields))
    if forbidden_columns:
        errors.append(f"pre-generation review TSV must not include generated-content columns: {forbidden_columns}")
    if len(rows) != 24:
        errors.append(f"pre-generation review TSV must contain exactly 24 rows; found {len(rows)}")

    source_fields, source_rows = read_tsv(SOURCE_TSV_PATH)
    source_ids = {row.get("exact_template_candidate_id") for row in source_rows}
    seen_ids: set[str] = set()
    decision_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    for row in rows:
        row_id = row.get("pre_generation_review_id", "unknown")
        if row_id in seen_ids:
            errors.append(f"duplicate pre-generation review id: {row_id}")
        seen_ids.add(row_id)
        if row.get("exact_template_candidate_id") not in source_ids:
            errors.append(f"{row_id} links to missing exact-template planning row")
        if row.get("approved_family") not in ALLOWED_FAMILIES:
            errors.append(f"{row_id} has disallowed family {row.get('approved_family')!r}")
        expected_decision = "approve_for_controlled_draft_generation" if row_id in DIRECT_APPROVAL_IDS else "approve_with_revision"
        expected_status = "approved_for_controlled_draft_generation" if row_id in DIRECT_APPROVAL_IDS else "blocked_pending_revision"
        for field in REVIEW_STATUS_FIELDS | YOSSI_DECISION_FIELDS:
            if row.get(field) != expected_decision:
                errors.append(f"{row_id} {field} must be {expected_decision}")
        if row.get("row_level_generation_status") != expected_status:
            errors.append(f"{row_id} row_level_generation_status must be {expected_status}")
        decision_counts[row.get("yossi_exact_wording_decision", "")] += 1
        status_counts[row.get("row_level_generation_status", "")] += 1
        for field in SAFETY_FIELDS:
            if row.get(field) != "false":
                errors.append(f"{row_id} {field} must remain false")
        if not row.get("yossi_notes"):
            errors.append(f"{row_id} yossi_notes must be populated")
        if not has_hebrew(row.get("hebrew_token", "")) or not has_hebrew(row.get("hebrew_phrase", "")):
            errors.append(f"{row_id} Hebrew token/phrase must contain real Hebrew")
        if "??" in row.get("hebrew_token", "") or "??" in row.get("hebrew_phrase", "") or "??" in row.get("row_level_cautions", ""):
            errors.append(f"{row_id} must not contain placeholder Hebrew corruption")
        if row.get("approved_family") == "direct_object_marker_recognition" and ET not in row.get("row_level_cautions", ""):
            errors.append(f"{row_id} must preserve {ET} function caution")
        if row.get("input_candidate_id") == "ppplan_b1_024" and (HIBDIL not in row.get("row_level_cautions", "") or BDL not in row.get("row_level_cautions", "")):
            errors.append(f"{row_id} must preserve {HIBDIL} / {BDL} shoresh caution")
        if row_id in {"preg_b1_001", "preg_b1_010"} and "base meaning" not in row.get("yossi_notes", ""):
            errors.append(f"{row_id} must preserve article/base meaning revision note")

    expected_counts = {
        "approve_for_controlled_draft_generation": 19,
        "approve_with_revision": 5,
        "needs_follow_up": 0,
        "block_for_now": 0,
        "source_only": 0,
    }
    for decision, expected_count in expected_counts.items():
        if decision_counts.get(decision, 0) != expected_count:
            errors.append(f"decision count for {decision} must be {expected_count}; found {decision_counts.get(decision, 0)}")

    draft_fields, draft_rows = read_tsv(CONTROLLED_DRAFT_TSV_PATH)
    draft_ids = {row.get("pre_generation_review_id") for row in draft_rows}
    if draft_ids != DIRECT_APPROVAL_IDS:
        errors.append("controlled draft layer must link exactly to the 19 direct-approved rows")
    if draft_ids & REVISION_IDS:
        errors.append("controlled draft layer must not include revision-required rows")

    if not REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append(f"review CSV must be UTF-8-BOM: {repo_relative(REVIEW_CSV_PATH)}")

    text_blob = "\n".join(path.read_text(encoding="utf-8") for path in (README_PATH, REVIEW_MD_PATH, REPORT_PATH, APPLIED_REPORT_PATH))
    for phrase in (ET, HIBDIL, BDL, HAMAYIM, HAADAMAH, HAARETZ, "Approved for controlled draft generation: 19", "Approved with revision: 5"):
        if phrase not in text_blob:
            errors.append(f"required pre-generation review phrase missing: {phrase!r}")
    if "??" in text_blob or "????" in text_blob:
        errors.append("pre-generation reports must not contain placeholder Hebrew corruption")
    for phrase in FORBIDDEN_PHRASES:
        if contains_forbidden_phrase(text_blob, phrase):
            errors.append(f"forbidden approval phrase appears without clear negation: {phrase}")

    readme_text = README_PATH.read_text(encoding="utf-8")
    for path in (REVIEW_TSV_PATH, REVIEW_MD_PATH, REVIEW_CSV_PATH, REPORT_PATH, APPLIED_REPORT_PATH):
        if repo_relative(path) not in readme_text:
            errors.append(f"README must link {repo_relative(path)}")

    return {"valid": not errors, "errors": errors, "row_count": len(rows), "decision_counts": dict(decision_counts), "status_counts": dict(status_counts)}


def main() -> int:
    summary = validate_pre_generation_review()
    if summary["valid"]:
        print("Pre-generation review validation passed.")
        print(f"Rows: {summary['row_count']}")
        print(f"Decision counts: {summary['decision_counts']}")
        return 0
    print("Pre-generation review validation failed:")
    for error in summary["errors"]:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
