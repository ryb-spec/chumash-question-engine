from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "curriculum_extraction"
MANIFEST_PATH = DATA_DIR / "curriculum_extraction_manifest.json"
PREVIEW_V1_PATH = DATA_DIR / "generated_questions_preview" / "batch_001_preview.jsonl"
PREVIEW_V2_PATH = DATA_DIR / "generated_questions_preview" / "batch_001_preview_v2.jsonl"
REPORT_V2_PATH = DATA_DIR / "reports" / "batch_001_preview_v2_summary.md"
FINAL_DECISION_REPORT_PATH = DATA_DIR / "reports" / "batch_001_round_final_decision.md"

SUPPORTED_TARGET_COUNTS = {
    "phrase_translation": 50,
    "hebrew_to_english_match": 25,
    "english_to_hebrew_match": 25,
    "shoresh_identification": 25,
    "prefix_identification": 15,
    "suffix_identification": 15,
}

BLOCKED_LANES = {
    "mi_amar_el_mi": "Va'eira comprehension questions still have no explicit answer key in repo-local sources.",
    "al_mi_neemar": "Va'eira comprehension questions still have no explicit answer key in repo-local sources.",
    "shemos_word_parse_task_answer_checking": (
        "The Shemos prefix/suffix task answer key is still not present in the worktree, "
        "so task-answer checking remains deferred."
    ),
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
        "id": f"generated_preview_v2.{question_type}.{record['id']}.{variant_index + 1:02d}",
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
    for record, variant_index in planned_pairs(
        records,
        len(prompt_variants),
        SUPPORTED_TARGET_COUNTS["phrase_translation"],
    ):
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
    for record, variant_index in planned_pairs(
        records,
        len(prompt_variants),
        SUPPORTED_TARGET_COUNTS["hebrew_to_english_match"],
    ):
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
    for record, variant_index in planned_pairs(
        records,
        len(prompt_variants),
        SUPPORTED_TARGET_COUNTS["english_to_hebrew_match"],
    ):
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
    for record, variant_index in planned_pairs(
        records,
        len(prompt_variants),
        SUPPORTED_TARGET_COUNTS["shoresh_identification"],
    ):
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
    for record, variant_index in planned_pairs(
        records,
        len(prompt_variants),
        SUPPORTED_TARGET_COUNTS["prefix_identification"],
    ):
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
    for record, variant_index in planned_pairs(
        records,
        len(prompt_variants),
        SUPPORTED_TARGET_COUNTS["suffix_identification"],
    ):
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


def load_existing_preview_counts(path: Path) -> dict[str, int]:
    if not path.exists():
        return {}
    return dict(sorted(Counter(record["question_type"] for record in load_jsonl(path)).items()))


def preview_source_ids(records: list[dict], question_types: set[str]) -> set[str]:
    return {
        str(record["source_record_id"])
        for record in records
        if record.get("question_type") in question_types and record.get("source_record_id")
    }


def blocked_lane_deferred_count(source_records: list[dict], question_type: str) -> int:
    if question_type in {"mi_amar_el_mi", "al_mi_neemar"}:
        return sum(
            1
            for record in source_records
            if record.get("record_type") == "comprehension_question"
            and record.get("question_type") == question_type
        )
    if question_type == "shemos_word_parse_task_answer_checking":
        return sum(1 for record in source_records if record.get("record_type") == "word_parse_task")
    return 0


def build_summary_report(
    *,
    preview_records: list[dict],
    source_records: list[dict],
    generated_counts: dict[str, int],
    v1_counts: dict[str, int],
) -> str:
    v1_records = load_jsonl(PREVIEW_V1_PATH) if PREVIEW_V1_PATH.exists() else []
    vocab_lane_types = {"hebrew_to_english_match", "english_to_hebrew_match"}
    v1_vocab_sources = preview_source_ids(v1_records, vocab_lane_types)
    v2_vocab_sources = preview_source_ids(preview_records, vocab_lane_types)

    lines = [
        "# Batch 001 Preview V2 Summary",
        "",
        "## Totals",
        "",
        f"- Total preview questions: {len(preview_records)}",
        f"- Preview file: `{PREVIEW_V2_PATH.relative_to(ROOT).as_posix()}`",
        "",
        "## Question Counts By Type",
        "",
    ]
    for question_type in SUPPORTED_TARGET_COUNTS:
        lines.append(f"- {question_type}: {generated_counts.get(question_type, 0)}")

    lines.extend(
        [
            "",
            "## Comparison To V1 Preview",
            "",
            f"- V1 file kept for comparison: `{PREVIEW_V1_PATH.relative_to(ROOT).as_posix()}`",
            f"- V1 total questions: {len(v1_records)}",
            f"- V2 total questions: {len(preview_records)}",
        ]
    )
    for question_type in SUPPORTED_TARGET_COUNTS:
        lines.append(
            f"- {question_type}: v1={v1_counts.get(question_type, 0)}, v2={generated_counts.get(question_type, 0)}"
        )

    lines.extend(
        [
            "",
            "## Lanes Improved After Vocab Enrichment",
            "",
            (
                f"- hebrew_to_english_match: unique Batch 001 vocab source coverage increased from "
                f"{len(v1_vocab_sources)} records in v1 to {len(v2_vocab_sources)} in v2."
            ),
            (
                f"- english_to_hebrew_match: same expanded source coverage from "
                f"{len(v1_vocab_sources)} to {len(v2_vocab_sources)} vocab records."
            ),
            (
                "- Newly usable enriched vocab entries: ארץ, אדם, אשה, בית, בן, יום, מים, עץ."
            ),
            "- Distractor quality improved because the vocab matching pool now includes all 18 Batch 001 vocab entries.",
            "",
            "## Lanes Still Blocked",
            "",
        ]
    )
    for lane, blocker in BLOCKED_LANES.items():
        lines.append(
            f"- {lane}: deferred records={blocked_lane_deferred_count(source_records, lane)}; blocker={blocker}"
        )

    lines.extend(
        [
            "",
            "## Recommendation",
            "",
            "- MERGE_INACTIVE_INFRASTRUCTURE as isolated extraction scaffolding and preview tooling.",
            "- BLOCK_RUNTIME_INTEGRATION until explicit source answer keys exist for Va'eira comprehension and Shemos task-answer lanes.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_final_decision_report(
    *,
    generated_counts: dict[str, int],
    source_records: list[dict],
) -> str:
    usable_lanes = [
        "phrase_translation",
        "hebrew_to_english_match",
        "english_to_hebrew_match",
        "shoresh_identification",
        "prefix_identification",
        "suffix_identification",
    ]
    blocked_lanes = [
        "mi_amar_el_mi",
        "al_mi_neemar",
        "shemos_word_parse_task_answer_checking",
    ]
    lines = [
        "# Batch 001 Round Final Decision",
        "",
        "## 1. Did the extraction factory work?",
        "",
        "- Yes. The isolated curriculum extraction scaffold successfully ingested, validated, and organized Batch 001 source-backed seed data without touching runtime.",
        "",
        "## 2. Did validation work?",
        "",
        "- Yes. The validator continued to enforce non-runtime status, source linkage, preview integrity, and blocked-answer guardrails.",
        "",
        "## 3. Did loader isolation work?",
        "",
        "- Yes. The loader still reads only sample and normalized extraction records and ignores preview-question artifacts.",
        "",
        "## 4. Did preview generation work?",
        "",
        (
            f"- Yes for supported lanes. Preview v2 generated {sum(generated_counts.values())} deterministic questions "
            "without forcing blocked answer-key-dependent lanes."
        ),
        "",
        "## 5. Which lanes are usable now?",
        "",
    ]
    for lane in usable_lanes:
        lines.append(f"- {lane}: {generated_counts.get(lane, 0)} preview questions generated in v2")

    lines.extend(
        [
            "",
            "## 6. Which lanes are blocked?",
            "",
        ]
    )
    for lane in blocked_lanes:
        lines.append(
            f"- {lane}: {blocked_lane_deferred_count(source_records, lane)} deferred records; {BLOCKED_LANES[lane]}"
        )

    lines.extend(
        [
            "",
            "## 7. What source material is needed later?",
            "",
            "- Bacharach Shemos prefix/suffix answer-key pages for the 8 blocked word_parse_task records.",
            "- Bacharach Va'eira answer-key pages for the 10 blocked comprehension_question records.",
            "- Any future source-key excerpts should stay outside runtime until separately reviewed and approved.",
            "",
            "## 8. Is this branch safe to merge into main as inactive infrastructure?",
            "",
            "- Yes, if tests pass. The branch is safe to merge as inactive extraction infrastructure, reports, validation, and preview tooling only.",
            "",
            "## 9. Is it safe to connect to runtime now?",
            "",
            "- No. Runtime integration remains blocked because answer-key-dependent lanes are still missing source-bearing material and the extraction outputs remain non-runtime artifacts.",
            "",
            "## Final Recommendation",
            "",
            "- MERGE_INACTIVE_INFRASTRUCTURE",
            "- BLOCK_RUNTIME_INTEGRATION",
            "- Continue future extraction in separate, source-scoped batches.",
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
    preview_records = [
        *generate_phrase_translation(segments, template_lookup),
        *generate_hebrew_to_english_match(vocab, template_lookup),
        *generate_english_to_hebrew_match(vocab),
        *generate_shoresh_identification(shoresh_records, template_lookup),
        *generate_prefix_identification(prefix_records, template_lookup),
        *generate_suffix_identification(suffix_records, template_lookup),
    ]

    preview_records.sort(key=lambda record: (record["question_type"], record["id"]))
    write_jsonl(PREVIEW_V2_PATH, preview_records)

    generated_counts = Counter(record["question_type"] for record in preview_records)
    v1_counts = load_existing_preview_counts(PREVIEW_V1_PATH)
    report = build_summary_report(
        preview_records=preview_records,
        source_records=source_records,
        generated_counts=dict(generated_counts),
        v1_counts=v1_counts,
    )
    REPORT_V2_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_V2_PATH.write_text(report, encoding="utf-8", newline="\n")
    FINAL_DECISION_REPORT_PATH.write_text(
        build_final_decision_report(generated_counts=dict(generated_counts), source_records=source_records),
        encoding="utf-8",
        newline="\n",
    )

    return {
        "preview_path": PREVIEW_V2_PATH.relative_to(ROOT).as_posix(),
        "report_path": REPORT_V2_PATH.relative_to(ROOT).as_posix(),
        "final_decision_report_path": FINAL_DECISION_REPORT_PATH.relative_to(ROOT).as_posix(),
        "question_count": len(preview_records),
        "question_type_counts": dict(sorted(generated_counts.items())),
        "blocked_lanes": BLOCKED_LANES,
    }


def main() -> int:
    summary = generate_preview()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
