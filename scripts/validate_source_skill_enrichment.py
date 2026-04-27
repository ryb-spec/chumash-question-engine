from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
ENRICHMENT_DIR = ROOT / "data" / "source_skill_enrichment"
SOURCE_MAP_PATH = ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_1_to_1_5_source_to_skill_map.tsv"

MORPHOLOGY_PATH = (
    ENRICHMENT_DIR / "morphology_candidates" / "bereishis_1_1_to_1_5_morphology_candidates.tsv"
)
STANDARDS_PATH = (
    ENRICHMENT_DIR / "standards_candidates" / "bereishis_1_1_to_1_5_standards_candidates.tsv"
)
VOCABULARY_PATH = (
    ENRICHMENT_DIR
    / "vocabulary_shoresh_candidates"
    / "bereishis_1_1_to_1_5_vocabulary_shoresh_candidates.tsv"
)

README_PATH = ENRICHMENT_DIR / "README.md"
AUDIT_REPORT_PATH = ENRICHMENT_DIR / "reports" / "morphology_standards_enrichment_audit.md"

REVIEW_SHEETS = {
    "morphology": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_morphology_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_morphology_enrichment_yossi_review_sheet.csv",
    ),
    "standards": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_standards_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_standards_enrichment_yossi_review_sheet.csv",
    ),
    "vocabulary_shoresh": (
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_vocabulary_shoresh_enrichment_yossi_review_sheet.md",
        ENRICHMENT_DIR / "reports" / "bereishis_1_1_to_1_5_vocabulary_shoresh_enrichment_yossi_review_sheet.csv",
    ),
}

APPLIED_REVIEW_REPORTS = {
    "morphology": (
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_1_to_1_5_morphology_enrichment_yossi_review_applied.md"
    ),
    "standards": (
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_1_to_1_5_standards_enrichment_yossi_review_applied.md"
    ),
    "vocabulary_shoresh": (
        ENRICHMENT_DIR
        / "reports"
        / "bereishis_1_1_to_1_5_vocabulary_shoresh_enrichment_yossi_review_applied.md"
    ),
}

FOLLOW_UP_INVENTORY_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_enrichment_follow_up_inventory.md"
)
FOLLOW_UP_REVIEW_MD_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_enrichment_follow_up_yossi_review_sheet.md"
)
FOLLOW_UP_REVIEW_CSV_PATH = (
    ENRICHMENT_DIR
    / "reports"
    / "bereishis_1_1_to_1_5_enrichment_follow_up_yossi_review_sheet.csv"
)

MORPHOLOGY_COLUMNS = [
    "candidate_id",
    "source_map_file",
    "source_row_id",
    "ref",
    "hebrew_phrase",
    "token_index",
    "hebrew_token",
    "clean_hebrew_no_nikud",
    "proposed_shoresh",
    "proposed_prefixes",
    "proposed_suffixes",
    "proposed_tense",
    "proposed_person",
    "proposed_gender",
    "proposed_number",
    "proposed_part_of_speech",
    "proposed_dikduk_feature",
    "evidence_source_id",
    "evidence_source_type",
    "evidence_note",
    "confidence",
    "enrichment_review_status",
    "yossi_decision",
    "yossi_notes",
    "question_allowed",
    "protected_preview_allowed",
    "runtime_allowed",
    "reviewed_bank_allowed",
]

STANDARDS_COLUMNS = [
    "candidate_id",
    "source_map_file",
    "source_row_id",
    "ref",
    "hebrew_phrase",
    "skill_primary",
    "skill_secondary",
    "proposed_skill_id",
    "proposed_zekelman_standard",
    "proposed_standard_level",
    "evidence_source_id",
    "evidence_source_type",
    "evidence_note",
    "confidence",
    "enrichment_review_status",
    "yossi_decision",
    "yossi_notes",
    "question_allowed",
    "protected_preview_allowed",
    "runtime_allowed",
    "reviewed_bank_allowed",
]

