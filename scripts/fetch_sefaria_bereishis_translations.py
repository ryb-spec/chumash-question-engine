from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_HEBREW_TSV = ROOT / "data" / "source_texts" / "bereishis_hebrew_menukad_taamim.tsv"
OUTPUT_DIR = ROOT / "data" / "source_texts" / "translations" / "sefaria"
RAW_SAMPLES_DIR = OUTPUT_DIR / "raw_samples"

VERSIONS_URL = "https://www.sefaria.org/api/texts/versions/Genesis"
TEXTS_V3_BASE_URL = "https://www.sefaria.org/api/v3/texts"
TEXT_VIEW_BASE_URL = "https://www.sefaria.org"
USER_AGENT = "TorahAI-Chumash-SourcePipeline/1.0"
SCHEMA_VERSION = "1.0"

VERSIONS_RAW_PATH = OUTPUT_DIR / "sefaria_genesis_versions_raw.json"
DISCOVERY_REPORT_PATH = OUTPUT_DIR / "sefaria_english_versions_genesis_report.json"
MANIFEST_PATH = OUTPUT_DIR / "bereishis_english_translations_manifest.json"
ALIGNMENT_REPORT_PATH = OUTPUT_DIR / "bereishis_english_translation_alignment_report.md"
LICENSE_REPORT_PATH = OUTPUT_DIR / "bereishis_english_translation_license_report.md"
FETCH_REPORT_PATH = OUTPUT_DIR / "bereishis_english_translation_fetch_report.json"
LICENSE_REVIEW_MATRIX_PATH = OUTPUT_DIR / "bereishis_english_translation_license_review_matrix.json"
HUMAN_REVIEW_PACKET_PATH = OUTPUT_DIR / "bereishis_english_translation_human_review_packet.md"
TRANSLATION_REGISTRY_PATH = ROOT / "data" / "source_texts" / "translations" / "translation_sources_registry.json"
RECONCILIATION_REPORT_MD_PATH = ROOT / "data" / "source_texts" / "reports" / "bereishis_hebrew_source_reconciliation_report.md"
RECONCILIATION_REPORT_JSON_PATH = ROOT / "data" / "source_texts" / "reports" / "bereishis_hebrew_source_reconciliation_report.json"
README_PATH = OUTPUT_DIR / "README.md"

TARGET_CONFIG = {
    "koren": {
        "display_name": "Koren / The Koren Jerusalem Bible",
        "exact_titles": ["The Koren Jerusalem Bible"],
        "candidate_terms": [
            "Koren",
            "Koren Jerusalem Bible",
            "The Koren Jerusalem Bible",
        ],
        "output_jsonl": OUTPUT_DIR / "bereishis_english_koren.jsonl",
        "sample_json": RAW_SAMPLES_DIR / "koren_sample.json",
    },
    "metsudah": {
        "display_name": "Metsudah / Metsudah Chumash, Metsudah Publications, 2009",
        "exact_titles": ["Metsudah Chumash, Metsudah Publications, 2009"],
        "candidate_terms": [
            "Metsudah",
            "Metsudah Chumash",
            "Metsudah Publications",
        ],
        "output_jsonl": OUTPUT_DIR / "bereishis_english_metsudah.jsonl",
        "sample_json": RAW_SAMPLES_DIR / "metsudah_sample.json",
    },
}

PERSISTABLE_LICENSES = {
    "CC-BY",
    "CC-BY-SA",
    "CC-BY-NC",
    "CC-BY-NC-SA",
    "CC0",
}


class FetchError(RuntimeError):
    """Raised when the pipeline hits a technical fetch error."""


def iso_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch and align Sefaria English Bereishis translations against the canonical Hebrew TSV."
    )
    parser.add_argument(
        "--target",
        action="append",
        choices=["koren", "metsudah", "all"],
        help="Target version key(s) to process. Defaults to koren and metsudah.",
    )
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Discover version metadata and write reports without persisting full translation JSONL files.",
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Refetch Sefaria metadata even if cached raw metadata already exists.",
    )
    return parser.parse_args()


def normalize_targets(raw_targets: list[str] | None) -> list[str]:
    if not raw_targets:
        return ["koren", "metsudah"]
    if "all" in raw_targets:
        return ["koren", "metsudah"]
    deduped: list[str] = []
    for target in raw_targets:
        if target not in deduped:
            deduped.append(target)
    return deduped


def cached_output_paths() -> list[Path]:
    return [
        VERSIONS_RAW_PATH,
        DISCOVERY_REPORT_PATH,
        MANIFEST_PATH,
        ALIGNMENT_REPORT_PATH,
        LICENSE_REPORT_PATH,
        FETCH_REPORT_PATH,
        LICENSE_REVIEW_MATRIX_PATH,
        HUMAN_REVIEW_PACKET_PATH,
        TRANSLATION_REGISTRY_PATH,
        RECONCILIATION_REPORT_MD_PATH,
        RECONCILIATION_REPORT_JSON_PATH,
        README_PATH,
    ]


def can_reuse_cached_outputs(*, targets: list[str], expected_total_refs: int, metadata_only: bool) -> bool:
    if metadata_only:
        return False
    if not all(path.exists() for path in cached_output_paths()):
        return False
    try:
        manifest = load_json(MANIFEST_PATH)
        fetch_report = load_json(FETCH_REPORT_PATH)
    except (OSError, json.JSONDecodeError):
        return False

    if not isinstance(manifest, dict) or not isinstance(fetch_report, dict):
        return False
    if manifest.get("expected_total_refs") != expected_total_refs:
        return False

    selected_versions = manifest.get("selected_versions", {})
    version_fetch_report = fetch_report.get("versions", {})
    reusable_statuses = {
        "source_fetched",
        "blocked_version_not_found",
        "blocked_license_unclear",
        "blocked_fetch_error",
        "version_discovered",
        "needs_license_review",
    }
    for target_key in targets:
        selected = selected_versions.get(target_key)
        if not isinstance(selected, dict):
            return False
        if selected.get("pipeline_status") not in reusable_statuses:
            return False
        if target_key not in version_fetch_report:
            return False
        if selected.get("pipeline_status") == "source_fetched" and not TARGET_CONFIG[target_key]["output_jsonl"].exists():
            return False
    return True


