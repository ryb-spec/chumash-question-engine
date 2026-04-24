import unittest

from scripts import load_curriculum_extraction as loader_module


class CurriculumExtractionLoaderTests(unittest.TestCase):
    def setUp(self):
        self.loader = loader_module.CurriculumExtractionLoader()

    def test_loader_loads_records(self):
        self.assertGreater(len(self.loader.records), 0)
        self.assertEqual(len(self.loader.normalized_records), 75)

    def test_loader_groups_by_source(self):
        self.assertIn("linear_chumash_translation_most_parshiyos_in_torah", self.loader.records_by_source)
        self.assertGreater(
            len(self.loader.records_by_source["linear_chumash_translation_most_parshiyos_in_torah"]),
            0,
        )

    def test_loader_groups_by_skill(self):
        self.assertIn("skill_tag.translation_context", self.loader.records_by_skill)
        self.assertGreater(len(self.loader.records_by_skill["skill_tag.translation_context"]), 0)
        self.assertIn("translation_context", self.loader.records_by_skill)

    def test_loader_summary_includes_batch_001(self):
        summary = self.loader.summary()
        self.assertEqual(summary["normalized_record_count"], 75)
        self.assertEqual(summary["batch_counts"]["batch_001_cleaned_seed"], 75)
        self.assertEqual(summary["record_type_counts"]["pasuk_segment"], 26)
        self.assertEqual(summary["review_status_counts"]["reviewed"], 75)
        self.assertEqual(summary["review_status_counts"]["needs_review"], 30)

    def test_loader_returns_records_for_bereishis_1_1(self):
        records = self.loader.records_for_pasuk("Bereishis", 1, 1)
        self.assertGreater(len(records), 0)
        self.assertTrue(
            all(record["sefer"] == "Bereishis" and record["perek"] == 1 and record["pasuk"] == 1 for record in records)
        )
        self.assertTrue(any(record["extraction_batch_id"] == "batch_001_cleaned_seed" for record in records))
        self.assertTrue(any(record["review_status"] == "reviewed" for record in records))

    def test_loader_returns_empty_list_for_missing_pasuk(self):
        self.assertEqual(self.loader.records_for_pasuk("Bereishis", 99, 99), [])


if __name__ == "__main__":
    unittest.main()