VOCABULARY_COLUMNS = [
    "candidate_id",
    "source_map_file",
    "source_row_id",
    "ref",
    "hebrew_phrase",
    "token_index",
    "hebrew_token",
    "clean_hebrew_no_nikud",
    "proposed_translation",
    "proposed_shoresh_or_keyword",
    "proposed_vocabulary_category",
    "first_150_match",
    "first_150_entry_id",
    "evidence_source_id",
    "evidence_source_type",
    "evidence_note",
    "confidence",
    "enrichment_review_status",
    "yossi_decision",
    "yossi_notes",
    "question_allowed",
    "protected_preview_allowed",
    "runtime_allowed",
    "reviewed_bank_allowed",
]

REVIEW_CSV_COLUMNS = [
    "candidate_id",
    "ref",
    "hebrew_phrase",
    "hebrew_token",
    "proposed_values",
    "evidence_source_id",
    "evidence_note",
    "confidence",
    "current_status",
    "what_to_check",
    "recommended_default_decision",
    "yossi_decision",
    "yossi_notes",
    "safety_warning",
]

FOLLOW_UP_CSV_COLUMNS = [
    "candidate_id",
    "type",
    "ref",
    "hebrew",
    "current_decision",
    "current_status",
    "current_evidence",
    "improved_evidence",
    "missing_evidence",
    "remaining_question",
    "recommended_decision",
    "yossi_decision",
    "yossi_notes",
]

