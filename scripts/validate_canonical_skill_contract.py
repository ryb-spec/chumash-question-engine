from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import skill_catalog


CONTRACT_PATH = ROOT / "data" / "standards" / "canonical_skill_contract.json"
ENRICHMENT_FILES = [
    ROOT / "data" / "source_skill_enrichment" / "morphology_candidates" / "bereishis_1_1_to_1_5_morphology_candidates.tsv",
    ROOT / "data" / "source_skill_enrichment" / "standards_candidates" / "bereishis_1_1_to_1_5_standards_candidates.tsv",
    ROOT / "data" / "source_skill_enrichment" / "vocabulary_shoresh_candidates" / "bereishis_1_1_to_1_5_vocabulary_shoresh_candidates.tsv",
]
VERIFIED_MAP_FILES = [
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_1_to_3_24_metsudah_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_1_to_1_5_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_6_to_1_13_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_14_to_1_23_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_24_to_1_31_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_2_1_to_2_3_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_2_4_to_2_17_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_2_18_to_2_25_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_3_1_to_3_7_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_3_8_to_3_16_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_3_17_to_3_24_source_to_skill_map.tsv",
]
ZEKELMAN_DRAFT_PATH = (
    ROOT / "data" / "standards" / "zekelman" / "crosswalks" / "zekelman_2025_standard_3_skill_mapping_draft.json"
)
EXPECTED_ACTIVE_SCOPE = "local_parsed_bereishis_1_1_to_3_24"
EXPECTED_SOURCE_SHA = "4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71"
ALLOWED_CANONICAL_STATUSES = {
    "review_only",
    "source_extraction_verified",
    "teacher_approved_input_candidate",
    "teacher_approved_for_protected_preview",
    "protected_preview_only",
    "reviewed_bank_candidate",
    "runtime_ready",
}
ALLOWED_MAPPING_STATUSES = {
    "review_only",
    "source_extraction_verified",
    "runtime_ready",
}
CANONICAL_SKILL_REQUIRED_FIELDS = {
    "canonical_skill_id",
    "display_name",
    "plain_english_definition",
    "student_task_definition",
    "skill_lane",
    "related_runtime_skill_ids",
    "related_question_types",
    "related_zekelman_standard_ids",
    "source_skill_labels_allowed",
    "enrichment_labels_allowed",
    "status",
    "allowed_usage",
    "forbidden_usage",
    "evidence_required_for_next_status",
    "review_notes",
}


def repo_relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def label_mapping_key(label_type: str, label: str) -> tuple[str, str]:
    return label_type, label.strip()


