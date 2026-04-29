from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "data" / "question_eligibility_audits"
README_PATH = AUDIT_DIR / "README.md"
AUDIT_PATH = AUDIT_DIR / "bereishis_perek_1_question_eligibility_audit.tsv"
REPORT_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_question_eligibility_audit_report.md"
REVIEW_MD_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_question_eligibility_yossi_review_sheet.md"
REVIEW_CSV_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_question_eligibility_yossi_review_sheet.csv"
APPLIED_REPORT_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_question_eligibility_yossi_review_applied.md"
PLANNING_MD_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_approved_input_candidate_planning_sheet.md"
PLANNING_CSV_PATH = AUDIT_DIR / "reports" / "bereishis_perek_1_approved_input_candidate_planning_sheet.csv"

REQUIRED_COLUMNS = [
    "audit_id",
    "source_candidate_file",
    "source_candidate_id",
    "source_candidate_type",
    "ref",
    "hebrew_token",
    "hebrew_phrase",
    "canonical_skill_id",
    "canonical_standard_anchor",
    "enrichment_review_status",
    "enrichment_evidence_summary",
    "proposed_question_family",
    "eligibility_recommendation",
    "recommendation_reason",
    "risk_level",
    "risk_reasons",
    "yossi_question_review_decision",
    "yossi_question_review_notes",
    "question_allowed",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "runtime_allowed",
]

REVIEW_COLUMNS = [
    "audit_id",
    "ref",
    "hebrew_token",
    "hebrew_phrase",
    "source_candidate_type",
    "canonical_skill_id",
    "proposed_question_family",
    "eligibility_recommendation",
    "recommendation_reason",
    "risk_level",
    "risk_reasons",
    "yossi_question_review_decision",
    "yossi_question_review_notes",
]

PLANNING_COLUMNS = [
    "audit_id",
    "ref",
    "hebrew_token",
    "hebrew_phrase",
    "source_candidate_type",
    "canonical_skill_id",
    "canonical_standard_anchor",
    "proposed_question_family",
    "risk_level",
    "risk_reasons",
    "yossi_question_review_notes",
    "future_template_needed",
    "future_wording_review_required",
]

ALLOWED_RECOMMENDATIONS = {
    "eligible_candidate_for_yossi_question_review",
    "source_only",
    "needs_follow_up",
    "blocked_for_questions",
}

ALLOWED_FAMILIES = {
    "vocabulary_meaning",
    "shoresh_identification",
    "basic_noun_recognition",
    "direct_object_marker_recognition",
    "basic_prefix_recognition",
    "basic_verb_form_recognition",
    "phrase_translation_context",
    "not_recommended",
}

ALLOWED_RISK_LEVELS = {"low", "medium", "high"}
ALLOWED_YOSSI_DECISIONS = {
    "approve_as_input_candidate",
    "source_only",
    "needs_follow_up",
    "block_for_questions",
}
APPROVED_FAMILIES = {
    "vocabulary_meaning",
    "basic_noun_recognition",
    "direct_object_marker_recognition",
    "shoresh_identification",
}
FORBIDDEN_ROW_LANGUAGE = {
    "question_ready",
    "protected_preview_ready",
    "reviewed_bank_ready",
    "runtime_ready",
    "student_facing",
    "approved_for_questions",
    "approved_for_preview",
}

