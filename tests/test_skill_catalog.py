import unittest

import pasuk_flow_generator
import progress_store
import streamlit_app
from scripts.generate_fake_attempts import QUESTION_TYPES
from skill_catalog import (
    ADAPTIVE_STANDARD_IDS,
    SKILL_CATALOG,
    MICRO_STANDARD_LABELS,
    resolve_skill_id,
    skill_difficulty_tier,
    skill_display_label,
    skill_ids_in_runtime_order,
    skill_micro_standard,
    skill_standard,
)
from skill_tracker import update_skill_progress_in_state


EXPECTED_RUNTIME_ORDER = [
    "identify_prefix_meaning",
    "identify_suffix_meaning",
    "identify_pronoun_suffix",
    "identify_verb_marker",
    "segment_word_parts",
    "identify_tense",
    "identify_prefix_future",
    "identify_suffix_past",
    "identify_present_pattern",
    "convert_future_to_command",
    "match_pronoun_to_verb",
    "part_of_speech",
    "shoresh",
    "prefix",
    "suffix",
    "translation",
    "verb_tense",
    "subject_identification",
    "object_identification",
    "preposition_meaning",
    "phrase_translation",
]


class SkillCatalogTests(unittest.TestCase):
    def test_skill_ids_are_unique(self):
        ids = [skill.id for skill in SKILL_CATALOG]
        self.assertEqual(len(ids), len(set(ids)))

    def test_aliases_resolve_to_canonical_skill_ids(self):
        self.assertEqual(resolve_skill_id("word_meaning"), "translation")
        self.assertEqual(
            resolve_skill_id("prefix_level_3_identify_prefix_meaning"),
            "identify_prefix_meaning",
        )
        self.assertEqual(skill_display_label("word_meaning"), "Word meaning")

    def test_runtime_order_is_stable_across_catalog_runtime_and_generator(self):
        self.assertEqual(skill_ids_in_runtime_order(), EXPECTED_RUNTIME_ORDER)
        self.assertEqual(streamlit_app.SKILL_ORDER, EXPECTED_RUNTIME_ORDER)
        self.assertEqual(pasuk_flow_generator.SKILLS, EXPECTED_RUNTIME_ORDER)

    def test_generator_metadata_comes_from_catalog(self):
        metadata = pasuk_flow_generator.SKILL_METADATA["verb_tense"]
        self.assertEqual(metadata["standard"], skill_standard("verb_tense"))
        self.assertEqual(metadata["micro_standard"], skill_micro_standard("verb_tense"))
        self.assertEqual(metadata["difficulty"], skill_difficulty_tier("verb_tense"))

    def test_progress_store_normalizes_aliases_and_uses_catalog_defaults(self):
        state = progress_store.ensure_progress_state(
            {
                "current_skill": "word_meaning",
                "skills": {"word_meaning": {"score": 55}},
            }
        )
        self.assertEqual(state["current_skill"], "translation")
        self.assertIn("translation", state["skills"])
        self.assertNotIn("word_meaning", state["skills"])
        self.assertEqual(tuple(state["standards"].keys()), ADAPTIVE_STANDARD_IDS)
        self.assertEqual(tuple(state["xp"].keys()), ADAPTIVE_STANDARD_IDS)

    def test_skill_tracker_updates_alias_skill_under_canonical_id(self):
        progress = {"skills": {}}
        update_skill_progress_in_state(progress, "word_meaning", True)
        self.assertIn("translation", progress["skills"])
        self.assertNotIn("word_meaning", progress["skills"])

    def test_existing_runtime_label_references_still_work(self):
        self.assertEqual(streamlit_app.skill_path_label("identify_prefix_meaning"), "How words are built")
        self.assertEqual(streamlit_app.plain_skill("PR"), "How words are built")
        self.assertEqual(streamlit_app.MICRO_STANDARD_NAMES["PR1"], MICRO_STANDARD_LABELS["PR1"])

    def test_analytics_script_question_types_use_catalog_standards(self):
        standards_by_skill = {item["skill"]: item["standard"] for item in QUESTION_TYPES}
        self.assertEqual(standards_by_skill["shoresh"], skill_standard("shoresh"))
        self.assertEqual(standards_by_skill["translation"], skill_standard("translation"))
        self.assertEqual(standards_by_skill["verb_tense"], skill_standard("verb_tense"))
        self.assertEqual(
            standards_by_skill["identify_prefix_meaning"],
            skill_standard("identify_prefix_meaning"),
        )


if __name__ == "__main__":
    unittest.main()