ALLOWED_REVIEW_STATUSES = {
    "pending_yossi_enrichment_review",
    "yossi_enrichment_verified",
    "needs_follow_up",
    "blocked_unclear_evidence",
    "source_only",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_YOSSI_DECISIONS = {
    "",
    "verified",
    "fix_morphology",
    "fix_standard",
    "fix_vocabulary",
    "source_only",
    "block_for_questions",
    "needs_follow_up",
}
SAFETY_WARNING_PHRASES = (
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
    "not student-facing approval",
)
FORBIDDEN_READY_VALUES = {"true", "yes", "approved", "runtime-ready", "question-ready", "student-facing"}


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


def source_rows_by_id() -> dict[str, dict[str, str]]:
    _, rows = load_tsv(SOURCE_MAP_PATH)
    return {f"row_{index:03d}": row for index, row in enumerate(rows, 1)}


def has_claim(row: dict[str, str], proposed_columns: Iterable[str]) -> bool:
    return any((row.get(column) or "").strip() for column in proposed_columns)


def validate_required_files(errors: list[str]) -> None:
    required = [
        README_PATH,
        AUDIT_REPORT_PATH,
        MORPHOLOGY_PATH,
        STANDARDS_PATH,
        VOCABULARY_PATH,
        SOURCE_MAP_PATH,
    ]
    for md_path, csv_path in REVIEW_SHEETS.values():
        required.extend([md_path, csv_path])
    required.extend(APPLIED_REVIEW_REPORTS.values())
    required.extend([FOLLOW_UP_INVENTORY_PATH, FOLLOW_UP_REVIEW_MD_PATH, FOLLOW_UP_REVIEW_CSV_PATH])
    for path in required:
        if not path.exists():
            errors.append(f"required enrichment artifact missing: {repo_relative(path)}")


def validate_columns(path: Path, columns: list[str], required_columns: list[str], errors: list[str]) -> None:
    missing = [column for column in required_columns if column not in columns]
    if missing:
        errors.append(f"{repo_relative(path)} missing required columns: {missing}")


def validate_candidate_rows(
    *,
    path: Path,
    rows: list[dict[str, str]],
    source_rows: dict[str, dict[str, str]],
    proposed_columns: list[str],
    errors: list[str],
) -> None:
    seen: set[str] = set()
    expected_source_map = repo_relative(SOURCE_MAP_PATH)
    for row in rows:
        candidate_id = row.get("candidate_id", "")
        context = f"{repo_relative(path)} candidate {candidate_id or '<blank>'}"
        if not candidate_id:
            errors.append(f"{context}: candidate_id is required")
        if candidate_id in seen:
            errors.append(f"{context}: duplicate candidate_id")
        seen.add(candidate_id)

        if row.get("source_map_file") != expected_source_map:
            errors.append(f"{context}: source_map_file must be {expected_source_map}")
        source_row_id = row.get("source_row_id", "")
        source_row = source_rows.get(source_row_id)
        if not source_row:
            errors.append(f"{context}: source_row_id {source_row_id!r} does not link to an existing source map row")
            continue
        if source_row.get("extraction_review_status") != "yossi_extraction_verified":
            errors.append(f"{context}: source row {source_row_id} is not yossi_extraction_verified")
        if row.get("ref") != source_row.get("ref"):
            errors.append(f"{context}: ref does not match linked source row {source_row_id}")
        if row.get("hebrew_phrase") != source_row.get("hebrew_word_or_phrase"):
            errors.append(f"{context}: hebrew_phrase does not match linked source row {source_row_id}")

        status = row.get("enrichment_review_status", "")
        if status not in ALLOWED_REVIEW_STATUSES:
            errors.append(f"{context}: enrichment_review_status {status!r} must be one of {sorted(ALLOWED_REVIEW_STATUSES)}")
        confidence = row.get("confidence", "")
        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"{context}: confidence {confidence!r} must be one of {sorted(ALLOWED_CONFIDENCE)}")
        yossi_decision = row.get("yossi_decision", "")
        if yossi_decision not in ALLOWED_YOSSI_DECISIONS:
            errors.append(f"{context}: yossi_decision {yossi_decision!r} is not allowed")
        if status == "yossi_enrichment_verified" and yossi_decision != "verified":
            errors.append(f"{context}: yossi_enrichment_verified rows must have yossi_decision=verified")
        if yossi_decision == "verified" and status != "yossi_enrichment_verified":
            errors.append(f"{context}: yossi_decision=verified must set enrichment_review_status=yossi_enrichment_verified")
        if yossi_decision.startswith("fix_") and status == "yossi_enrichment_verified":
            errors.append(f"{context}: fix decisions must not be marked yossi_enrichment_verified")
        if yossi_decision == "needs_follow_up" and status != "needs_follow_up":
            errors.append(f"{context}: needs_follow_up decisions must keep enrichment_review_status=needs_follow_up")
        if row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: question_allowed must remain needs_review")
        if row.get("protected_preview_allowed") != "false":
            errors.append(f"{context}: protected_preview_allowed must remain false")
        if row.get("runtime_allowed") != "false":
            errors.append(f"{context}: runtime_allowed must remain false")
        if row.get("reviewed_bank_allowed") != "false":
            errors.append(f"{context}: reviewed_bank_allowed must remain false")
        if status == "yossi_enrichment_verified" and not row.get("yossi_notes", "").strip():
            errors.append(f"{context}: verified enrichment candidates must include yossi_notes")

        for field_name, value in row.items():
            normalized_value = str(value).strip().lower()
            if field_name in {"question_allowed", "protected_preview_allowed", "runtime_allowed", "reviewed_bank_allowed"}:
                continue
            if field_name == "first_150_match":
                continue
            if field_name == "evidence_note" and "not question approval" in normalized_value:
                continue
            if field_name == "student_facing" and normalized_value in {"true", "yes", "approved"}:
                errors.append(f"{context}: student_facing must not be enabled")
            if normalized_value in {"runtime-ready", "question-ready", "student-facing"}:
                errors.append(f"{context}: contains forbidden readiness value {normalized_value!r}")

        if has_claim(row, proposed_columns) and not row.get("evidence_note", "").strip():
            errors.append(f"{context}: proposes enrichment fields but has no evidence_note")
        if has_claim(row, proposed_columns) and not row.get("evidence_source_id", "").strip():
            errors.append(f"{context}: proposes enrichment fields but has no evidence_source_id")
        if "koren" in row.get("evidence_source_id", "").lower() and "secondary" not in row.get("evidence_note", "").lower():
            errors.append(f"{context}: Koren evidence must be described as secondary noncommercial support")
        if "reviewed_bank" in row.get("evidence_source_id", "").lower() and "reference only" not in row.get("evidence_note", "").lower():
            errors.append(f"{context}: reviewed-bank evidence must be reference only")
        if row.get("first_150_match") == "true" and row.get("question_allowed") != "needs_review":
            errors.append(f"{context}: First 150 evidence cannot open question_allowed")
        if row.get("first_150_match") == "true":
            if not row.get("first_150_entry_id", "").strip():
                errors.append(f"{context}: First 150 claims must include first_150_entry_id")
            if not row.get("evidence_source_id", "").strip() or not row.get("evidence_note", "").strip():
                errors.append(f"{context}: First 150 claims must include evidence_source_id and evidence_note")


