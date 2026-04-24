from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "curriculum_extraction" / "curriculum_extraction_manifest.json"
PREVIEW_V1_PATH = (
    ROOT
    / "data"
    / "curriculum_extraction"
    / "generated_questions_preview"
    / "batch_001_preview.jsonl"
)
PREVIEW_V2_PATH = (
    ROOT
    / "data"
    / "curriculum_extraction"
    / "generated_questions_preview"
    / "batch_001_preview_v2.jsonl"
)
PREVIEW_V2_RELATIVE = "data/curriculum_extraction/generated_questions_preview/batch_001_preview_v2.jsonl"
BATCH_002_PREVIEW_PATH = (
    ROOT
    / "data"
    / "curriculum_extraction"
    / "generated_questions_preview"
    / "batch_002_preview.jsonl"
)
BATCH_002_PREVIEW_RELATIVE = "data/curriculum_extraction/generated_questions_preview/batch_002_preview.jsonl"
BATCH_003_PREVIEW_PATH = (
    ROOT
    / "data"
    / "curriculum_extraction"
    / "generated_questions_preview"
    / "batch_003_preview.jsonl"
)
BATCH_003_PREVIEW_RELATIVE = "data/curriculum_extraction/generated_questions_preview/batch_003_preview.jsonl"

REQUIRED_FIELDS = {
    "id",
    "schema_version",
    "record_type",
    "source_record_id",
    "source_package_id",
    "question_type",
    "prompt",
    "answer",
    "distractors",
    "skill_tags",
    "source_trace",
    "review_status",
    "runtime_status",
    "confidence",
}

EXPECTED_COUNTS = {
    "phrase_translation": 50,
    "hebrew_to_english_match": 25,
    "english_to_hebrew_match": 25,
    "shoresh_identification": 25,
    "prefix_identification": 15,
    "suffix_identification": 15,
}
BLOCKED_COUNTS = {
    "mi_amar_el_mi": 0,
    "al_mi_neemar": 0,
}

BATCH_002_EXPECTED_COUNTS = {
    "phrase_translation": 50,
    "hebrew_to_english_match": 25,
    "english_to_hebrew_match": 25,
}