def ensure_output_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_SAMPLES_DIR.mkdir(parents=True, exist_ok=True)


def json_dump(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_canonical_hebrew_rows() -> list[dict[str, str]]:
    if not CANONICAL_HEBREW_TSV.exists():
        raise FetchError(
            f"Canonical Hebrew TSV not found at required path: {repo_relative(CANONICAL_HEBREW_TSV)}"
        )
    with CANONICAL_HEBREW_TSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
    if not rows:
        raise FetchError("Canonical Hebrew TSV is empty.")
    return rows


def build_expected_ref_index(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], dict[int, int], dict[str, dict[str, Any]]]:
    expected_rows: list[dict[str, Any]] = []
    chapter_counts: Counter[int] = Counter()
    lookup: dict[str, dict[str, Any]] = {}
    for row in rows:
        perek = int(row["perek"])
        pasuk = int(row["pasuk"])
        english_ref = f"Genesis {perek}:{pasuk}"
        expected = {
            "sefer": row["sefer"],
            "perek": perek,
            "pasuk": pasuk,
            "hebrew_ref": row["ref"],
            "ref": english_ref,
            "canonical_hebrew_source_ref": english_ref,
        }
        expected_rows.append(expected)
        chapter_counts[perek] += 1
        lookup[english_ref] = expected
    return expected_rows, dict(sorted(chapter_counts.items())), lookup


def fetch_json(url: str, *, timeout: int = 60, retries: int = 3, backoff_seconds: float = 1.0) -> Any:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except Exception as error:  # pragma: no cover - exercised only on transient network issues
            last_error = error
            if attempt == retries:
                break
            time.sleep(backoff_seconds * attempt)
    raise FetchError(f"Failed to fetch {url}: {last_error}") from last_error


def load_or_fetch_versions(*, force_refresh: bool) -> list[dict[str, Any]]:
    if VERSIONS_RAW_PATH.exists() and not force_refresh:
        payload = load_json(VERSIONS_RAW_PATH)
    else:
        payload = fetch_json(VERSIONS_URL)
        json_dump(VERSIONS_RAW_PATH, payload)
    if not isinstance(payload, list):
        raise FetchError("Sefaria Versions API returned an unexpected payload type; expected top-level list.")
    return payload


def english_versions(versions_payload: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in versions_payload if isinstance(record, dict) and record.get("language") == "en"]


def candidate_metadata(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "versionTitle": record.get("versionTitle"),
        "language": record.get("language"),
        "license": record.get("license"),
        "licenseVetted": record.get("licenseVetted"),
        "status": record.get("status"),
        "priority": record.get("priority"),
        "shortVersionTitle": record.get("shortVersionTitle"),
        "versionTitleInHebrew": record.get("versionTitleInHebrew"),
        "versionSource": record.get("versionSource"),
        "versionNotes": record.get("versionNotes"),
        "versionNotesInHebrew": record.get("versionNotesInHebrew"),
        "versionUrl": record.get("versionUrl"),
        "digitizedBySefaria": record.get("digitizedBySefaria"),
        "purchaseInformationURL": record.get("purchaseInformationURL"),
        "purchaseInformationImage": record.get("purchaseInformationImage"),
        "actualLanguage": record.get("actualLanguage"),
        "languageFamilyName": record.get("languageFamilyName"),
        "method": record.get("method"),
    }


