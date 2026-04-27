from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "curriculum_extraction" / "curriculum_extraction_manifest.json"
HEBREW_SOURCE_PATH = ROOT / "data" / "source_texts" / "bereishis_hebrew_menukad_taamim.tsv"
METSUDAH_PATH = ROOT / "data" / "source_texts" / "translations" / "sefaria" / "bereishis_english_metsudah.jsonl"
KOREN_PATH = ROOT / "data" / "source_texts" / "translations" / "sefaria" / "bereishis_english_koren.jsonl"

MAP_COLUMNS = (
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

DEFAULT_BLOCKED_QUESTION_TYPES = "all_until_yossi_extraction_accuracy_and_future_question_gate"
DEFAULT_UNCERTAINTY = (
    "Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, "
    "difficulty, and question-type eligibility are not safely row-level consolidated yet."
)


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def display_path(path: Path) -> str:
    try:
        return repo_relative(path)
    except ValueError:
        return path.as_posix()


def parse_ref(ref: str) -> tuple[int, int]:
    match = re.fullmatch(r"(?:Bereishis|Genesis) (\d+):(\d+)", ref.strip())
    if not match:
        raise ValueError(f"Unsupported ref format: {ref!r}")
    return int(match.group(1)), int(match.group(2))


def ref_in_scope(ref: str, start_ref: str, end_ref: str) -> bool:
    ref_key = parse_ref(ref)
    return parse_ref(start_ref) <= ref_key <= parse_ref(end_ref)


def safe_filename_scope(start_ref: str, end_ref: str) -> str:
    start_perek, start_pasuk = parse_ref(start_ref)
    end_perek, end_pasuk = parse_ref(end_ref)
    return f"bereishis_{start_perek}_{start_pasuk}_to_{end_perek}_{end_pasuk}"


def strip_nikud(value: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFD", value or "") if unicodedata.category(ch) != "Mn")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_translation_by_hebrew_ref(path: Path) -> dict[str, dict[str, Any]]:
    translations: dict[str, dict[str, Any]] = {}
    for record in load_jsonl(path):
        hebrew_ref = record.get("hebrew_ref")
        if hebrew_ref:
            translations[hebrew_ref] = record
    return translations


def load_hebrew_refs(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row.get("ref", "") for row in csv.DictReader(handle, delimiter="\t")}


def manifest_normalized_paths(manifest: dict[str, Any]) -> list[Path]:
    paths: list[Path] = []
    for item in manifest.get("normalized_data_files", []):
        if isinstance(item, str):
            paths.append(ROOT / item)
        elif isinstance(item, dict):
            path = item.get("path") or item.get("file_path")
            if path:
                paths.append(ROOT / path)
    for batch in manifest.get("resource_batches", []):
        for path in batch.get("normalized_data_files", []):
            candidate = ROOT / path
            if candidate not in paths:
                paths.append(candidate)
    return paths


def manifest_raw_paths_by_batch(manifest: dict[str, Any]) -> dict[str, list[str]]:
    by_batch: dict[str, list[str]] = {}
    for batch in manifest.get("resource_batches", []):
        batch_id = batch.get("batch_id")
        if batch_id:
            by_batch[batch_id] = list(batch.get("raw_source_files", []))
    return by_batch


def collect_pasuk_segment_records(manifest: dict[str, Any], start_ref: str, end_ref: str) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in manifest_normalized_paths(manifest):
        if not path.exists():
            continue
        for record in load_jsonl(path):
            if record.get("record_type") != "pasuk_segment":
                continue
            ref = record.get("canonical_ref")
            if ref and ref_in_scope(ref, start_ref, end_ref):
                records.append((path, record))
    records.sort(
        key=lambda pair: (
            parse_ref(pair[1]["canonical_ref"]),
            int(pair[1].get("segment_order") or 0),
            pair[1].get("id", ""),
        )
    )
    return records


def build_source_files_used(normalized_path: Path, record: dict[str, Any], raw_paths_by_batch: dict[str, list[str]]) -> str:
    paths = [repo_relative(normalized_path)]
    batch_id = record.get("extraction_batch_id")
    paths.extend(raw_paths_by_batch.get(batch_id, []))
    source_file = (record.get("source_trace") or {}).get("source_file")
    if source_file and source_file not in paths:
        paths.append(source_file)
    paths.extend(
        [
            repo_relative(METSUDAH_PATH),
            repo_relative(KOREN_PATH),
        ]
    )
    deduped: list[str] = []
    for path in paths:
        if path and path not in deduped:
            deduped.append(path)
    return "; ".join(deduped)


def build_map_rows(start_ref: str, end_ref: str, strict: bool = False) -> tuple[list[dict[str, str]], dict[str, Any]]:
    required_paths = [MANIFEST_PATH, HEBREW_SOURCE_PATH, METSUDAH_PATH, KOREN_PATH]
    missing_paths = [repo_relative(path) for path in required_paths if not path.exists()]
    if missing_paths:
        raise FileNotFoundError(f"Required source files missing: {missing_paths}")

    manifest = load_json(MANIFEST_PATH)
    records = collect_pasuk_segment_records(manifest, start_ref, end_ref)
    if not records:
        raise ValueError(f"No pasuk_segment records found for {start_ref} through {end_ref}")

    hebrew_refs = load_hebrew_refs(HEBREW_SOURCE_PATH)
    metsudah = load_translation_by_hebrew_ref(METSUDAH_PATH)
    koren = load_translation_by_hebrew_ref(KOREN_PATH)
    raw_paths_by_batch = manifest_raw_paths_by_batch(manifest)

    rows: list[dict[str, str]] = []
    missing_hebrew_refs: set[str] = set()
    missing_metsudah_refs: set[str] = set()
    missing_koren_refs: set[str] = set()
    source_paths: set[str] = set()

    for normalized_path, record in records:
        ref = record["canonical_ref"]
        if ref not in hebrew_refs:
            missing_hebrew_refs.add(ref)
        metsudah_record = metsudah.get(ref)
        koren_record = koren.get(ref)
        if metsudah_record is None:
            missing_metsudah_refs.add(ref)
        if koren_record is None:
            missing_koren_refs.add(ref)
        source_files_used = build_source_files_used(normalized_path, record, raw_paths_by_batch)
        source_paths.update(path.strip() for path in source_files_used.split(";") if path.strip())

        hebrew = record.get("hebrew_raw") or ""
        skills = record.get("skill_tags") or []
        skill_primary = skills[0] if skills else "phrase_translation"
        skill_secondary = "translation_context" if skill_primary == "phrase_translation" else ""

        uncertainty_reasons = [DEFAULT_UNCERTAINTY]
        if not metsudah_record:
            uncertainty_reasons.append("Metsudah translation context missing for this ref.")
        if not koren_record:
            uncertainty_reasons.append("Koren secondary translation context missing for this ref.")
        if "source_pdf_text_layer_noisy" in record.get("extraction_quality_flags", []):
            uncertainty_reasons.append("Source PDF text layer was noisy; phrase alignment needs Yossi extraction review.")

        rows.append(
            {
                "sefer": record.get("sefer", "Bereishis"),
                "perek": str(record.get("perek", "")),
                "pasuk": str(record.get("pasuk", "")),
                "ref": ref,
                "hebrew_word_or_phrase": hebrew,
                "clean_hebrew_no_nikud": strip_nikud(hebrew),
                "source_translation_metsudah": (metsudah_record or {}).get("translation_text", ""),
                "alternate_translation": record.get("english_raw") or "",
                "secondary_translation_koren": (koren_record or {}).get("translation_text", ""),
                "source_id": "sefaria_bereishis_english_metsudah; linear_chumash_translation_most_parshiyos_in_torah",
                "source_version_title": "Metsudah Chumash, Metsudah Publications, 2009; Linear Chumash Translation for Most Parshiyos in Torah",
                "source_license": "CC-BY; trusted_teacher_source",
                "source_preference": "primary_preferred_translation_source",
                "requires_attribution": "true",
                "shoresh": "",
                "prefixes": "",
                "suffixes": "",
                "tense": "",
                "part_of_speech": "",
                "dikduk_feature": "",
                "skill_primary": skill_primary,
                "skill_secondary": skill_secondary,
                "skill_id": skill_primary,
                "zekelman_standard": "",
                "difficulty_level": "",
                "question_allowed": "needs_review",
                "question_type_allowed": "",
                "blocked_question_types": DEFAULT_BLOCKED_QUESTION_TYPES,
                "runtime_allowed": "false",
                "protected_preview_allowed": "false",
                "reviewed_bank_allowed": "false",
                "extraction_review_status": "pending_yossi_extraction_accuracy_pass",
                "review_notes": (
                    "Deterministically built from existing trusted source-derived extraction plus Metsudah/Koren "
                    "translation context; pending Yossi extraction-accuracy review. This is not runtime approval "
                    "or question approval."
                ),
                "uncertainty_reason": " ".join(uncertainty_reasons),
                "source_files_used": source_files_used,
            }
        )

    if strict and (missing_hebrew_refs or missing_metsudah_refs or missing_koren_refs):
        raise ValueError(
            "Strict build failed: "
            f"missing_hebrew_refs={sorted(missing_hebrew_refs)}, "
            f"missing_metsudah_refs={sorted(missing_metsudah_refs)}, "
            f"missing_koren_refs={sorted(missing_koren_refs)}"
        )

    summary = {
        "start_ref": start_ref,
        "end_ref": end_ref,
        "row_count": len(rows),
        "refs": sorted({row["ref"] for row in rows}, key=parse_ref),
        "source_files_used": sorted(source_paths),
        "missing_hebrew_refs": sorted(missing_hebrew_refs, key=parse_ref),
        "missing_metsudah_refs": sorted(missing_metsudah_refs, key=parse_ref),
        "missing_koren_refs": sorted(missing_koren_refs, key=parse_ref),
        "skill_primary_counts": dict(Counter(row["skill_primary"] for row in rows)),
        "extraction_review_status": "pending_yossi_extraction_accuracy_pass",
        "question_allowed": "needs_review",
        "runtime_allowed": "false",
        "protected_preview_allowed": "false",
        "reviewed_bank_allowed": "false",
    }
    return rows, summary


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MAP_COLUMNS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def representative_rows(rows: list[dict[str, str]], limit: int = 5) -> list[dict[str, str]]:
    if len(rows) <= limit:
        return rows
    indexes = sorted({0, len(rows) // 3, len(rows) // 2, (2 * len(rows)) // 3, len(rows) - 1})
    return [rows[index] for index in indexes[:limit]]


def markdown_table_or_none(rows: list[dict[str, str]], note: str) -> str:
    if not rows:
        return note
    return "\n".join(
        f"| {row['ref']} | {row['hebrew_word_or_phrase']} | {row['alternate_translation']} | {row['uncertainty_reason']} |"
        for row in rows
    )


def contains_parenthetical(row: dict[str, str]) -> bool:
    return any("(" in row.get(field, "") or ")" in row.get(field, "") for field in ("alternate_translation", "source_translation_metsudah", "secondary_translation_koren"))


def awkward_source_wording(row: dict[str, str]) -> bool:
    text = row.get("alternate_translation", "").lower()
    return any(marker in text for marker in ("spread", "small(er)", "big luminary", "made for", "face of"))


def write_build_report(path: Path, summary: dict[str, Any], output_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    source_lines = "\n".join(f"- `{source}`" for source in summary["source_files_used"])
    text = f"""# Source-to-Skill Map Build Report

## Scope

- Start ref: {summary['start_ref']}
- End ref: {summary['end_ref']}
- Output map: `{display_path(output_path)}`
- Row count: {summary['row_count']}
- Refs covered: {', '.join(summary['refs'])}

## Source Files Used

{source_lines}

## Coverage Findings

- Hebrew source coverage missing refs: {summary['missing_hebrew_refs'] or 'none'}
- Metsudah translation missing refs: {summary['missing_metsudah_refs'] or 'none'}
- Koren secondary translation missing refs: {summary['missing_koren_refs'] or 'none'}
- Skill primary counts: {summary['skill_primary_counts']}

## Status Defaults

- Extraction review status: `pending_yossi_extraction_accuracy_pass`
- Question allowed: `needs_review`
- Runtime allowed: `false`
- Protected preview allowed: `false`
- Reviewed bank allowed: `false`

## Build Finding

This slice was built deterministically from existing trusted source-derived data. It is pending Yossi extraction-accuracy review and does not authorize question generation, protected preview generation, reviewed-bank promotion, runtime activation, or student-facing use.
"""
    path.write_text(text, encoding="utf-8")


def write_review_packet(path: Path, rows: list[dict[str, str]], summary: dict[str, Any], output_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    source_lines = "\n".join(f"- `{source}`" for source in summary["source_files_used"])
    clean_lines = "\n".join(
        f"| {row['ref']} | {row['hebrew_word_or_phrase']} | {row['alternate_translation']} | {row['skill_primary']} | pending, non-runtime |"
        for row in representative_rows(rows)
    )
    parenthetical_rows = [row for row in rows if contains_parenthetical(row)]
    long_parenthetical_rows = [row for row in parenthetical_rows if len(row["alternate_translation"]) >= 55]
    long_hebrew_rows = sorted(rows, key=lambda row: len(row["hebrew_word_or_phrase"]), reverse=True)[:10]
    high_risk_rows = sorted(
        {id(row): row for row in [*long_parenthetical_rows, *long_hebrew_rows]}.values(),
        key=lambda row: (parse_ref(row["ref"]), row["hebrew_word_or_phrase"]),
    )
    awkward_rows = [row for row in rows if awkward_source_wording(row)]
    uncertainty_lines = "\n".join(
        f"| {row['ref']} | {row['hebrew_word_or_phrase']} | {row['uncertainty_reason']} |"
        for row in rows[:10]
    )
    missing_translation_rows = [
        row
        for row in rows
        if not row["source_translation_metsudah"] or not row["secondary_translation_koren"] or not row["alternate_translation"]
    ]
    missing_translation_lines = (
        "\n".join(
            f"| {row['ref']} | {row['hebrew_word_or_phrase']} | Metsudah: {'missing' if not row['source_translation_metsudah'] else 'present'}; "
            f"Koren: {'missing' if not row['secondary_translation_koren'] else 'present'}; Linear: {'missing' if not row['alternate_translation'] else 'present'} |"
            for row in missing_translation_rows
        )
        or "No rows are missing Linear phrase translation, Metsudah verse context, or Koren secondary verse context."
    )
    source_only_lines = "\n".join(
        f"| {row['ref']} | {row['hebrew_word_or_phrase']} | Keep source-only until separate question/protected-preview gate. |"
        for row in rows[:8]
    )
    text = f"""# {summary['start_ref']}-{summary['end_ref']} Source-to-Skill Map Exceptions Review Packet

This is extraction-accuracy and mapping confirmation for trusted source-derived content. It is not generated-question review, not question approval, not protected-preview approval, not reviewed-bank approval, and not runtime approval.

## A. Scope

- Map file: `{display_path(output_path)}`
- Scope: {summary['start_ref']} through {summary['end_ref']}
- Row count: {summary['row_count']} phrase-level rows
- Current status: deterministic pending source-to-skill slice only
- Extraction review status: `pending_yossi_extraction_accuracy_pass`

## B. Source Files Used

{source_lines}

## C. What Yossi Is Confirming

Yossi is confirming:

- the Linear Chumash phrase extraction matches the trusted source
- Hebrew phrase text is faithful enough for source-derived planning
- Metsudah verse translation context was joined to the correct pasuk
- Koren secondary noncommercial context was joined to the correct pasuk
- `phrase_translation` / `translation_context` classification is reasonable
- uncertainty fields correctly identify what is not yet safe to use

## D. What Yossi Is Not Approving

This packet does not approve:

- generated questions
- answer choices
- answer keys
- protected preview generation
- reviewed-bank promotion
- runtime activation
- student-facing use
- commercial use of Koren

## E. Representative Clean Rows

| Ref | Hebrew phrase | Linear translation | Skill | Safety |
|---|---|---|---|---|
{clean_lines}

## F. Rows With Uncertainty

All rows currently carry an uncertainty reason because morphology, Zekelman Standard mapping, difficulty, and question-type eligibility are not safely consolidated at row level yet.

| Ref | Hebrew phrase | Uncertainty reason |
|---|---|---|
{uncertainty_lines}

## F1. High-Risk Rows Needing Yossi Review

These rows were selected because they have long English explanations, parenthetical wording, or long Hebrew phrase boundaries. They are not unsafe; they are the rows most worth checking before any future extraction verification.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
{markdown_table_or_none(high_risk_rows, "No high-risk rows were detected by the deterministic selection rules.")}

## G. Missing Translations

{missing_translation_lines}

## H. Ambiguous Phrase Joins

Rows were generated from existing phrase-level Linear Chumash extraction. Yossi should confirm that each phrase join is faithful to the trusted source before verification.

## H1. Long Parentheticals Needing Review

Yossi should confirm that each parenthetical explanation belongs to the Hebrew phrase shown here, not to a neighboring phrase.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
{markdown_table_or_none(long_parenthetical_rows, "No long parenthetical rows were detected.")}

## H2. Long Hebrew Phrase Boundaries Needing Review

Yossi should confirm that these longer Hebrew phrase boundaries match the source phrase breaks and segment order.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
{markdown_table_or_none(long_hebrew_rows, "No long Hebrew phrase-boundary rows were detected.")}

## H3. Awkward But Source-Derived Wording

These rows contain wording that may feel awkward in English but appears to be source-derived from the Linear Chumash extraction. Yossi should confirm the wording is copied/extracted accurately rather than normalized into smoother generated language.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
{markdown_table_or_none(awkward_rows, "No awkward source-derived wording rows were detected.")}

## I. Missing Or Uncertain Morphology

Shoresh, prefixes, suffixes, tense, part of speech, and dikduk-feature fields are intentionally blank. The builder does not invent morphology.

## J. Skill Mapping Questions

Current mapping:

- `skill_primary`: `phrase_translation`
- `skill_secondary`: `translation_context`
- `skill_id`: `phrase_translation`

Question for Yossi/project lead: Is this the correct planning classification for these phrase-level Linear Chumash rows before any future protected preview work?

## K. Standards Mapping Questions

Zekelman Standard mapping is intentionally blank. A separate standards-mapping pass is needed before these rows can support standards-specific protected-preview planning.

## L. Rows Recommended As Source-Only

| Ref | Hebrew phrase | Recommendation |
|---|---|---|
{source_only_lines}

All rows should remain source-only until Yossi extraction verification and a later explicit question/protected-preview gate.

## M. Safety Status Summary

- Runtime: blocked
- Question generation: blocked
- Question-ready status: blocked
- Protected preview: blocked
- Reviewed bank: blocked
- Student-facing use: blocked

## N. Recommended Next Action

Yossi should review this packet for extraction accuracy and mapping reasonableness. If all rows are accurate, run a separate verification-recording task that marks only this slice `yossi_extraction_verified` while keeping all question/runtime/student-facing gates closed.
"""
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic source-to-skill map slices from trusted data.")
    parser.add_argument("--start-ref", required=True)
    parser.add_argument("--end-ref", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report-output")
    parser.add_argument("--review-packet-output")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    rows, summary = build_map_rows(args.start_ref, args.end_ref, strict=args.strict)
    output_path = ROOT / args.output

    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    write_tsv(output_path, rows)
    if args.report_output:
        write_build_report(ROOT / args.report_output, summary, output_path)
    if args.review_packet_output:
        write_review_packet(ROOT / args.review_packet_output, rows, summary, output_path)

    print(json.dumps({**summary, "output": display_path(output_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
