from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_HEBREW_TSV = ROOT / "data" / "source_texts" / "bereishis_hebrew_menukad_taamim.tsv"
OUTPUT_DIR = ROOT / "data" / "source_texts" / "translations" / "sefaria"

MANIFEST_PATH = OUTPUT_DIR / "bereishis_english_translations_manifest.json"
DISCOVERY_REPORT_PATH = OUTPUT_DIR / "sefaria_english_versions_genesis_report.json"
LICENSE_REPORT_PATH = OUTPUT_DIR / "bereishis_english_translation_license_report.md"
ALIGNMENT_REPORT_PATH = OUTPUT_DIR / "bereishis_english_translation_alignment_report.md"
FETCH_REPORT_PATH = OUTPUT_DIR / "bereishis_english_translation_fetch_report.json"
README_PATH = OUTPUT_DIR / "README.md"
LICENSE_REVIEW_MATRIX_PATH = OUTPUT_DIR / "bereishis_english_translation_license_review_matrix.json"
HUMAN_REVIEW_PACKET_PATH = OUTPUT_DIR / "bereishis_english_translation_human_review_packet.md"
TRANSLATION_REGISTRY_PATH = ROOT / "data" / "source_texts" / "translations" / "translation_sources_registry.json"
RECONCILIATION_REPORT_MD_PATH = ROOT / "data" / "source_texts" / "reports" / "bereishis_hebrew_source_reconciliation_report.md"
RECONCILIATION_REPORT_JSON_PATH = ROOT / "data" / "source_texts" / "reports" / "bereishis_hebrew_source_reconciliation_report.json"

JSONL_PATHS = {
    "koren": OUTPUT_DIR / "bereishis_english_koren.jsonl",
    "metsudah": OUTPUT_DIR / "bereishis_english_metsudah.jsonl",
}

REQUIRED_ROW_FIELDS = {
    "sefer",
    "perek",
    "pasuk",
    "ref",
    "hebrew_ref",
    "canonical_hebrew_source_ref",
    "translation_version_key",
    "translation_version_title",
    "translation_language",
    "translation_text",
    "source",
    "source_api_endpoint",
    "source_url",
    "retrieved_at",
    "license",
    "license_vetted",
    "license_note",
    "provenance",
    "status",
}

REQUIRED_PROVENANCE_FIELDS = {
    "versionTitle",
    "versionSource",
    "versionNotes",
    "versionTitleInHebrew",
    "shortVersionTitle",
}

FORBIDDEN_STATUSES = {
    "approved",
    "reviewed",
    "production",
    "production_ready",
    "runtime_active",
    "active",
}


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError as error:
                raise ValueError(f"{repo_relative(path)} line {line_number}: invalid JSON ({error})") from error
            if not isinstance(payload, dict):
                raise ValueError(f"{repo_relative(path)} line {line_number}: expected JSON object")
            rows.append(payload)
    return rows


def load_canonical_ref_lookup() -> dict[str, dict[str, Any]]:
    with CANONICAL_HEBREW_TSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
    lookup: dict[str, dict[str, Any]] = {}
    for row in rows:
        english_ref = f"Genesis {int(row['perek'])}:{int(row['pasuk'])}"
        lookup[english_ref] = row
    return lookup


