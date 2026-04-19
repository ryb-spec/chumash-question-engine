import unittest

from skill_catalog import (
    canonical_skill_ids_for_runtime_skill,
    canonical_skill_record,
    intentionally_unmapped_runtime_skills,
    runtime_skill_alignment_records,
    skill_ids_in_runtime_order,
)


class RuntimeSkillAlignmentTests(unittest.TestCase):
    def test_every_runtime_skill_has_explicit_alignment_status(self):
        records = runtime_skill_alignment_records()

        self.assertEqual(len(records), len(skill_ids_in_runtime_order()))
        self.assertTrue(records)
        self.assertTrue(all(record["status"] in {"mapped", "intentionally_unmapped"} for record in records))
        self.assertTrue(all(record["status"] != "review_pending" for record in records))

    def test_current_review_leaves_no_runtime_skills_unmapped(self):
        self.assertEqual(intentionally_unmapped_runtime_skills(), {})

    def test_reviewed_runtime_skills_map_to_expected_canonical_ids(self):
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("part_of_speech"),
            ["WORD.PART_OF_SPEECH_BASIC"],
        )
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("translation"),
            ["WORD.MEANING_BASIC"],
        )
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("prefix"),
            ["PREFIX.FORM_IDENTIFY"],
        )
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("phrase_translation"),
            ["PHRASE.UNIT_TRANSLATE"],
        )
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("preposition_meaning"),
            ["PREFIX.BASIC_PREPOSITIONS"],
        )
        self.assertIn("ROOT.IDENTIFY", canonical_skill_ids_for_runtime_skill("shoresh"))
        self.assertIn("ROOT.IDENTIFY_DROPPED", canonical_skill_ids_for_runtime_skill("shoresh"))
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("subject_identification"),
            ["VERB.SUBJECT_OBJECT"],
        )
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("object_identification"),
            ["VERB.SUBJECT_OBJECT"],
        )
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("verb_tense"),
            ["VERB.TENSE.PAST", "VERB.TENSE.PRESENT", "VERB.TENSE.FUTURE"],
        )

    def test_extension_records_are_explicitly_marked(self):
        self.assertEqual(
            canonical_skill_record("WORD.MEANING_BASIC")["system_layer"],
            "engine_extension",
        )
        self.assertEqual(
            canonical_skill_record("PREFIX.FORM_IDENTIFY")["system_layer"],
            "engine_extension",
        )
        self.assertEqual(
            canonical_skill_record("PHRASE.UNIT_TRANSLATE")["system_layer"],
            "engine_extension",
        )

    def test_runtime_skill_canonical_lists_do_not_duplicate_ids(self):
        for skill in skill_ids_in_runtime_order():
            canonical_ids = canonical_skill_ids_for_runtime_skill(skill)
            self.assertEqual(
                len(canonical_ids),
                len(set(canonical_ids)),
                skill,
            )


if __name__ == "__main__":
    unittest.main()