def validate_canonical_skill_contract(contract_path: Path | None = None) -> dict[str, object]:
    path = contract_path or CONTRACT_PATH
    errors: list[str] = []
    if not path.exists():
        return {"valid": False, "errors": [f"missing contract file: {repo_relative(path)}"]}

    contract = load_json(path)
    metadata = contract.get("metadata", {})
    canonical_skills = contract.get("canonical_skills", [])
    runtime_mappings = contract.get("runtime_skill_mappings", [])
    zekelman_mappings = contract.get("zekelman_skill_mappings", [])
    verified_label_mappings = contract.get("verified_source_skill_label_mappings", [])
    enrichment_candidate_mappings = contract.get("source_skill_enrichment_candidate_mappings", [])

    if metadata.get("active_source_scope") != EXPECTED_ACTIVE_SCOPE:
        errors.append("contract metadata.active_source_scope must remain local_parsed_bereishis_1_1_to_3_24")
    if metadata.get("canonical_source_sha") != EXPECTED_SOURCE_SHA:
        errors.append("contract metadata.canonical_source_sha must remain the expected Bereishis canonical SHA")
    if set(metadata.get("allowed_statuses", [])) != ALLOWED_CANONICAL_STATUSES:
        errors.append("contract metadata.allowed_statuses must match the supported canonical status model")

    canonical_ids: set[str] = set()
    canonical_skill_map: dict[str, dict] = {}
    for index, record in enumerate(canonical_skills):
        missing = sorted(CANONICAL_SKILL_REQUIRED_FIELDS - set(record))
        if missing:
            errors.append(f"canonical_skills[{index}] missing required fields: {missing}")
        canonical_skill_id = record.get("canonical_skill_id")
        if not canonical_skill_id:
            errors.append(f"canonical_skills[{index}] missing canonical_skill_id")
            continue
        if canonical_skill_id in canonical_ids:
            errors.append(f"duplicate canonical_skill_id: {canonical_skill_id}")
        canonical_ids.add(canonical_skill_id)
        canonical_skill_map[canonical_skill_id] = record
        if record.get("status") not in ALLOWED_CANONICAL_STATUSES:
            errors.append(f"{canonical_skill_id}: unsupported status {record.get('status')!r}")
        for field in (
            "related_runtime_skill_ids",
            "related_question_types",
            "related_zekelman_standard_ids",
            "source_skill_labels_allowed",
            "enrichment_labels_allowed",
            "allowed_usage",
            "forbidden_usage",
        ):
            if not isinstance(record.get(field), list):
                errors.append(f"{canonical_skill_id}: {field} must be a list")
        if record.get("status") != "runtime_ready":
            if any("runtime" in str(item) for item in record.get("allowed_usage", [])):
                errors.append(f"{canonical_skill_id}: non-runtime-ready skills must not advertise runtime usage")
        if record.get("status") == "runtime_ready" and not record.get("related_runtime_skill_ids"):
            errors.append(f"{canonical_skill_id}: runtime_ready skills must list at least one runtime skill id")

    runtime_contract_map = {item["runtime_skill_id"]: item for item in runtime_mappings if item.get("runtime_skill_id")}
    runtime_skill_ids = set(skill_catalog.skill_ids_in_runtime_order())
    if set(runtime_contract_map) != runtime_skill_ids:
        missing = sorted(runtime_skill_ids - set(runtime_contract_map))
        extra = sorted(set(runtime_contract_map) - runtime_skill_ids)
        errors.append(f"runtime_skill_mappings must cover exactly runtime skills; missing={missing}, extra={extra}")
    for runtime_skill_id in runtime_skill_ids:
        mapping = runtime_contract_map.get(runtime_skill_id)
        if mapping is None:
            continue
        if mapping.get("mapping_status") != "runtime_ready":
            errors.append(f"{runtime_skill_id}: runtime mapping status must be runtime_ready")
        contract_ids = mapping.get("canonical_skill_ids", [])
        if not isinstance(contract_ids, list) or not contract_ids:
            errors.append(f"{runtime_skill_id}: canonical_skill_ids must be a non-empty list")
            continue
        for canonical_skill_id in contract_ids:
            if canonical_skill_id not in canonical_skill_map:
                errors.append(f"{runtime_skill_id}: unknown canonical skill {canonical_skill_id}")
        existing_ids = skill_catalog.canonical_skill_ids_for_runtime_skill(runtime_skill_id)
        if contract_ids != existing_ids:
            errors.append(
                f"{runtime_skill_id}: contract mapping {contract_ids} does not match skill_catalog mapping {existing_ids}"
            )
        for evidence_path in mapping.get("evidence_paths", []):
            if not (ROOT / evidence_path).exists():
                errors.append(f"{runtime_skill_id}: missing runtime evidence path {evidence_path}")

    zekelman_draft = load_json(ZEKELMAN_DRAFT_PATH)
    expected_draft_ids = {
        entry["skill_id_draft"]
        for entry in zekelman_draft.get("mappings", [])
        if entry.get("skill_id_draft")
    }
    zekelman_contract_map = {
        item["zekelman_skill_id"]: item for item in zekelman_mappings if item.get("zekelman_skill_id")
    }
    if set(zekelman_contract_map) != expected_draft_ids:
        missing = sorted(expected_draft_ids - set(zekelman_contract_map))
        extra = sorted(set(zekelman_contract_map) - expected_draft_ids)
        errors.append(f"zekelman_skill_mappings must cover exactly draft skill ids; missing={missing}, extra={extra}")
    for item in zekelman_mappings:
        mapping_status = item.get("mapping_status")
        if mapping_status not in ALLOWED_MAPPING_STATUSES - {"runtime_ready"}:
            errors.append(f"{item.get('zekelman_skill_id', '<blank>')}: invalid Zekelman mapping status {mapping_status!r}")
        for canonical_skill_id in item.get("canonical_skill_ids", []):
            if canonical_skill_id not in canonical_skill_map:
                errors.append(f"{item.get('zekelman_skill_id', '<blank>')}: unknown canonical skill {canonical_skill_id}")
        for evidence_path in item.get("evidence_paths", []):
            if not (ROOT / evidence_path).exists():
                errors.append(f"{item.get('zekelman_skill_id', '<blank>')}: missing Zekelman evidence path {evidence_path}")

    verified_label_map = {
        label_mapping_key(item.get("label_type", ""), item.get("label", "")): item
        for item in verified_label_mappings
        if item.get("label_type") and item.get("label")
    }
    found_labels: set[tuple[str, str]] = set()
    for verified_map_path in VERIFIED_MAP_FILES:
        for row in load_tsv(verified_map_path):
            for label_type in ("skill_primary", "skill_secondary", "skill_id"):
                label = (row.get(label_type) or "").strip()
                if label:
                    found_labels.add(label_mapping_key(label_type, label))
            if row.get("question_allowed") not in {"needs_review", "no", "false", ""}:
                errors.append(f"{repo_relative(verified_map_path)} row {row.get('ref')}: question_allowed must remain closed")
            for field_name in ("runtime_allowed", "protected_preview_allowed", "reviewed_bank_allowed"):
                if row.get(field_name) != "false":
                    errors.append(f"{repo_relative(verified_map_path)} row {row.get('ref')}: {field_name} must remain false")
    if set(verified_label_map) != found_labels:
        missing = sorted(found_labels - set(verified_label_map))
        extra = sorted(set(verified_label_map) - found_labels)
        errors.append(f"verified_source_skill_label_mappings must cover exactly source-map labels; missing={missing}, extra={extra}")
    for key, item in verified_label_map.items():
        if item.get("mapping_status") != "source_extraction_verified":
            errors.append(f"{key}: verified source label mappings must stay source_extraction_verified")
        for canonical_skill_id in item.get("canonical_skill_ids", []):
            if canonical_skill_id not in canonical_skill_map:
                errors.append(f"{key}: unknown canonical skill {canonical_skill_id}")
        for evidence_path in item.get("evidence_paths", []):
            if not (ROOT / evidence_path).exists():
                errors.append(f"{key}: missing verified-source evidence path {evidence_path}")

    enrichment_candidate_map = {
        item["candidate_id"]: item for item in enrichment_candidate_mappings if item.get("candidate_id")
    }
    enrichment_rows: list[tuple[Path, dict[str, str]]] = []
    for enrichment_path in ENRICHMENT_FILES:
        for row in load_tsv(enrichment_path):
            enrichment_rows.append((enrichment_path, row))
            candidate_id = row.get("candidate_id", "")
            if candidate_id not in enrichment_candidate_map:
                errors.append(f"{repo_relative(enrichment_path)} missing candidate mapping for {candidate_id}")
                continue
            mapping = enrichment_candidate_map[candidate_id]
            if mapping.get("mapping_status") not in ALLOWED_MAPPING_STATUSES - {"runtime_ready"}:
                errors.append(f"{candidate_id}: enrichment mapping status must stay review_only or source_extraction_verified")
            for canonical_skill_id in mapping.get("canonical_skill_ids", []):
                if canonical_skill_id not in canonical_skill_map:
                    errors.append(f"{candidate_id}: unknown canonical skill {canonical_skill_id}")
            for evidence_path in mapping.get("evidence_paths", []):
                if not (ROOT / evidence_path).exists():
                    errors.append(f"{candidate_id}: missing enrichment evidence path {evidence_path}")
            if row.get("question_allowed") != "needs_review":
                errors.append(f"{candidate_id}: enrichment question_allowed must remain needs_review")
            for field_name in ("protected_preview_allowed", "runtime_allowed", "reviewed_bank_allowed"):
                if row.get(field_name) != "false":
                    errors.append(f"{candidate_id}: enrichment {field_name} must remain false")
            proposed_skill_id = (row.get("proposed_skill_id") or "").strip()
            if proposed_skill_id and proposed_skill_id != "needs_mapping_review" and proposed_skill_id not in zekelman_contract_map:
                errors.append(f"{candidate_id}: proposed_skill_id {proposed_skill_id!r} must exist in Zekelman contract mappings")

    all_candidate_ids = {row.get("candidate_id", "") for _, row in enrichment_rows}
    if set(enrichment_candidate_map) != all_candidate_ids:
        missing = sorted(all_candidate_ids - set(enrichment_candidate_map))
        extra = sorted(set(enrichment_candidate_map) - all_candidate_ids)
        errors.append(f"source_skill_enrichment_candidate_mappings must cover exactly enrichment candidates; missing={missing}, extra={extra}")

    summary = {
        "valid": not errors,
        "contract_path": repo_relative(path),
        "canonical_skill_count": len(canonical_skills),
        "runtime_skill_mapping_count": len(runtime_mappings),
        "zekelman_skill_mapping_count": len(zekelman_mappings),
        "verified_source_label_mapping_count": len(verified_label_mappings),
        "source_skill_enrichment_candidate_mapping_count": len(enrichment_candidate_mappings),
        "active_source_scope": metadata.get("active_source_scope"),
        "canonical_source_sha": metadata.get("canonical_source_sha"),
        "errors": errors,
    }
    return summary


def main() -> int:
    summary = validate_canonical_skill_contract()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
