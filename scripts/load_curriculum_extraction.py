from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "curriculum_extraction"
MANIFEST_PATH = DATA_DIR / "curriculum_extraction_manifest.json"

SKILL_TAG_ALIASES = {
    "phrase_translation": {"translation_context", "skill_tag.translation_context"},
    "translation_context": {"translation_context", "skill_tag.translation_context"},
    "word_translation": {"translation_context", "skill_tag.translation_context"},
    "shoresh": {"shoresh_identification", "skill_tag.shoresh_identification"},
    "prefix_suffix": {
        "prefix_meaning",
        "skill_tag.prefix_meaning",
        "suffix_meaning",
        "skill_tag.suffix_meaning",
    },
    "vocabulary": {"vocabulary_priority", "skill_tag.vocabulary_priority"},
    "pasuk_comprehension": {"text_comprehension", "skill_tag.text_comprehension"},
    "al_mi_neemar": {
        "text_comprehension",
        "skill_tag.text_comprehension",
        "phrase_intent",
        "skill_tag.phrase_intent",
    },
    "mi_amar_el_mi": {
        "text_comprehension",
        "skill_tag.text_comprehension",
        "phrase_intent",
        "skill_tag.phrase_intent",
    },
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


class CurriculumExtractionLoader:
    def __init__(self) -> None:
        self.manifest = load_json(MANIFEST_PATH)
        if not isinstance(self.manifest, dict):
            raise ValueError("curriculum_extraction_manifest.json must be a JSON object")
        self.sample_records = self._load_records(self.manifest.get("sample_files", []))
        self.normalized_records = self._load_records(self.manifest.get("normalized_data_files", []))
        self.records = [*self.sample_records, *self.normalized_records]
        self.records_by_source = self._group_by_source()
        self.records_by_skill = self._group_by_skill()
        self.records_by_pasuk = self._group_by_pasuk()
        self.records_by_batch = self._group_by_batch()

    def _load_records(self, relative_paths: list[str]) -> list[dict]:
        records: list[dict] = []
        for relative in relative_paths:
            path = ROOT / relative
            if path.exists():
                records.extend(load_jsonl(path))
        return records

    def _group_by_source(self) -> dict[str, list[dict]]:
        grouped: dict[str, list[dict]] = defaultdict(list)
        for record in self.records:
            grouped[str(record.get("source_package_id", ""))].append(record)
        return dict(grouped)

    def _group_by_batch(self) -> dict[str, list[dict]]:
        grouped: dict[str, list[dict]] = defaultdict(list)
        for record in self.records:
            grouped[str(record.get("extraction_batch_id", ""))].append(record)
        return dict(grouped)

    def _group_by_skill(self) -> dict[str, list[dict]]:
        grouped: dict[str, list[dict]] = defaultdict(list)
        for record in self.records:
            keys: set[str] = set()
            if record.get("record_type") == "skill_tag":
                if record.get("id"):
                    keys.add(str(record["id"]))
                if record.get("skill_key"):
                    keys.add(str(record["skill_key"]))
            for skill_tag in record.get("skill_tags", []) or []:
                skill_tag = str(skill_tag)
                keys.add(skill_tag)
                if skill_tag.startswith("skill_tag."):
                    keys.add(skill_tag.split("skill_tag.", 1)[1])
                for alias in SKILL_TAG_ALIASES.get(skill_tag, set()):
                    keys.add(alias)
                    if alias.startswith("skill_tag."):
                        keys.add(alias.split("skill_tag.", 1)[1])
            for key in keys:
                grouped[key].append(record)
        return dict(grouped)

    def _group_by_pasuk(self) -> dict[tuple[str, int, int], list[dict]]:
        grouped: dict[tuple[str, int, int], list[dict]] = defaultdict(list)
        for record in self.records:
            sefer = record.get("sefer")
            perek = record.get("perek")
            pasuk = record.get("pasuk")
            if isinstance(sefer, str) and isinstance(perek, int) and isinstance(pasuk, int):
                grouped[(sefer, perek, pasuk)].append(record)
        return dict(grouped)

    def summary(self) -> dict:
        record_type_counts = Counter(record.get("record_type") for record in self.records if record.get("record_type"))
        review_status_counts = Counter(record.get("review_status") for record in self.records if record.get("review_status"))
        runtime_status_counts = Counter(record.get("runtime_status") for record in self.records if record.get("runtime_status"))
        source_counts = {key: len(value) for key, value in sorted(self.records_by_source.items())}
        skill_counts = {key: len(value) for key, value in sorted(self.records_by_skill.items())}
        batch_counts = {key: len(value) for key, value in sorted(self.records_by_batch.items())}
        return {
            "manifest_version": self.manifest.get("version"),
            "status": self.manifest.get("status"),
            "integration_status": self.manifest.get("integration_status"),
            "runtime_active": self.manifest.get("runtime_active"),
            "sample_record_count": len(self.sample_records),
            "normalized_record_count": len(self.normalized_records),
            "record_count": len(self.records),
            "record_type_counts": dict(sorted(record_type_counts.items())),
            "review_status_counts": dict(sorted(review_status_counts.items())),
            "runtime_status_counts": dict(sorted(runtime_status_counts.items())),
            "source_package_counts": source_counts,
            "skill_group_counts": skill_counts,
            "batch_counts": batch_counts,
            "pasuk_group_count": len(self.records_by_pasuk),
        }

    def records_for_pasuk(self, sefer: str, perek: int, pasuk: int) -> list[dict]:
        return list(self.records_by_pasuk.get((sefer, perek, pasuk), []))

    def records_for_skill(self, skill_key: str) -> list[dict]:
        return list(self.records_by_skill.get(skill_key, []))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read isolated curriculum extraction scaffold data.")
    parser.add_argument("--summary", action="store_true", help="Print a summary of loaded records.")
    parser.add_argument("--pasuk", nargs=3, metavar=("SEFER", "PEREK", "PASUK"), help="Return records for one pasuk.")
    parser.add_argument("--skill", metavar="SKILL_KEY", help="Return records for one skill tag or skill key.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    loader = CurriculumExtractionLoader()

    if args.pasuk:
        sefer, perek, pasuk = args.pasuk
        payload = loader.records_for_pasuk(sefer, int(perek), int(pasuk))
    elif args.skill:
        payload = loader.records_for_skill(args.skill)
    else:
        payload = loader.summary()

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
