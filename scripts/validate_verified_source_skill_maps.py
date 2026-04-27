from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAP_DIR = ROOT / "data" / "verified_source_skill_maps"
SEED_MAP_PATH = MAP_DIR / "bereishis_1_1_to_3_24_metsudah_skill_map.tsv"
PROOF_MAP_PATH = MAP_DIR / "bereishis_1_1_to_1_5_source_to_skill_map.tsv"
SEED_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_1_1_to_3_24_metsudah_skill_map_extraction_accuracy_review_packet.md"
)
PROOF_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_1_1_to_1_5_source_to_skill_map_exceptions_review_packet.md"
)
PROOF_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_1_1_to_1_5_yossi_extraction_verification_report.md"
)
NEXT_SLICE_MAP_PATH = MAP_DIR / "bereishis_1_6_to_1_13_source_to_skill_map.tsv"
NEXT_SLICE_BUILD_REPORT_PATH = MAP_DIR / "reports" / "bereishis_1_6_to_1_13_source_to_skill_map_build_report.md"
NEXT_SLICE_REVIEW_PACKET_PATH = (
    MAP_DIR / "reports" / "bereishis_1_6_to_1_13_source_to_skill_map_exceptions_review_packet.md"
)
NEXT_SLICE_VERIFICATION_REPORT_PATH = (
    MAP_DIR / "reports" / "bereishis_1_6_to_1_13_yossi_extraction_verification_report.md"
)
AUDIT_REPORT_PATH = MAP_DIR / "reports" / "source_to_skill_map_audit.json"

REQUIRED_COLUMNS = (
    "sefer",
    "perek",
    "pasuk",
    "ref",
    "hebrew_word_or_phrase",
    "clean_hebrew_no_nikud",
    "source_translation_metsudah",
    "alternate_translation",
    "secondary_translation_koren",
    "source_id",
    "source_version_title",
    "source_license",
    "source_preference",
    "requires_attribution",
    "skill_primary",
    "skill_secondary",
    "zekelman_standard",
    "difficulty_level",
    "question_allowed",
    "runtime_allowed",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "extraction_review_status",
    "review_notes",
    "uncertainty_reason",
)

OPTIONAL_KOREN_POLICY_COLUMNS = (
    "secondary_source_id",
    "secondary_source_version_title",
    "secondary_source_license",
    "secondary_source_preference",
    "secondary_commercial_use_allowed",
)

PROOF_REQUIRED_COLUMNS = (
    "sefer",
    "perek",
    "pasuk",
    "ref",
    "hebrew_word_or_phrase",
    "clean_hebrew_no_nikud",
    "source_translation_metsudah",
    "alternate_translation",
    "secondary_translation_koren",
    "source_id",
    "source_version_title",
    "source_license",
    "source_preference",
    "requires_attribution",
    "shoresh",
    "prefixes",
    "suffixes",
    "tense",
    "part_of_speech",
    "dikduk_feature",
    "skill_primary",
    "skill_secondary",
    "skill_id",
    "zekelman_standard",
    "difficulty_level",
    "question_allowed",
    "question_type_allowed",
    "blocked_question_types",
    "runtime_allowed",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "extraction_review_status",
    "review_notes",
    "uncertainty_reason",
    "source_files_used",
)

ALLOWED_SOURCE_PREFERENCES = {
    "primary_preferred_translation_source",
    "secondary_noncommercial_translation_support",
}

ALLOWED_EXTRACTION_REVIEW_STATUSES = {
    "pending_yossi_extraction_accuracy_pass",
    "yossi_extraction_verified",
    "needs_specific_confirmation",
    "blocked_unclear_source",
}

OPEN_QUESTION_ALLOWED_VALUES = {"no", "needs_review", "false", ""}
CLOSED_BOOLEAN_VALUES = {"false", "no", ""}
FORBIDDEN_READY_VALUES = {
    "runtime_ready",
    "question_ready",
    "student_facing",
    "reviewed_bank_ready",
    "protected_preview_ready",
    "approved",
    "promoted",
}

REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy confirmation for trusted source-derived content",
    "not generated-question review",
    "not runtime approval",
)

PROOF_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not runtime approval",
)

