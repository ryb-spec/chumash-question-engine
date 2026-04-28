from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

import skill_catalog
from scripts import validate_canonical_skill_contract as validator


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data" / "standards" / "canonical_skill_contract.json"
ZEKELMAN_DRAFT_PATH = (
    ROOT / "data" / "standards" / "zekelman" / "crosswalks" / "zekelman_2025_standard_3_skill_mapping_draft.json"
)
ENRICHMENT_FILES = [
    ROOT / "data" / "source_skill_enrichment" / "morphology_candidates" / "bereishis_1_1_to_1_5_morphology_candidates.tsv",
    ROOT / "data" / "source_skill_enrichment" / "standards_candidates" / "bereishis_1_1_to_1_5_standards_candidates.tsv",
    ROOT / "data" / "source_skill_enrichment" / "vocabulary_shoresh_candidates" / "bereishis_1_1_to_1_5_vocabulary_shoresh_candidates.tsv",
]
VERIFIED_MAP_FILES = [
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_1_to_3_24_metsudah_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_1_1_to_1_5_source_to_skill_map.tsv",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


class CanonicalSkillContractTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_canonical_skill_contract()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["canonical_skill_count"], 28)
        self.assertEqual(summary["runtime_skill_mapping_count"], len(skill_catalog.skill_ids_in_runtime_order()))
        self.assertEqual(summary["zekelman_skill_mapping_count"], 13)
        self.assertEqual(summary["verified_source_label_mapping_count"], 3)
        self.assertEqual(summary["source_skill_enrichment_candidate_mapping_count"], 17)

    def test_contract_metadata_preserves_scope_and_source_sha(self):
        contract = load_json(CONTRACT_PATH)
        metadata = contract["metadata"]
        self.assertEqual(metadata["active_source_scope"], "local_parsed_bereishis_1_1_to_3_24")
        self.assertEqual(
            metadata["canonical_source_sha"],
            "4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71",
        )
        self.assertEqual(set(metadata["allowed_statuses"]), validator.ALLOWED_CANONICAL_STATUSES)

    def test_contract_canonical_ids_are_unique(self):
        contract = load_json(CONTRACT_PATH)
        canonical_ids = [record["canonical_skill_id"] for record in contract["canonical_skills"]]
        self.assertEqual(len(canonical_ids), len(set(canonical_ids)))

    def test_runtime_mappings_match_skill_catalog(self):
        contract = load_json(CONTRACT_PATH)
        runtime_map = {
            row["runtime_skill_id"]: row["canonical_skill_ids"]
            for row in contract["runtime_skill_mappings"]
        }
        for runtime_skill_id in skill_catalog.skill_ids_in_runtime_order():
            with self.subTest(runtime_skill_id=runtime_skill_id):
                self.assertEqual(
                    runtime_map[runtime_skill_id],
                    skill_catalog.canonical_skill_ids_for_runtime_skill(runtime_skill_id),
                )

    def test_skill_catalog_merges_contract_status_fields(self):
        phrase_record = skill_catalog.canonical_skill_record("PHRASE.UNIT_TRANSLATE")
        self.assertIsNotNone(phrase_record)
        self.assertEqual(phrase_record["status"], "runtime_ready")
        self.assertEqual(phrase_record["skill_lane"], "phrase_translation")
        self.assertEqual(phrase_record["system_layer"], "engine_extension")

        direct_object_record = skill_catalog.canonical_skill_record("PARTICLE.DIRECT_OBJECT_MARKER")
        self.assertIsNotNone(direct_object_record)
        self.assertEqual(direct_object_record["status"], "review_only")
        self.assertEqual(direct_object_record["related_runtime_skill_ids"], [])

    def test_zekelman_draft_skills_all_map_into_contract(self):
        contract = load_json(CONTRACT_PATH)
        draft = load_json(ZEKELMAN_DRAFT_PATH)
        mapped_ids = {row["zekelman_skill_id"] for row in contract["zekelman_skill_mappings"]}
        draft_ids = {row["skill_id_draft"] for row in draft["mappings"]}
        self.assertEqual(mapped_ids, draft_ids)

    def test_verified_source_skill_labels_all_map_into_contract(self):
        contract = load_json(CONTRACT_PATH)
        mapping_keys = {
            (row["label_type"], row["label"])
            for row in contract["verified_source_skill_label_mappings"]
        }
        found_keys = set()
        for verified_map_path in VERIFIED_MAP_FILES:
            for row in load_tsv(verified_map_path):
                for label_type in ("skill_primary", "skill_secondary", "skill_id"):
                    label = (row.get(label_type) or "").strip()
                    if label:
                        found_keys.add((label_type, label))
        self.assertEqual(mapping_keys, found_keys)
        self.assertEqual(mapping_keys, {("skill_primary", "phrase_translation"), ("skill_secondary", "translation_context"), ("skill_id", "phrase_translation")})

    def test_enrichment_candidates_all_map_into_contract(self):
        contract = load_json(CONTRACT_PATH)
        mapped_ids = {row["candidate_id"] for row in contract["source_skill_enrichment_candidate_mappings"]}
        candidate_ids = set()
        for enrichment_path in ENRICHMENT_FILES:
            candidate_ids.update(row["candidate_id"] for row in load_tsv(enrichment_path))
        self.assertEqual(mapped_ids, candidate_ids)

    def test_contract_keeps_review_only_gates_closed(self):
        contract = load_json(CONTRACT_PATH)
        for record in contract["canonical_skills"]:
            with self.subTest(canonical_skill_id=record["canonical_skill_id"]):
                if record["status"] != "runtime_ready":
                    self.assertFalse(any("runtime" in item for item in record["allowed_usage"]))
                joined = " ".join(record["forbidden_usage"]).lower()
                self.assertTrue("do_not" in joined or "no_" in joined)

    def test_validator_rejects_missing_or_bad_canonical_ids(self):
        contract = load_json(CONTRACT_PATH)
        contract["canonical_skills"][0]["status"] = "unsafe_status"
        contract["runtime_skill_mappings"][0]["canonical_skill_ids"] = ["MISSING.SKILL"]
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "bad_contract.json"
            temp_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            summary = validator.validate_canonical_skill_contract(temp_path)
        self.assertFalse(summary["valid"])
        joined = "\n".join(summary["errors"])
        self.assertIn("unsupported status", joined)
        self.assertIn("unknown canonical skill MISSING.SKILL", joined)


if __name__ == "__main__":
    unittest.main()