def validate_review_sheets(errors: list[str]) -> None:
    for label, (md_path, csv_path) in REVIEW_SHEETS.items():
        if not md_path.exists() or not csv_path.exists():
            continue
        text = md_path.read_text(encoding="utf-8")
        for phrase in SAFETY_WARNING_PHRASES:
            if phrase not in text:
                errors.append(f"{repo_relative(md_path)} missing safety warning phrase: {phrase!r}")
        for decision in ALLOWED_YOSSI_DECISIONS - {""}:
            if f"`{decision}`" not in text:
                errors.append(f"{repo_relative(md_path)} missing allowed decision: {decision}")
        if not csv_path.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"{repo_relative(csv_path)} must be UTF-8-BOM encoded for Hebrew spreadsheet review")
        columns, rows = load_csv(csv_path)
        validate_columns(csv_path, columns, REVIEW_CSV_COLUMNS, errors)
        if not rows:
            errors.append(f"{repo_relative(csv_path)} must contain review rows")
        for row in rows:
            context = f"{repo_relative(csv_path)} candidate {row.get('candidate_id', '<blank>')}"
            if row.get("yossi_decision", "") != "":
                errors.append(f"{context}: yossi_decision must be blank by default")
            if row.get("yossi_notes", "") != "":
                errors.append(f"{context}: yossi_notes must be blank by default")
            warning = row.get("safety_warning", "").lower()
            for phrase in ("not question", "not runtime", "not student-facing"):
                if phrase not in warning:
                    errors.append(f"{context}: safety_warning must include {phrase!r}")
            if label == "vocabulary_shoresh" and "First 150" not in text:
                errors.append(f"{repo_relative(md_path)} must document First 150 evidence as candidate evidence only")


def candidate_is_unresolved(row: dict[str, str]) -> bool:
    return (
        row.get("enrichment_review_status") != "yossi_enrichment_verified"
        or row.get("yossi_decision", "").startswith("fix_")
    )