PROOF_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed the Bereishis 1:1-1:5 source-to-skill proof map",
    "verified all rows for extraction accuracy",
    "not runtime approval",
    "not question approval",
    "Question allowed: `needs_review`",
)

NEXT_SLICE_REVIEW_PACKET_REQUIRED_PHRASES = (
    "extraction-accuracy and mapping confirmation for trusted source-derived content",
    "not generated-question review",
    "not question approval",
    "not protected-preview approval",
    "not reviewed-bank approval",
    "not runtime approval",
)

NEXT_SLICE_BUILD_REPORT_REQUIRED_PHRASES = (
    "pending Yossi extraction-accuracy review",
    "does not authorize question generation",
    "runtime activation",
)

NEXT_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES = (
    "Yossi reviewed and verified all 37 rows",
    "extraction-accuracy confirmation only",
    "Not question approval",
    "Not protected-preview approval",
    "Not runtime approval",
    "`question_allowed` remains `needs_review`",
    "`runtime_allowed` remains `false`",
)

REVIEW_PACKET_FORBIDDEN_PHRASES = (
    "approved for runtime",
    "runtime-ready",
    "question-ready",
    "student-facing approved",
)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def normalized(value: object) -> str:
    return str(value or "").strip()


def validate_required_files(errors: list[str]) -> None:
    if not MAP_DIR.exists():
        errors.append("data/verified_source_skill_maps directory is missing")
    if not SEED_MAP_PATH.exists():
        errors.append(f"required seed source-to-skill map missing: {repo_relative(SEED_MAP_PATH)}")
    if not PROOF_MAP_PATH.exists():
        errors.append(f"required proof source-to-skill map missing: {repo_relative(PROOF_MAP_PATH)}")
    if not SEED_REVIEW_PACKET_PATH.exists():
        errors.append(f"required source-to-skill review packet missing: {repo_relative(SEED_REVIEW_PACKET_PATH)}")
    if not PROOF_REVIEW_PACKET_PATH.exists():
        errors.append(f"required proof source-to-skill review packet missing: {repo_relative(PROOF_REVIEW_PACKET_PATH)}")
    if not PROOF_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required proof source-to-skill extraction verification report missing: {repo_relative(PROOF_VERIFICATION_REPORT_PATH)}"
        )
    if not NEXT_SLICE_MAP_PATH.exists():
        errors.append(f"required pending expansion source-to-skill map missing: {repo_relative(NEXT_SLICE_MAP_PATH)}")
    if not NEXT_SLICE_BUILD_REPORT_PATH.exists():
        errors.append(f"required pending expansion build report missing: {repo_relative(NEXT_SLICE_BUILD_REPORT_PATH)}")
    if not NEXT_SLICE_REVIEW_PACKET_PATH.exists():
        errors.append(f"required pending expansion review packet missing: {repo_relative(NEXT_SLICE_REVIEW_PACKET_PATH)}")
    if not NEXT_SLICE_VERIFICATION_REPORT_PATH.exists():
        errors.append(
            f"required next-slice extraction verification report missing: {repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH)}"
        )
    if not AUDIT_REPORT_PATH.exists():
        errors.append(f"required source-to-skill audit report missing: {repo_relative(AUDIT_REPORT_PATH)}")


