import unittest

import streamlit_app
from foundation_benchmark import (
    benchmark_canonical_skill_bucket_map,
    benchmark_relevant_focus_sections,
    benchmark_section_weight_map,
    get_benchmark_question_archetype,
)
from foundation_lexicon import (
    get_high_frequency_lexicon_entry,
    lexicon_priority_profile,
)
from foundation_paradigms import (
    paradigm_instructional_uses,
    pronoun_form,
    verb_paradigm_form,
)
from foundation_teacher_ops import (
    teacher_deployment_cycle,
    teacher_readiness_criteria,
    teacher_system_outputs,
)
from skill_catalog import (
    canonical_skill_ids_for_runtime_skill,
    canonical_skill_record,
    primary_canonical_skill_id,
    resolve_skill_id,
    skill_metadata_record,
)


class FoundationHelperLayerTests(unittest.TestCase):
    def test_runtime_skills_resolve_to_crosswalk_backed_canonical_ids(self):
        self.assertEqual(
            primary_canonical_skill_id("identify_prefix_meaning"),
            "PREFIX.BASIC_PREPOSITIONS",
        )
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("identify_suffix_meaning"),
            ["SUFFIX.FIRST_PERSON", "SUFFIX.SECOND_PERSON"],
        )
        self.assertIn(
            "VERB.TENSE.PAST",
            canonical_skill_ids_for_runtime_skill("identify_tense"),
        )
        self.assertEqual(
            canonical_skill_record("PREFIX.BASIC_PREPOSITIONS")["display_name"],
            "Translate common prefixes before nouns",
        )
        self.assertEqual(
            skill_metadata_record("identify_prefix_meaning")["canonical_skill_ids"],
            ["PREFIX.BASIC_PREPOSITIONS"],
        )
        self.assertEqual(
            primary_canonical_skill_id("translation"),
            "WORD.MEANING_BASIC",
        )
        self.assertEqual(
            primary_canonical_skill_id("phrase_translation"),
            "PHRASE.UNIT_TRANSLATE",
        )

    def test_benchmark_layer_loads_section_weights_and_archetypes(self):
        self.assertEqual(benchmark_section_weight_map()["Chumash Skills"], 23)
        self.assertIn("Critical Thinking", benchmark_section_weight_map())
        self.assertIn("Chumash Skills", benchmark_relevant_focus_sections())
        archetype = get_benchmark_question_archetype("mcq_context_translation")
        self.assertEqual(archetype["skills"], ["COMP.CONTEXT_TRANSLATION"])
        self.assertIn(
            "Decoding / morphology",
            benchmark_canonical_skill_bucket_map()["VERB.COMMAND"],
        )

    def test_paradigms_can_be_queried_without_runtime_integration(self):
        self.assertEqual(
            pronoun_form(
                "subject_pronouns",
                number="plural",
                person="3",
                gender="masculine",
            )["hebrew"],
            "הֵם",
        )
        self.assertEqual(
            verb_paradigm_form(
                "future",
                number="singular",
                person="2",
                gender="feminine",
            )["hebrew"],
            "תִּשְׁמְרִי",
        )
        self.assertIn(
            "Pre-teach playlist cards",
            paradigm_instructional_uses(),
        )

    def test_lexicon_priority_layer_exposes_frequency_and_priority(self):
        self.assertEqual(
            get_high_frequency_lexicon_entry("אָמַר")["tier"],
            "A",
        )
        self.assertEqual(
            get_high_frequency_lexicon_entry("אמר")["gloss"][0],
            "said",
        )
        self.assertEqual(
            get_high_frequency_lexicon_entry("בוא")["category"],
            "verb",
        )
        profile = lexicon_priority_profile("בַּיִת")
        self.assertEqual(profile["frequency_tier"], "A")
        self.assertEqual(profile["mastery_priority"], "highest")
        self.assertEqual(profile["review_priority"], "highest")

    def test_teacher_ops_layer_loads_admin_workflow_data(self):
        self.assertIn("Instructional Leadership", teacher_readiness_criteria())
        self.assertEqual(teacher_deployment_cycle()[0]["name"], "Select your focus")
        outputs = teacher_system_outputs()
        self.assertIn("after_assessment", outputs)
        self.assertIn("recommended reteach groups", outputs["after_assessment"])

    def test_benchmark_data_is_not_treated_as_runtime_truth(self):
        self.assertEqual(
            canonical_skill_ids_for_runtime_skill("translation"),
            ["WORD.MEANING_BASIC"],
        )
        self.assertIsNone(resolve_skill_id("COMP.CONTEXT_TRANSLATION"))
        self.assertIn("translation", streamlit_app.SKILL_ORDER)
        self.assertNotIn("COMP.CONTEXT_TRANSLATION", streamlit_app.SKILL_ORDER)


if __name__ == "__main__":
    unittest.main()
