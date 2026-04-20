import unittest

from foundation_governance import (
    crosswalk_engine_extension_rows,
    engine_extension_governance_status_values,
    engine_extension_recommended_disposition_values,
    engine_extension_review_record,
    engine_extension_review_records,
    governed_engine_extension_ids,
    ungoverned_engine_extension_ids,
)
from foundation_resources import load_foundation_resource
from skill_catalog import canonical_skill_record


class EngineExtensionGovernanceTests(unittest.TestCase):
    def test_governance_queue_shape_and_supported_statuses(self):
        records = engine_extension_review_records()
        self.assertTrue(records)
        self.assertEqual(
            engine_extension_governance_status_values(),
            (
                "proposed",
                "under_review",
                "approved_internal",
                "kept_engine_only",
                "merged",
                "rejected",
            ),
        )
        self.assertEqual(
            engine_extension_recommended_disposition_values(),
            (
                "keep_engine_extension",
                "promote_reviewed_internal_supplement",
                "merge_into_existing_canonical_skill",
                "rename_for_clarity",
            ),
        )
        for record in records:
            self.assertIn(record["governance_status"], engine_extension_governance_status_values())
            self.assertIn(
                record["recommended_disposition"],
                engine_extension_recommended_disposition_values(),
            )
            self.assertIsInstance(record["human_review_needed"], bool)

    def test_governance_queue_covers_current_engine_extension_rows(self):
        crosswalk_ids = {
            record["canonical_skill_id"]
            for record in crosswalk_engine_extension_rows()
        }
        self.assertEqual(set(governed_engine_extension_ids()), crosswalk_ids)
        self.assertEqual(ungoverned_engine_extension_ids(), ())

    def test_engine_extension_rows_are_not_silently_promoted_to_external_truth(self):
        for canonical_skill_id in governed_engine_extension_ids():
            self.assertEqual(
                canonical_skill_record(canonical_skill_id)["system_layer"],
                "engine_extension",
            )
        queue = load_foundation_resource("engine_extension_review_queue")
        self.assertTrue(all(record["human_review_needed"] for record in queue["records"]))
        self.assertTrue(
            all(record["governance_status"] != "approved_internal" for record in queue["records"])
        )

    def test_review_records_capture_current_recommendations(self):
        self.assertEqual(
            engine_extension_review_record("WORD.MEANING_BASIC")["recommended_disposition"],
            "promote_reviewed_internal_supplement",
        )
        self.assertEqual(
            engine_extension_review_record("PREFIX.FORM_IDENTIFY")["recommended_disposition"],
            "keep_engine_extension",
        )
        self.assertEqual(
            engine_extension_review_record("PHRASE.UNIT_TRANSLATE")["recommended_disposition"],
            "promote_reviewed_internal_supplement",
        )


if __name__ == "__main__":
    unittest.main()
