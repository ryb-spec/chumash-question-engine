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


def normalized_records_by_type(record_type):
    return [record for record in load_all_normalized_records() if record["record_type"] == record_type]


class CurriculumExtractionValidationTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_curriculum_extraction(check_git_diff=True)
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["normalized_record_count"], 75)
        self.assertEqual(summary["review_status_counts"]["reviewed"], 75)
        self.assertEqual(summary["review_status_counts"]["needs_review"], 30)

    def test_manifest_is_not_runtime_active(self):
        manifest = load_manifest()
        self.assertFalse(manifest["runtime_active"])
        self.assertEqual(manifest["integration_status"], "not_runtime_active")
        self.assertEqual(len(manifest.get("normalized_data_files", [])), 6)
        batches = {batch["batch_id"]: batch for batch in manifest.get("resource_batches", [])}
        self.assertIn("batch_001_cleaned_seed", batches)
        self.assertEqual(batches["batch_001_cleaned_seed"]["review_status"], "reviewed")
        self.assertEqual(batches["batch_001_cleaned_seed"]["status"], "cleaned_seed_reviewed_non_runtime")

    def test_phase_1_sample_records_stay_needs_review(self):
        for record in load_all_sample_records():
            self.assertEqual(record["review_status"], "needs_review", record["id"])

    def test_batch_001_normalized_records_are_reviewed(self):
        for record in load_all_normalized_records():
            self.assertEqual(record["review_status"], "reviewed", record["id"])
            self.assertEqual(record["source_trace"]["review_status"], "reviewed", record["id"])

    def test_no_record_is_runtime_active(self):
        for record in load_all_records():
            self.assertEqual(record["runtime_status"], "not_runtime_active", record["id"])

    def test_no_record_has_high_confidence(self):
        for record in load_all_records():
            self.assertNotEqual(record["confidence"], "high", record["id"])

    def test_batch_001_normalized_records_move_to_medium_confidence(self):
        for record in load_all_normalized_records():
            self.assertEqual(record["confidence"], "medium", record["id"])

    def test_every_record_has_source_package_and_source_trace(self):
        for record in load_all_records():
            self.assertIn("source_package_id", record)
            self.assertTrue(record["source_package_id"])
            self.assertIn("source_trace", record)
            self.assertIsInstance(record["source_trace"], dict)

    def test_batch_001_records_have_manual_review_confirmed_flag(self):
        for record in load_all_normalized_records():
            self.assertIn("manual_review_confirmed", record["extraction_quality_flags"], record["id"])
            self.assertNotIn("requires_manual_review", record["extraction_quality_flags"], record["id"])

    def test_batch_001_vocab_entries_without_glosses_are_flagged_for_review(self):
        empty_gloss_ids = []
        for record in normalized_records_by_type("vocab_entry"):
            if not record.get("english_glosses"):
                empty_gloss_ids.append(record["id"])
                self.assertTrue(record["needs_gloss_review"], record["id"])
                self.assertIn("missing_english_gloss", record["extraction_quality_flags"], record["id"])
        self.assertEqual(len(empty_gloss_ids), 8)

    def test_batch_001_comprehension_records_without_answers_are_flagged(self):
        records = normalized_records_by_type("comprehension_question")
        self.assertEqual(len(records), 10)
        for record in records:
            self.assertIsNone(record["expected_answer"], record["id"])
            self.assertEqual(record["answer_status"], "not_provided", record["id"])
            self.assertIn("missing_expected_answer", record["extraction_quality_flags"], record["id"])

    def test_batch_001_word_parse_task_records_without_answer_key_are_flagged(self):
        records = normalized_records_by_type("word_parse_task")
        self.assertEqual(len(records), 8)
        for record in records:
            self.assertEqual(record["answer_status"], "not_extracted", record["id"])
            self.assertFalse(record["expected_word_in_pasuk"], record["id"])
            self.assertEqual(record["prefixes"], [], record["id"])
            self.assertEqual(record["suffixes"], [], record["id"])
            self.assertIn("answer_key_not_extracted", record["extraction_quality_flags"], record["id"])

    def test_batch_001_word_parse_incomplete_fields_are_flagged(self):
        records = normalized_records_by_type("word_parse")
        missing_shoresh = [
            record["id"]
            for record in records
            if "missing_explicit_shoresh" in record["extraction_quality_flags"]
        ]
        missing_suffix = [
            record["id"]
            for record in records
            if "missing_suffix_payload" in record["extraction_quality_flags"]
        ]
        self.assertEqual(len(missing_shoresh), 4)
        self.assertEqual(len(missing_suffix), 6)

    def test_forbidden_runtime_files_are_not_changed(self):
        changed_paths = validator.collect_changed_paths()
        disallowed = [path for path in changed_paths if not validator.is_allowed_change(path)]
        self.assertEqual(disallowed, [], [validator.forbidden_reason(path) for path in disallowed])


if __name__ == "__main__":
    unittest.main()
