from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "docs" / "sources" / "trusted_teacher_source_extraction_review_packet_template.md"
POLICY_PATH = ROOT / "docs" / "sources" / "trusted_teacher_source_policy.md"
REGISTRY_PATH = ROOT / "data" / "curriculum_extraction" / "source_resource_registry.json"
MANIFEST_PATH = ROOT / "data" / "curriculum_extraction" / "curriculum_extraction_manifest.json"
CONFIRMATION_ITEMS_PATH = ROOT / "data" / "source_review_confirmation_items.json"


TRUSTED_SOURCE_STATUS = "trusted_teacher_source"
PENDING_ACCURACY_PASS = "pending_yossi_extraction_accuracy_pass"
NOT_RUNTIME_READY = "not_runtime_ready"
NOT_QUESTION_READY = "not_question_ready"
MAX_REVIEW_SAMPLES = 15
EXPANDED_REVIEW_SAMPLE_LIMIT = 60
PAGE_BREAK = '<div style="page-break-after: always;"></div>'


def repo_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{repo_relative(path)} must contain a JSON object")
    return payload


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            if not isinstance(payload, dict):
                raise ValueError(f"{repo_relative(path)} line {line_number}: expected JSON object")
            payload["_source_line_number"] = line_number
            payload["_source_file_path"] = repo_relative(path)
            records.append(payload)
    return records


def load_template_text(path: Path = TEMPLATE_PATH) -> str:
    return path.read_text(encoding="utf-8")


