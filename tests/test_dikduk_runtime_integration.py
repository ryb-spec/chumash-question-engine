import unittest

from assessment_scope import ACTIVE_ASSESSMENT_SCOPE
from engine.flow_builder import standalone_translation_requires_context
from foundation_dikduk import (
    dikduk_foundation_metadata,
    load_dikduk_runtime_bundle,
    load_unresolved_candidates,
)


class DikdukRuntimeIntegrationTests(unittest.TestCase):
    def test_runtime_bundle_loads_validated_seed_data_only(self):
        bundle = load_dikduk_runtime_bundle()

        self.assertIn("skills", bundle)
        self.assertIn("rules", bundle)
        self.assertIn("patterns", bundle)
        self.assertIn("vocab_by_normalized", bundle)
        self.assertNotIn("unresolved_candidates", bundle)
        self.assertIn(
            "vocab_amar",
            {
                record["vocab_id"]
                for records in bundle["vocab_by_normalized"].values()
                for record in records
            },
        )

    def test_unresolved_candidates_stay_out_of_runtime_metadata(self):
        unresolved = load_unresolved_candidates()

        self.assertTrue(
            any(
                candidate.get("proposed_id") == "vocab_pronoun_core_set"
                for candidate in unresolved.get("vocabulary", [])
            )
        )
        metadata = dikduk_foundation_metadata("אני")
        self.assertFalse(metadata["used"])
        self.assertEqual(metadata["vocab_ids"], [])

    def test_pattern_backed_metadata_marks_seed_supported_ambiguity(self):
        entry = {
            "type": "verb",
            "part_of_speech": "verb",
            "tense": "future",
            "number": "singular",
        }

        metadata = dikduk_foundation_metadata("תשמר", entry, skill="translation")

        self.assertTrue(metadata["used"])
        self.assertIn("pat_verb_future_tav_ambiguous", metadata["pattern_ids"])
        self.assertIn("rule_verb_future_tav_ambiguous", metadata["rule_ids"])
        self.assertIn("conf_tav_future_ambiguity", metadata["confusion_pattern_ids"])
        self.assertTrue(metadata["safe_seed_only"])

    def test_ambiguous_tav_future_requires_context_for_standalone_translation(self):
        entry = {
            "type": "verb",
            "part_of_speech": "verb",
            "tense": "future",
            "translation": "you will guard",
            "translation_context": "you will guard",
        }

        metadata = dikduk_foundation_metadata("תשמר", entry, skill="translation")

        self.assertTrue(metadata["ambiguous_without_context"])
        self.assertTrue(standalone_translation_requires_context(entry, "תשמר"))

    def test_active_scope_remains_current_promoted_scope(self):
        self.assertEqual(ACTIVE_ASSESSMENT_SCOPE, "local_parsed_bereishis_1_1_to_3_24")


if __name__ == "__main__":
    unittest.main()