def validate_review_packet(errors: list[str]) -> None:
    if not SEED_REVIEW_PACKET_PATH.exists():
        return
    text = SEED_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
    for phrase in REVIEW_PACKET_REQUIRED_PHRASES:
        if phrase not in text:
            errors.append(
                f"{repo_relative(SEED_REVIEW_PACKET_PATH)} is missing required extraction-accuracy language: {phrase!r}"
            )
    for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
        if phrase in text and f"not {phrase}" not in text:
            errors.append(
                f"{repo_relative(SEED_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
            )
    if PROOF_REVIEW_PACKET_PATH.exists():
        proof_text = PROOF_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in PROOF_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in proof_text:
                errors.append(
                    f"{repo_relative(PROOF_REVIEW_PACKET_PATH)} is missing required proof review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in proof_text and f"not {phrase}" not in proof_text:
                errors.append(
                    f"{repo_relative(PROOF_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if PROOF_VERIFICATION_REPORT_PATH.exists():
        verification_text = PROOF_VERIFICATION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in PROOF_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in verification_text:
                errors.append(
                    f"{repo_relative(PROOF_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in verification_text and f"not {phrase}" not in verification_text:
                errors.append(
                    f"{repo_relative(PROOF_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if NEXT_SLICE_REVIEW_PACKET_PATH.exists():
        next_text = NEXT_SLICE_REVIEW_PACKET_PATH.read_text(encoding="utf-8")
        for phrase in NEXT_SLICE_REVIEW_PACKET_REQUIRED_PHRASES:
            if phrase not in next_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_REVIEW_PACKET_PATH)} is missing required pending-slice review language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in next_text and f"not {phrase}" not in next_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_REVIEW_PACKET_PATH)} contains forbidden readiness language: {phrase!r}"
                )
    if NEXT_SLICE_BUILD_REPORT_PATH.exists():
        build_text = NEXT_SLICE_BUILD_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in NEXT_SLICE_BUILD_REPORT_REQUIRED_PHRASES:
            if phrase not in build_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_BUILD_REPORT_PATH)} is missing required build-report language: {phrase!r}"
                )
    if NEXT_SLICE_VERIFICATION_REPORT_PATH.exists():
        next_verification_text = NEXT_SLICE_VERIFICATION_REPORT_PATH.read_text(encoding="utf-8")
        for phrase in NEXT_SLICE_VERIFICATION_REPORT_REQUIRED_PHRASES:
            if phrase not in next_verification_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH)} is missing required verification language: {phrase!r}"
                )
        for phrase in REVIEW_PACKET_FORBIDDEN_PHRASES:
            if phrase in next_verification_text and f"not {phrase}" not in next_verification_text:
                errors.append(
                    f"{repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH)} contains forbidden readiness language: {phrase!r}"
                )


