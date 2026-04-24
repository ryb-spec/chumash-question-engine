from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "curriculum_extraction"
MANIFEST_PATH = DATA_DIR / "curriculum_extraction_manifest.json"
PREVIEW_PATH = DATA_DIR / "generated_questions_preview" / "batch_001_preview.jsonl"
REPORT_PATH = DATA_DIR / "reports" / "batch_001_preview_summary.md"

TARGET_COUNTS = {
    "phrase_translation": 50,
    "hebrew_to_english_match": 25,
    "english_to_hebrew_match": 25,
    "shoresh_identification": 25,
    "prefix_identification": 15,
    "suffix_identification": 15,
    "mi_amar_el_mi": 10,
    "al_mi_neemar": 10,
}

QUESTION_SKILL_TAGS = {
    "phrase_translation": ["translation_context"],
    "hebrew_to_english_match": ["vocabulary_priority", "translation_context"],
    "english_to_hebrew_match": ["vocabulary_priority", "translation_context"],
    "shoresh_identification": ["shoresh_identification"],
    "prefix_identification": ["prefix_meaning"],
    "suffix_identification": ["suffix_meaning"],
    "mi_amar_el_mi": ["text_comprehension", "phrase_intent"],
    "al_mi_neemar": ["text_comprehension", "phrase_intent"],
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            if isinstance(payload, dict):
                records.append(payload)
    return records


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_template_lookup(manifest: dict) -> dict[str, dict]:
    template_lookup: dict[str, dict] = {}
    for relative in manifest.get("sample_files", []):
        path = ROOT / relative
        if not path.exists():
            continue
        for record in load_jsonl(path):
            if record.get("record_type") == "question_template" and record.get("template_key"):
                template_lookup[str(record["template_key"])] = record
    return template_lookup


def load_batch_001_records(manifest: dict) -> list[dict]:
    records: list[dict] = []
    for relative in manifest.get("normalized_data_files", []):
        path = ROOT / relative
        if not path.exists():
            continue
        for record in load_jsonl(path):
            if record.get("extraction_batch_id") == "batch_001_cleaned_seed":
                records.append(record)
    return records


def non_empty_text(value: object) -> str:
    if isinstance(value, str):
        return value.strip()
    return ""


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if not value:
            continue
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def literal_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    results: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            results.append(item.strip())
    return results


def first_gloss(record: dict) -> str:
    glosses = literal_list(record.get("english_glosses"))
    return glosses[0] if glosses else ""


def source_sort_key(record: dict) -> tuple:
    return (
        str(record.get("sefer", "")),
        int(record.get("perek", 0) or 0),
        int(record.get("pasuk", 0) or 0),
        int(record.get("segment_order", 0) or 0),
        str(record.get("id", "")),
    )


def candidate_similarity_key(target: str, candidate: str) -> tuple:
    return (
        abs(len(target.split()) - len(candidate.split())),
        abs(len(target) - len(candidate)),
        candidate.lower(),
    )


def choose_distractors(answer: str, candidates: list[str], limit: int) -> list[str]:
    unique_candidates = unique_preserve_order([candidate for candidate in candidates if candidate != answer])
    ranked = sorted(unique_candidates, key=lambda candidate: candidate_similarity_key(answer, candidate))
    return ranked[:limit]


def preview_skill_tags(record: dict, question_type: str) -> list[str]:
    source_tags = [str(tag) for tag in record.get("skill_tags", []) if isinstance(tag, str)]
    requested_tags = QUESTION_SKILL_TAGS.get(question_type, [])
    return unique_preserve_order([*requested_tags, *source_tags])


def build_preview_record(
    *,
    question_type: str,
    record: dict,
    variant_index: int,
    prompt: str,
    answer: str,
    distractors: list[str],
) -> dict:
    return {
        "id": f"generated_preview.{question_type}.{record['id']}.{variant_index + 1:02d}",
        "schema_version": "0.1",
        "record_type": "generated_question_preview",
        "source_record_id": record["id"],
        "source_package_id": record["source_package_id"],
        "question_type": question_type,
        "prompt": prompt,
        "answer": answer,
        "distractors": distractors,
        "skill_tags": preview_skill_tags(record, question_type),
        "source_trace": deepcopy(record["source_trace"]),
        "review_status": "needs_review",
        "runtime_status": "not_runtime_active",
        "confidence": "low",
    }


def planned_pairs(records: list[dict], variant_count: int, target_count: int) -> list[tuple[dict, int]]:
    pairs: list[tuple[dict, int]] = []
    for variant_index in range(variant_count):
        for record in records:
            pairs.append((record, variant_index))
    return pairs[:target_count]


def generate_phrase_translation(records: list[dict], template_lookup: dict[str, dict]) -> list[dict]:
    template = template_lookup["translation_core_context"]
    prompt_variants = [
        lambda record: template["prompt_template"].replace("{{segment_text}}", record["hebrew_raw"]),
        lambda record: f"Translate this Hebrew phrase into English: {record['hebrew_raw']} ({record['canonical_ref']}).",
        lambda record: f"In {record['canonical_ref']}, what is the best English translation of {record['hebrew_raw']}?",
    ]
    generated: list[dict] = []
    for record, variant_index in planned_pairs(records, len(prompt_variants), TARGET_COUNTS["phrase_translation"]):
        generated.append(
            build_preview_record(
                question_type="phrase_translation",
                record=record,
                variant_index=variant_index,
                prompt=prompt_variants[variant_index](record),
                answer=record["english_raw"],
                distractors=[],
            )
        )
    return generated


def generate_hebrew_to_english_match(records: list[dict], template_lookup: dict[str, dict]) -> list[dict]:
    template = template_lookup["vocab_priority_review"]
    prompt_variants = [
        lambda record: f"Which English gloss best matches the Hebrew word {record['hebrew']}?",
        lambda record: f"Choose the best English meaning for {record['hebrew']}.",
        lambda record: template["prompt_template"].replace("{{hebrew}}", record["hebrew"]) + " Which English gloss fits best?",
    ]
    pool = [first_gloss(record) for record in records]
    generated: list[dict] = []
    for record, variant_index in planned_pairs(records, len(prompt_variants), TARGET_COUNTS["hebrew_to_english_match"]):
        answer = first_gloss(record)
        generated.append(
            build_preview_record(
                question_type="hebrew_to_english_match",
                record=record,
                variant_index=variant_index,
                prompt=prompt_variants[variant_index](record),
                answer=answer,
                distractors=choose_distractors(answer, pool, 3),
            )
        )
    return generated


def generate_english_to_hebrew_match(records: list[dict]) -> list[dict]:
    prompt_variants = [
        lambda record: f"Which Hebrew word best matches the English gloss '{first_gloss(record)}'?",
        lambda record: f"Choose the Hebrew match for '{first_gloss(record)}'.",
        lambda record: f"What is the best Hebrew match for the English meaning '{first_gloss(record)}'?",
    ]
    pool = [non_empty_text(record.get("hebrew")) for record in records]
    generated: list[dict] = []
    for record, variant_index in planned_pairs(records, len(prompt_variants), TARGET_COUNTS["english_to_hebrew_match"]):
        answer = non_empty_text(record.get("hebrew"))
        generated.append(
            build_preview_record(
                question_type="english_to_hebrew_match",
                record=record,
                variant_index=variant_index,
                prompt=prompt_variants[variant_index](record),
                answer=answer,
                distractors=choose_distractors(answer, pool, 3),
            )
        )
    return generated


def generate_shoresh_identification(records: list[dict], template_lookup: dict[str, dict]) -> list[dict]:
    template = template_lookup["word_parse_shoresh"]
    prompt_variants = [
        lambda record: template["prompt_template"].replace("{{word_in_pasuk_raw}}", record["word_in_pasuk_raw"]),
        lambda record: f"What is the shoresh of {record['word_in_pasuk_raw']} in {record['canonical_ref']}?",
        lambda record: f"Identify the shoresh of {record['word_in_pasuk_raw']} ({record['contextual_translation']}).",
        lambda record: f"Which shoresh fits the word {record['word_in_pasuk_raw']}?",
        lambda record: f"For the word {record['word_in_pasuk_raw']}, what is the underlying shoresh?",
    ]
    pool = [non_empty_text(record.get("target_shoresh_raw")) for record in records]
    generated: list[dict] = []
    for record, variant_index in planned_pairs(records, len(prompt_variants), TARGET_COUNTS["shoresh_identification"]):
        answer = non_empty_text(record.get("target_shoresh_raw"))
        generated.append(
            build_preview_record(
                question_type="shoresh_identification",
                record=record,
                variant_index=variant_index,
                prompt=prompt_variants[variant_index](record),
                answer=answer,
                distractors=choose_distractors(answer, pool, 3),
            )
        )
    return generated


def first_affix_text(record: dict, affix_key: str) -> str:
    value = record.get(affix_key)
    if not isinstance(value, list):
        return ""
    for item in value:
        if isinstance(item, dict):
            text = non_empty_text(item.get("text"))
            if text:
                return text
    return ""


def generate_prefix_identification(records: list[dict], template_lookup: dict[str, dict]) -> list[dict]:
    template = template_lookup["word_parse_task_scan"]
    prompt_variants = [
        lambda record: template["prompt_template"].replace("{{expected_word_in_pasuk}}", record["word_in_pasuk_raw"]),
        lambda record: f"In the word {record['word_in_pasuk_raw']}, which prefix is present?",
        lambda record: f"Identify the prefix in {record['word_in_pasuk_raw']} ({record['contextual_translation']}).",
    ]
    pool = [first_affix_text(record, "prefixes") for record in records]
    generated: list[dict] = []
    for record, variant_index in planned_pairs(records, len(prompt_variants), TARGET_COUNTS["prefix_identification"]):
        answer = first_affix_text(record, "prefixes")
        generated.append(
            build_preview_record(
                question_type="prefix_identification",
                record=record,
                variant_index=variant_index,
                prompt=prompt_variants[variant_index](record),
                answer=answer,
                distractors=choose_distractors(answer, pool, 3),
            )
        )
    return generated


def generate_suffix_identification(records: list[dict], template_lookup: dict[str, dict]) -> list[dict]:
    template = template_lookup["word_parse_task_scan"]
    prompt_variants = [
        lambda record: template["prompt_template"].replace("{{expected_word_in_pasuk}}", record["word_in_pasuk_raw"]).replace(
            "What prefix or suffix can you identify?",
            "What suffix can you identify?",
        ),
        lambda record: f"In the word {record['word_in_pasuk_raw']}, which suffix is present?",
        lambda record: f"Identify the suffix in {record['word_in_pasuk_raw']} ({record['contextual_translation']}).",
        lambda record: f"What suffix do you see attached to {record['word_in_pasuk_raw']}?",
    ]
    pool = [first_affix_text(record, "suffixes") for record in records]
    generated: list[dict] = []
    for record, variant_index in planned_pairs(records, len(prompt_variants), TARGET_COUNTS["suffix_identification"]):
        answer = first_affix_text(record, "suffixes")
        generated.append(
            build_preview_record(
                question_type="suffix_identification",
                record=record,
                variant_index=variant_index,
                prompt=prompt_variants[variant_index](record),
                answer=answer,
                distractors=choose_distractors(answer, pool, 2),
            )
        )
    return generated


def usable_source_ids(records: list[dict]) -> set[str]:
    usable_ids: set[str] = set()
    for record in records:
        record_type = record.get("record_type")
        if record_type == "pasuk_segment":
            if non_empty_text(record.get("hebrew_raw")) and non_empty_text(record.get("english_raw")):
                usable_ids.add(str(record["id"]))
        elif record_type == "word_parse":
            if (
                non_empty_text(record.get("target_shoresh_raw"))
                or first_affix_text(record, "prefixes")
                or first_affix_text(record, "suffixes")
            ):
                usable_ids.add(str(record["id"]))
        elif record_type == "vocab_entry":
            if first_gloss(record):
                usable_ids.add(str(record["id"]))
    return usable_ids


def relevant_source_ids(records: list[dict]) -> set[str]:
    relevant_types = {
        "pasuk_segment",
        "word_parse",
        "word_parse_task",
        "comprehension_question",
        "vocab_entry",
    }
    return {str(record["id"]) for record in records if record.get("record_type") in relevant_types}


def build_summary_report(
    *,
    preview_records: list[dict],
    source_records: list[dict],
    generated_counts: dict[str, int],
    skipped_question_slots: dict[str, int],
) -> str:
    usable_ids = usable_source_ids(source_records)
    relevant_ids = relevant_source_ids(source_records)
    skipped_source_ids = sorted(relevant_ids - usable_ids)
    usable_pct = 0.0 if not relevant_ids else (len(usable_ids) / len(relevant_ids)) * 100.0
    weak_areas = [
        "All 10 comprehension_question records are missing expected_answer, so mi_amar_el_mi and al_mi_neemar previews were skipped.",
        "All 8 word_parse_task records have answer_status=not_extracted and no expected_word/prefix/suffix payload.",
        "Only 6 of 10 word_parse records include an explicit shoresh.",
        "Only 4 of 10 word_parse records include a suffix payload.",
        "8 of 18 vocab_entry records still have empty english_glosses and remain unusable for matching previews.",
    ]
    structural_issues = [
        "Requested comprehension preview distribution could not be met without inventing answers.",
        "Preview generation currently depends on repeating prompt families across a small approved source pool.",
        "Affix lanes are sourced from word_parse records only because the task-model records have no answer payload yet.",
    ]
    recommendation = "NOT READY"

    lines = [
        "# Batch 001 Preview Summary",
        "",
        "## Totals",
        "",
        f"- Total question count: {len(preview_records)}",
        f"- Skipped source record count: {len(skipped_source_ids)}",
        f"- Skipped requested question slots: {sum(skipped_question_slots.values())}",
        f"- Usable source records: {len(usable_ids)} / {len(relevant_ids)} ({usable_pct:.1f}%)",
        "",
        "## Count By Type",
        "",
    ]
    for question_type in TARGET_COUNTS:
        lines.append(f"- {question_type}: {generated_counts.get(question_type, 0)}")

    lines.extend(
        [
            "",
            "## Weak Data Areas",
            "",
        ]
    )
    for item in weak_areas:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Structural Issues Found",
            "",
        ]
    )
    for item in structural_issues:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            f"- {recommendation} for the next phase until comprehension answers and task-model answer payloads are present.",
        ]
    )
    return "\n".join(lines) + "\n"