def validate_follow_up_artifacts(
    *,
    morphology_rows: list[dict[str, str]],
    standards_rows: list[dict[str, str]],
    vocabulary_rows: list[dict[str, str]],
    errors: list[str],
) -> None:
    if not FOLLOW_UP_INVENTORY_PATH.exists() or not FOLLOW_UP_REVIEW_MD_PATH.exists() or not FOLLOW_UP_REVIEW_CSV_PATH.exists():
        return

    all_rows = morphology_rows + standards_rows + vocabulary_rows
    unresolved = {row["candidate_id"]: row for row in all_rows if candidate_is_unresolved(row)}
    verified = {row["candidate_id"] for row in all_rows if row["enrichment_review_status"] == "yossi_enrichment_verified"}

    inventory_text = FOLLOW_UP_INVENTORY_PATH.read_text(encoding="utf-8")
    md_text = FOLLOW_UP_REVIEW_MD_PATH.read_text(encoding="utf-8")

    for phrase in (
        "This inventory lists exactly the unresolved candidates",
        "Already verified candidates are not repeated",
        "Data hygiene audit",
    ):
        if phrase not in inventory_text:
            errors.append(f"{repo_relative(FOLLOW_UP_INVENTORY_PATH)} missing inventory phrase: {phrase!r}")

    safety_phrase = (
        "This is enrichment follow-up review only. It is not question approval, protected-preview approval, "
        "reviewed-bank approval, runtime approval, or student-facing approval."
    )
    if safety_phrase not in md_text:
        errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_MD_PATH)} missing follow-up safety warning")
    for heading in ("Vocabulary/Shoresh Follow-Up", "Morphology Follow-Up", "Standards Follow-Up"):
        if heading not in md_text:
            errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_MD_PATH)} missing section heading: {heading}")
    for decision in (
        "verified",
        "needs_follow_up",
        "source_only",
        "block_for_questions",
        "fix_morphology",
        "fix_standard",
        "fix_vocabulary",
    ):
        if f"`{decision}`" not in md_text:
            errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_MD_PATH)} missing allowed decision: {decision}")

    if not FOLLOW_UP_REVIEW_CSV_PATH.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_CSV_PATH)} must be UTF-8-BOM encoded")
    columns, csv_rows = load_csv(FOLLOW_UP_REVIEW_CSV_PATH)
    validate_columns(FOLLOW_UP_REVIEW_CSV_PATH, columns, FOLLOW_UP_CSV_COLUMNS, errors)
    csv_ids = {row.get("candidate_id", "") for row in csv_rows}

    if csv_ids != set(unresolved):
        missing = sorted(set(unresolved) - csv_ids)
        extra = sorted(csv_ids - set(unresolved))
        errors.append(
            f"{repo_relative(FOLLOW_UP_REVIEW_CSV_PATH)} must list exactly unresolved candidates; "
            f"missing={missing}, extra={extra}"
        )
    for candidate_id in unresolved:
        if candidate_id not in inventory_text:
            errors.append(f"{repo_relative(FOLLOW_UP_INVENTORY_PATH)} missing unresolved candidate {candidate_id}")
        if candidate_id not in md_text:
            errors.append(f"{repo_relative(FOLLOW_UP_REVIEW_MD_PATH)} missing unresolved candidate {candidate_id}")
    for candidate_id in verified:
        if f"### `{candidate_id}`" in inventory_text or f"### `{candidate_id}`" in md_text:
            errors.append(f"{candidate_id} is already verified and must not appear as a follow-up review row")

    for row in csv_rows:
        context = f"{repo_relative(FOLLOW_UP_REVIEW_CSV_PATH)} candidate {row.get('candidate_id', '<blank>')}"
        if row.get("yossi_decision", "") != "":
            errors.append(f"{context}: yossi_decision must be blank for follow-up review")
        if row.get("yossi_notes", "") != "":
            errors.append(f"{context}: yossi_notes must be blank for follow-up review")
        if row.get("recommended_decision") not in {
            "verified",
            "needs_follow_up",
            "source_only",
            "block_for_questions",
            "fix_morphology",
            "fix_standard",
            "fix_vocabulary",
        }:
            errors.append(f"{context}: recommended_decision is not allowed")

    standards_by_id = {row["candidate_id"]: row for row in standards_rows}
    for candidate_id in ("std_b1_1_r002", "std_b1_1_r003", "std_b1_3_r013", "std_b1_5_r020"):
        note = standards_by_id.get(candidate_id, {}).get("evidence_note", "").lower()
        if "token-level" not in note or not any(marker in note for marker in ("split", "separate")):
            errors.append(f"{candidate_id}: phrase-level standards follow-up must be flagged for token-level split")


def validate_reports(errors: list[str]) -> None:
    if README_PATH.exists():
        text = README_PATH.read_text(encoding="utf-8")
        for phrase in (
            "Question eligibility",
            "Separate later gate",
            "Koren remains secondary noncommercial support only",
            "No enrichment candidate may claim question-ready",
            "Pilot Review Status",
        ):
            if phrase not in text:
                errors.append(f"{repo_relative(README_PATH)} missing required enrichment policy phrase: {phrase!r}")
    if AUDIT_REPORT_PATH.exists():
        text = AUDIT_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "reviewed-bank examples; reference only",
            "Koren as primary",
            "Do not backfill all morphology fields",
            "What Should Not Be Auto-Filled",
        ):
            if phrase not in text:
                errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} missing audit finding phrase: {phrase!r}")
    for path in APPLIED_REVIEW_REPORTS.values():
        if path.exists():
            text = path.read_text(encoding="utf-8")
            for phrase in SAFETY_WARNING_PHRASES:
                if phrase not in text:
                    errors.append(f"{repo_relative(path)} missing applied-review safety warning phrase: {phrase!r}")
            if "No source-to-skill map rows were changed" not in text:
                errors.append(f"{repo_relative(path)} must confirm source-to-skill maps were not changed")


