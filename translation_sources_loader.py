from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
TRANSLATION_REGISTRY_PATH = ROOT / "data" / "source_texts" / "translations" / "translation_sources_registry.json"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError as error:
                raise ValueError(f"{path.as_posix()} line {line_number}: invalid JSON ({error})") from error
            if not isinstance(payload, dict):
                raise ValueError(f"{path.as_posix()} line {line_number}: expected JSON object")
            rows.append(payload)
    return rows


def load_translation_registry() -> dict[str, Any]:
    if not TRANSLATION_REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Translation registry not found: {TRANSLATION_REGISTRY_PATH}")
    payload = _load_json(TRANSLATION_REGISTRY_PATH)
    if not isinstance(payload, dict):
        raise ValueError("Translation registry must be a JSON object.")
    return payload


def _registry_entry_by_version_key(version_key: str) -> dict[str, Any]:
    registry = load_translation_registry()
    for entry in registry.get("available_translation_versions", []):
        if entry.get("translation_version_key") == version_key:
            return entry
    raise KeyError(f"Translation version not found in registry: {version_key}")


def load_bereishis_translation(version_key: str) -> list[dict[str, Any]]:
    entry = _registry_entry_by_version_key(version_key)
    file_path = ROOT / entry["file_path"]
    if not file_path.exists():
        raise FileNotFoundError(f"Translation file not found for {version_key}: {file_path}")
    return _load_jsonl(file_path)


def get_translation_by_ref(version_key: str, ref: str) -> dict[str, Any]:
    for row in load_bereishis_translation(version_key):
        if row.get("ref") == ref:
            return row
    raise KeyError(f"Ref {ref!r} not found for translation version {version_key!r}")


def get_available_translation_versions() -> list[str]:
    registry = load_translation_registry()
    return [entry["translation_version_key"] for entry in registry.get("available_translation_versions", [])]


def get_translation_license_status(version_key: str) -> str:
    return _registry_entry_by_version_key(version_key)["license_status"]


def compare_translations_by_ref(ref: str) -> dict[str, dict[str, Any]]:
    comparison: dict[str, dict[str, Any]] = {}
    for version_key in get_available_translation_versions():
        comparison[version_key] = get_translation_by_ref(version_key, ref)
    return comparison
