from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIKDUK_RULES_DIR = ROOT / "data" / "dikduk_rules"
MANIFEST_PATH = DIKDUK_RULES_DIR / "dikduk_rules_manifest.json"
RULE_GROUPS_PATH = DIKDUK_RULES_DIR / "rule_groups.json"
RULES_PATH = DIKDUK_RULES_DIR / "rules_loshon_foundation.jsonl"
QUESTION_TEMPLATES_PATH = DIKDUK_RULES_DIR / "question_templates.jsonl"
ERROR_PATTERNS_PATH = DIKDUK_RULES_DIR / "student_error_patterns.jsonl"


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path} line {line_number} is not valid JSON: {exc}") from exc
            if not isinstance(parsed, dict):
                raise ValueError(f"{path} line {line_number} must decode to a JSON object.")
            records.append(parsed)
    return records


@lru_cache(maxsize=1)
def load_dikduk_rules_manifest() -> dict:
    return _load_json(MANIFEST_PATH)


@lru_cache(maxsize=1)
def load_dikduk_rule_groups() -> list[dict]:
    data = _load_json(RULE_GROUPS_PATH)
    if not isinstance(data, list):
        raise ValueError("rule_groups.json must be a JSON list.")
    return data


@lru_cache(maxsize=1)
def load_dikduk_rules() -> list[dict]:
    return _load_jsonl(RULES_PATH)


@lru_cache(maxsize=1)
def load_dikduk_question_templates() -> list[dict]:
    return _load_jsonl(QUESTION_TEMPLATES_PATH)


@lru_cache(maxsize=1)
def load_dikduk_error_patterns() -> list[dict]:
    return _load_jsonl(ERROR_PATTERNS_PATH)


@lru_cache(maxsize=1)
def rule_group_index() -> dict[str, dict]:
    return {record["group_id"]: record for record in load_dikduk_rule_groups()}


@lru_cache(maxsize=1)
def dikduk_rule_index() -> dict[str, dict]:
    return {record["rule_id"]: record for record in load_dikduk_rules()}


@lru_cache(maxsize=1)
def dikduk_template_index() -> dict[str, dict]:
    return {record["template_id"]: record for record in load_dikduk_question_templates()}


@lru_cache(maxsize=1)
def dikduk_error_index() -> dict[str, dict]:
    return {record["error_id"]: record for record in load_dikduk_error_patterns()}


def get_rules_by_group(group_id: str) -> list[dict]:
    return [record for record in load_dikduk_rules() if record.get("rule_group") == group_id]


def get_rules_by_mastery_tag(tag: str) -> list[dict]:
    return [record for record in load_dikduk_rules() if tag in record.get("mastery_tags", [])]


def get_templates_for_rule(rule_id: str) -> list[dict]:
    return [record for record in load_dikduk_question_templates() if record.get("rule_id") == rule_id]


def get_errors_for_rule(rule_id: str) -> list[dict]:
    return [
        record
        for record in load_dikduk_error_patterns()
        if rule_id in record.get("linked_rule_ids", [])
    ]