def validate_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(SEED_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")

    if normalized(row.get("source_translation_metsudah")):
        if row.get("source_license") != "CC-BY":
            errors.append(f"Map row {ref} / {clean_hebrew} has Metsudah translation but source_license is not CC-BY")
        if row.get("source_version_title") != "Metsudah Chumash, Metsudah Publications, 2009":
            errors.append(f"Map row {ref} / {clean_hebrew} has unexpected Metsudah source_version_title")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"Map row {ref} / {clean_hebrew} must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"Map row {ref} / {clean_hebrew} has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")):
        if row.get("secondary_source_license") != "CC-BY-NC":
            errors.append(f"Map row {ref} / {clean_hebrew} has Koren secondary translation but secondary_source_license is not CC-BY-NC")
        if row.get("secondary_source_preference") != "secondary_noncommercial_translation_support":
            errors.append(f"Map row {ref} / {clean_hebrew} must mark Koren as secondary_noncommercial_translation_support")
        if row.get("secondary_commercial_use_allowed") != "false":
            errors.append(f"Map row {ref} / {clean_hebrew} must not mark Koren commercial use as allowed")

    if row.get("source_preference") and row["source_preference"] not in ALLOWED_SOURCE_PREFERENCES:
        errors.append(f"{context}: source_preference must be one of {sorted(ALLOWED_SOURCE_PREFERENCES)}")

    extraction_status = row.get("extraction_review_status")
    if extraction_status not in ALLOWED_EXTRACTION_REVIEW_STATUSES:
        errors.append(f"{context}: extraction_review_status must be one of {sorted(ALLOWED_EXTRACTION_REVIEW_STATUSES)}")
    if extraction_status == "pending_yossi_extraction_accuracy_pass":
        if "Yossi" not in row.get("review_notes", ""):
            errors.append(f"{context}: pending rows should clearly name Yossi extraction-accuracy confirmation in review_notes")

    if row.get("question_allowed") not in OPEN_QUESTION_ALLOWED_VALUES:
        errors.append(f"{context}: question_allowed must remain no/needs_review/false until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) not in CLOSED_BOOLEAN_VALUES:
            errors.append(f"{context}: {field} must remain false/no/blank until a future gate")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")

    if (not normalized(row.get("zekelman_standard")) or not normalized(row.get("difficulty_level"))) and not normalized(
        row.get("uncertainty_reason")
    ):
        errors.append(f"{context}: missing standards/difficulty fields require uncertainty_reason")


def validate_proof_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(PROOF_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"Map row {ref} / {clean_hebrew} has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"Map row {ref} / {clean_hebrew} has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"Map row {ref} / {clean_hebrew} must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"Map row {ref} / {clean_hebrew} has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"Map row {ref} / {clean_hebrew} has Koren secondary translation but source_files_used omits Koren JSONL")

    if row.get("question_allowed") not in OPEN_QUESTION_ALLOWED_VALUES:
        errors.append(f"{context}: question_allowed must remain no/needs_review/false until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) not in CLOSED_BOOLEAN_VALUES:
            errors.append(f"{context}: {field} must remain false/no/blank until a future gate")
    if row.get("extraction_review_status") not in ALLOWED_EXTRACTION_REVIEW_STATUSES:
        errors.append(f"{context}: extraction_review_status must be one of {sorted(ALLOWED_EXTRACTION_REVIEW_STATUSES)}")
    if row.get("extraction_review_status") == "yossi_extraction_verified" and not PROOF_VERIFICATION_REPORT_PATH.exists():
        errors.append(f"{context}: yossi_extraction_verified rows require {repo_relative(PROOF_VERIFICATION_REPORT_PATH)}")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: proof-map rows must explain uncertainty_reason")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_pending_expansion_row(row: dict[str, str], row_number: int, errors: list[str]) -> None:
    context = f"{repo_relative(NEXT_SLICE_MAP_PATH)} row {row_number}"
    ref = normalized(row.get("ref")) or f"row {row_number}"
    hebrew = normalized(row.get("hebrew_word_or_phrase"))
    clean_hebrew = normalized(row.get("clean_hebrew_no_nikud"))

    if not ref:
        errors.append(f"{context}: ref must be populated")
    if not hebrew:
        errors.append(f"{context}: hebrew_word_or_phrase must be populated")
    if not clean_hebrew:
        errors.append(f"{context}: clean_hebrew_no_nikud must be populated")
    if not normalized(row.get("source_files_used")):
        errors.append(f"{context}: source_files_used must record the contributing source paths")

    if normalized(row.get("source_translation_metsudah")):
        if "CC-BY" not in row.get("source_license", ""):
            errors.append(f"{context}: has Metsudah translation but source_license does not include CC-BY")
        if "Metsudah Chumash, Metsudah Publications, 2009" not in row.get("source_version_title", ""):
            errors.append(f"{context}: has Metsudah translation but source_version_title is missing Metsudah")
        if row.get("source_preference") != "primary_preferred_translation_source":
            errors.append(f"{context}: must mark Metsudah as primary_preferred_translation_source")
        if row.get("requires_attribution") != "true":
            errors.append(f"{context}: has source translation but requires_attribution is not true")

    if normalized(row.get("secondary_translation_koren")) and "bereishis_english_koren.jsonl" not in row.get(
        "source_files_used",
        "",
    ):
        errors.append(f"{context}: has Koren secondary translation but source_files_used omits Koren JSONL")

    extraction_status = row.get("extraction_review_status")
    if extraction_status not in {"pending_yossi_extraction_accuracy_pass", "yossi_extraction_verified"}:
        errors.append(f"{context}: extraction_review_status must remain pending or yossi_extraction_verified")
    if extraction_status == "pending_yossi_extraction_accuracy_pass" and "Yossi" not in row.get("review_notes", ""):
        errors.append(f"{context}: pending rows should clearly name Yossi extraction-accuracy confirmation in review_notes")
    if extraction_status == "yossi_extraction_verified":
        if not NEXT_SLICE_VERIFICATION_REPORT_PATH.exists():
            errors.append(
                f"{context}: yossi_extraction_verified rows require {repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH)}"
            )
        if "Yossi confirmed extraction accuracy" not in row.get("review_notes", ""):
            errors.append(f"{context}: verified rows must record Yossi extraction-accuracy confirmation in review_notes")
    if row.get("question_allowed") != "needs_review":
        errors.append(f"{context}: question_allowed must remain needs_review until a future gate")
    for field in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
        if row.get(field) != "false":
            errors.append(f"{context}: {field} must remain false until a future gate")
    if not normalized(row.get("uncertainty_reason")):
        errors.append(f"{context}: pending expansion rows must explain uncertainty_reason")
    if not normalized(row.get("blocked_question_types")):
        errors.append(f"{context}: blocked_question_types must explain that question use is blocked")

    for field, value in row.items():
        lowered = normalized(value).lower()
        if field not in {"review_notes", "uncertainty_reason", "blocked_question_types"} and lowered in FORBIDDEN_READY_VALUES:
            errors.append(f"{context}: field {field} contains forbidden readiness value {value!r}")


def validate_audit_report(errors: list[str]) -> None:
    if not AUDIT_REPORT_PATH.exists():
        return
    try:
        audit = json.loads(AUDIT_REPORT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} is invalid JSON: {error}")
        return
    if audit.get("audit_finding") != "partial_not_full_canonical_map":
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} must record audit_finding partial_not_full_canonical_map")
    if audit.get("shortest_path_decision") != "C_existing_data_is_partial_create_small_proof_consolidation_map":
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} must record shortest path decision C")
    if audit.get("map_created") != repo_relative(PROOF_MAP_PATH):
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} must link the proof map path")
    if not isinstance(audit.get("field_coverage"), list) or not audit["field_coverage"]:
        errors.append(f"{repo_relative(AUDIT_REPORT_PATH)} must include field_coverage entries")


