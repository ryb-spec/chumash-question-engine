from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "curriculum_extraction" / "curriculum_extraction_manifest.json"
PREVIEW_PATH = (
    ROOT
    / "data"
    / "curriculum_extraction"
    / "generated_questions_preview"
    / "batch_001_preview.jsonl"
)

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
    for key in ("sample_files", "normalized_data_files"):
        for relative in manifest.get(key, []):
            for record in load_jsonl(ROOT / relative):
                if isinstance(record, dict) and record.get("id"):
                    record_ids.add(str(record["id"]))
    return record_ids


def test_preview_file_exists_and_has_minimum_count() -> None:
    assert PREVIEW_PATH.exists()
    records = load_jsonl(PREVIEW_PATH)
    assert len(records) >= 120


def test_preview_records_are_valid_jsonl_with_required_fields() -> None:
    records = load_jsonl(PREVIEW_PATH)
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


def test_preview_validator_accepts_generated_preview() -> None:
    module = load_module(
        "validate_curriculum_extraction",
        ROOT / "scripts" / "validate_curriculum_extraction.py",
    )
    summary = module.validate_curriculum_extraction()
    assert summary["valid"] is True
    assert summary["preview_file_count"] == 1
    assert summary["preview_record_count"] >= 120
    assert summary["preview_question_type_counts"] == EXPECTED_COUNTS


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