def validate_source_skill_enrichment() -> dict[str, object]:
    errors: list[str] = []
    validate_required_files(errors)
    if errors:
        return {"valid": False, "errors": errors}

    source_rows = source_rows_by_id()

    morphology_columns, morphology_rows = load_tsv(MORPHOLOGY_PATH)
    standards_columns, standards_rows = load_tsv(STANDARDS_PATH)
    vocabulary_columns, vocabulary_rows = load_tsv(VOCABULARY_PATH)

    validate_columns(MORPHOLOGY_PATH, morphology_columns, MORPHOLOGY_COLUMNS, errors)
    validate_columns(STANDARDS_PATH, standards_columns, STANDARDS_COLUMNS, errors)
    validate_columns(VOCABULARY_PATH, vocabulary_columns, VOCABULARY_COLUMNS, errors)

    validate_candidate_rows(
        path=MORPHOLOGY_PATH,
        rows=morphology_rows,
        source_rows=source_rows,
        proposed_columns=[
            "proposed_shoresh",
            "proposed_prefixes",
            "proposed_suffixes",
            "proposed_tense",
            "proposed_person",
            "proposed_gender",
            "proposed_number",
            "proposed_part_of_speech",
            "proposed_dikduk_feature",
        ],
        errors=errors,
    )
    validate_candidate_rows(
        path=STANDARDS_PATH,
        rows=standards_rows,
        source_rows=source_rows,
        proposed_columns=["proposed_skill_id", "proposed_zekelman_standard", "proposed_standard_level"],
        errors=errors,
    )
    validate_candidate_rows(
        path=VOCABULARY_PATH,
        rows=vocabulary_rows,
        source_rows=source_rows,
        proposed_columns=["proposed_translation", "proposed_shoresh_or_keyword", "proposed_vocabulary_category"],
        errors=errors,
    )
    validate_review_sheets(errors)
    validate_follow_up_artifacts(
        morphology_rows=morphology_rows,
        standards_rows=standards_rows,
        vocabulary_rows=vocabulary_rows,
        errors=errors,
    )
    validate_reports(errors)

    return {
        "valid": not errors,
        "readme_path": repo_relative(README_PATH),
        "audit_report_path": repo_relative(AUDIT_REPORT_PATH),
        "morphology_candidate_path": repo_relative(MORPHOLOGY_PATH),
        "standards_candidate_path": repo_relative(STANDARDS_PATH),
        "vocabulary_candidate_path": repo_relative(VOCABULARY_PATH),
        "morphology_candidate_count": len(morphology_rows),
        "standards_candidate_count": len(standards_rows),
        "vocabulary_candidate_count": len(vocabulary_rows),
        "review_sheet_count": len(REVIEW_SHEETS),
        "applied_review_report_count": len(APPLIED_REVIEW_REPORTS),
        "follow_up_inventory_path": repo_relative(FOLLOW_UP_INVENTORY_PATH),
        "follow_up_review_md_path": repo_relative(FOLLOW_UP_REVIEW_MD_PATH),
        "follow_up_review_csv_path": repo_relative(FOLLOW_UP_REVIEW_CSV_PATH),
        "follow_up_candidate_count": sum(
            1 for row in morphology_rows + standards_rows + vocabulary_rows if candidate_is_unresolved(row)
        ),
        "errors": errors,
    }


def main() -> int:
    summary = validate_source_skill_enrichment()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