def find_target_candidates(target_key: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    config = TARGET_CONFIG[target_key]
    candidate_terms = [term.lower() for term in config["candidate_terms"]]
    matches: list[dict[str, Any]] = []
    for record in records:
        haystacks = [
            str(record.get("versionTitle") or ""),
            str(record.get("shortVersionTitle") or ""),
            str(record.get("versionSource") or ""),
        ]
        lowered = " | ".join(value.lower() for value in haystacks)
        if any(term in lowered for term in candidate_terms):
            matches.append(candidate_metadata(record))

    exact_record = None
    exact_title = None
    for desired_title in config["exact_titles"]:
        for record in records:
            if record.get("versionTitle") == desired_title:
                exact_record = record
                exact_title = desired_title
                break
        if exact_record is not None:
            break

    near_matches = [
        match for match in matches if match.get("versionTitle") not in set(config["exact_titles"])
    ]

    blockers: list[str] = []
    rejected_near_matches: list[dict[str, Any]] = []
    for match in near_matches:
        rejected_near_matches.append(
            {
                "versionTitle": match.get("versionTitle"),
                "reason": "Candidate matched target terms but was not the exact requested versionTitle.",
            }
        )
    if exact_record is None:
        blockers.append(
            f"No exact versionTitle match found for {target_key}: expected one of {config['exact_titles']!r}."
        )

    return {
        "target_key": target_key,
        "display_name": config["display_name"],
        "candidate_matches": matches,
        "rejected_near_matches": rejected_near_matches,
        "exact_found": exact_record is not None,
        "exact_version_title": exact_title,
        "selected_version_metadata": candidate_metadata(exact_record) if exact_record else None,
        "blockers": blockers,
    }


def classify_license(record: dict[str, Any] | None) -> dict[str, Any]:
    if not record:
        return {
            "license_status": "blocked_version_not_found",
            "allow_full_text_persist": False,
            "suitable_for_internal_draft_use": False,
            "suitable_for_future_production_use": False,
            "license_note": "Target version was not found; no license decision possible.",
        }

    license_value = record.get("license")
    if not license_value:
        return {
            "license_status": "blocked_license_unclear",
            "allow_full_text_persist": False,
            "suitable_for_internal_draft_use": False,
            "suitable_for_future_production_use": False,
            "license_note": "No license metadata was returned by Sefaria; do not persist full text.",
        }

    if license_value in PERSISTABLE_LICENSES:
        if "NC" in license_value:
            return {
                "license_status": "needs_license_review",
                "allow_full_text_persist": True,
                "suitable_for_internal_draft_use": True,
                "suitable_for_future_production_use": False,
                "license_note": (
                    f"Sefaria returned license={license_value}. This appears reusable for non-commercial internal draft work, "
                    "but future production use requires human legal review."
                ),
            }
        return {
            "license_status": "needs_license_review",
            "allow_full_text_persist": True,
            "suitable_for_internal_draft_use": True,
            "suitable_for_future_production_use": False,
            "license_note": (
                f"Sefaria returned license={license_value}. Full text was persisted for source-pipeline work, "
                "but future production use still requires human review and attribution checks."
            ),
        }

    return {
        "license_status": "blocked_license_unclear",
        "allow_full_text_persist": False,
        "suitable_for_internal_draft_use": False,
        "suitable_for_future_production_use": False,
        "license_note": (
            f"Sefaria returned license={license_value}, which this pipeline does not machine-classify as safe for full persistence."
        ),
    }


def version_text_url(version_title: str, chapter: int) -> str:
    params = urllib.parse.urlencode(
        {
            "version": f"english|{version_title}",
            "return_format": "text_only",
            "fill_in_missing_segments": "0",
        }
    )
    return f"{TEXTS_V3_BASE_URL}/Genesis.{chapter}?{params}"


def build_row(
    *,
    expected_ref: dict[str, Any],
    version_key: str,
    version_metadata: dict[str, Any],
    chapter_url: str,
    translation_text: str,
    retrieved_at: str,
    license_note: str,
) -> dict[str, Any]:
    return {
        "sefer": expected_ref["sefer"],
        "perek": expected_ref["perek"],
        "pasuk": expected_ref["pasuk"],
        "ref": expected_ref["ref"],
        "hebrew_ref": expected_ref["hebrew_ref"],
        "canonical_hebrew_source_ref": expected_ref["canonical_hebrew_source_ref"],
        "translation_version_key": version_key,
        "translation_version_title": version_metadata.get("versionTitle"),
        "translation_language": "en",
        "translation_text": translation_text,
        "source": "Sefaria",
        "source_api_endpoint": chapter_url,
        "source_url": f"{TEXT_VIEW_BASE_URL}/Genesis.{expected_ref['perek']}.{expected_ref['pasuk']}",
        "retrieved_at": retrieved_at,
        "license": version_metadata.get("license"),
        "license_vetted": version_metadata.get("licenseVetted"),
        "license_note": license_note,
        "provenance": {
            "versionTitle": version_metadata.get("versionTitle"),
            "versionSource": version_metadata.get("versionSource"),
            "versionNotes": version_metadata.get("versionNotes"),
            "versionTitleInHebrew": version_metadata.get("versionTitleInHebrew"),
            "shortVersionTitle": version_metadata.get("shortVersionTitle"),
        },
        "status": "needs_human_review",
    }


def fetch_version_rows(
    *,
    version_key: str,
    version_metadata: dict[str, Any],
    chapter_counts: dict[int, int],
    ref_lookup: dict[str, dict[str, Any]],
    license_note: str,
) -> dict[str, Any]:
    retrieved_at = iso_now()
    rows: list[dict[str, Any]] = []
    missing_refs: list[str] = []
    extra_refs: list[str] = []
    blank_refs: list[str] = []
    duplicate_refs: list[str] = []
    chapter_fetches: list[dict[str, Any]] = []
    warnings_seen: list[dict[str, Any]] = []
    seen_refs: set[str] = set()

    for chapter, expected_verse_count in chapter_counts.items():
        url = version_text_url(version_metadata["versionTitle"], chapter)
        payload = fetch_json(url)
        if not isinstance(payload, dict):
            raise FetchError(
                f"Sefaria v3 Texts API returned unexpected payload type for {version_key} chapter {chapter}: {type(payload).__name__}"
            )

        versions = payload.get("versions") or []
        version_payload = versions[0] if versions else {}
        chapter_text = version_payload.get("text") or []
        if not isinstance(chapter_text, list):
            raise FetchError(
                f"Sefaria v3 Texts API returned non-list chapter text for {version_key} chapter {chapter}."
            )

        warning_list = payload.get("warnings") or []
        if warning_list:
            warnings_seen.append({"chapter": chapter, "warnings": warning_list})

        if chapter == 1:
            sample_payload = {
                "target_key": version_key,
                "requested_version_title": version_metadata.get("versionTitle"),
                "source_api_endpoint": url,
                "retrieved_at": retrieved_at,
                "license": version_metadata.get("license"),
                "warnings": warning_list,
                "returned_version_title": version_payload.get("versionTitle"),
                "first_three_verses": chapter_text[:3],
            }
            json_dump(TARGET_CONFIG[version_key]["sample_json"], sample_payload)

        blank_count = 0
        returned_count = len(chapter_text)
        for pasuk_index, translation_text in enumerate(chapter_text, start=1):
            english_ref = f"Genesis {chapter}:{pasuk_index}"
            if pasuk_index > expected_verse_count:
                extra_refs.append(english_ref)
                continue

            if translation_text is None:
                normalized_text = ""
            else:
                normalized_text = str(translation_text)

            if not normalized_text.strip():
                blank_refs.append(english_ref)
                blank_count += 1

            if english_ref in seen_refs:
                duplicate_refs.append(english_ref)
                continue

            row = build_row(
                expected_ref=ref_lookup[english_ref],
                version_key=version_key,
                version_metadata=version_metadata,
                chapter_url=url,
                translation_text=normalized_text,
                retrieved_at=retrieved_at,
                license_note=license_note,
            )
            rows.append(row)
            seen_refs.add(english_ref)

        if returned_count < expected_verse_count:
            for pasuk_index in range(returned_count + 1, expected_verse_count + 1):
                missing_refs.append(f"Genesis {chapter}:{pasuk_index}")

        chapter_fetches.append(
            {
                "chapter": chapter,
                "source_api_endpoint": url,
                "expected_verse_count": expected_verse_count,
                "returned_verse_count": returned_count,
                "blank_row_count": blank_count,
                "missing_ref_count": max(expected_verse_count - returned_count, 0),
                "extra_ref_count": max(returned_count - expected_verse_count, 0),
                "warnings": warning_list,
            }
        )

    return {
        "rows": rows,
        "row_count": len(rows),
        "missing_refs": missing_refs,
        "extra_refs": extra_refs,
        "blank_refs": blank_refs,
        "duplicate_refs": duplicate_refs,
        "chapter_fetches": chapter_fetches,
        "warnings_seen": warnings_seen,
        "fetched": True,
        "persisted": True,
        "persist_reason": "Full text persisted because Sefaria returned a machine-readable license field.",
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_discovery_report(
    *,
    all_english_versions: list[dict[str, Any]],
    target_results: dict[str, dict[str, Any]],
    fetch_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    discovered = [candidate_metadata(record) for record in all_english_versions]
    exact_titles_used = {
        target_key: result.get("exact_version_title")
        for target_key, result in target_results.items()
    }
    target_outcomes: dict[str, Any] = {}
    for target_key, result in target_results.items():
        fetch_meta = (fetch_report or {}).get("versions", {}).get(target_key, {})
        selection_reason = (
            "Exact requested versionTitle was discovered in the Genesis Versions API response."
            if result.get("exact_found")
            else "No exact requested versionTitle was discovered, so the pipeline did not substitute a near-match."
        )
        target_outcomes[target_key] = {
            "display_name": TARGET_CONFIG[target_key]["display_name"],
            "exact_target_found": result.get("exact_found", False),
            "chosen_exact_version_title": result.get("exact_version_title"),
            "selection_reason": selection_reason,
            "reason_for_rejection_of_near_matches": result.get("rejected_near_matches", []),
            "full_text_fetched": fetch_meta.get("text_fetched", False),
            "full_text_persisted": fetch_meta.get("text_persisted", False),
            "blockers": [*result.get("blockers", []), *fetch_meta.get("blockers", [])],
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": iso_now(),
        "source_api_endpoint": VERSIONS_URL,
        "english_version_count": len(discovered),
        "all_english_versions": discovered,
        "koren_candidate_matching": target_results["koren"],
        "metsudah_candidate_matching": target_results["metsudah"],
        "chosen_exact_version_titles": exact_titles_used,
        "target_outcomes": target_outcomes,
    }


def render_license_report(manifest: dict[str, Any], fetch_report: dict[str, Any]) -> str:
    lines = [
        "# Bereishis English Translation License Report",
        "",
        f"- Generated at: `{manifest['generated_at']}`",
        f"- Production status: `{manifest['production_status']}`",
        f"- Runtime status: `{manifest['runtime_status']}`",
        "",
        "## Summary",
        "",
        "API availability is not the same as production reuse permission. This branch records the license metadata Sefaria returned and keeps both translations non-production and human-review-only.",
        "",
    ]
    for target_key in ["koren", "metsudah"]:
        selected = manifest["selected_versions"][target_key]
        lines.extend(
            [
                f"## {selected['display_name']}",
                "",
                f"- Exact versionTitle found: `{selected['exact_found']}`",
                f"- Exact versionTitle used: `{selected.get('exact_version_title')}`",
                f"- Sefaria license metadata: `{selected.get('license')}`",
                f"- License status: `{manifest['license_status_by_version'][target_key]}`",
                f"- Full text fetched: `{selected['text_fetched']}`",
                f"- Full text persisted: `{selected['text_persisted']}`",
                f"- Suitable for internal draft use: `{selected['suitable_for_internal_draft_use']}`",
                f"- Suitable for future production use: `{selected['suitable_for_future_production_use']}`",
                f"- License note: {selected['license_note']}",
                "",
            ]
        )
        blockers = fetch_report["versions"][target_key].get("blockers") or []
        if blockers:
            lines.append("### Blockers")
            lines.append("")
            for blocker in blockers:
                lines.append(f"- {blocker}")
            lines.append("")

    lines.extend(
        [
            "## Recommended next legal / human-review step",
            "",
            "- Verify the current Sefaria metadata against the publisher's intended reuse terms before any production or commercial integration.",
            "- Keep runtime integration off until legal review, content review, and alignment review are completed.",
            f"- Review the structured matrix at `{repo_relative(LICENSE_REVIEW_MATRIX_PATH)}` before any diagnostic or runtime integration work.",
            "",
        ]
    )
    return "\n".join(lines)


def render_alignment_report(
    *,
    manifest: dict[str, Any],
    fetch_report: dict[str, Any],
    chapter_counts: dict[int, int],
) -> str:
    lines = [
        "# Bereishis English Translation Alignment Report",
        "",
        f"- Generated at: `{manifest['generated_at']}`",
        f"- Canonical Hebrew source: `{manifest['canonical_hebrew_source_path']}`",
        f"- Expected canonical Hebrew refs: `{manifest['expected_total_refs']}`",
        f"- Fallback filling requested: `{fetch_report['request_defaults']['fill_in_missing_segments']}`",
        "",
        "Fallback filling remained disabled throughout this pipeline. Any missing segments are reported explicitly below.",
        "",
    ]
    for target_key in ["koren", "metsudah"]:
        target = fetch_report["versions"][target_key]
        manifest_selected = manifest["selected_versions"][target_key]
        lines.extend(
            [
                f"## {manifest_selected['display_name']}",
                "",
                f"- Exact versionTitle used: `{manifest_selected.get('exact_version_title')}`",
                f"- Rows persisted: `{manifest['row_counts_by_version'][target_key]}`",
                f"- Missing refs: `{len(manifest['missing_refs_by_version'][target_key])}`",
                f"- Extra refs: `{len(target.get('extra_refs', []))}`",
                f"- Duplicate refs: `{manifest['duplicate_refs_by_version'][target_key]}`",
                f"- Blank translation rows: `{manifest['blank_rows_by_version'][target_key]}`",
                f"- Version warnings returned by Sefaria: `{len(target.get('warnings_seen', []))}`",
                f"- Missing segment warnings returned by Sefaria: `{target.get('missing_segment_warning_detected', False)}`",
                "",
                "### Chapter-level fetch summary",
                "",
            ]
        )
        for chapter_result in target.get("chapter_fetches", []):
            lines.append(
                f"- Genesis {chapter_result['chapter']}: expected {chapter_result['expected_verse_count']}, "
                f"returned {chapter_result['returned_verse_count']}, blanks {chapter_result['blank_row_count']}, "
                f"warnings {len(chapter_result['warnings'])}"
            )
        if not target.get("chapter_fetches"):
            lines.append("- No chapter fetches were run for this target.")
        missing_refs = manifest["missing_refs_by_version"][target_key]
        if missing_refs:
            lines.append("")
            lines.append("### Missing refs")
            lines.append("")
            for missing_ref in missing_refs:
                lines.append(f"- {missing_ref}")
        lines.append("")
    lines.extend(
        [
            "## Reconciliation note",
            "",
            f"- Canonical Hebrew reconciliation report: `{repo_relative(RECONCILIATION_REPORT_MD_PATH)}`",
            f"- Canonical Hebrew reconciliation JSON: `{repo_relative(RECONCILIATION_REPORT_JSON_PATH)}`",
            "",
        ]
    )
    lines.extend(
        [
            "## Canonical chapter backbone",
            "",
            *(f"- Genesis {chapter}: {count} expected verses" for chapter, count in chapter_counts.items()),
            "",
        ]
    )
    return "\n".join(lines)


def render_readme(manifest: dict[str, Any], discovery_report: dict[str, Any]) -> str:
    koren = manifest["selected_versions"]["koren"]
    metsudah = manifest["selected_versions"]["metsudah"]
    lines = [
        "# Sefaria Bereishis English Translation Source Package",
        "",
        "This package stores a source-traceable, license-aware English translation pipeline for Sefer Bereishis.",
        "",
        "## Why this exists",
        "",
        "- Future translation-skill diagnostics need verse-aligned English text, not chapter blobs.",
        "- The canonical Hebrew TSV is the alignment backbone, so every English row maps to an existing Hebrew ref.",
        "- This package is source-ingestion only. Nothing here is runtime-active or production-approved.",
        "",
        "## Which Sefaria endpoints were used",
        "",
        f"- Version discovery: `{VERSIONS_URL}`",
        f"- Chapter text retrieval: `{TEXTS_V3_BASE_URL}/Genesis.{{chapter}}` with `version=english|{{exact versionTitle}}`, `return_format=text_only`, and `fill_in_missing_segments=0`.",
        "",
        "## Which target versions were found",
        "",
        f"- Koren exact match found: `{koren['exact_found']}` (`{koren.get('exact_version_title')}`)",
        f"- Metsudah exact match found: `{metsudah['exact_found']}` (`{metsudah.get('exact_version_title')}`)",
        f"- Total English Genesis versions discovered: `{discovery_report['english_version_count']}`",
        f"- Final canonical Hebrew ref count: `{manifest['expected_total_refs']}`",
        "",
        "## What was fetched and persisted",
        "",
        f"- Koren text fetched: `{koren['text_fetched']}`",
        f"- Koren text persisted: `{koren['text_persisted']}`",
        f"- Metsudah text fetched: `{metsudah['text_fetched']}`",
        f"- Metsudah text persisted: `{metsudah['text_persisted']}`",
        f"- Koren final row count: `{manifest['row_counts_by_version']['koren']}`",
        f"- Metsudah final row count: `{manifest['row_counts_by_version']['metsudah']}`",
        "",
        "## License metadata and review status",
        "",
        f"- Koren license metadata: `{koren.get('license')}`",
        f"- Metsudah license metadata: `{metsudah.get('license')}`",
        "- Both versions remain human-review-only for future production use.",
        "- API availability does not equal production reuse approval.",
        f"- License review matrix: `{repo_relative(LICENSE_REVIEW_MATRIX_PATH)}`",
        f"- Human review packet: `{repo_relative(HUMAN_REVIEW_PACKET_PATH)}`",
        "",
        "## What happened with Genesis 35:30",
        "",
        "- The prior canonical Hebrew TSV incorrectly included an extra row labeled `Bereishis 35:30`.",
        "- Sefaria Hebrew `Miqra according to the Masorah` and both English translations end chapter 35 at verse 29.",
        "- The extra local row duplicated the burial verse of Yitzchak, so the canonical Hebrew TSV was corrected to `1533` refs.",
        f"- Reconciliation report: `{repo_relative(RECONCILIATION_REPORT_MD_PATH)}`",
        "",
        "## How to rerun",
        "",
        "```powershell",
        "python scripts/fetch_sefaria_bereishis_translations.py --target koren --target metsudah",
        "python scripts/validate_bereishis_translations.py",
        "```",
        "",
        "## What the next branch should do",
        "",
        "- Review the fetched translations for pedagogy and licensing, then build a non-runtime translation-review layer or diagnostic integration layer that uses the translation registry without activating runtime.",
        "",
    ]
    return "\n".join(lines)


def build_manifest(
    *,
    expected_total_refs: int,
    target_results: dict[str, dict[str, Any]],
    fetch_report: dict[str, Any],
) -> dict[str, Any]:
    selected_versions: dict[str, Any] = {}
    discovered_candidates: dict[str, Any] = {}
    exact_titles_used: dict[str, str | None] = {}
    row_counts_by_version: dict[str, int] = {}
    missing_refs_by_version: dict[str, list[str]] = {}
    blank_rows_by_version: dict[str, int] = {}
    duplicate_refs_by_version: dict[str, int] = {}
    license_status_by_version: dict[str, str] = {}

    for target_key in ["koren", "metsudah"]:
        result = target_results[target_key]
        fetch_meta = fetch_report["versions"][target_key]
        selected_versions[target_key] = {
            "display_name": TARGET_CONFIG[target_key]["display_name"],
            "exact_found": result["exact_found"],
            "exact_version_title": result.get("exact_version_title"),
            "license": fetch_meta.get("license"),
            "license_vetted": fetch_meta.get("license_vetted"),
            "text_fetched": fetch_meta.get("text_fetched", False),
            "text_persisted": fetch_meta.get("text_persisted", False),
            "pipeline_status": fetch_meta.get("pipeline_status"),
            "license_note": fetch_meta.get("license_note"),
            "suitable_for_internal_draft_use": fetch_meta.get("suitable_for_internal_draft_use", False),
            "suitable_for_future_production_use": fetch_meta.get("suitable_for_future_production_use", False),
        }
        discovered_candidates[target_key] = result["candidate_matches"]
        exact_titles_used[target_key] = result.get("exact_version_title")
        row_counts_by_version[target_key] = fetch_meta.get("row_count", 0)
        missing_refs_by_version[target_key] = fetch_meta.get("missing_refs", [])
        blank_rows_by_version[target_key] = len(fetch_meta.get("blank_refs", []))
        duplicate_refs_by_version[target_key] = len(fetch_meta.get("duplicate_refs", []))
        license_status_by_version[target_key] = fetch_meta.get("license_status", "blocked_license_unclear")

    return {
        "schema_version": SCHEMA_VERSION,
        "branch_scope": "feature/source-bereishis-english-translations-sefaria",
        "canonical_hebrew_source_path": repo_relative(CANONICAL_HEBREW_TSV),
        "expected_total_refs": expected_total_refs,
        "selected_versions": selected_versions,
        "discovered_candidates": discovered_candidates,
        "exact_version_titles_used": exact_titles_used,
        "row_counts_by_version": row_counts_by_version,
        "missing_refs_by_version": missing_refs_by_version,
        "blank_rows_by_version": blank_rows_by_version,
        "duplicate_refs_by_version": duplicate_refs_by_version,
        "license_status_by_version": license_status_by_version,
        "reconciliation_report_paths": {
            "markdown": repo_relative(RECONCILIATION_REPORT_MD_PATH),
            "json": repo_relative(RECONCILIATION_REPORT_JSON_PATH),
        },
        "license_review_artifacts": {
            "matrix_path": repo_relative(LICENSE_REVIEW_MATRIX_PATH),
            "human_review_packet_path": repo_relative(HUMAN_REVIEW_PACKET_PATH),
        },
        "translation_registry_path": repo_relative(TRANSLATION_REGISTRY_PATH),
        "integration_status": "source_ready_license_pending",
        "production_status": "not_production_ready",
        "runtime_status": "not_runtime_active",
        "validation_command": "python scripts/validate_bereishis_translations.py",
        "test_command": "python -m pytest tests/test_bereishis_translation_sources.py -q",
        "generated_at": iso_now(),
    }


def write_blocked_outputs(
    *,
    message: str,
    expected_total_refs: int | None = None,
) -> None:
    ensure_output_dirs()
    now = iso_now()
    minimal_manifest = {
        "schema_version": SCHEMA_VERSION,
        "branch_scope": "feature/source-bereishis-english-translations-sefaria",
        "canonical_hebrew_source_path": repo_relative(CANONICAL_HEBREW_TSV),
        "expected_total_refs": expected_total_refs,
        "selected_versions": {
            "koren": {
                "display_name": TARGET_CONFIG["koren"]["display_name"],
                "exact_found": False,
                "exact_version_title": None,
                "license": None,
                "license_vetted": None,
                "text_fetched": False,
                "text_persisted": False,
                "pipeline_status": "blocked_fetch_error",
                "license_note": message,
                "suitable_for_internal_draft_use": False,
                "suitable_for_future_production_use": False,
            },
            "metsudah": {
                "display_name": TARGET_CONFIG["metsudah"]["display_name"],
                "exact_found": False,
                "exact_version_title": None,
                "license": None,
                "license_vetted": None,
                "text_fetched": False,
                "text_persisted": False,
                "pipeline_status": "blocked_fetch_error",
                "license_note": message,
                "suitable_for_internal_draft_use": False,
                "suitable_for_future_production_use": False,
            },
        },
        "discovered_candidates": {"koren": [], "metsudah": []},
        "exact_version_titles_used": {"koren": None, "metsudah": None},
        "row_counts_by_version": {"koren": 0, "metsudah": 0},
        "missing_refs_by_version": {"koren": [], "metsudah": []},
        "blank_rows_by_version": {"koren": 0, "metsudah": 0},
        "duplicate_refs_by_version": {"koren": 0, "metsudah": 0},
        "license_status_by_version": {"koren": "blocked_fetch_error", "metsudah": "blocked_fetch_error"},
        "reconciliation_report_paths": {
            "markdown": repo_relative(RECONCILIATION_REPORT_MD_PATH),
            "json": repo_relative(RECONCILIATION_REPORT_JSON_PATH),
        },
        "license_review_artifacts": {
            "matrix_path": repo_relative(LICENSE_REVIEW_MATRIX_PATH),
            "human_review_packet_path": repo_relative(HUMAN_REVIEW_PACKET_PATH),
        },
        "translation_registry_path": repo_relative(TRANSLATION_REGISTRY_PATH),
        "integration_status": "source_ready_license_pending",
        "production_status": "not_production_ready",
        "runtime_status": "not_runtime_active",
        "validation_command": "python scripts/validate_bereishis_translations.py",
        "test_command": "python -m pytest tests/test_bereishis_translation_sources.py -q",
        "generated_at": now,
    }
    blocked_fetch_report = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": now,
        "request_defaults": {
            "return_format": "text_only",
            "fill_in_missing_segments": 0,
            "user_agent": USER_AGENT,
        },
        "blockers": [message],
        "versions": {
            "koren": {"pipeline_status": "blocked_fetch_error", "blockers": [message]},
            "metsudah": {"pipeline_status": "blocked_fetch_error", "blockers": [message]},
        },
    }
    json_dump(MANIFEST_PATH, minimal_manifest)
    json_dump(DISCOVERY_REPORT_PATH, {"schema_version": SCHEMA_VERSION, "generated_at": now, "blockers": [message]})
    json_dump(FETCH_REPORT_PATH, blocked_fetch_report)
    json_dump(LICENSE_REVIEW_MATRIX_PATH, build_license_review_matrix(minimal_manifest))
    TRANSLATION_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    json_dump(TRANSLATION_REGISTRY_PATH, build_translation_registry(minimal_manifest))
    LICENSE_REPORT_PATH.write_text(
        "# Bereishis English Translation License Report\n\n"
        f"- Status: `blocked_fetch_error`\n- Blocker: {message}\n",
        encoding="utf-8",
    )
    ALIGNMENT_REPORT_PATH.write_text(
        "# Bereishis English Translation Alignment Report\n\n"
        f"- Status: `blocked_fetch_error`\n- Blocker: {message}\n",
        encoding="utf-8",
    )
    README_PATH.write_text(
        "# Sefaria Bereishis English Translation Source Package\n\n"
        f"This pipeline is currently blocked: {message}\n",
        encoding="utf-8",
    )
    HUMAN_REVIEW_PACKET_PATH.write_text(
        "# Bereishis English Translation Human Review Packet\n\n"
        f"- Status: `blocked_fetch_error`\n- Blocker: {message}\n",
        encoding="utf-8",
    )


def build_license_review_matrix(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    review_records: list[dict[str, Any]] = []
    for target_key in ["koren", "metsudah"]:
        selected = manifest["selected_versions"][target_key]
        if target_key == "koren":
            recommendation = "blocked_pending_human_license_review"
            reason = "Non-commercial license requires policy and legal review before production use."
        else:
            recommendation = "blocked_pending_human_attribution_review"
            reason = "CC-BY requires correct attribution and human review before production use."
        review_records.append(
            {
                "translation_version_key": target_key,
                "translation_version_title": selected.get("exact_version_title"),
                "license": selected.get("license"),
                "license_vetted": selected.get("license_vetted"),
                "production_use_recommendation": recommendation,
                "reason": reason,
                "required_attribution_fields": [],
                "human_review_required": True,
                "status": "needs_license_review",
            }
        )
    return review_records


def render_human_review_packet(manifest: dict[str, Any], fetch_report: dict[str, Any]) -> str:
    lines = [
        "# Bereishis English Translation Human Review Packet",
        "",
        f"- Generated at: `{manifest['generated_at']}`",
        f"- Canonical Hebrew ref count: `{manifest['expected_total_refs']}`",
        f"- Registry path: `{repo_relative(TRANSLATION_REGISTRY_PATH)}`",
        "",
        "## Scope",
        "",
        "- This packet supports human review of the non-runtime Sefaria translation source layer for Bereishis.",
        "- Nothing here is production-approved or runtime-active.",
        "",
    ]
    for target_key in ["koren", "metsudah"]:
        selected = manifest["selected_versions"][target_key]
        version_fetch = fetch_report["versions"][target_key]
        lines.extend(
            [
                f"## {selected['display_name']}",
                "",
                f"- Exact versionTitle: `{selected.get('exact_version_title')}`",
                f"- License: `{selected.get('license')}`",
                f"- Pipeline status: `{selected.get('pipeline_status')}`",
                f"- Row count: `{manifest['row_counts_by_version'][target_key]}`",
                f"- Missing refs: `{len(manifest['missing_refs_by_version'][target_key])}`",
                f"- Duplicate refs: `{manifest['duplicate_refs_by_version'][target_key]}`",
                f"- Blank rows: `{manifest['blank_rows_by_version'][target_key]}`",
                f"- Text fetched: `{selected['text_fetched']}`",
                f"- Text persisted: `{selected['text_persisted']}`",
                f"- Human review status: `needs_license_review`",
                "",
                "### Review questions",
                "",
                "- Does the license metadata returned by Sefaria match the intended publisher reuse policy?",
                "- Is the translation appropriate for future student-facing translation diagnostics?",
                "- Are attribution requirements fully known and documentable?",
                "",
            ]
        )
        blockers = version_fetch.get("blockers") or []
        if blockers:
            lines.append("### Blockers")
            lines.append("")
            for blocker in blockers:
                lines.append(f"- {blocker}")
            lines.append("")

    lines.extend(
        [
            "## Canonical Hebrew reconciliation",
            "",
            "- `Bereishis 35:30` was removed from the canonical Hebrew TSV after reconciliation.",
            f"- See `{repo_relative(RECONCILIATION_REPORT_MD_PATH)}` for the evidence and preserved removed row.",
            "",
            "## Final recommendation placeholder",
            "",
            "- [ ] LEGAL_REVIEW_COMPLETE",
            "- [x] NEEDS_HUMAN_REVIEW",
            "- [ ] SAFE_FOR_RUNTIME_INTEGRATION",
            "",
        ]
    )
    return "\n".join(lines)


def build_translation_registry(manifest: dict[str, Any]) -> dict[str, Any]:
    versions: list[dict[str, Any]] = []
    for target_key in ["koren", "metsudah"]:
        selected = manifest["selected_versions"][target_key]
        versions.append(
            {
                "translation_version_key": target_key,
                "translation_version_title": selected.get("exact_version_title"),
                "file_path": repo_relative(TARGET_CONFIG[target_key]["output_jsonl"]),
                "license": selected.get("license"),
                "license_status": manifest["license_status_by_version"][target_key],
                "alignment_status": "aligned_complete" if not manifest["missing_refs_by_version"][target_key] else "aligned_with_missing_refs",
                "row_count": manifest["row_counts_by_version"][target_key],
                "missing_refs": manifest["missing_refs_by_version"][target_key],
                "runtime_eligibility": "not_runtime_active",
                "production_eligibility": "not_production_ready",
                "human_review_required": True,
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "source_package_name": "sefaria_bereishis_english_translations",
        "canonical_hebrew_backbone_path": repo_relative(CANONICAL_HEBREW_TSV),
        "available_translation_versions": versions,
        "loader_path": "translation_sources_loader.py",
        "runtime_status": "not_runtime_active",
        "production_status": "not_production_ready",
        "integration_status": "source_ready_license_pending",
        "generated_at": iso_now(),
    }


def run_pipeline(args: argparse.Namespace) -> int:
    ensure_output_dirs()
    rows = load_canonical_hebrew_rows()
    expected_rows, chapter_counts, ref_lookup = build_expected_ref_index(rows)
    targets = normalize_targets(args.target)

    if not args.force_refresh and can_reuse_cached_outputs(
        targets=targets,
        expected_total_refs=len(expected_rows),
        metadata_only=bool(args.metadata_only),
    ):
        print(
            json.dumps(
                {
                    "status": "cached_outputs_reused",
                    "targets": targets,
                    "expected_total_refs": len(expected_rows),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    versions_payload = load_or_fetch_versions(force_refresh=args.force_refresh)
    english = english_versions(versions_payload)
    target_results = {
        target_key: find_target_candidates(target_key, english) for target_key in ["koren", "metsudah"]
    }

    fetch_report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": iso_now(),
        "canonical_hebrew_source_path": repo_relative(CANONICAL_HEBREW_TSV),
        "request_defaults": {
            "return_format": "text_only",
            "fill_in_missing_segments": 0,
            "user_agent": USER_AGENT,
        },
        "versions": {},
        "blockers": [],
    }

    technical_failures: list[str] = []

    for target_key in ["koren", "metsudah"]:
        result = target_results[target_key]
        version_metadata = result.get("selected_version_metadata")
        license_gate = classify_license(version_metadata)

        version_report = {
            "target_key": target_key,
            "display_name": TARGET_CONFIG[target_key]["display_name"],
            "exact_version_title": result.get("exact_version_title"),
            "pipeline_status": "blocked_version_not_found" if not result["exact_found"] else "version_discovered",
            "license_status": license_gate["license_status"],
            "license": version_metadata.get("license") if version_metadata else None,
            "license_vetted": version_metadata.get("licenseVetted") if version_metadata else None,
            "license_note": license_gate["license_note"],
            "suitable_for_internal_draft_use": license_gate["suitable_for_internal_draft_use"],
            "suitable_for_future_production_use": license_gate["suitable_for_future_production_use"],
            "text_fetched": False,
            "text_persisted": False,
            "row_count": 0,
            "missing_refs": [],
            "extra_refs": [],
            "blank_refs": [],
            "duplicate_refs": [],
            "chapter_fetches": [],
            "warnings_seen": [],
            "missing_segment_warning_detected": False,
            "blockers": [*result.get("blockers", [])],
        }

        if target_key not in targets:
            version_report["blockers"].append("Target not requested in this run.")
            fetch_report["versions"][target_key] = version_report
            continue

        if not result["exact_found"]:
            fetch_report["versions"][target_key] = version_report
            continue

        if args.metadata_only:
            version_report["pipeline_status"] = "version_discovered"
            version_report["blockers"].append("Metadata-only mode; full text fetch skipped.")
            fetch_report["versions"][target_key] = version_report
            continue

        if not license_gate["allow_full_text_persist"]:
            version_report["pipeline_status"] = license_gate["license_status"]
            version_report["blockers"].append(license_gate["license_note"])
            fetch_report["versions"][target_key] = version_report
            continue

        try:
            fetched = fetch_version_rows(
                version_key=target_key,
                version_metadata=version_metadata,
                chapter_counts=chapter_counts,
                ref_lookup=ref_lookup,
                license_note=license_gate["license_note"],
            )
        except FetchError as error:
            version_report["pipeline_status"] = "blocked_fetch_error"
            version_report["blockers"].append(str(error))
            technical_failures.append(str(error))
            fetch_report["versions"][target_key] = version_report
            continue

        write_jsonl(TARGET_CONFIG[target_key]["output_jsonl"], fetched["rows"])
        version_report.update(
            {
                "pipeline_status": "source_fetched",
                "text_fetched": fetched["fetched"],
                "text_persisted": fetched["persisted"],
                "row_count": fetched["row_count"],
                "missing_refs": fetched["missing_refs"],
                "extra_refs": fetched["extra_refs"],
                "blank_refs": fetched["blank_refs"],
                "duplicate_refs": fetched["duplicate_refs"],
                "chapter_fetches": fetched["chapter_fetches"],
                "warnings_seen": fetched["warnings_seen"],
                "missing_segment_warning_detected": any(
                    "missing" in " ".join(map(str, warning.get("warnings", []))).lower()
                    for warning in fetched["warnings_seen"]
                ),
            }
        )
        fetch_report["versions"][target_key] = version_report

    manifest = build_manifest(
        expected_total_refs=len(expected_rows),
        target_results=target_results,
        fetch_report=fetch_report,
    )
    discovery_report = build_discovery_report(
        all_english_versions=english,
        target_results=target_results,
        fetch_report=fetch_report,
    )
    json_dump(DISCOVERY_REPORT_PATH, discovery_report)
    json_dump(MANIFEST_PATH, manifest)
    json_dump(FETCH_REPORT_PATH, fetch_report)
    json_dump(LICENSE_REVIEW_MATRIX_PATH, build_license_review_matrix(manifest))
    TRANSLATION_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    json_dump(TRANSLATION_REGISTRY_PATH, build_translation_registry(manifest))
    ALIGNMENT_REPORT_PATH.write_text(
        render_alignment_report(manifest=manifest, fetch_report=fetch_report, chapter_counts=chapter_counts),
        encoding="utf-8",
    )
    LICENSE_REPORT_PATH.write_text(render_license_report(manifest, fetch_report), encoding="utf-8")
    HUMAN_REVIEW_PACKET_PATH.write_text(render_human_review_packet(manifest, fetch_report), encoding="utf-8")
    README_PATH.write_text(render_readme(manifest, discovery_report), encoding="utf-8")

    return 1 if technical_failures else 0


def main() -> int:
    args = parse_args()
    try:
        return run_pipeline(args)
    except FetchError as error:
        expected_total_refs = None
        if CANONICAL_HEBREW_TSV.exists():
            try:
                expected_total_refs = len(load_canonical_hebrew_rows())
            except FetchError:
                expected_total_refs = None
        write_blocked_outputs(message=str(error), expected_total_refs=expected_total_refs)
        print(str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
