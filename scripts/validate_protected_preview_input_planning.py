from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / "data" / "protected_preview_input_planning"
README_PATH = PLANNING_DIR / "README.md"
TSV_PATH = PLANNING_DIR / "bereishis_perek_1_first_input_candidate_planning.tsv"
REPORTS_DIR = PLANNING_DIR / "reports"
BALANCE_REPORT_PATH = REPORTS_DIR / "bereishis_perek_1_first_input_candidate_batch_balance_report.md"
PLANNING_REPORT_PATH = REPORTS_DIR / "bereishis_perek_1_first_input_candidate_planning_report.md"
REVIEW_MD_PATH = REPORTS_DIR / "bereishis_perek_1_first_input_candidate_yossi_review_sheet.md"
REVIEW_CSV_PATH = REPORTS_DIR / "bereishis_perek_1_first_input_candidate_yossi_review_sheet.csv"
APPLIED_REPORT_PATH = REPORTS_DIR / "bereishis_perek_1_first_input_candidate_yossi_review_applied.md"
SOURCE_PLANNING_CSV = (
    ROOT
    / "data"
    / "question_eligibility_audits"
    / "reports"
    / "bereishis_perek_1_approved_input_candidate_planning_sheet.csv"
)

ALLOWED_FAMILIES = {
    "vocabulary_meaning",
    "basic_noun_recognition",
    "direct_object_marker_recognition",
    "shoresh_identification",
}
REQUIRED_COLUMNS = {
    "input_candidate_id",
    "audit_id",
    "ref",
    "hebrew_token",
    "hebrew_phrase",
    "approved_family",
    "canonical_skill_id",
    "canonical_standard_anchor",
    "source_candidate_type",
    "risk_level",
    "risk_reasons",
    "required_template_family",
    "wording_policy_version",
    "teacher_wording_review_status",
    "answer_key_review_status",
    "distractor_review_status",
    "context_display_review_status",
    "hebrew_rendering_review_status",
    "protected_preview_candidate_status",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "runtime_allowed",
    "student_facing_allowed",
    "selection_reason",
    "notes",
    "yossi_input_planning_decision",
    "yossi_notes",
}
REVIEW_STATUS_FIELDS = {
    "teacher_wording_review_status",
    "answer_key_review_status",
    "distractor_review_status",
    "context_display_review_status",
    "hebrew_rendering_review_status",
}
SAFETY_GATE_FIELDS = {
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "runtime_allowed",
    "student_facing_allowed",
}
FORBIDDEN_COLUMNS = {
    "question",
    "question_text",
    "prompt",
    "prompt_text",
    "answer",
    "answer_choices",
    "answer_key",
    "correct_answer",
    "distractors",
}
BALANCE_REPORT_PHRASES = {
    "total selected input candidates",
    "count by family",
    "count by risk level",
    "count by perek/pasuk range",
    "duplicate hebrew tokens",
    "direct-object-marker inclusion reasons",
    "shoresh inclusion reasons",
}
FORBIDDEN_PHRASES = {
    "question_ready",
    "protected_preview_ready",
    "reviewed_bank_ready",
    "runtime_ready",
    "student_facing",
    "approved_for_questions",
    "approved_for_preview",
}


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_csv_sig(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_has_utf8_bom(path: Path) -> bool:
    with path.open("rb") as handle:
        return handle.read(3) == b"\xef\xbb\xbf"


def contains_placeholder_hebrew(value: str) -> bool:
    return "?" in value


def contains_forbidden_phrase(text: str, phrase: str) -> bool:
    for line in text.lower().splitlines():
        if phrase not in line:
            continue
        if (
            "forbidden" in line
            or "not " in line
            or "no " in line
            or "nothing marked " in line
            or "does not" in line
            or "must not" in line
            or "remain false" in line
            or "all gates remain closed" in line
            or "= false" in line
            or "_allowed" in line
        ):
            continue
        return True
    return False


def validate_protected_preview_input_planning() -> dict[str, object]:
    errors: list[str] = []
    required_paths = (
        README_PATH,
        TSV_PATH,
        BALANCE_REPORT_PATH,
        PLANNING_REPORT_PATH,
        REVIEW_MD_PATH,
        REVIEW_CSV_PATH,
        APPLIED_REPORT_PATH,
        SOURCE_PLANNING_CSV,
    )
    for path in required_paths:
        if not path.exists():
            errors.append(f"required protected-preview input-planning artifact missing: {repo_relative(path)}")
    if errors:
        return {"valid": False, "errors": errors}

    source_rows = read_csv_sig(SOURCE_PLANNING_CSV)
    source_by_audit_id = {row["audit_id"]: row for row in source_rows}
    rows = read_tsv(TSV_PATH)
    fieldnames = set(rows[0].keys()) if rows else set()

    missing_columns = sorted(REQUIRED_COLUMNS - fieldnames)
    if missing_columns:
        errors.append(f"{repo_relative(TSV_PATH)} missing required columns: {missing_columns}")
    forbidden_columns = sorted(FORBIDDEN_COLUMNS & fieldnames)
    if forbidden_columns:
        errors.append(f"{repo_relative(TSV_PATH)} must not include generated-question columns: {forbidden_columns}")
    if not 20 <= len(rows) <= 30:
        errors.append(f"{repo_relative(TSV_PATH)} row count must be between 20 and 30; found {len(rows)}")

    input_ids: set[str] = set()
    family_counts: Counter[str] = Counter()
    risk_counts: Counter[str] = Counter()
    direct_marker_rows: list[dict[str, str]] = []
    shoresh_rows: list[dict[str, str]] = []

    for row_number, row in enumerate(rows, start=2):
        row_id = row.get("input_candidate_id", f"row {row_number}")
        if row_id in input_ids:
            errors.append(f"{repo_relative(TSV_PATH)} duplicate input_candidate_id: {row_id}")
        input_ids.add(row_id)

        audit_id = row.get("audit_id", "")
        source_row = source_by_audit_id.get(audit_id)
        if source_row is None:
            errors.append(f"{row_id} links to missing approved input-candidate audit row: {audit_id}")
            continue

        family = row.get("approved_family", "")
        family_counts[family] += 1
        if family not in ALLOWED_FAMILIES:
            errors.append(f"{row_id} uses disallowed approved_family: {family}")
        if family == "basic_verb_form_recognition":
            errors.append(f"{row_id} must not include deferred basic_verb_form_recognition")
        if family != source_row.get("proposed_question_family"):
            errors.append(
                f"{row_id} approved_family {family!r} does not match source planning family "
                f"{source_row.get('proposed_question_family')!r}"
            )

        if row.get("ref") != source_row.get("ref"):
            errors.append(f"{row_id} ref does not match approved planning sheet source row")
        if row.get("hebrew_token") != source_row.get("hebrew_token"):
            errors.append(f"{row_id} hebrew_token does not match approved planning sheet source row")

        risk = row.get("risk_level", "")
        risk_counts[risk] += 1
        if risk == "high":
            errors.append(f"{row_id} must not include high-risk rows")

        for field in REVIEW_STATUS_FIELDS:
            if row.get(field) != "needs_review":
                errors.append(f"{row_id} {field} must be needs_review")
        if row.get("protected_preview_candidate_status") != "planning_only":
            errors.append(f"{row_id} protected_preview_candidate_status must be planning_only")
        if row.get("yossi_input_planning_decision") != "approve_for_template_skeleton_planning":
            errors.append(f"{row_id} yossi_input_planning_decision must be approve_for_template_skeleton_planning")
        if "not question approval" not in row.get("yossi_notes", ""):
            errors.append(f"{row_id} yossi_notes must preserve planning-only safety language")
        for gate in SAFETY_GATE_FIELDS:
            if row.get(gate) != "false":
                errors.append(f"{row_id} {gate} must remain false")

        for field in ("hebrew_token", "hebrew_phrase"):
            if contains_placeholder_hebrew(row.get(field, "")):
                errors.append(f"{row_id} {field} contains placeholder '?' instead of real UTF-8 Hebrew")

        if not row.get("selection_reason", "").strip():
            errors.append(f"{row_id} selection_reason must not be blank")
        if family == "direct_object_marker_recognition":
            direct_marker_rows.append(row)
            if "function" not in row.get("selection_reason", "").lower():
                errors.append(f"{row_id} direct-object-marker selection_reason must explain function wording")
            if "function of את" not in row.get("yossi_notes", ""):
                errors.append(f"{row_id} direct-object-marker yossi_notes must preserve function-of-et caution")
        if family == "shoresh_identification":
            shoresh_rows.append(row)
            if "root" not in row.get("selection_reason", "").lower() and "shoresh" not in row.get("selection_reason", "").lower():
                errors.append(f"{row_id} shoresh selection_reason must explain root/shoresh suitability")
        if row_id == "ppplan_b1_024":
            notes = row.get("yossi_notes", "")
            if "בדל" not in notes or "הבדיל" not in notes:
                errors.append("ppplan_b1_024 yossi_notes must preserve הבדיל / בדל shoresh caution")
        if row.get("hebrew_token") in {"המים", "האדמה", "הארץ"}:
            if "article" not in row.get("yossi_notes", "").lower() and "base meaning" not in row.get("yossi_notes", "").lower():
                errors.append(f"{row_id} yossi_notes must preserve article/base-meaning answer-key review caution")

    if not direct_marker_rows:
        errors.append(f"{repo_relative(TSV_PATH)} should include a small direct-object-marker sample")
    if not 1 <= len(shoresh_rows) <= 3:
        errors.append(f"{repo_relative(TSV_PATH)} should include 1-3 shoresh rows; found {len(shoresh_rows)}")

    review_rows = read_csv_sig(REVIEW_CSV_PATH)
    if not file_has_utf8_bom(REVIEW_CSV_PATH):
        errors.append(f"{repo_relative(REVIEW_CSV_PATH)} must be UTF-8-BOM")
    if len(review_rows) != len(rows):
        errors.append(f"{repo_relative(REVIEW_CSV_PATH)} row count must match planning TSV")
    for row in review_rows:
        if row.get("yossi_input_planning_decision") != "approve_for_template_skeleton_planning":
            errors.append(f"{repo_relative(REVIEW_CSV_PATH)} row {row.get('input_candidate_id')} missing applied Yossi decision")

    balance_text = BALANCE_REPORT_PATH.read_text(encoding="utf-8")
    balance_lower = balance_text.lower()
    for phrase in BALANCE_REPORT_PHRASES:
        if phrase not in balance_lower:
            errors.append(f"{repo_relative(BALANCE_REPORT_PATH)} missing required balance phrase: {phrase!r}")
    for row in direct_marker_rows + shoresh_rows:
        if row["input_candidate_id"] not in balance_text:
            errors.append(f"{repo_relative(BALANCE_REPORT_PATH)} missing inclusion reason for {row['input_candidate_id']}")

    review_text = REVIEW_MD_PATH.read_text(encoding="utf-8")
    if "This is an input-candidate planning review only." not in review_text:
        errors.append(f"{repo_relative(REVIEW_MD_PATH)} missing required planning-only warning")
    if "approve_for_template_skeleton_planning" not in review_text:
        errors.append(f"{repo_relative(REVIEW_MD_PATH)} must record approve_for_template_skeleton_planning decisions")

    applied_text = APPLIED_REPORT_PATH.read_text(encoding="utf-8")
    for phrase in (
        "Total planning candidates reviewed: 24",
        "Approved for template-skeleton planning: 24",
        "direct-object-marker",
        "הבדיל",
        "בדל",
        "article or only the base meaning",
        "No protected-preview input list was created",
    ):
        if phrase not in applied_text:
            errors.append(f"{repo_relative(APPLIED_REPORT_PATH)} missing required phrase: {phrase!r}")

    readme_text = README_PATH.read_text(encoding="utf-8")
    for path in (TSV_PATH, BALANCE_REPORT_PATH, PLANNING_REPORT_PATH, REVIEW_MD_PATH, REVIEW_CSV_PATH, APPLIED_REPORT_PATH):
        if repo_relative(path) not in readme_text:
            errors.append(f"{repo_relative(README_PATH)} must link {repo_relative(path)}")

    combined_text = "\n".join(
        [
            README_PATH.read_text(encoding="utf-8"),
            balance_text,
            PLANNING_REPORT_PATH.read_text(encoding="utf-8"),
            review_text,
            applied_text,
        ]
    )
    for phrase in FORBIDDEN_PHRASES:
        if contains_forbidden_phrase(combined_text, phrase):
            errors.append(f"forbidden approval phrase appears without clear negation: {phrase}")

    return {
        "valid": not errors,
        "errors": errors,
        "row_count": len(rows),
        "family_counts": dict(family_counts),
        "risk_counts": dict(risk_counts),
        "direct_object_marker_count": len(direct_marker_rows),
        "shoresh_count": len(shoresh_rows),
    }


def main() -> int:
    summary = validate_protected_preview_input_planning()
    if summary["valid"]:
        print("Protected-preview input planning validation passed.")
        print(f"Rows: {summary['row_count']}")
        print(f"Family counts: {summary['family_counts']}")
        print(f"Risk counts: {summary['risk_counts']}")
        return 0
    print("Protected-preview input planning validation failed:")
    for error in summary["errors"]:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