def generate_preview() -> dict:
    manifest = load_json(MANIFEST_PATH)
    if not isinstance(manifest, dict):
        raise ValueError("curriculum_extraction_manifest.json must be a JSON object")

    template_lookup = load_template_lookup(manifest)
    source_records = load_batch_001_records(manifest)

    segments = sorted(
        [
            record
            for record in source_records
            if record.get("record_type") == "pasuk_segment"
            and non_empty_text(record.get("hebrew_raw"))
            and non_empty_text(record.get("english_raw"))
        ],
        key=source_sort_key,
    )
    vocab = sorted(
        [
            record
            for record in source_records
            if record.get("record_type") == "vocab_entry" and first_gloss(record)
        ],
        key=lambda record: (int(record.get("priority_level", 0) or 0), non_empty_text(record.get("hebrew"))),
    )
    shoresh_records = sorted(
        [
            record
            for record in source_records
            if record.get("record_type") == "word_parse" and non_empty_text(record.get("target_shoresh_raw"))
        ],
        key=source_sort_key,
    )
    prefix_records = sorted(
        [
            record
            for record in source_records
            if record.get("record_type") == "word_parse" and first_affix_text(record, "prefixes")
        ],
        key=source_sort_key,
    )
    suffix_records = sorted(
        [
            record
            for record in source_records
            if record.get("record_type") == "word_parse" and first_affix_text(record, "suffixes")
        ],
        key=source_sort_key,
    )
    mi_amar_records = sorted(
        [
            record
            for record in source_records
            if record.get("record_type") == "comprehension_question"
            and record.get("question_type") == "mi_amar_el_mi"
            and non_empty_text(record.get("expected_answer"))
        ],
        key=source_sort_key,
    )
    al_mi_records = sorted(
        [
            record
            for record in source_records
            if record.get("record_type") == "comprehension_question"
            and record.get("question_type") == "al_mi_neemar"
            and non_empty_text(record.get("expected_answer"))
        ],
        key=source_sort_key,
    )

    preview_records = [
        *generate_phrase_translation(segments, template_lookup),
        *generate_hebrew_to_english_match(vocab, template_lookup),
        *generate_english_to_hebrew_match(vocab),
        *generate_shoresh_identification(shoresh_records, template_lookup),
        *generate_prefix_identification(prefix_records, template_lookup),
        *generate_suffix_identification(suffix_records, template_lookup),
    ]

    preview_records.sort(key=lambda record: (record["question_type"], record["id"]))
    write_jsonl(PREVIEW_PATH, preview_records)

    generated_counts = Counter(record["question_type"] for record in preview_records)
    skipped_question_slots = {
        question_type: max(TARGET_COUNTS[question_type] - generated_counts.get(question_type, 0), 0)
        for question_type in ("mi_amar_el_mi", "al_mi_neemar")
    }
    report = build_summary_report(
        preview_records=preview_records,
        source_records=source_records,
        generated_counts=dict(generated_counts),
        skipped_question_slots=skipped_question_slots,
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8", newline="\n")

    return {
        "preview_path": PREVIEW_PATH.relative_to(ROOT).as_posix(),
        "report_path": REPORT_PATH.relative_to(ROOT).as_posix(),
        "question_count": len(preview_records),
        "question_type_counts": dict(sorted(generated_counts.items())),
        "skipped_question_slots": skipped_question_slots,
    }


def main() -> int:
    summary = generate_preview()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