SAFETY_WARNING = (
    "This is a question-eligibility audit only. It does not generate questions, "
    "approve protected-preview use, approve reviewed-bank use, approve runtime use, "
    "or approve student-facing use."
)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def source_candidate_index(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    index: dict[tuple[str, str], dict[str, str]] = {}
    paths = sorted({row["source_candidate_file"] for row in rows})
    for raw_path in paths:
        path = ROOT / raw_path
        _, source_rows = load_tsv(path)
        for row in source_rows:
            index[(raw_path, row.get("candidate_id", ""))] = row
    return index


def count_in_report(text: str, label: str) -> int | None:
    match = re.search(rf"- {re.escape(label)}: (\d+)", text)
    return int(match.group(1)) if match else None


def validate_question_eligibility_audit() -> dict[str, object]:
    errors: list[str] = []
    for path in (
        README_PATH,
        AUDIT_PATH,
        REPORT_PATH,
        REVIEW_MD_PATH,
        REVIEW_CSV_PATH,
        APPLIED_REPORT_PATH,
        PLANNING_MD_PATH,
        PLANNING_CSV_PATH,
    ):
        if not path.exists():
            errors.append(f"required question-eligibility artifact missing: {repo_relative(path)}")

    if errors:
        return {"valid": False, "errors": errors}

    columns, rows = load_tsv(AUDIT_PATH)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in columns]
    if missing_columns:
        errors.append(f"{repo_relative(AUDIT_PATH)} missing required columns: {missing_columns}")

    source_index = source_candidate_index(rows)
    seen_ids: set[str] = set()
    for row in rows:
        audit_id = row.get("audit_id", "")
        context = f"Audit row {audit_id or '<blank>'}"
        if not audit_id:
            errors.append(f"{context}: audit_id is required")
        if audit_id in seen_ids:
            errors.append(f"{context}: duplicate audit_id")
        seen_ids.add(audit_id)

        source_key = (row.get("source_candidate_file", ""), row.get("source_candidate_id", ""))
        source_row = source_index.get(source_key)
        if source_row is None:
            errors.append(f"{context}: source candidate does not exist: {source_key}")
        elif row.get("enrichment_review_status") != source_row.get("enrichment_review_status"):
            errors.append(
                f"{context}: enrichment_review_status does not match source candidate {row.get('source_candidate_id')}"
            )

        if row.get("eligibility_recommendation") not in ALLOWED_RECOMMENDATIONS:
            errors.append(f"{context}: unsupported eligibility_recommendation {row.get('eligibility_recommendation')!r}")
        if row.get("proposed_question_family") not in ALLOWED_FAMILIES:
            errors.append(f"{context}: unsupported proposed_question_family {row.get('proposed_question_family')!r}")
        if row.get("risk_level") not in ALLOWED_RISK_LEVELS:
            errors.append(f"{context}: unsupported risk_level {row.get('risk_level')!r}")

        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        for gate in ("protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed"):
            if row.get(gate) != "false":
                errors.append(f"{context}: {gate} must remain false")

        if row.get("yossi_question_review_decision") not in ALLOWED_YOSSI_DECISIONS:
            errors.append(
                f"{context}: unsupported yossi_question_review_decision {row.get('yossi_question_review_decision')!r}"
            )
        if not row.get("yossi_question_review_notes"):
            errors.append(f"{context}: yossi_question_review_notes must be populated after first-pass review")

        joined_row_text = " ".join(row.values()).lower()
        for forbidden in FORBIDDEN_ROW_LANGUAGE:
            if forbidden in joined_row_text:
                errors.append(f"{context}: forbidden approval language appears: {forbidden}")

        if "???" in row.get("hebrew_token", "") or "???" in row.get("hebrew_phrase", ""):
            errors.append(f"{context}: Hebrew field contains placeholder question marks")

        if row.get("eligibility_recommendation") == "eligible_candidate_for_yossi_question_review":
            if row.get("enrichment_review_status") != "yossi_enrichment_verified":
                errors.append(
                    f"{context}: marked eligible but source candidate is not yossi_enrichment_verified"
                )
            if row.get("proposed_question_family") == "not_recommended":
                errors.append(f"{context}: marked eligible but proposed_question_family is not_recommended")
            if row.get("source_candidate_type") == "token_split_standards":
                if not row.get("canonical_skill_id") or not row.get("canonical_standard_anchor"):
                    errors.append(f"{context}: eligible token-split standards row lacks canonical contract anchors")
            if row.get("proposed_question_family") in APPROVED_FAMILIES:
                if row.get("yossi_question_review_decision") != "approve_as_input_candidate":
                    errors.append(f"{context}: clean eligible family should be approve_as_input_candidate")
            elif row.get("proposed_question_family") == "basic_verb_form_recognition":
                if row.get("yossi_question_review_decision") != "needs_follow_up":
                    errors.append(f"{context}: basic_verb_form_recognition must remain needs_follow_up")

        if row.get("eligibility_recommendation") == "needs_follow_up":
            if row.get("proposed_question_family") != "not_recommended":
                errors.append(f"{context}: needs_follow_up rows must use not_recommended question family")
            if row.get("yossi_question_review_decision") != "needs_follow_up":
                errors.append(f"{context}: needs_follow_up rows must keep yossi_question_review_decision=needs_follow_up")
        if row.get("eligibility_recommendation") == "source_only" and row.get("yossi_question_review_decision") != "source_only":
            errors.append(f"{context}: source_only rows must keep yossi_question_review_decision=source_only")
        if (
            row.get("eligibility_recommendation") == "blocked_for_questions"
            and row.get("yossi_question_review_decision") != "block_for_questions"
        ):
            errors.append(f"{context}: blocked_for_questions rows must use yossi_question_review_decision=block_for_questions")

    review_md = REVIEW_MD_PATH.read_text(encoding="utf-8")
    if SAFETY_WARNING not in review_md:
        errors.append(f"{repo_relative(REVIEW_MD_PATH)} missing required safety warning")
    if "???" in review_md:
        errors.append(f"{repo_relative(REVIEW_MD_PATH)} contains placeholder question marks")

    if not REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append(f"{repo_relative(REVIEW_CSV_PATH)} must be UTF-8-BOM encoded")
    review_columns, review_rows = load_csv(REVIEW_CSV_PATH)
    if review_columns != REVIEW_COLUMNS:
        errors.append(f"{repo_relative(REVIEW_CSV_PATH)} columns do not match expected review sheet columns")
    review_ids = {row["audit_id"] for row in review_rows}
    eligible_ids = {row["audit_id"] for row in rows if row["eligibility_recommendation"] == "eligible_candidate_for_yossi_question_review"}
    blocked_ids = {row["audit_id"] for row in rows if row["eligibility_recommendation"] == "blocked_for_questions"}
    missing_review_ids = sorted((eligible_ids | blocked_ids) - review_ids)
    if missing_review_ids:
        errors.append(f"{repo_relative(REVIEW_CSV_PATH)} missing eligible/blocked audit rows: {missing_review_ids[:10]}")

    report_text = REPORT_PATH.read_text(encoding="utf-8")
    for phrase in (
        "opens no gates",
        "no questions generated",
        "no answer choices generated",
        "no answer keys generated",
        "no protected-preview inputs created",
        "no reviewed-bank entries created",
        "no runtime changes",
        "all existing source/enrichment gates remain closed",
    ):
        if phrase not in report_text:
            errors.append(f"{repo_relative(REPORT_PATH)} missing required safety phrase: {phrase!r}")

    rec_counts = Counter(row["eligibility_recommendation"] for row in rows)
    family_counts = Counter(row["proposed_question_family"] for row in rows)
    risk_counts = Counter(row["risk_level"] for row in rows)
    decision_counts = Counter(row["yossi_question_review_decision"] for row in rows)
    approved_family_counts = Counter(
        row["proposed_question_family"] for row in rows if row["yossi_question_review_decision"] == "approve_as_input_candidate"
    )
    verified_total = sum(1 for row in rows if row["enrichment_review_status"] == "yossi_enrichment_verified")

    expected_decisions = {
        "approve_as_input_candidate": 133,
        "needs_follow_up": 155,
        "source_only": 6,
        "block_for_questions": 5,
    }
    for label, expected in expected_decisions.items():
        if decision_counts[label] != expected:
            errors.append(f"{repo_relative(AUDIT_PATH)} expected {expected} {label} decisions, found {decision_counts[label]}")
    expected_approved_families = {
        "vocabulary_meaning": 56,
        "basic_noun_recognition": 60,
        "direct_object_marker_recognition": 14,
        "shoresh_identification": 3,
    }
    for label, expected in expected_approved_families.items():
        if approved_family_counts[label] != expected:
            errors.append(
                f"{repo_relative(AUDIT_PATH)} expected {expected} approved {label} rows, found {approved_family_counts[label]}"
            )
    if approved_family_counts["basic_verb_form_recognition"] != 0:
        errors.append(f"{repo_relative(AUDIT_PATH)} must not approve basic_verb_form_recognition rows")

    expected_report_counts = {
        "total enrichment candidates considered": len(rows),
        "total verified enrichment candidates considered": verified_total,
        "total audit rows created": len(rows),
    }
    for label, expected in expected_report_counts.items():
        actual = count_in_report(report_text, label)
        if actual != expected:
            errors.append(f"{repo_relative(REPORT_PATH)} count for {label!r} should be {expected}, found {actual}")
    for label, expected in rec_counts.items():
        actual = count_in_report(report_text, label)
        if actual != expected:
            errors.append(f"{repo_relative(REPORT_PATH)} recommendation count for {label!r} should be {expected}, found {actual}")
    for label, expected in family_counts.items():
        actual = count_in_report(report_text, label)
        if actual != expected:
            errors.append(f"{repo_relative(REPORT_PATH)} family count for {label!r} should be {expected}, found {actual}")
    for label, expected in risk_counts.items():
        actual = count_in_report(report_text, label)
        if actual != expected:
            errors.append(f"{repo_relative(REPORT_PATH)} risk count for {label!r} should be {expected}, found {actual}")

    applied_text = APPLIED_REPORT_PATH.read_text(encoding="utf-8")
    for phrase in (
        "total audit rows reviewed: 299",
        "approved input-candidate count: 133",
        "needs_follow_up count: 155",
        "source_only count: 6",
        "blocked_for_questions count: 5",
        "vocabulary_meaning: 56",
        "basic_noun_recognition: 60",
        "direct_object_marker_recognition: 14",
        "shoresh_identification: 3",
        "basic_verb_form_recognition: 25",
        "no questions were generated",
        "no answer choices were generated",
        "no answer keys were generated",
        "no protected-preview inputs were created",
        "no reviewed-bank entries were created",
        "no runtime changes were made",
        "approved input candidates are not approved questions",
        "protected preview remains a separate later gate",
    ):
        if phrase not in applied_text:
            errors.append(f"{repo_relative(APPLIED_REPORT_PATH)} missing required phrase: {phrase!r}")

    if not PLANNING_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append(f"{repo_relative(PLANNING_CSV_PATH)} must be UTF-8-BOM encoded")
    planning_columns, planning_rows = load_csv(PLANNING_CSV_PATH)
    if planning_columns != PLANNING_COLUMNS:
        errors.append(f"{repo_relative(PLANNING_CSV_PATH)} columns do not match expected planning sheet columns")
    if len(planning_rows) != 133:
        errors.append(f"{repo_relative(PLANNING_CSV_PATH)} expected 133 planning rows, found {len(planning_rows)}")
    planning_ids = {row["audit_id"] for row in planning_rows}
    expected_planning_ids = {
        row["audit_id"] for row in rows if row["yossi_question_review_decision"] == "approve_as_input_candidate"
    }
    if planning_ids != expected_planning_ids:
        errors.append(f"{repo_relative(PLANNING_CSV_PATH)} rows must exactly match approved input-candidate decisions")
    if any(row.get("future_template_needed") != "true" for row in planning_rows):
        errors.append(f"{repo_relative(PLANNING_CSV_PATH)} all rows must set future_template_needed=true")
    if any(row.get("future_wording_review_required") != "true" for row in planning_rows):
        errors.append(f"{repo_relative(PLANNING_CSV_PATH)} all rows must set future_wording_review_required=true")

    planning_text = PLANNING_MD_PATH.read_text(encoding="utf-8")
    if "protected-preview input list" in PLANNING_MD_PATH.name:
        errors.append(f"{repo_relative(PLANNING_MD_PATH)} must not be named as a protected-preview input list")
    for phrase in (
        "This is a planning sheet only.",
        "not a protected-preview input list",
        "not question approval",
        "not reviewed-bank approval",
        "not runtime approval",
        "not student-facing approval",
    ):
        if phrase not in planning_text:
            errors.append(f"{repo_relative(PLANNING_MD_PATH)} missing required planning boundary phrase: {phrase!r}")

    readme_text = README_PATH.read_text(encoding="utf-8")
    for phrase in (
        "audit-only layer",
        "does not generate questions",
        "does not approve protected-preview",
        "does not approve reviewed-bank",
        "does not approve runtime",
        "Existing source-to-skill and enrichment safety gates remain closed",
        "Eligibility recommendations require later Yossi review",
    ):
        if phrase not in readme_text:
            errors.append(f"{repo_relative(README_PATH)} missing required boundary phrase: {phrase!r}")

    return {
        "valid": not errors,
        "audit_path": repo_relative(AUDIT_PATH),
        "report_path": repo_relative(REPORT_PATH),
        "review_md_path": repo_relative(REVIEW_MD_PATH),
        "review_csv_path": repo_relative(REVIEW_CSV_PATH),
        "applied_report_path": repo_relative(APPLIED_REPORT_PATH),
        "planning_md_path": repo_relative(PLANNING_MD_PATH),
        "planning_csv_path": repo_relative(PLANNING_CSV_PATH),
        "audit_row_count": len(rows),
        "verified_enrichment_rows_considered": verified_total,
        "recommendation_counts": dict(sorted(rec_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "approved_family_counts": dict(sorted(approved_family_counts.items())),
        "question_family_counts": dict(sorted(family_counts.items())),
        "risk_level_counts": dict(sorted(risk_counts.items())),
        "review_sheet_row_count": len(review_rows),
        "planning_sheet_row_count": len(planning_rows),
        "errors": errors,
    }


def main() -> int:
    summary = validate_question_eligibility_audit()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
