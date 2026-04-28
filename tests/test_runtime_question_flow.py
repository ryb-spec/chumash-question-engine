import unittest
from unittest.mock import patch

import streamlit as st

from assessment_scope import active_pesukim_records
import runtime.pilot_logging as pilot_logging
from runtime.question_flow import (
    candidate_quality_breakdown,
    display_context_policy,
    question_signature,
    rank_ready_rows,
    recent_question_repeat_reason,
    select_pasuk_first_question,
    validate_question_for_serve,
)
import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app


def pasuk_text_by_id(pasuk_id):
    for record in active_pesukim_records():
        if record.get("pasuk_id") == pasuk_id:
            return record["text"]
    raise AssertionError(f"Missing active pasuk {pasuk_id}")


class RuntimeQuestionFlowTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        streamlit_app.init_session_state()
        st.session_state.practice_type = "Learn Mode"

    def test_candidate_source_cache_keys_by_analyzer_callable(self):
        question_flow._cached_candidate_source.cache_clear()

        def first_analyzer(pasuk):
            return {"source": "first", "pasuk": pasuk}

        def second_analyzer(pasuk):
            return {"source": "second", "pasuk": pasuk}

        self.assertEqual(
            question_flow._cached_candidate_source(first_analyzer, "pasuk")["source"],
            "first",
        )
        self.assertEqual(
            question_flow._cached_candidate_source(second_analyzer, "pasuk")["source"],
            "second",
        )

    def test_candidate_source_for_pasuk_uses_current_patched_analyzer(self):
        question_flow._cached_candidate_source.cache_clear()

        def first_analyzer(pasuk):
            return {"source": "first", "pasuk": pasuk}

        def second_analyzer(pasuk):
            return {"source": "second", "pasuk": pasuk}

        with patch.object(question_flow, "analyze_generator_pasuk", side_effect=first_analyzer):
            self.assertEqual(question_flow.candidate_source_for_pasuk("pasuk")["source"], "first")

        with patch.object(question_flow, "analyze_generator_pasuk", side_effect=second_analyzer):
            self.assertEqual(question_flow.candidate_source_for_pasuk("pasuk")["source"], "second")

    def _translation_question(self, word="בָּרָא", prompt="What does בָּרָא mean?"):
        return {
            "skill": "translation",
            "question_type": "translation",
            "question": prompt,
            "selected_word": word,
            "word": word,
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        }

    def test_question_signature_captures_target_prompt_and_pasuk(self):
        signature = question_signature(self._translation_question())

        self.assertEqual(signature["skill"], "translation")
        self.assertTrue(signature["target_word"])
        self.assertEqual(signature["prompt_family"], "translation")
        self.assertEqual(signature["correct_answer"], "created")
        self.assertEqual(signature["source_pasuk"], "not in active parsed dataset")

    def test_question_signature_prefers_dikduk_foundation_repeat_key_when_present(self):
        question = self._translation_question(word="יאמר", prompt="What form is shown?")
        question["skill"] = "identify_tense"
        question["question_type"] = "identify_tense"
        question["correct_answer"] = "future"
        question["choices"] = ["future", "past", "present", "to do form"]
        question["dikduk_foundation"] = {"repeat_key": "shoresh:אמר"}

        signature = question_signature(question)

        self.assertEqual(signature["target_family"], "shoresh:אמר")
        self.assertEqual(signature["foundation_repeat_key"], "shoresh:אמר")

    def test_recent_question_repeat_reason_blocks_exact_and_near_duplicates(self):
        first = self._translation_question()
        recent = [question_signature(first)]

        exact_reason = recent_question_repeat_reason(first, recent)
        near_duplicate = self._translation_question(prompt="Choose the meaning of בָּרָא.")
        near_duplicate["question_type"] = "translation_variant"
        near_reason = recent_question_repeat_reason(near_duplicate, recent)

        self.assertEqual(exact_reason, "recent_exact_repeat")
        self.assertEqual(near_reason, "recent_target_repeat")

    def test_recent_question_repeat_reason_blocks_same_word_across_skill_lanes(self):
        previous = {
            "skill": "part_of_speech",
            "question_type": "part_of_speech",
            "question": "What kind of word is בָּרָא?",
            "selected_word": "בָּרָא",
            "correct_answer": "action word",
            "choices": ["action word", "naming word", "small helper word", "direction word"],
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        }
        translation = self._translation_question()

        reason = recent_question_repeat_reason(translation, [question_signature(previous)])

        self.assertEqual(reason, "recent_exact_word_repeat")

    def test_recent_question_repeat_reason_blocks_translation_exact_word_across_longer_window(self):
        previous = self._translation_question(word="אָמַר", prompt="What does אָמַר mean?")
        previous["correct_answer"] = "said"
        previous["choices"] = ["said", "made", "saw", "called"]

        fillers = []
        for index in range(8):
            filler = {
                "skill": "part_of_speech",
                "question_type": "part_of_speech",
                "question": f"What kind of word is filler-{index}?",
                "selected_word": f"מִלָּה{index}",
                "word": f"מִלָּה{index}",
                "correct_answer": "naming word",
                "choices": ["naming word", "action word", "small helper word", "direction word"],
                "pasuk": f"dummy pasuk {index}",
            }
            fillers.append(question_signature(filler))

        repeated = self._translation_question(word="אָמַר", prompt="What does אָמַר mean?")
        repeated["correct_answer"] = "said"
        repeated["choices"] = ["said", "made", "saw", "called"]

        recent = [question_signature(previous), *fillers]
        reason = recent_question_repeat_reason(repeated, recent)

        self.assertEqual(reason, "recent_exact_word_repeat")

    def test_recent_question_repeat_reason_blocks_same_pasuk_same_intent_repeat(self):
        active_record = active_pesukim_records()[0]
        previous = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does created-word mean?",
            "selected_word": "בָּרָא",
            "word": "בָּרָא",
            "part_of_speech": "verb",
            "correct_answer": "and he created",
            "choices": ["and he created", "and he made", "and he called", "and he saw"],
            "pasuk": active_record["text"],
        }
        next_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does God-word mean?",
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "part_of_speech": "verb",
            "correct_answer": "and he made",
            "choices": ["and he made", "and he saw", "and he called", "and he formed"],
            "pasuk": active_record["text"],
        }

        reason = recent_question_repeat_reason(next_question, [question_signature(previous)])

        self.assertEqual(reason, "recent_same_pasuk_intent_repeat")

    def test_recent_question_repeat_reason_blocks_semantic_sibling_word_family(self):
        previous = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does light-word mean?",
            "selected_word": "אוֹר",
            "word": "אוֹר",
            "part_of_speech": "noun",
            "correct_answer": "light",
            "choices": ["light", "earth", "water", "garden"],
            "pasuk": "מקור א",
            "pasuk_ref": {"label": "Bereishis 1:3", "pasuk_id": "bereishis_1_3"},
        }
        sibling = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does the-light-word mean?",
            "selected_word": "הָאוֹר",
            "word": "הָאוֹר",
            "part_of_speech": "noun",
            "correct_answer": "the light",
            "choices": ["the light", "the earth", "the water", "the garden"],
            "pasuk": "מקור ב",
            "pasuk_ref": {"label": "Bereishis 1:4", "pasuk_id": "bereishis_1_4"},
        }

        reason = recent_question_repeat_reason(sibling, [question_signature(previous)])

        self.assertEqual(reason, "recent_meaning_repeat")

    def test_recent_question_repeat_reason_blocks_translation_meaning_repeat(self):
        previous = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "word": "בָּרָא",
            "correct_answer": "made",
            "choices": ["made", "saw", "called", "light"],
            "pasuk": "מקור א",
        }
        repeated_meaning = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does עָשָׂה mean?",
            "selected_word": "עָשָׂה",
            "word": "עָשָׂה",
            "correct_answer": "made",
            "choices": ["made", "saw", "called", "light"],
            "pasuk": "מקור ב",
        }

        reason = recent_question_repeat_reason(repeated_meaning, [question_signature(previous)])

        self.assertEqual(reason, "recent_meaning_repeat")

    def test_recent_question_repeat_reason_blocks_translation_phrase_pattern_repeat(self):
        previous_record = next(
            record for record in active_pesukim_records()
            if record.get("pasuk_id") == "bereishis_1_22"
        )
        repeated_record = next(
            record for record in active_pesukim_records()
            if record.get("pasuk_id") == "bereishis_1_17"
        )
        previous = {
            "skill": "translation",
            "question_type": "phrase_translation",
            "question": "What does this phrase mean?",
            "selected_word": "×•Ö·×™Ö°×‘Ö¸×¨Ö¶×šÖ° ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
            "word": "×•Ö·×™Ö°×‘Ö¸×¨Ö¶×šÖ° ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
            "correct_answer": "and God blessed them",
            "choices": [
                "and God blessed them",
                "and God placed them",
                "and God made them",
                "and God saw them",
            ],
            "pasuk": previous_record["text"],
            "pasuk_ref": {"label": "Bereishis 1:22", "pasuk_id": "bereishis_1_22"},
        }
        repeated_pattern = {
            "skill": "translation",
            "question_type": "phrase_translation",
            "question": "What does this phrase mean?",
            "selected_word": "×•Ö·×™Ö¼Ö´×ªÖ¼Öµ×Ÿ ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
            "word": "×•Ö·×™Ö¼Ö´×ªÖ¼Öµ×Ÿ ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
            "correct_answer": "and God placed them",
            "choices": [
                "and God placed them",
                "and God blessed them",
                "and God made them",
                "and God saw them",
            ],
            "pasuk": repeated_record["text"],
            "pasuk_ref": {"label": "Bereishis 1:17", "pasuk_id": "bereishis_1_17"},
        }

        reason = recent_question_repeat_reason(repeated_pattern, [question_signature(previous)])

        self.assertEqual(reason, "recent_translation_phrase_pattern_repeat")

    def test_recent_question_repeat_reason_blocks_tense_lane_overlap_on_same_target(self):
        previous = {
            "skill": "identify_tense",
            "question_type": "identify_tense",
            "question": "What form is shown?",
            "selected_word": "וְתֵרָאֶה",
            "word": "וְתֵרָאֶה",
            "correct_answer": "future",
            "choices": ["future", "past", "present", "to do form"],
            "pasuk": "מקור א",
            "pasuk_ref": {"label": "Bereishis 1:9", "pasuk_id": "bereishis_1_9"},
        }
        repeated_lane = {
            "skill": "verb_tense",
            "question_type": "verb_tense",
            "question": "What form is shown?",
            "selected_word": "וְתֵרָאֶה",
            "word": "וְתֵרָאֶה",
            "correct_answer": "future",
            "choices": ["future", "past", "present", "to do form"],
            "pasuk": "מקור ב",
            "pasuk_ref": {"label": "Bereishis 1:14", "pasuk_id": "bereishis_1_14"},
        }

        reason = recent_question_repeat_reason(repeated_lane, [question_signature(previous)])

        self.assertEqual(reason, "recent_target_repeat")

    def test_recent_question_repeat_reason_blocks_repeated_shoresh_surface_pattern(self):
        previous = {
            "skill": "shoresh",
            "question_type": "shoresh",
            "question": "What is the shoresh of וַיֹּאמֶר?",
            "selected_word": "וַיֹּאמֶר",
            "word": "וַיֹּאמֶר",
            "correct_answer": "אמר",
            "choices": ["אמר", "קרא", "ראה", "ברא"],
            "pasuk": "מקור א",
            "pasuk_ref": {"label": "Bereishis 1:3", "pasuk_id": "bereishis_1_3"},
        }
        repeated_surface = {
            "skill": "shoresh",
            "question_type": "shoresh",
            "question": "What is the shoresh of וַיַּרְא?",
            "selected_word": "וַיַּרְא",
            "word": "וַיַּרְא",
            "correct_answer": "ראה",
            "choices": ["ראה", "אמר", "קרא", "ברא"],
            "pasuk": "מקור ב",
            "pasuk_ref": {"label": "Bereishis 1:4", "pasuk_id": "bereishis_1_4"},
        }

        reason = recent_question_repeat_reason(repeated_surface, [question_signature(previous)])

        self.assertEqual(reason, "recent_same_pasuk_intent_repeat")

    def test_recent_question_repeat_reason_uses_dikduk_foundation_repeat_key(self):
        previous = {
            "skill": "identify_tense",
            "question_type": "identify_tense",
            "question": "What form is shown?",
            "selected_word": "יאמר",
            "word": "יאמר",
            "correct_answer": "future",
            "choices": ["future", "past", "present", "to do form"],
            "pasuk": "מקור א",
            "dikduk_foundation": {"repeat_key": "shoresh:אמר"},
        }
        repeated_family = {
            "skill": "verb_tense",
            "question_type": "verb_tense",
            "question": "What form is shown?",
            "selected_word": "תאמר",
            "word": "תאמר",
            "correct_answer": "future",
            "choices": ["future", "past", "present", "to do form"],
            "pasuk": "מקור ב",
            "dikduk_foundation": {"repeat_key": "shoresh:אמר"},
        }

        reason = recent_question_repeat_reason(
            repeated_family,
            [question_signature(previous)],
        )

        self.assertEqual(reason, "recent_target_family_repeat")

    def test_display_context_policy_keeps_simple_word_questions_compact(self):
        question = {
            "skill": "identify_prefix_meaning",
            "question_type": "prefix_level_2_identify_prefix_meaning",
            "question": "What does the prefix mean?",
        }

        policy = display_context_policy(question)

        self.assertEqual(policy["mode"], "compact")
        self.assertEqual(policy["reason"], "word_level_question")

    def test_candidate_quality_breakdown_prefers_novel_safe_candidate(self):
        recent_questions = [question_signature(self._translation_question())]
        stale = {
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            "word": "בָּרָא",
            "question": self._translation_question(),
        }
        fresh_question = self._translation_question(word="אֱלֹקִים", prompt="What does אֱלֹקִים mean?")
        fresh_question["correct_answer"] = "God"
        fresh_question["choices"] = ["God", "created", "light", "water"]
        fresh = {
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            "word": "אֱלֹקִים",
            "question": fresh_question,
        }

        stale_breakdown = candidate_quality_breakdown(
            stale,
            recent_pesukim=["בְּרֵאשִׁית בָּרָא אֱלֹקִים"],
            recent_words=["בָּרָא"],
            recent_questions=recent_questions,
            progress={},
            adaptive_context={},
        )
        fresh_breakdown = candidate_quality_breakdown(
            fresh,
            recent_pesukim=[],
            recent_words=[],
            recent_questions=[],
            progress={},
            adaptive_context={},
        )

        self.assertGreater(fresh_breakdown["novelty"], stale_breakdown["novelty"])
        self.assertGreater(fresh_breakdown["total"], stale_breakdown["total"])

    def test_rank_ready_rows_prefers_reviewed_rows_on_weight_tie(self):
        ready_rows = [
            {"pasuk": "pasuk_a", "word": "word_a", "reviewed": False},
            {"pasuk": "pasuk_b", "word": "word_b", "reviewed": True},
        ]

        with patch.object(question_flow, "candidate_weight", return_value=1.0):
            ranked = rank_ready_rows(
                ready_rows,
                recent_pesukim=[],
                recent_words=[],
                progress={},
                adaptive_context={},
            )

        self.assertTrue(ranked[0]["reviewed"])
        self.assertFalse(ranked[1]["reviewed"])

    def test_rank_ready_rows_prefers_reviewed_standalone_translation_rows_for_translation_skill(self):
        ready_rows = [
            {
                "pasuk": "phrase_pasuk",
                "word": "×•Ö·×™Ö°×‘Ö¸×¨Ö¶×šÖ° ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
                "reviewed": True,
                "question_type": "phrase_translation",
                "analysis_source": "active_scope_reviewed_bank",
            },
            {
                "pasuk": "word_pasuk",
                "word": "×•Ö·×™Ö¹Ö¼××žÖ¶×¨",
                "reviewed": True,
                "question_type": "translation",
                "analysis_source": "active_scope_reviewed_bank",
            },
        ]

        with patch.object(question_flow, "candidate_weight", return_value=1.0):
            ranked = rank_ready_rows(
                ready_rows,
                recent_pesukim=[],
                recent_words=[],
                skill="translation",
                recent_questions=[],
                progress={},
                adaptive_context={},
            )

        self.assertEqual(ranked[0]["question_type"], "translation")
        self.assertEqual(ranked[1]["question_type"], "phrase_translation")

    def test_select_pasuk_first_question_shortlists_before_full_generation(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        ready_rows = [
            {
                "pasuk": f"pasuk_{index}",
                "word": f"word_{index}",
                "feature": "translation",
                "prefix": "",
                "morpheme_family": "",
            }
            for index in range(12)
        ]

        def generate_question(skill, candidate_source, **kwargs):
            return {
                "skill": "translation",
                "question_type": "translation",
                "question": f"What does {candidate_source} mean?",
                "selected_word": candidate_source,
                "word": candidate_source,
                "correct_answer": "answer",
                "choices": ["answer", "other1", "other2", "other3"],
                "pasuk": candidate_source,
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question) as mocked_generate, \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("translation", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertLessEqual(mocked_generate.call_count, 8)
        self.assertIn("selection_timing", result.get("_debug_trace", {}))
        self.assertLessEqual(
            result.get("_debug_trace", {}).get("selection_timing", {}).get("full_generation_rows", 99),
            8,
        )

    def test_select_pasuk_first_question_blocks_recent_exact_word_and_uses_fresh_word(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        st.session_state.recent_questions = [
            question_signature(
                {
                    "skill": "part_of_speech",
                    "question_type": "part_of_speech",
                    "question": "What kind of word is בָּרָא?",
                    "selected_word": "בָּרָא",
                    "correct_answer": "action word",
                    "choices": ["action word", "naming word", "small helper word", "direction word"],
                    "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
                }
            )
        ]
        ready_rows = [
            {"pasuk": "repeat_pasuk", "word": "בָּרָא", "feature": "translation", "prefix": "", "morpheme_family": ""},
            {"pasuk": "fresh_pasuk", "word": "אֱלֹקִים", "feature": "translation", "prefix": "", "morpheme_family": ""},
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == "repeat_pasuk":
                return {
                    "skill": "translation",
                    "question_type": "translation",
                    "question": "What does בָּרָא mean?",
                    "selected_word": "בָּרָא",
                    "word": "בָּרָא",
                    "correct_answer": "created",
                    "choices": ["created", "light", "earth", "water"],
                    "pasuk": "repeat_pasuk",
                }
            return {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does אֱלֹקִים mean?",
                "selected_word": "אֱלֹקִים",
                "word": "אֱלֹקִים",
                "correct_answer": "God",
                "choices": ["God", "light", "earth", "water"],
                "pasuk": "fresh_pasuk",
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("translation", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["selected_word"], "אֱלֹקִים")

    def test_select_pasuk_first_question_blocks_translation_exact_word_seen_longer_window_and_uses_fresh_word(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        previous = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does אָמַר mean?",
            "selected_word": "אָמַר",
            "word": "אָמַר",
            "correct_answer": "said",
            "choices": ["said", "made", "saw", "called"],
            "pasuk": "repeat_previous_pasuk",
        }
        filler_signatures = []
        for index in range(8):
            filler = {
                "skill": "part_of_speech",
                "question_type": "part_of_speech",
                "question": f"What kind of word is filler-{index}?",
                "selected_word": f"מִלָּה{index}",
                "word": f"מִלָּה{index}",
                "correct_answer": "naming word",
                "choices": ["naming word", "action word", "small helper word", "direction word"],
                "pasuk": f"filler pasuk {index}",
            }
            filler_signatures.append(question_signature(filler))
        st.session_state.recent_questions = [question_signature(previous), *filler_signatures]

        ready_rows = [
            {"pasuk": "repeat_pasuk", "word": "אָמַר", "feature": "translation", "prefix": "", "morpheme_family": ""},
            {"pasuk": "fresh_pasuk", "word": "קוֹל", "feature": "translation", "prefix": "", "morpheme_family": ""},
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == "repeat_pasuk":
                return {
                    "skill": "translation",
                    "question_type": "translation",
                    "question": "What does אָמַר mean?",
                    "selected_word": "אָמַר",
                    "word": "אָמַר",
                    "correct_answer": "said",
                    "choices": ["said", "made", "saw", "called"],
                    "pasuk": "repeat_pasuk",
                }
            return {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does קוֹל mean?",
                "selected_word": "קוֹל",
                "word": "קוֹל",
                "correct_answer": "voice / sound",
                "choices": ["voice / sound", "said", "light", "earth"],
                "pasuk": "fresh_pasuk",
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("translation", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["selected_word"], "קוֹל")

    def test_select_pasuk_first_question_prefers_reviewed_standalone_translation_when_reviewed_phrase_exists(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        ready_rows = [
            {
                "pasuk": "phrase_pasuk",
                "word": "×•Ö·×™Ö°×‘Ö¸×¨Ö¶×šÖ° ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
                "feature": "translation",
                "prefix": "",
                "morpheme_family": "",
                "reviewed": True,
                "question_type": "phrase_translation",
                "analysis_source": "active_scope_reviewed_bank",
            },
            {
                "pasuk": "word_pasuk",
                "word": "×•Ö·×™Ö¹Ö¼××žÖ¶×¨",
                "feature": "translation",
                "prefix": "",
                "morpheme_family": "",
                "reviewed": True,
                "question_type": "translation",
                "analysis_source": "active_scope_reviewed_bank",
            },
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == "phrase_pasuk":
                return {
                    "skill": "translation",
                    "question_type": "phrase_translation",
                    "question": "What does this phrase mean?",
                    "selected_word": "×•Ö·×™Ö°×‘Ö¸×¨Ö¶×šÖ° ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
                    "word": "×•Ö·×™Ö°×‘Ö¸×¨Ö¶×šÖ° ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
                    "correct_answer": "and God blessed them",
                    "choices": [
                        "and God blessed them",
                        "and God placed them",
                        "and God made them",
                        "and God saw them",
                    ],
                    "pasuk": "phrase_pasuk",
                    "analysis_source": "active_scope_reviewed_bank",
                }
            return {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does ×•Ö·×™Ö¹Ö¼××žÖ¶×¨ mean?",
                "selected_word": "×•Ö·×™Ö¹Ö¼××žÖ¶×¨",
                "word": "×•Ö·×™Ö¹Ö¼××žÖ¶×¨",
                "correct_answer": "and he said",
                "choices": ["and he said", "and he made", "and he saw", "and he called"],
                "pasuk": "word_pasuk",
                "analysis_source": "active_scope_reviewed_bank",
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("translation", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["question_type"], "translation")
        self.assertEqual(result["selected_word"], "×•Ö·×™Ö¹Ö¼××žÖ¶×¨")

    def test_select_pasuk_first_question_can_surface_alternate_reviewed_translation_from_same_pasuk(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        pasuk = pasuk_text_by_id("bereishis_3_7")
        previous = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does עֵירֻמִּם mean?",
            "selected_word": "עֵירֻמִּם",
            "word": "עֵירֻמִּם",
            "correct_answer": "naked",
            "choices": ["naked", "fig", "belts", "good"],
            "pasuk": pasuk,
        }
        st.session_state.recent_questions = [question_signature(previous)]
        ready_rows = [
            {
                "pasuk": pasuk,
                "word": "עֵירֻמִּם",
                "feature": "translation",
                "prefix": "",
                "morpheme_family": "",
                "reviewed": True,
                "question_type": "translation",
                "analysis_source": "active_scope_reviewed_bank",
            }
        ]

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("translation", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["question_type"], "translation")
        self.assertEqual(result["analysis_source"], "active_scope_reviewed_bank")
        self.assertEqual(result["selected_word"], "תְאֵנָה")
        self.assertEqual(result["correct_answer"], "fig")

    def test_select_pasuk_first_question_suppresses_phrase_pattern_when_reviewed_standalone_exists(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        previous = {
            "skill": "translation",
            "question_type": "phrase_translation",
            "question": "What does this phrase mean?",
            "selected_word": "×•Ö·×™Ö°×‘Ö¸×¨Ö¶×šÖ° ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
            "word": "×•Ö·×™Ö°×‘Ö¸×¨Ö¶×šÖ° ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
            "correct_answer": "and God blessed them",
            "choices": [
                "and God blessed them",
                "and God placed them",
                "and God made them",
                "and God saw them",
            ],
            "pasuk": "phrase repeat previous",
        }
        st.session_state.recent_questions = [question_signature(previous)]
        ready_rows = [
            {
                "pasuk": "phrase_pasuk",
                "word": "×•Ö·×™Ö¼Ö´×ªÖ¼Öµ×Ÿ ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
                "feature": "translation",
                "prefix": "",
                "morpheme_family": "",
                "reviewed": True,
                "question_type": "phrase_translation",
                "analysis_source": "active_scope_reviewed_bank",
            },
            {
                "pasuk": "word_pasuk",
                "word": "×•Ö·×™Ö¹Ö¼××žÖ¶×¨",
                "feature": "translation",
                "prefix": "",
                "morpheme_family": "",
                "reviewed": True,
                "question_type": "translation",
                "analysis_source": "active_scope_reviewed_bank",
            },
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == "phrase_pasuk":
                return {
                    "skill": "translation",
                    "question_type": "phrase_translation",
                    "question": "What does this phrase mean?",
                    "selected_word": "×•Ö·×™Ö¼Ö´×ªÖ¼Öµ×Ÿ ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
                    "word": "×•Ö·×™Ö¼Ö´×ªÖ¼Öµ×Ÿ ×Ö¹×ªÖ¸× ×Ö±×œÖ¹×§Ö´×™×",
                    "correct_answer": "and God placed them",
                    "choices": [
                        "and God placed them",
                        "and God blessed them",
                        "and God made them",
                        "and God saw them",
                    ],
                    "pasuk": "phrase_pasuk",
                    "analysis_source": "active_scope_reviewed_bank",
                }
            return {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does ×•Ö·×™Ö¹Ö¼××žÖ¶×¨ mean?",
                "selected_word": "×•Ö·×™Ö¹Ö¼××žÖ¶×¨",
                "word": "×•Ö·×™Ö¹Ö¼××žÖ¶×¨",
                "correct_answer": "and he said",
                "choices": ["and he said", "and he made", "and he saw", "and he called"],
                "pasuk": "word_pasuk",
                "analysis_source": "active_scope_reviewed_bank",
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("translation", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["question_type"], "translation")
        self.assertEqual(result["selected_word"], "×•Ö·×™Ö¹Ö¼××žÖ¶×¨")

    def test_select_pasuk_first_question_skips_repeated_translation_meaning_when_fresh_option_exists(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        previous = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "word": "בָּרָא",
            "correct_answer": "made",
            "choices": ["made", "light", "earth", "water"],
            "pasuk": "repeat_meaning_previous",
        }
        st.session_state.recent_questions = [question_signature(previous)]
        ready_rows = [
            {"pasuk": "repeat_meaning_pasuk", "word": "עָשָׂה", "feature": "translation", "prefix": "", "morpheme_family": ""},
            {"pasuk": "fresh_meaning_pasuk", "word": "אוֹר", "feature": "translation", "prefix": "", "morpheme_family": ""},
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == "repeat_meaning_pasuk":
                return {
                    "skill": "translation",
                    "question_type": "translation",
                    "question": "What does עָשָׂה mean?",
                    "selected_word": "עָשָׂה",
                    "word": "עָשָׂה",
                    "correct_answer": "made",
                    "choices": ["made", "light", "earth", "water"],
                    "pasuk": "repeat_meaning_pasuk",
                }
            return {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does אוֹר mean?",
                "selected_word": "אוֹר",
                "word": "אוֹר",
                "correct_answer": "light",
                "choices": ["light", "made", "earth", "water"],
                "pasuk": "fresh_meaning_pasuk",
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("translation", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["selected_word"], "אוֹר")

    def test_select_pasuk_first_question_skips_same_pasuk_intent_repeat_when_fresh_option_exists(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        active_records = active_pesukim_records()[:2]
        previous = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action here?",
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "correct_answer": "God",
            "choices": ["God", "the man", "the earth", "the light"],
            "pasuk": active_records[0]["text"],
        }
        st.session_state.recent_questions = [question_signature(previous)]
        ready_rows = [
            {"pasuk": active_records[0]["text"], "word": "אֱלֹקִים", "feature": "subject_identification", "prefix": "", "morpheme_family": ""},
            {"pasuk": active_records[1]["text"], "word": "הָאָרֶץ", "feature": "subject_identification", "prefix": "", "morpheme_family": ""},
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == active_records[0]["text"]:
                return {
                    "skill": "subject_identification",
                    "question_type": "subject_identification",
                    "question": "Who is doing the action here?",
                    "selected_word": "אֱלֹקִים",
                    "word": "אֱלֹקִים",
                    "correct_answer": "God",
                    "choices": ["God", "the man", "the earth", "the light"],
                    "pasuk": active_records[0]["text"],
                }
            return {
                "skill": "subject_identification",
                "question_type": "subject_identification",
                "question": "Who is doing the action here?",
                "selected_word": "הָאָרֶץ",
                "word": "הָאָרֶץ",
                "correct_answer": "the earth",
                "choices": ["the earth", "God", "light", "water"],
                "pasuk": active_records[1]["text"],
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("subject_identification", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["pasuk"], active_records[1]["text"])

    def test_select_pasuk_first_question_blocks_tense_lane_overlap_when_fresh_target_exists(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        previous = {
            "skill": "identify_tense",
            "question_type": "identify_tense",
            "question": "What form is shown?",
            "selected_word": "וְתֵרָאֶה",
            "word": "וְתֵרָאֶה",
            "correct_answer": "future",
            "choices": ["future", "past", "present", "to do form"],
            "pasuk": "previous_tense_pasuk",
        }
        st.session_state.recent_questions = [question_signature(previous)]
        ready_rows = [
            {"pasuk": "repeat_tense_pasuk", "word": "וְתֵרָאֶה", "feature": "verb", "prefix": "", "morpheme_family": ""},
            {"pasuk": "fresh_tense_pasuk", "word": "וַיִּקְרָא", "feature": "verb", "prefix": "", "morpheme_family": ""},
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == "repeat_tense_pasuk":
                return {
                    "skill": "verb_tense",
                    "question_type": "verb_tense",
                    "question": "What form is shown?",
                    "selected_word": "וְתֵרָאֶה",
                    "word": "וְתֵרָאֶה",
                    "correct_answer": "future",
                    "choices": ["future", "past", "present", "to do form"],
                    "pasuk": "repeat_tense_pasuk",
                }
            return {
                "skill": "verb_tense",
                "question_type": "verb_tense",
                "question": "What form is shown?",
                "selected_word": "וַיִּקְרָא",
                "word": "וַיִּקְרָא",
                "correct_answer": "past",
                "choices": ["past", "future", "present", "to do form"],
                "pasuk": "fresh_tense_pasuk",
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("verb_tense", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["selected_word"], "וַיִּקְרָא")

    def test_select_pasuk_first_question_prefers_non_repetitive_shoresh_surface_when_available(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        previous = {
            "skill": "shoresh",
            "question_type": "shoresh",
            "question": "What is the shoresh of וַיֹּאמֶר?",
            "selected_word": "וַיֹּאמֶר",
            "word": "וַיֹּאמֶר",
            "correct_answer": "אמר",
            "choices": ["אמר", "ראה", "קרא", "ברא"],
            "pasuk": "previous_shoresh_pasuk",
        }
        st.session_state.recent_questions = [question_signature(previous)]
        ready_rows = [
            {"pasuk": "repeat_surface_pasuk", "word": "וַיַּרְא", "feature": "verb", "prefix": "", "morpheme_family": ""},
            {"pasuk": "fresh_surface_pasuk", "word": "בָּרָא", "feature": "verb", "prefix": "", "morpheme_family": ""},
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == "repeat_surface_pasuk":
                return {
                    "skill": "shoresh",
                    "question_type": "shoresh",
                    "question": "What is the shoresh of וַיַּרְא?",
                    "selected_word": "וַיַּרְא",
                    "word": "וַיַּרְא",
                    "correct_answer": "ראה",
                    "choices": ["ראה", "אמר", "קרא", "ברא"],
                    "pasuk": "repeat_surface_pasuk",
                }
            return {
                "skill": "shoresh",
                "question_type": "shoresh",
                "question": "What is the shoresh of בָּרָא?",
                "selected_word": "בָּרָא",
                "word": "בָּרָא",
                "correct_answer": "ברא",
                "choices": ["ברא", "אמר", "ראה", "קרא"],
                "pasuk": "fresh_surface_pasuk",
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("shoresh", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["selected_word"], "בָּרָא")

    def test_select_pasuk_first_question_skips_unmappable_candidate_in_trusted_scope(self):
        active_records = active_pesukim_records()[:2]
        ready_rows = [
            {
                "pasuk": active_records[0]["text"],
                "word": "bad_word",
                "feature": "subject_identification",
                "prefix": "",
                "morpheme_family": "",
            },
            {
                "pasuk": active_records[1]["text"],
                "word": "good_word",
                "feature": "subject_identification",
                "prefix": "",
                "morpheme_family": "",
            },
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == active_records[0]["text"]:
                return {
                    "skill": "subject_identification",
                    "question_type": "subject_identification",
                    "question": "Who is doing the action here?",
                    "selected_word": "מִחוּץ",
                    "word": "מִחוּץ",
                    "correct_answer": "outside",
                    "choices": ["outside", "inside", "light", "earth"],
                    "pasuk": "outside active pilot block text",
                }
            return {
                "skill": "subject_identification",
                "question_type": "subject_identification",
                "question": "Who is doing the action here?",
                "selected_word": "הָאָרֶץ",
                "word": "הָאָרֶץ",
                "correct_answer": "the earth",
                "choices": ["the earth", "God", "light", "water"],
                "pasuk": active_records[1]["text"],
            }

        captured_events = []
        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question) as mocked_generate, \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"), \
             patch.object(
                 pilot_logging,
                 "append_pilot_event",
                 side_effect=lambda event, **kwargs: captured_events.append(event) or True,
             ):
            result = select_pasuk_first_question("subject_identification", progress={"prefix_level": 1}, adaptive_context={})
            pilot_logging.sync_pilot_served_question(result, practice_type="Learn Mode")

        self.assertIsNotNone(result)
        self.assertEqual(mocked_generate.call_count, 2)
        self.assertEqual(result["selected_word"], "הָאָרֶץ")
        self.assertEqual(result["pasuk"], active_records[1]["text"])
        self.assertEqual(result["pasuk_id"], active_records[1]["pasuk_id"])
        self.assertEqual(captured_events[0]["scope_membership"], "active_parsed")
        self.assertNotEqual(
            captured_events[0]["pasuk_ref"]["label"],
            pilot_logging.OUTSIDE_ACTIVE_PARSED_LABEL,
        )

    def test_select_pasuk_first_question_serves_new_chunk_in_scope_in_trusted_mode(self):
        active_record = next(
            record
            for record in active_pesukim_records()
            if record.get("ref", {}).get("perek") == 2
            and record.get("ref", {}).get("pasuk") == 15
        )
        ready_rows = [
            {
                "pasuk": active_record["text"],
                "word": "וַיִּקַּח",
                "feature": "phrase_translation",
                "prefix": "",
                "morpheme_family": "",
            }
        ]
        generated_question = {
            "skill": "phrase_translation",
            "question_type": "phrase_translation",
            "question": "What does this phrase mean?",
            "selected_word": "וַיִּקַּח יְהוָה אֱלֹהִים אֶת הָאָדָם",
            "word": "וַיִּקַּח יְהוָה אֱלֹהִים אֶת הָאָדָם",
            "correct_answer": "and the LORD God took the man",
            "choices": [
                "and the LORD God took the man",
                "and the LORD God placed the man",
                "and the LORD God commanded the man",
                "and God took the man",
            ],
        }

        captured_events = []
        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", return_value=dict(generated_question)), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"), \
             patch.object(
                 pilot_logging,
                 "append_pilot_event",
                 side_effect=lambda event, **kwargs: captured_events.append(event) or True,
             ):
            result = select_pasuk_first_question(
                "phrase_translation",
                progress={"prefix_level": 1},
                adaptive_context={},
            )
            pilot_logging.sync_pilot_served_question(result, practice_type="Learn Mode")

        self.assertIsNotNone(result)
        self.assertEqual(result["pasuk"], active_record["text"])
        self.assertEqual(result["pasuk_id"], active_record["pasuk_id"])
        self.assertEqual(captured_events[0]["scope_membership"], "active_parsed")
        self.assertEqual(captured_events[0]["pasuk_ref"]["pasuk_id"], active_record["pasuk_id"])
        self.assertEqual(captured_events[0]["pasuk_ref"]["label"], "Bereishis 2:15")

    def test_select_pasuk_first_question_keeps_lamor_in_scope_in_trusted_mode_with_real_generator(self):
        active_record = next(
            record
            for record in active_pesukim_records()
            if record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk") == 5
        )
        ready_rows = [
            {
                "pasuk": active_record["text"],
                "word": "לָאוֹר",
                "feature": "prefix",
                "prefix": "ל",
                "morpheme_family": "",
            }
        ]

        captured_events = []
        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"), \
             patch.object(
                 pilot_logging,
                 "append_pilot_event",
                 side_effect=lambda event, **kwargs: captured_events.append(event) or True,
             ):
            result = select_pasuk_first_question(
                "identify_prefix_meaning",
                progress={"prefix_level": 3},
                adaptive_context={},
            )
            pilot_logging.sync_pilot_served_question(result, practice_type="Learn Mode")

        self.assertIsNotNone(result)
        self.assertEqual(result["question_type"], "prefix_level_3_apply_prefix_meaning")
        self.assertEqual(result["selected_word"], "לָאוֹר")
        self.assertEqual(result["pasuk"], active_record["text"])
        self.assertEqual(result["pasuk_id"], active_record["pasuk_id"])
        self.assertEqual(result["pasuk_ref"]["pasuk_id"], active_record["pasuk_id"])
        self.assertEqual(captured_events[0]["scope_membership"], "active_parsed")
        self.assertEqual(captured_events[0]["pasuk_ref"]["pasuk_id"], active_record["pasuk_id"])
        self.assertEqual(captured_events[0]["pasuk_ref"]["label"], "Bereishis 1:5")

    def test_build_followup_question_skips_unmappable_candidate_in_trusted_scope(self):
        active_record = active_pesukim_records()[0]
        progress = {"current_skill": "subject_identification", "prefix_level": 1}
        current_question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "pasuk": active_record["text"],
            "pasuk_id": active_record["pasuk_id"],
            "selected_word": "אֱלֹקִים",
            "question": "Who is doing the action in בָּרָא?",
        }
        bad_followup = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action here?",
            "selected_word": "מִחוּץ",
            "word": "מִחוּץ",
            "correct_answer": "outside",
            "choices": ["outside", "inside", "light", "earth"],
            "pasuk": "outside active pilot block text",
        }
        good_followup = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action here?",
            "selected_word": "הַשָּׁמַיִם",
            "word": "הַשָּׁמַיִם",
            "correct_answer": "the heavens",
            "choices": ["the heavens", "God", "the earth", "the light"],
        }

        with patch.object(question_flow, "analyze_generator_pasuk", return_value=[{"word": "אֱלֹקִים"}]), \
             patch.object(question_flow, "generate_skill_question", side_effect=[bad_followup, good_followup]), \
             patch.object(question_flow, "generate_practice_question") as practice_fallback, \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.build_followup_question(progress, current_question)

        self.assertIsNotNone(result)
        self.assertEqual(result["pasuk"], active_record["text"])
        self.assertEqual(result["pasuk_id"], active_record["pasuk_id"])
        self.assertEqual(result["selected_word"], "הַשָּׁמַיִם")
        self.assertEqual(result["_assessment_source"], "targeted follow-up from active parsed dataset")
        practice_fallback.assert_not_called()

    def test_validate_question_for_serve_rejects_selected_word_not_in_bound_pasuk(self):
        active_record = active_pesukim_records()[0]
        question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does לָאוֹר mean?",
            "selected_word": "לָאוֹר",
            "word": "לָאוֹר",
            "correct_answer": "to / for light",
            "choices": ["to / for light", "and light", "the light", "in light"],
            "pasuk": active_record["text"],
        }

        validation = validate_question_for_serve(
            question,
            validation_path="unit_test",
            trusted_active_scope=True,
        )

        self.assertFalse(validation["valid"])
        self.assertIn("target_not_in_bound_pasuk", validation["rejection_codes"])

    def test_validate_question_for_serve_rejects_invalid_tense_target(self):
        active_record = next(
            record
            for record in active_pesukim_records()
            if record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk") == 1
        )
        question = {
            "skill": "verb_tense",
            "question_type": "verb_tense",
            "question": "What form is shown?",
            "selected_word": "אֱלֹקִים",
            "word": "אֱלֹקִים",
            "correct_answer": "future",
            "choices": ["future", "past", "present", "to do form"],
            "pasuk": active_record["text"],
        }

        validation = validate_question_for_serve(
            question,
            validation_path="unit_test",
            trusted_active_scope=True,
        )

        self.assertFalse(validation["valid"])
        self.assertIn("invalid_tense_target", validation["rejection_codes"])

    def test_select_pasuk_first_question_skips_duplicate_distractor_candidate_before_serve(self):
        st.session_state.pilot_scope_mode = "trusted_active_scope"
        active_records = active_pesukim_records()[:2]
        ready_rows = [
            {"pasuk": active_records[0]["text"], "word": "אֱלֹקִים", "feature": "subject_identification", "prefix": "", "morpheme_family": ""},
            {"pasuk": active_records[1]["text"], "word": "הָאָרֶץ", "feature": "subject_identification", "prefix": "", "morpheme_family": ""},
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == active_records[0]["text"]:
                return {
                    "skill": "subject_identification",
                    "question_type": "subject_identification",
                    "question": "Who is doing the action in בָּרָא?",
                    "selected_word": "אֱלֹקִים",
                    "word": "אֱלֹקִים",
                    "correct_answer": "God",
                    "choices": ["God", "God", "the earth", "the light"],
                    "pasuk": active_records[0]["text"],
                }
            return {
                "skill": "subject_identification",
                "question_type": "subject_identification",
                "question": "Who is doing the action here?",
                "selected_word": "הָאָרֶץ",
                "word": "הָאָרֶץ",
                "correct_answer": "the earth",
                "choices": ["the earth", "God", "light", "water"],
                "pasuk": active_records[1]["text"],
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("subject_identification", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["selected_word"], "הָאָרֶץ")
        self.assertEqual(
            result.get("_debug_trace", {}).get("rejection_counts", {}).get("duplicate_distractors"),
            1,
        )

    def test_build_followup_question_rejects_stale_mismatched_pasuk_before_serve(self):
        current_record = active_pesukim_records()[0]
        stale_record = active_pesukim_records()[1]
        progress = {"current_skill": "subject_identification", "prefix_level": 1}
        current_question = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "pasuk": current_record["text"],
            "pasuk_id": current_record["pasuk_id"],
            "selected_word": "אֱלֹקִים",
            "question": "Who is doing the action in בָּרָא?",
        }
        bad_followup = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action in הָיְתָה?",
            "selected_word": "הָאָרֶץ",
            "word": "הָאָרֶץ",
            "correct_answer": "the earth",
            "choices": ["the earth", "God", "light", "water"],
            "pasuk": stale_record["text"],
            "pasuk_ref": {"pasuk_id": stale_record["pasuk_id"], "label": "Bereishis 1:2"},
        }
        good_followup = {
            "skill": "subject_identification",
            "question_type": "subject_identification",
            "question": "Who is doing the action here?",
            "selected_word": "הַשָּׁמַיִם",
            "word": "הַשָּׁמַיִם",
            "correct_answer": "the heavens",
            "choices": ["the heavens", "God", "the earth", "the light"],
            "pasuk": current_record["text"],
            "pasuk_id": current_record["pasuk_id"],
            "pasuk_ref": {
                "pasuk_id": current_record["pasuk_id"],
                "label": "Bereishis 1:1",
            },
        }

        def generate_followup(skill, candidate_source, **kwargs):
            if isinstance(candidate_source, dict):
                return dict(bad_followup)
            return dict(good_followup)

        with patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: {"pasuk": pasuk}), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_followup), \
             patch.object(question_flow, "generate_practice_question") as practice_fallback, \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.build_followup_question(progress, current_question)

        self.assertIsNotNone(result)
        self.assertEqual(result["pasuk"], current_record["text"])
        self.assertEqual(result["selected_word"], "הַשָּׁמַיִם")
        self.assertEqual(
            result.get("_debug_trace", {}).get("rejection_counts", {}).get("pasuk_ref_mismatch"),
            1,
        )
        practice_fallback.assert_not_called()


if __name__ == "__main__":
    unittest.main()