def validate_verified_source_skill_maps() -> dict[str, Any]:
    errors: list[str] = []
    validate_required_files(errors)
    validate_review_packet(errors)
    validate_audit_report(errors)

    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if SEED_MAP_PATH.exists():
        columns, rows = load_tsv(SEED_MAP_PATH)
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in columns]
        if missing_columns:
            errors.append(f"{repo_relative(SEED_MAP_PATH)} missing required columns: {missing_columns}")
        for column in OPTIONAL_KOREN_POLICY_COLUMNS:
            if column not in columns:
                errors.append(f"{repo_relative(SEED_MAP_PATH)} missing Koren policy column: {column}")
        for row_number, row in enumerate(rows, 2):
            validate_row(row, row_number, errors)
    proof_rows: list[dict[str, str]] = []
    proof_columns: list[str] = []
    if PROOF_MAP_PATH.exists():
        proof_columns, proof_rows = load_tsv(PROOF_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in proof_columns]
        if missing_columns:
            errors.append(f"{repo_relative(PROOF_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(proof_rows, 2):
            validate_proof_row(row, row_number, errors)
    next_slice_rows: list[dict[str, str]] = []
    next_slice_columns: list[str] = []
    if NEXT_SLICE_MAP_PATH.exists():
        next_slice_columns, next_slice_rows = load_tsv(NEXT_SLICE_MAP_PATH)
        missing_columns = [column for column in PROOF_REQUIRED_COLUMNS if column not in next_slice_columns]
        if missing_columns:
            errors.append(f"{repo_relative(NEXT_SLICE_MAP_PATH)} missing required columns: {missing_columns}")
        for row_number, row in enumerate(next_slice_rows, 2):
            validate_pending_expansion_row(row, row_number, errors)

    return {
        "valid": not errors,
        "map_path": repo_relative(SEED_MAP_PATH),
        "proof_map_path": repo_relative(PROOF_MAP_PATH),
        "review_packet_path": repo_relative(SEED_REVIEW_PACKET_PATH),
        "proof_review_packet_path": repo_relative(PROOF_REVIEW_PACKET_PATH),
        "proof_verification_report_path": repo_relative(PROOF_VERIFICATION_REPORT_PATH),
        "next_slice_map_path": repo_relative(NEXT_SLICE_MAP_PATH),
        "next_slice_build_report_path": repo_relative(NEXT_SLICE_BUILD_REPORT_PATH),
        "next_slice_review_packet_path": repo_relative(NEXT_SLICE_REVIEW_PACKET_PATH),
        "next_slice_verification_report_path": repo_relative(NEXT_SLICE_VERIFICATION_REPORT_PATH),
        "audit_report_path": repo_relative(AUDIT_REPORT_PATH),
        "row_count": len(rows),
        "proof_row_count": len(proof_rows),
        "next_slice_row_count": len(next_slice_rows),
        "columns": columns,
        "proof_columns": proof_columns,
        "next_slice_columns": next_slice_columns,
        "errors": errors,
    }


def main() -> int:
    summary = validate_verified_source_skill_maps()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