BATCH_003_EXPECTED_COUNTS = {
    "phrase_translation": 50,
    "hebrew_to_english_match": 25,
    "english_to_hebrew_match": 25,
}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Could not load module at {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_record_ids() -> set[str]:
    manifest = load_json(MANIFEST_PATH)
    assert isinstance(manifest, dict)
    record_ids: set[str] = set()
    relative_paths: list[str] = []
    seen: set[str] = set()

    def add_paths(values: object) -> None:
        if not isinstance(values, list):
            return
        for relative in values:
            if isinstance(relative, str) and relative not in seen:
                seen.add(relative)
                relative_paths.append(relative)

    add_paths(manifest.get("sample_files", []))
    add_paths(manifest.get("normalized_data_files", []))
    for batch in manifest.get("resource_batches", []):
        if isinstance(batch, dict):
            add_paths(batch.get("sample_files", []))
            add_paths(batch.get("normalized_data_files", []))

    for relative in relative_paths:
        for record in load_jsonl(ROOT / relative):
            if isinstance(record, dict) and record.get("id"):
                record_ids.add(str(record["id"]))
    return record_ids


def test_preview_v1_is_preserved_and_v2_exists_with_minimum_count() -> None:
    assert PREVIEW_V1_PATH.exists()
    assert PREVIEW_V2_PATH.exists()
    assert BATCH_002_PREVIEW_PATH.exists()
    assert BATCH_003_PREVIEW_PATH.exists()
    records = load_jsonl(PREVIEW_V2_PATH)
    assert len(records) >= 120


def test_batch_002_preview_exists_with_minimum_count() -> None:
    records = load_jsonl(BATCH_002_PREVIEW_PATH)
    assert len(records) >= 100


def test_batch_003_preview_exists_with_minimum_count() -> None:
    records = load_jsonl(BATCH_003_PREVIEW_PATH)
    assert len(records) >= 100


def test_preview_v2_records_are_valid_jsonl_with_required_fields() -> None:
    records = load_jsonl(PREVIEW_V2_PATH)
    record_ids = source_record_ids()
    prompts: set[str] = set()
    counts = Counter(record["question_type"] for record in records)

    for record in records:
        assert REQUIRED_FIELDS.issubset(record)
        assert record["schema_version"] == "0.1"
        assert record["record_type"] == "generated_question_preview"
        assert record["source_record_id"] in record_ids
        assert record["review_status"] == "needs_review"
        assert record["runtime_status"] == "not_runtime_active"
        assert record["confidence"] == "low"
        assert isinstance(record["distractors"], list)
        assert isinstance(record["skill_tags"], list)
        assert isinstance(record["source_trace"], dict)
        assert record["prompt"] not in prompts
        prompts.add(record["prompt"])

    assert dict(counts) == EXPECTED_COUNTS
    for blocked_type, blocked_count in BLOCKED_COUNTS.items():
        assert counts.get(blocked_type, 0) == blocked_count


def test_batch_002_preview_records_are_valid_jsonl_with_required_fields() -> None:
    records = load_jsonl(BATCH_002_PREVIEW_PATH)
    record_ids = source_record_ids()
    prompts: set[str] = set()
    counts = Counter(record["question_type"] for record in records)

    for record in records:
        assert REQUIRED_FIELDS.issubset(record)
        assert record["schema_version"] == "0.1"
        assert record["record_type"] == "generated_question_preview"
        assert record["source_record_id"] in record_ids
        assert record["review_status"] == "needs_review"
        assert record["runtime_status"] == "not_runtime_active"
        assert record["confidence"] == "low"
        assert isinstance(record["distractors"], list)
        assert isinstance(record["skill_tags"], list)
        assert isinstance(record["source_trace"], dict)
        assert record["prompt"] not in prompts
        prompts.add(record["prompt"])

    assert dict(counts) == BATCH_002_EXPECTED_COUNTS


def test_batch_003_preview_records_are_valid_jsonl_with_required_fields() -> None:
    records = load_jsonl(BATCH_003_PREVIEW_PATH)
    record_ids = source_record_ids()
    prompts: set[str] = set()
    counts = Counter(record["question_type"] for record in records)

    for record in records:
        assert REQUIRED_FIELDS.issubset(record)
        assert record["schema_version"] == "0.1"
        assert record["record_type"] == "generated_question_preview"
        assert record["source_record_id"] in record_ids
        assert record["review_status"] == "needs_review"
        assert record["runtime_status"] == "not_runtime_active"
        assert record["confidence"] == "low"
        assert isinstance(record["distractors"], list)
        assert isinstance(record["skill_tags"], list)
        assert isinstance(record["source_trace"], dict)
        assert record["prompt"] not in prompts
        prompts.add(record["prompt"])

    assert dict(counts) == BATCH_003_EXPECTED_COUNTS


def test_preview_v2_vocab_lanes_improve_source_coverage_over_v1() -> None:
    v1_records = load_jsonl(PREVIEW_V1_PATH)
    v2_records = load_jsonl(PREVIEW_V2_PATH)
    vocab_types = {"hebrew_to_english_match", "english_to_hebrew_match"}

    def source_ids(records: list[dict]) -> set[str]:
        return {
            str(record["source_record_id"])
            for record in records
            if record["question_type"] in vocab_types
        }

    v1_sources = source_ids(v1_records)
    v2_sources = source_ids(v2_records)

    assert len(v2_sources) > len(v1_sources)
    expected_enriched_ids = {
        "vocab_entry_batch_001_011_ארץ",
        "vocab_entry_batch_001_012_אדם",
        "vocab_entry_batch_001_013_אשה",
        "vocab_entry_batch_001_014_בית",
        "vocab_entry_batch_001_015_בן",
        "vocab_entry_batch_001_016_יום",
        "vocab_entry_batch_001_017_מים",
        "vocab_entry_batch_001_018_עץ",
    }
    assert expected_enriched_ids.issubset(v2_sources)


def test_preview_validator_accepts_generated_preview() -> None:
    module = load_module(
        "validate_curriculum_extraction",
        ROOT / "scripts" / "validate_curriculum_extraction.py",
    )
    summary = module.validate_curriculum_extraction()
    assert summary["valid"] is True
    assert summary["preview_file_count"] == 4
    assert summary["preview_record_count"] == 510
    assert summary["preview_file_question_type_counts"][PREVIEW_V2_RELATIVE] == EXPECTED_COUNTS
    assert summary["preview_file_question_type_counts"][BATCH_002_PREVIEW_RELATIVE] == BATCH_002_EXPECTED_COUNTS
    assert summary["preview_file_question_type_counts"][BATCH_003_PREVIEW_RELATIVE] == BATCH_003_EXPECTED_COUNTS


def test_loader_ignores_preview_data_safely() -> None:
    module = load_module(
        "load_curriculum_extraction",
        ROOT / "scripts" / "load_curriculum_extraction.py",
    )
    loader = module.CurriculumExtractionLoader()
    summary = loader.summary()
    assert summary["sample_record_count"] == 30
    assert summary["normalized_record_count"] == 75
    assert summary["record_count"] == 105
    assert "generated_question_preview" not in summary["record_type_counts"]
