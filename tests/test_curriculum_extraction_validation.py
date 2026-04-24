import json
import unittest
from pathlib import Path

from scripts import validate_curriculum_extraction as validator


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "curriculum_extraction" / "curriculum_extraction_manifest.json"


def load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_all_sample_records():
    manifest = load_manifest()
    records = []
    for relative in manifest["sample_files"]:
        path = ROOT / relative
        records.extend(validator.load_jsonl(path))
    return records


def load_all_normalized_records():
    manifest = load_manifest()
    records = []
    for relative in manifest.get("normalized_data_files", []):
        path = ROOT / relative
        records.extend(validator.load_jsonl(path))
    return records


def load_all_records():
    return [*load_all_sample_records(), *load_all_normalized_records()]


class CurriculumExtractionValidationTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_curriculum_extraction(check_git_diff=True)
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["normalized_record_count"], 75)

    def test_manifest_is_not_runtime_active(self):
        manifest = load_manifest()
        self.assertFalse(manifest["runtime_active"])
        self.assertEqual(manifest["integration_status"], "not_runtime_active")
        self.assertEqual(len(manifest.get("normalized_data_files", [])), 6)
        batch_ids = {batch["batch_id"] for batch in manifest.get("resource_batches", [])}
        self.assertIn("batch_001_cleaned_seed", batch_ids)

    def test_no_record_is_reviewed(self):
        for record in load_all_records():
            self.assertEqual(record["review_status"], "needs_review", record["id"])

    def test_no_record_is_runtime_active(self):
        for record in load_all_records():
            self.assertEqual(record["runtime_status"], "not_runtime_active", record["id"])

    def test_no_record_has_high_confidence(self):
        for record in load_all_records():
            self.assertNotEqual(record["confidence"], "high", record["id"])

    def test_every_record_has_source_package_and_source_trace(self):
        for record in load_all_records():
            self.assertIn("source_package_id", record)
            self.assertTrue(record["source_package_id"])
            self.assertIn("source_trace", record)
            self.assertIsInstance(record["source_trace"], dict)

    def test_batch_001_vocab_entries_without_glosses_are_flagged_for_review(self):
        empty_gloss_ids = []
        for record in load_all_normalized_records():
            if record["record_type"] != "vocab_entry":
                continue
            if not record.get("english_glosses"):
                empty_gloss_ids.append(record["id"])
                self.assertTrue(record["needs_gloss_review"], record["id"])
        self.assertGreater(len(empty_gloss_ids), 0)

    def test_forbidden_runtime_files_are_not_changed(self):
        changed_paths = validator.collect_changed_paths()
        disallowed = [path for path in changed_paths if not validator.is_allowed_change(path)]
        self.assertEqual(disallowed, [], [validator.forbidden_reason(path) for path in disallowed])


if __name__ == "__main__":
    unittest.main()