def nonempty_file(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def validate_translation_rows(
    *,
    target_key: str,
    rows: list[dict[str, Any]],
    manifest: dict[str, Any],
    fetch_report: dict[str, Any],
    canonical_lookup: dict[str, dict[str, Any]],
    errors: list[str],
) -> dict[str, Any]:
    seen_refs: set[str] = set()
    titles: set[str] = set()
    blank_count = 0
    duplicate_count = 0

    for row in rows:
        missing_fields = REQUIRED_ROW_FIELDS - row.keys()
        if missing_fields:
            errors.append(f"{target_key}: missing required fields {sorted(missing_fields)}")
            continue

        if row["status"] in FORBIDDEN_STATUSES:
            errors.append(f"{target_key}: forbidden row status {row['status']!r} for {row['ref']}")

        if row["translation_version_key"] != target_key:
            errors.append(
                f"{target_key}: translation_version_key mismatch for {row['ref']}: {row['translation_version_key']!r}"
            )

        ref = row["ref"]
        if ref not in canonical_lookup:
            errors.append(f"{target_key}: unexpected ref {ref!r} not found in canonical Hebrew TSV")
        else:
            canonical = canonical_lookup[ref]
            expected_hebrew_ref = canonical["ref"]
            if row["hebrew_ref"] != expected_hebrew_ref:
                errors.append(
                    f"{target_key}: hebrew_ref mismatch for {ref}: expected {expected_hebrew_ref!r}, got {row['hebrew_ref']!r}"
                )

        if ref in seen_refs:
            duplicate_count += 1
            errors.append(f"{target_key}: duplicate ref {ref!r}")
        else:
            seen_refs.add(ref)

        if not isinstance(row["provenance"], dict):
            errors.append(f"{target_key}: provenance must be a JSON object for {ref}")
        else:
            missing_provenance = REQUIRED_PROVENANCE_FIELDS - row["provenance"].keys()
            if missing_provenance:
                errors.append(f"{target_key}: missing provenance fields {sorted(missing_provenance)} for {ref}")

        if row["source"] != "Sefaria":
            errors.append(f"{target_key}: source must be 'Sefaria' for {ref}")

        if "fill_in_missing_segments=0" not in row["source_api_endpoint"]:
            errors.append(f"{target_key}: source_api_endpoint missing fill_in_missing_segments=0 for {ref}")

        if row["translation_text"] == "":
            blank_count += 1

        titles.add(row["translation_version_title"])

    if len(titles) > 1:
        errors.append(f"{target_key}: multiple translation_version_title values found: {sorted(titles)}")

    expected_title = manifest["exact_version_titles_used"].get(target_key)
    if titles and expected_title not in titles:
        errors.append(
            f"{target_key}: manifest exact_version_titles_used={expected_title!r} does not match JSONL title set {sorted(titles)}"
        )

    manifest_count = manifest["row_counts_by_version"].get(target_key)
    if manifest_count != len(rows):
        errors.append(
            f"{target_key}: manifest row_counts_by_version={manifest_count} does not match JSONL row count {len(rows)}"
        )

    manifest_blank = manifest["blank_rows_by_version"].get(target_key)
    if manifest_blank != blank_count:
        errors.append(
            f"{target_key}: manifest blank_rows_by_version={manifest_blank} does not match computed blank count {blank_count}"
        )

    manifest_duplicate = manifest["duplicate_refs_by_version"].get(target_key)
    if manifest_duplicate != duplicate_count:
        errors.append(
            f"{target_key}: manifest duplicate_refs_by_version={manifest_duplicate} does not match computed duplicate count {duplicate_count}"
        )

    fetch_version = fetch_report["versions"].get(target_key, {})
    if fetch_version.get("row_count") != len(rows):
        errors.append(
            f"{target_key}: fetch report row_count={fetch_version.get('row_count')} does not match JSONL row count {len(rows)}"
        )

    missing_refs = sorted(set(canonical_lookup.keys()) - seen_refs)
    if missing_refs != sorted(manifest["missing_refs_by_version"].get(target_key, [])):
        errors.append(
            f"{target_key}: manifest missing_refs_by_version does not match actual missing refs"
        )

    if missing_refs != sorted(fetch_version.get("missing_refs", [])):
        errors.append(f"{target_key}: fetch report missing_refs does not match actual missing refs")

    return {
        "row_count": len(rows),
        "missing_refs": missing_refs,
        "blank_count": blank_count,
        "duplicate_count": duplicate_count,
        "title_set": sorted(titles),
    }


def validate_bereishis_translations() -> dict[str, Any]:
    errors: list[str] = []

    required_files = [
        CANONICAL_HEBREW_TSV,
        MANIFEST_PATH,
        DISCOVERY_REPORT_PATH,
        LICENSE_REPORT_PATH,
        ALIGNMENT_REPORT_PATH,
        FETCH_REPORT_PATH,
        LICENSE_REVIEW_MATRIX_PATH,
        HUMAN_REVIEW_PACKET_PATH,
        TRANSLATION_REGISTRY_PATH,
        RECONCILIATION_REPORT_MD_PATH,
        RECONCILIATION_REPORT_JSON_PATH,
        README_PATH,
    ]
    for path in required_files:
        if not path.exists():
            errors.append(f"required file missing: {repo_relative(path)}")

    if errors:
        return {"valid": False, "errors": errors}

    canonical_lookup = load_canonical_ref_lookup()
    manifest = load_json(MANIFEST_PATH)
    discovery_report = load_json(DISCOVERY_REPORT_PATH)
    fetch_report = load_json(FETCH_REPORT_PATH)
    license_review_matrix = load_json(LICENSE_REVIEW_MATRIX_PATH)
    translation_registry = load_json(TRANSLATION_REGISTRY_PATH)
    reconciliation_report = load_json(RECONCILIATION_REPORT_JSON_PATH)

    if len(canonical_lookup) != len(set(canonical_lookup)):
        errors.append("canonical Hebrew TSV contains duplicate refs")
    if "Genesis 35:30" in canonical_lookup:
        errors.append("canonical Hebrew TSV still contains invalid Genesis 35:30 after reconciliation")
    if len(canonical_lookup) != 1533:
        errors.append(f"canonical Hebrew TSV expected reconciled count 1533, found {len(canonical_lookup)}")

    if manifest.get("canonical_hebrew_source_path") != repo_relative(CANONICAL_HEBREW_TSV):
        errors.append("manifest canonical_hebrew_source_path does not match expected canonical Hebrew TSV path")
    if manifest.get("expected_total_refs") != len(canonical_lookup):
        errors.append("manifest expected_total_refs does not match canonical Hebrew TSV ref count")
    if manifest.get("integration_status") != "source_ready_license_pending":
        errors.append("manifest integration_status must be source_ready_license_pending")
    if manifest.get("production_status") != "not_production_ready":
        errors.append("manifest production_status must be not_production_ready")
    if manifest.get("runtime_status") != "not_runtime_active":
        errors.append("manifest runtime_status must be not_runtime_active")

    request_defaults = fetch_report.get("request_defaults", {})
    if request_defaults.get("fill_in_missing_segments") != 0:
        errors.append("fetch report must record fill_in_missing_segments=0")
    if request_defaults.get("return_format") != "text_only":
        errors.append("fetch report must record return_format=text_only")

    if discovery_report.get("source_api_endpoint") != "https://www.sefaria.org/api/texts/versions/Genesis":
        errors.append("discovery report source_api_endpoint is unexpected")

    if not nonempty_file(LICENSE_REPORT_PATH):
        errors.append("license report exists but is empty")
    if not nonempty_file(ALIGNMENT_REPORT_PATH):
        errors.append("alignment report exists but is empty")
    if not nonempty_file(HUMAN_REVIEW_PACKET_PATH):
        errors.append("human review packet exists but is empty")

    if not isinstance(license_review_matrix, list) or len(license_review_matrix) != 2:
        errors.append("license review matrix must be a JSON array with one record for koren and one for metsudah")
    else:
        matrix_by_key = {entry.get("translation_version_key"): entry for entry in license_review_matrix if isinstance(entry, dict)}
        for target_key in ["koren", "metsudah"]:
            entry = matrix_by_key.get(target_key)
            if not entry:
                errors.append(f"license review matrix missing record for {target_key}")
                continue
            if entry.get("status") != "needs_license_review":
                errors.append(f"license review matrix status for {target_key} must be needs_license_review")
            if entry.get("human_review_required") is not True:
                errors.append(f"license review matrix human_review_required must be true for {target_key}")
            if entry.get("production_use_recommendation") in FORBIDDEN_STATUSES:
                errors.append(f"license review matrix contains forbidden recommendation for {target_key}")

    if not isinstance(translation_registry, dict):
        errors.append("translation registry must be a JSON object")
    else:
        if translation_registry.get("runtime_status") != "not_runtime_active":
            errors.append("translation registry runtime_status must be not_runtime_active")
        if translation_registry.get("production_status") != "not_production_ready":
            errors.append("translation registry production_status must be not_production_ready")
        if translation_registry.get("integration_status") != "source_ready_license_pending":
            errors.append("translation registry integration_status must be source_ready_license_pending")
        registry_versions = translation_registry.get("available_translation_versions")
        if not isinstance(registry_versions, list) or len(registry_versions) != 2:
            errors.append("translation registry must list two available translation versions")
        else:
            for entry in registry_versions:
                version_key = entry.get("translation_version_key")
                if version_key not in {"koren", "metsudah"}:
                    errors.append(f"translation registry contains unexpected version key {version_key!r}")
                if entry.get("runtime_eligibility") != "not_runtime_active":
                    errors.append(f"translation registry runtime_eligibility must be not_runtime_active for {version_key}")
                if entry.get("production_eligibility") != "not_production_ready":
                    errors.append(f"translation registry production_eligibility must be not_production_ready for {version_key}")
                if entry.get("source_authority") != "trusted_teacher_source":
                    errors.append(f"translation registry source_authority must be trusted_teacher_source for {version_key}")
                if entry.get("source_platform") != "Sefaria":
                    errors.append(f"translation registry source_platform must be Sefaria for {version_key}")
                if entry.get("requires_attribution") is not True:
                    errors.append(f"translation registry requires_attribution must be true for {version_key}")
                if entry.get("requires_yossi_accuracy_pass") is not True:
                    errors.append(f"translation registry requires_yossi_accuracy_pass must be true for {version_key}")
                if entry.get("extraction_review_status") != "pending_yossi_extraction_accuracy_pass":
                    errors.append(
                        f"translation registry extraction_review_status must be pending_yossi_extraction_accuracy_pass for {version_key}"
                    )
                if entry.get("question_ready_status") != "not_question_ready":
                    errors.append(f"translation registry question_ready_status must be not_question_ready for {version_key}")
                if entry.get("student_facing_status") != "not_student_facing":
                    errors.append(f"translation registry student_facing_status must be not_student_facing for {version_key}")
                if version_key == "metsudah":
                    if entry.get("source_preference") != "primary_preferred_translation_source":
                        errors.append("translation registry must mark Metsudah as primary_preferred_translation_source")
                    if entry.get("license") != "CC-BY":
                        errors.append("translation registry must keep Metsudah license as CC-BY")
                if version_key == "koren":
                    if entry.get("source_preference") != "secondary_noncommercial_translation_support":
                        errors.append("translation registry must mark Koren as secondary_noncommercial_translation_support")
                    if entry.get("license") != "CC-BY-NC":
                        errors.append("translation registry must keep Koren license as CC-BY-NC")
                    if entry.get("commercial_use_status") != "requires_direct_written_permission":
                        errors.append("translation registry must keep Koren commercial use blocked pending direct permission")

    if not isinstance(reconciliation_report, dict):
        errors.append("reconciliation report JSON must be an object")
    else:
        if reconciliation_report.get("status") != "reconciled":
            errors.append("reconciliation report status must be reconciled")
        if reconciliation_report.get("corrected_total_row_count") != len(canonical_lookup):
            errors.append("reconciliation report corrected_total_row_count does not match canonical TSV ref count")
        if reconciliation_report.get("canonical_tsv_changed") is not True:
            errors.append("reconciliation report must record canonical_tsv_changed=true")

    summaries: dict[str, Any] = {}
    for target_key, path in JSONL_PATHS.items():
        selected = manifest["selected_versions"].get(target_key)
        if not selected:
            errors.append(f"manifest missing selected_versions entry for {target_key}")
            continue

        license_status = manifest["license_status_by_version"].get(target_key)
        if not license_status:
            errors.append(f"manifest missing license_status_by_version entry for {target_key}")

        pipeline_status = selected.get("pipeline_status")
        if pipeline_status in FORBIDDEN_STATUSES:
            errors.append(f"manifest selected_versions[{target_key}] has forbidden status {pipeline_status!r}")

        if path.exists():
            rows = load_jsonl(path)
            summaries[target_key] = validate_translation_rows(
                target_key=target_key,
                rows=rows,
                manifest=manifest,
                fetch_report=fetch_report,
                canonical_lookup=canonical_lookup,
                errors=errors,
            )
            if pipeline_status != "source_fetched":
                errors.append(
                    f"{target_key}: JSONL exists at {repo_relative(path)} but manifest pipeline_status is {pipeline_status!r}"
                )
            if len(rows) != len(canonical_lookup):
                errors.append(
                    f"{target_key}: JSONL row count {len(rows)} does not match canonical Hebrew ref count {len(canonical_lookup)}"
                )
        else:
            summaries[target_key] = {
                "row_count": 0,
                "missing_refs": manifest["missing_refs_by_version"].get(target_key, []),
                "blank_count": 0,
                "duplicate_count": 0,
                "title_set": [],
            }
            if pipeline_status == "source_fetched":
                errors.append(
                    f"{target_key}: manifest says source_fetched but JSONL file is missing at {repo_relative(path)}"
                )
            if pipeline_status not in {
                "blocked_version_not_found",
                "blocked_license_unclear",
                "blocked_fetch_error",
                "version_discovered",
            }:
                errors.append(
                    f"{target_key}: missing JSONL file requires an explicit blocked or metadata-only pipeline_status, got {pipeline_status!r}"
                )

    for target_key in ["koren", "metsudah"]:
        if target_key not in fetch_report.get("versions", {}):
            errors.append(f"fetch report missing versions entry for {target_key}")
            continue
        version_report = fetch_report["versions"][target_key]
        if version_report.get("license_status") not in {
            "source_fetched",
            "needs_license_review",
            "needs_human_review",
            "blocked_version_not_found",
            "blocked_license_unclear",
            "blocked_missing_segments",
            "blocked_fetch_error",
            "version_discovered",
        }:
            errors.append(
                f"{target_key}: unexpected license/pipeline status in fetch report: {version_report.get('license_status')!r}"
            )
        if version_report.get("missing_segment_warning_detected"):
            errors.append(f"{target_key}: fetch report indicates missing-segment warning while fallback filling is supposed to stay off")
        if version_report.get("pipeline_status") == "source_fetched":
            if version_report.get("missing_refs"):
                errors.append(f"{target_key}: fetch report missing_refs must be empty after reconciliation")
            if version_report.get("extra_refs"):
                errors.append(f"{target_key}: fetch report extra_refs must be empty after reconciliation")
            if manifest["missing_refs_by_version"].get(target_key):
                errors.append(f"{target_key}: manifest missing_refs_by_version must be empty after reconciliation")

    return {
        "valid": not errors,
        "errors": errors,
        "canonical_ref_count": len(canonical_lookup),
        "koren": summaries.get("koren", {}),
        "metsudah": summaries.get("metsudah", {}),
    }


def main() -> int:
    summary = validate_bereishis_translations()
    if not summary["valid"]:
        print("Bereishis translation package validation FAILED")
        for error in summary["errors"]:
            print(f"- {error}")
        return 1

    print("Bereishis translation package validation PASSED")
    print(f"- Canonical Hebrew refs: {summary['canonical_ref_count']}")
    print(
        f"- Koren rows: {summary['koren'].get('row_count', 0)}; missing refs: {len(summary['koren'].get('missing_refs', []))}"
    )
    print(
        f"- Metsudah rows: {summary['metsudah'].get('row_count', 0)}; missing refs: {len(summary['metsudah'].get('missing_refs', []))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
