import unittest

from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    active_scope_override_for_pasuk_id,
    active_scope_override_for_text,
    load_active_scope_overrides_data,
)
from pasuk_flow_generator import generate_question


class ActiveScopeOverrideTests(unittest.TestCase):
    def test_override_file_metadata_matches_active_scope(self):
        data = load_active_scope_overrides_data()

        self.assertEqual(data.get("metadata", {}).get("scope_id"), ACTIVE_ASSESSMENT_SCOPE)
        self.assertIsInstance(data.get("overrides"), dict)
        self.assertIn("bereishis_1_1", data.get("overrides", {}))

    def test_override_lookup_is_bound_to_active_scope_pasuks(self):
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_1_1"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_1_16"))
        self.assertIsNone(active_scope_override_for_pasuk_id("bereishis_99_1"))
        self.assertIsNone(active_scope_override_for_text("בְּרֵאשִׁית בָּרָא אֱלֹקִים"))

    def test_phrase_suppression_override_keeps_known_weak_case_skipped(self):
        question = generate_question(
            "phrase_translation",
            "וַיְכֻלּוּ הַשָּׁמַיִם וְהָאָרֶץ, וְכׇל־צְבָאָם.",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("source"), "active scope override")
        self.assertEqual(
            question.get("reason"),
            "No quiz-ready phrase target found in this pasuk.",
        )


if __name__ == "__main__":
    unittest.main()