def source_packages_by_id(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    packages = registry.get("source_packages", [])
    if not isinstance(packages, list):
        raise ValueError("source_resource_registry.json: source_packages must be a list")
    return {
        str(package["source_package_id"]): package
        for package in packages
        if isinstance(package, dict) and package.get("source_package_id")
    }


def batches_by_id(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    batches = manifest.get("resource_batches", [])
    if not isinstance(batches, list):
        raise ValueError("curriculum_extraction_manifest.json: resource_batches must be a list")
    return {
        str(batch["batch_id"]): batch
        for batch in batches
        if isinstance(batch, dict) and batch.get("batch_id")
    }


def require_trusted_source_package(package: dict[str, Any]) -> None:
    if package.get("teacher_source_status") != TRUSTED_SOURCE_STATUS:
        raise ValueError(
            f"{package.get('source_package_id', '<unknown>')}: trusted-source extraction packets "
            "may only be generated for trusted teacher-source packages"
        )
    if package.get("runtime_status") != NOT_RUNTIME_READY:
        raise ValueError(f"{package['source_package_id']}: runtime_status must remain {NOT_RUNTIME_READY!r}")
    if package.get("question_ready_status") != NOT_QUESTION_READY:
        raise ValueError(f"{package['source_package_id']}: question_ready_status must remain {NOT_QUESTION_READY!r}")


def require_trusted_source_batch(batch: dict[str, Any]) -> None:
    if batch.get("runtime_active") is not False:
        raise ValueError(f"{batch.get('batch_id', '<unknown>')}: runtime_active must be false")
    if batch.get("integration_status") != "not_runtime_active":
        raise ValueError(f"{batch.get('batch_id', '<unknown>')}: integration_status must be not_runtime_active")
    if batch.get("extraction_review_status") not in {PENDING_ACCURACY_PASS, "yossi_extraction_verified"}:
        raise ValueError(
            f"{batch.get('batch_id', '<unknown>')}: extraction_review_status must be a trusted-source review status"
        )


def markdown_list(values: list[Any] | None) -> list[str]:
    if not values:
        return ["- none listed"]
    return [f"- `{value}`" for value in values]


def md(value: object) -> str:
    text = str(value if value is not None else "").replace("\n", "<br>")
    return text.replace("|", "\\|").strip()


def brief(value: object, *, limit: int = 260) -> str:
    text = md(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def load_batch_records(batch: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for relative in batch.get("normalized_data_files") or []:
        path = ROOT / relative
        records.extend(load_jsonl(path))
    return records


def record_hebrew(record: dict[str, Any]) -> str:
    for key in ("hebrew_raw", "word_in_pasuk_raw", "quoted_phrase_raw", "hebrew"):
        value = record.get(key)
        if value:
            return str(value)
    return ""


def record_english(record: dict[str, Any]) -> str:
    for key in ("english_raw", "literal_translation", "contextual_translation", "expected_answer"):
        value = record.get(key)
        if value:
            return str(value)
    glosses = record.get("english_glosses")
    if isinstance(glosses, list) and glosses:
        return "; ".join(str(item) for item in glosses)
    return ""


def record_ref(record: dict[str, Any]) -> str:
    return str(record.get("canonical_ref") or record.get("source_trace", {}).get("source_ref") or "")


def record_mapping(record: dict[str, Any]) -> str:
    skill_tags = record.get("skill_tags")
    if isinstance(skill_tags, list):
        return ", ".join(str(tag) for tag in skill_tags)
    return ""


def has_missing_display_field(record: dict[str, Any]) -> bool:
    return not record_ref(record) or not record_hebrew(record) or not record_english(record)


def has_unclear_mapping(record: dict[str, Any]) -> bool:
    return not record_mapping(record)


def record_parenthetical_text(record: dict[str, Any]) -> str:
    value = record.get("parenthetical_clarification")
    if value:
        return str(value)
    english = record_english(record)
    matches = []
    for start, end in (("(", ")"), ("[", "]")):
        fragment = ""
        in_fragment = False
        for character in english:
            if character == start:
                in_fragment = True
                fragment = character
            elif character == end and in_fragment:
                fragment += character
                matches.append(fragment)
                in_fragment = False
            elif in_fragment:
                fragment += character
    return "; ".join(matches)


def has_suspicious_display_field(record: dict[str, Any]) -> bool:
    if has_missing_display_field(record) or has_unclear_mapping(record):
        return True
    source_trace = record.get("source_trace") if isinstance(record.get("source_trace"), dict) else {}
    source_snippet = str(source_trace.get("source_snippet_raw") or "")
    return bool(source_snippet and "=" not in source_snippet and record.get("record_type") == "pasuk_segment")


def deterministic_random_indices(records: list[dict[str, Any]], *, count: int = 10) -> list[int]:
    scored: list[tuple[str, int]] = []
    for index, record in enumerate(records):
        stable_key = f"{record.get('id', '')}|{record_ref(record)}|{record_hebrew(record)}"
        digest = hashlib.sha256(stable_key.encode("utf-8")).hexdigest()
        scored.append((digest, index))
    return [index for _, index in sorted(scored)[: min(count, len(scored))]]


def sample_reason(record: dict[str, Any], index: int, records: list[dict[str, Any]]) -> list[str]:
    reasons: list[str] = []
    if index == 0:
        reasons.append("first extracted record")
    if index == len(records) - 1:
        reasons.append("last extracted record")
    if has_missing_display_field(record):
        reasons.append("missing display field")
    if has_unclear_mapping(record):
        reasons.append("unclear mapping")
    flags = record.get("extraction_quality_flags")
    if isinstance(flags, list) and flags:
        reasons.append("warning flags present")
    return reasons


def choose_review_samples(records: list[dict[str, Any]], *, limit: int = EXPANDED_REVIEW_SAMPLE_LIMIT) -> list[dict[str, Any]]:
    if not records:
        return []

    selected_reasons: dict[int, list[str]] = {}

    def add(index: int, reason: str) -> None:
        if 0 <= index < len(records):
            selected_reasons.setdefault(index, [])
            if reason not in selected_reasons[index]:
                selected_reasons[index].append(reason)

    for index in range(min(5, len(records))):
        add(index, "first 5 records")

    for index in range(max(0, len(records) - 5), len(records)):
        add(index, "last 5 records")

    for index in deterministic_random_indices(records, count=10):
        add(index, "deterministic random sample")

    for index in sorted(range(len(records)), key=lambda item: len(record_english(records[item])), reverse=True)[:10]:
        add(index, "10 longest English/explanatory records")

    for index in sorted(range(len(records)), key=lambda item: len(record_hebrew(records[item])), reverse=True)[:10]:
        add(index, "10 longest Hebrew phrase segments")

    for index, record in enumerate(records):
        parenthetical = record_parenthetical_text(record)
        if len(parenthetical) >= 24 or len(record_english(record)) >= 90 and ("(" in record_english(record) or ")" in record_english(record)):
            add(index, "long parenthetical/explanatory alignment")

    for index, record in enumerate(records):
        if has_suspicious_display_field(record):
            add(index, "missing or suspicious display field")

    samples: list[dict[str, Any]] = []
    for index in sorted(selected_reasons)[:limit]:
        record = records[index]
        samples.append(
            {
                "index": index,
                "record": record,
                "reasons": [*selected_reasons[index], *sample_reason(record, index, records)],
            }
        )
    return samples


def sample_selection_summary(records: list[dict[str, Any]], samples: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for sample in samples:
        for reason in sample["reasons"]:
            counts[reason] += 1
    return dict(sorted(counts.items()))


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    record_types = Counter(str(record.get("record_type", "")) for record in records)
    return {
        "total_records": len(records),
        "record_types": dict(sorted(record_types.items())),
        "with_hebrew": sum(1 for record in records if record_hebrew(record)),
        "with_translation": sum(1 for record in records if record_english(record)),
        "missing_source_reference": sum(1 for record in records if not record_ref(record)),
        "missing_hebrew": sum(1 for record in records if not record_hebrew(record)),
        "missing_translation": sum(1 for record in records if not record_english(record)),
        "with_mapping": sum(1 for record in records if record_mapping(record)),
        "with_warnings": sum(1 for record in records if record.get("extraction_quality_flags")),
    }


def batch_range(records: list[dict[str, Any]]) -> str:
    refs = [record_ref(record) for record in records if record_ref(record)]
    if not refs:
        return "unknown"
    if refs[0] == refs[-1]:
        return refs[0]
    return f"{refs[0]} through {refs[-1]}"


def confirmation_items_for_batch(
    confirmation_items: dict[str, Any],
    *,
    batch: dict[str, Any] | None,
    package: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    items = [item for item in confirmation_items.get("confirmation_items", []) if isinstance(item, dict)]
    if not batch:
        return [], items

    batch_paths = set(batch.get("raw_source_files") or []) | set(batch.get("normalized_data_files") or [])
    package_id = str(package.get("source_package_id", ""))
    package_name = str(package.get("display_name", ""))
    relevant: list[dict[str, Any]] = []
    global_items: list[dict[str, Any]] = []
    for item in items:
        item_path = str(item.get("file_path", ""))
        item_source = str(item.get("source_name", ""))
        if item_path in batch_paths or package_id in item_path or package_name in item_source:
            relevant.append(item)
        else:
            global_items.append(item)
    return relevant, global_items


def render_confirmation_table(items: list[dict[str, Any]]) -> list[str]:
    if not items:
        return ["No targeted confirmation items are specific to this batch."]
    lines = [
        "| Confirmation Item ID | Source Name | File Path | Unclear Issue | Exact Question For Yossi | Current Status | Recommended Status |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in items:
        lines.append(
            "| "
            f"`{md(item.get('confirmation_item_id'))}` | "
            f"{brief(item.get('source_name'))} | "
            f"`{md(item.get('file_path'))}` | "
            f"{brief(item.get('unclear_issue'))} | "
            f"{brief(item.get('exact_question_for_yossi'))} | "
            f"`{md(item.get('current_status'))}` | "
            f"{brief(item.get('recommended_status_after_confirmation'))} |"
        )
    return lines


def batch_review_recommendation(batch_id: str | None, summary: dict[str, Any]) -> str:
    if batch_id == "batch_002_linear_bereishis":
        return (
            "Not fully approved yet. Sample extractions look generally plausible, but all 123 records carry "
            "warning flags due to noisy PDF extraction and Hebrew alignment from canonical pasuk text. Please use "
            "this expanded packet to confirm Hebrew-English phrase matching, long parenthetical alignment, and long "
            "phrase boundaries before marking this batch Yossi extraction verified."
        )
    if batch_id == "batch_003_linear_bereishis_2_4_to_2_25":
        return (
            "Not fully approved yet. Sample extractions look generally plausible, but all 90 records carry warning "
            "flags due to noisy PDF extraction and Hebrew alignment from canonical pasuk text. Please use this "
            "expanded packet to confirm Hebrew-English phrase matching, long parenthetical alignment, and long phrase "
            "boundaries before marking this batch Yossi extraction verified."
        )
    warning_count = summary.get("with_warnings", 0)
    total_count = summary.get("total_records", 0)
    if warning_count:
        return (
            f"Not fully approved yet. {warning_count} of {total_count} records carry warning flags. "
            "Use this expanded packet to confirm extraction accuracy before marking this batch Yossi extraction verified."
        )
    return "Pending Yossi extraction-accuracy review. Use this packet to confirm extraction accuracy before verification."


def generated_batch_confirmation_items(summary: dict[str, Any]) -> list[dict[str, Any]]:
    warning_count = summary["with_warnings"]
    return [
        {
            "confirmation_item_id": "confirm_hebrew_english_phrase_matching",
            "source_name": "Batch source extraction",
            "file_path": "batch normalized records",
            "unclear_issue": f"All or many records carry warning flags ({warning_count} warnings counted).",
            "exact_question_for_yossi": "Does each sampled Hebrew phrase match the attached English translation phrase?",
            "current_status": PENDING_ACCURACY_PASS,
            "recommended_status_after_confirmation": "If all rows are accurate, a separate task may mark the batch yossi_extraction_verified.",
        },
        {
            "confirmation_item_id": "confirm_parenthetical_explanation_alignment",
            "source_name": "Batch source extraction",
            "file_path": "batch normalized records",
            "unclear_issue": "Parenthetical explanations may be attached to the wrong Hebrew phrase if phrase boundaries drifted.",
            "exact_question_for_yossi": "Are parenthetical explanations aligned to the correct Hebrew phrase or segment?",
            "current_status": PENDING_ACCURACY_PASS,
            "recommended_status_after_confirmation": "Correct any misaligned row before verification.",
        },
        {
            "confirmation_item_id": "confirm_long_phrase_boundary_accuracy",
            "source_name": "Batch source extraction",
            "file_path": "batch normalized records",
            "unclear_issue": "Long Hebrew or English segments are more likely to hide phrase-boundary mistakes.",
            "exact_question_for_yossi": "Do long Hebrew phrase boundaries match the source and pasuk flow?",
            "current_status": PENDING_ACCURACY_PASS,
            "recommended_status_after_confirmation": "Keep unclear long rows pending until corrected.",
        },
        {
            "confirmation_item_id": "confirm_source_wording_not_generated",
            "source_name": "Batch source extraction",
            "file_path": "cleaned source excerpt and normalized records",
            "unclear_issue": "The packet must distinguish copied/extracted source wording from generated wording.",
            "exact_question_for_yossi": "Is the English wording copied/extracted from the trusted source rather than generated by the system?",
            "current_status": PENDING_ACCURACY_PASS,
            "recommended_status_after_confirmation": "Only source-derived wording may become extraction-verified.",
        },
        {
            "confirmation_item_id": "confirm_cleanup_normalization_acceptable",
            "source_name": "Batch source extraction",
            "file_path": "cleaned source excerpt and normalized records",
            "unclear_issue": "Cleaned text may have normalized noisy PDF output beyond acceptable extraction cleanup.",
            "exact_question_for_yossi": "Was the cleaned text normalized only enough to recover the source, without changing meaning?",
            "current_status": PENDING_ACCURACY_PASS,
            "recommended_status_after_confirmation": "Document or correct any over-normalized row.",
        },
        {
            "confirmation_item_id": "confirm_segment_order_matches_pasuk_flow",
            "source_name": "Batch source extraction",
            "file_path": "batch normalized records",
            "unclear_issue": "Segment order must match the pasuk flow for future map expansion.",
            "exact_question_for_yossi": "Does segment order follow the pasuk flow in the source?",
            "current_status": PENDING_ACCURACY_PASS,
            "recommended_status_after_confirmation": "Correct ordering before verification if needed.",
        },
    ]
def render_sample(sample: dict[str, Any], item_number: int) -> list[str]:
    record = sample["record"]
    source_trace = record.get("source_trace") if isinstance(record.get("source_trace"), dict) else {}
    item_id = str(record.get("id", ""))
    ref = record_ref(record)
    flags = record.get("extraction_quality_flags") or []
    flags_text = ", ".join(str(flag) for flag in flags) if isinstance(flags, list) else str(flags)
    extracted_classification = f"{record.get('record_type', '')}; {record.get('translation_type', '')}".strip("; ")
    source_snippet = source_trace.get("source_snippet_raw") or (
        "Raw source side-by-side comparison could not be automatically aligned; reviewer should compare against source path."
    )
    source_hebrew = source_snippet.split("=", 1)[0].strip() if "=" in source_snippet else source_snippet
    source_english = source_snippet.split("=", 1)[1].strip() if "=" in source_snippet else source_snippet
    parenthetical = record_parenthetical_text(record)
    alignment_reason = (
        "The source excerpt contains an equals-sign phrase pair, the extracted Hebrew is the canonical Hebrew phrase "
        "aligned for this source-backed ref, and the extracted English matches the cleaned source phrase after the equals sign."
    )
    if "source_pdf_text_layer_noisy" in flags:
        alignment_reason += " The PDF text layer was noisy, so Yossi must confirm that this canonical-Hebrew alignment is acceptable."
    return [
        f"### Item {item_number} - {md(ref)} / `{md(item_id)}`",
        "",
        f"Sample reasons: {', '.join(dict.fromkeys(sample['reasons']))}.",
        "",
        f"- Reference: `{md(ref)}`",
        f"- Source reference: `{md(source_trace.get('source_ref') or source_trace.get('source_section') or '')}`",
        f"- Source excerpt: {brief(source_snippet, limit=520)}",
        f"- Cleaned source Hebrew side: {brief(source_hebrew, limit=260)}",
        f"- Extracted Hebrew: {brief(record_hebrew(record), limit=260)}",
        f"- Source English / Translation side: {brief(source_english, limit=360)}",
        f"- Extracted English / Translation: {brief(record_english(record), limit=360)}",
        f"- Parenthetical / explanatory text: {brief(parenthetical or 'none recorded', limit=300)}",
        f"- Segment order: `{md(record.get('segment_order'))}`",
        f"- Classification: `{md(extracted_classification)}`",
        f"- Mapping / skill: `{md(record_mapping(record))}`",
        f"- Warning flags: `{md(flags_text)}`",
        f"- Source extraction method: `{md(source_trace.get('extraction_method') or '')}`",
        f"- Source extraction note: {brief(source_trace.get('extraction_note') or '', limit=520)}",
        f"- Why this match is believed correct: {alignment_reason}",
        "",
        "Human review question: Does the extracted Hebrew phrase correctly match the source English/translation phrase and any parenthetical explanation for this specific segment?",
        "",
        "Yossi checks:",
        "",
        "- [ ] Source match",
        "- [ ] Hebrew phrase alignment",
        "- [ ] English / translation alignment",
        "- [ ] Parenthetical explanation alignment",
        "- [ ] Segment order matches pasuk flow",
        "- [ ] Classification and mapping reasonable",
        "- [ ] Needs correction",
        "",
        "Yossi notes: ____________________________________________________",
        "",
    ]


def render_packet(
    *,
    source_package_id: str,
    batch_id: str | None = None,
    registry: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    confirmation_items: dict[str, Any] | None = None,
    template_text: str | None = None,
    print_friendly: bool = True,
) -> str:
    registry = registry or load_json(REGISTRY_PATH)
    manifest = manifest or load_json(MANIFEST_PATH)
    confirmation_items = confirmation_items or load_json(CONFIRMATION_ITEMS_PATH)
    template_text = template_text or load_template_text()

    packages = source_packages_by_id(registry)
    if source_package_id not in packages:
        raise ValueError(f"Unknown source_package_id: {source_package_id}")
    package = packages[source_package_id]
    require_trusted_source_package(package)

    batch = None
    records: list[dict[str, Any]] = []
    if batch_id:
        batches = batches_by_id(manifest)
        if batch_id not in batches:
            raise ValueError(f"Unknown batch_id: {batch_id}")
        batch = batches[batch_id]
        if batch.get("source_package_id") != source_package_id:
            raise ValueError(f"{batch_id}: batch source_package_id does not match {source_package_id}")
        require_trusted_source_batch(batch)
        records = load_batch_records(batch)

    summary = summarize_records(records)
    samples = choose_review_samples(records)
    selection_summary = sample_selection_summary(records, samples)
    relevant_items, global_items = confirmation_items_for_batch(
        confirmation_items,
        batch=batch,
        package=package,
    )
    relevant_items = [*generated_batch_confirmation_items(summary), *relevant_items]
    raw_paths = batch.get("raw_source_files", []) if batch else []
    normalized_paths = batch.get("normalized_data_files", []) if batch else []
    recommendation = batch_review_recommendation(batch_id, summary)

    lines = [
        "# Trusted Source Extraction Accuracy Review Packet",
        "",
        "Packet family: Trusted Teacher Source Extraction Accuracy Review Packet",
        "",
        "This packet is print-friendly Markdown generated from the trusted teacher-source extraction review template for Yossi's extraction-accuracy confirmation pass. It is not broad educational re-approval, not generated-question review, and not runtime approval.",
        "",
        "## 1. One-Page Review Summary",
        "",
        f"- Batch ID: `{batch_id or 'not batch-specific'}`",
        f"- Source package: `{source_package_id}` - {package.get('display_name', '')}",
        f"- Source authority: `{package.get('source_authority', '')}`",
        f"- Pasuk/content range: {batch_range(records)}",
        "- Raw source file path:",
        *markdown_list(raw_paths),
        "- Normalized data file path:",
        *markdown_list(normalized_paths),
        f"- Number of extracted records: `{summary['total_records']}`",
        f"- Record types included: `{', '.join(summary['record_types'].keys()) or 'none'}`",
        f"- Extraction review status: `{batch.get('extraction_review_status') if batch else package.get('extraction_review_status')}`",
        f"- Runtime status: `{NOT_RUNTIME_READY}` / `not_runtime_active`",
        f"- Question status: `{NOT_QUESTION_READY}`",
        f"- Question-generation status: `{NOT_QUESTION_READY}`",
        "- Student-facing status: `not_student_facing`",
        f"- Recommended current Yossi decision: {recommendation}",
        "",
        "Yossi decision box:",
        "",
        "- [ ] Approved extraction accuracy",
        "- [ ] Approved with corrections needed",
        "- [ ] Not approved yet",
        "",
        "Signature / reviewer:",
        "",
        "Date:",
        "",
        "Notes:",
        "",
        PAGE_BREAK if print_friendly else "",
        "",
        "## 2. What Yossi Is Checking",
        "",
        "- I am checking extraction accuracy only.",
        "- I am not re-approving the educational value of this trusted source.",
        "- I am not approving runtime use.",
        "- I am not approving generated questions.",
        "- Do not re-approve the educational value of this trusted source from scratch.",
        "",
        "Yossi should confirm source matching, Hebrew fidelity, OCR/copy accuracy, extracted translation/explanation accuracy, classification, and mapping.",
        "",
        "Important current decision: Do not mark this batch fully `yossi_extraction_verified` yet. The expanded evidence below is intended to make that future decision possible after Yossi checks Hebrew-English phrase matching, long parenthetical alignment, and long phrase boundaries.",
        "",
        "## 3. Safety Boundaries",
        "",
        "- Runtime: blocked",
        "- Question generation: blocked",
        "- Student-facing use: blocked",
        "- Reviewed bank: blocked",
        "",
        "This packet does not authorize generated questions, protected previews, answer choices, answer keys, reviewed-bank promotion, runtime activation, or student-facing use.",
        "",
        "## 4. Review Instructions",
        "",
        "1. Review the expanded source/evidence cards.",
        "2. Check Hebrew-English phrase matching.",
        "3. Check parenthetical/explanatory alignment.",
        "4. Check long phrase boundaries and segment order.",
        "5. Mark any row needing correction before verification.",
        "6. Leave the batch pending unless all sampled evidence supports full extraction accuracy.",
        "",
        PAGE_BREAK if print_friendly else "",
        "",
        "## 5. Expanded Source Evidence Review Samples",
        "",
    ]

    if not samples:
        lines.extend(
            [
                "No normalized records were available for automatic sampling.",
                "",
                "Raw source side-by-side comparison could not be automatically aligned; reviewer should compare against source path.",
                "",
            ]
        )
    else:
        for item_number, sample in enumerate(samples, 1):
            lines.extend(render_sample(sample, item_number))

    lines.extend(
        [
            PAGE_BREAK if print_friendly else "",
            "",
            "## 6. Expanded Sample Selection Logic",
            "",
            "The generator selected an expanded deterministic evidence set because every record in Batch 002/003 currently carries warning flags from noisy PDF extraction and canonical-Hebrew alignment.",
            "",
            "- First records: first 5 records",
            "- Last records: last 5 records",
            "- Deterministic random records: 10 records selected by stable SHA-256 ordering",
            "- Longest English / explanatory records: top 10 by extracted English length",
            "- Long parenthetical records: all records with substantial parenthetical or explanatory text",
            "- Long Hebrew records: top 10 by extracted Hebrew phrase length",
            "- Missing/suspicious display fields: all records detected by the generator",
            f"- Samples included in this packet: `{len(samples)}`",
            f"- Sample bucket counts: `{selection_summary}`",
            f"- Full normalized file(s): {', '.join(f'`{path}`' for path in normalized_paths) or '`none listed`'}",
            "",
            "## 7. Extraction Summary Table",
            "",
            "| Count Type | Count |",
            "|---|---:|",
            f"| Total records | {summary['total_records']} |",
            f"| Records by type | {md(summary['record_types'])} |",
            f"| Records with Hebrew | {summary['with_hebrew']} |",
            f"| Records with English/translation | {summary['with_translation']} |",
            f"| Records missing source reference | {summary['missing_source_reference']} |",
            f"| Records missing Hebrew | {summary['missing_hebrew']} |",
            f"| Records missing translation | {summary['missing_translation']} |",
            f"| Records with classification/mapping | {summary['with_mapping']} |",
            f"| Records with warnings | {summary['with_warnings']} |",
            "",
            "## 8. Targeted Confirmation Items",
            "",
            "Batch-specific targeted confirmation items:",
            "",
            *render_confirmation_table(relevant_items),
            "",
        ]
    )
    if global_items:
        lines.extend(
            [
                "Unrelated global confirmation items were intentionally omitted from this batch packet. They should be reviewed in a separate global source-confirmation packet, not as part of the Batch 002/003 extraction decision.",
                "",
            ]
        )

    lines.extend(
        [
            "## 9. Corrections Log",
            "",
            "| Item ID | Issue Type | Correction Needed | Yossi Notes | Resolved? |",
            "|---|---|---|---|---|",
            "|  | Hebrew/OCR |  |  |  |",
            "|  | Translation/explanation |  |  |  |",
            "|  | Missing record |  |  |  |",
            "|  | Wrong reference |  |  |  |",
            "|  | Wrong classification |  |  |  |",
            "|  | Wrong mapping |  |  |  |",
            "|  | Unclear source |  |  |  |",
            "|  | Other |  |  |  |",
            "",
            PAGE_BREAK if print_friendly else "",
            "",
            "## 10. Final Decision Page",
            "",
            f"Batch: `{batch_id or 'not batch-specific'}`",
            "",
            "Reviewer:",
            "",
            "Date:",
            "",
            "Decision:",
            "",
            "- [ ] Approved extraction accuracy",
            "- [ ] Approved with corrections needed",
            "- [ ] Not approved yet",
            "",
            "Required corrections:",
            "",
            "1.",
            "2.",
            "3.",
            "",
            "Final notes:",
            "",
            "____________________________________________________",
            "",
            "## Appendix: Review Paths That Remain Strict",
            "",
            "- AI-generated questions still require full generated-question review.",
            "- Protected preview packets still require protected preview review.",
            "- Answer choices and answer keys still require their own review before use.",
            "- Reviewed-bank promotion still requires a reviewed-bank promotion gate.",
            "- Runtime activation still requires a runtime activation gate.",
            "",
            "## Appendix: Template Source",
            "",
            f"- Policy: `{repo_relative(POLICY_PATH)}`",
            f"- Template: `{repo_relative(TEMPLATE_PATH)}`",
            "",
            "Required template language present: one extraction-accuracy confirmation pass. Confirm that the copied or OCRed source text matches the source. Confirm that Hebrew spelling, nikud, and table layout are faithful. Confirm that translations, explanations, answer keys, or examples were extracted accurately. Confirm that classification and standards/skill mapping are reasonable.",
        ]
    )
    return "\n".join(line for line in lines if line is not None) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a trusted teacher-source extraction accuracy review packet."
    )
    parser.add_argument("--source-package-id", required=True)
    parser.add_argument("--batch-id")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--no-print-friendly",
        action="store_true",
        help="Omit Markdown page-break helpers. By default packets are print-friendly.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = render_packet(
        source_package_id=args.source_package_id,
        batch_id=args.batch_id,
        print_friendly=not args.no_print_friendly,
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(packet, encoding="utf-8")
    else:
        print(packet, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
