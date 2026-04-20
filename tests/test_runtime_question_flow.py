import unittest
from unittest.mock import patch

import streamlit as st

from assessment_scope import active_pesukim_records
import runtime.pilot_logging as pilot_logging
from runtime.question_flow import (
    candidate_quality_breakdown,
    display_context_policy,
    question_signature,
    recent_question_repeat_reason,
    select_pasuk_first_question,
)
import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app


class RuntimeQuestionFlowTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        streamlit_app.init_session_state()
        st.session_state.practice_type = "Learn Mode"

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
        }

        reason = recent_question_repeat_reason(sibling, [question_signature(previous)])

        self.assertEqual(reason, "recent_semantic_sibling_repeat")

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

    def test_select_pasuk_first_question_skips_same_pasuk_intent_repeat_when_fresh_option_exists(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        active_records = active_pesukim_records()[:2]
        previous = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does created-word mean?",
            "selected_word": "בָּרָא",
            "word": "בָּרָא",
            "part_of_speech": "verb",
            "correct_answer": "and he created",
            "choices": ["and he created", "and he made", "and he saw", "and he called"],
            "pasuk": active_records[0]["text"],
        }
        st.session_state.recent_questions = [question_signature(previous)]
        ready_rows = [
            {"pasuk": active_records[0]["text"], "word": "אֱלֹקִים", "feature": "translation", "prefix": "", "morpheme_family": ""},
            {"pasuk": active_records[1]["text"], "word": "אֱלֹקִים", "feature": "translation", "prefix": "", "morpheme_family": ""},
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == active_records[0]["text"]:
                return {
                    "skill": "translation",
                    "question_type": "translation",
                    "question": "What does God-word mean?",
                    "selected_word": "אֱלֹקִים",
                    "word": "אֱלֹקִים",
                    "part_of_speech": "verb",
                    "correct_answer": "and he made",
                    "choices": ["and he made", "and he saw", "and he called", "and he formed"],
                    "pasuk": active_records[0]["text"],
                }
            return {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does God-word mean?",
                "selected_word": "אֱלֹקִים",
                "word": "אֱלֹקִים",
                "part_of_speech": "noun",
                "correct_answer": "God",
                "choices": ["God", "the LORD", "the man", "someone else"],
                "pasuk": active_records[1]["text"],
            }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = select_pasuk_first_question("translation", progress={"prefix_level": 1}, adaptive_context={})

        self.assertIsNotNone(result)
        self.assertEqual(result["pasuk"], active_records[1]["text"])

    def test_select_pasuk_first_question_skips_unmappable_candidate_in_trusted_scope(self):
        active_records = active_pesukim_records()[:2]
        ready_rows = [
            {
                "pasuk": active_records[0]["text"],
                "word": "bad_word",
                "feature": "translation",
                "prefix": "",
                "morpheme_family": "",
            },
            {
                "pasuk": active_records[1]["text"],
                "word": "good_word",
                "feature": "translation",
                "prefix": "",
                "morpheme_family": "",
            },
        ]

        def generate_question(skill, candidate_source, **kwargs):
            if candidate_source == active_records[0]["text"]:
                return {
                    "skill": "translation",
                    "question_type": "translation",
                    "question": "What does this word mean?",
                    "selected_word": "מִחוּץ",
                    "word": "מִחוּץ",
                    "correct_answer": "outside",
                    "choices": ["outside", "inside", "light", "earth"],
                    "pasuk": "outside active pilot block text",
                }
            return {
                "skill": "translation",
                "question_type": "translation",
                "question": "What does this word mean?",
                "selected_word": "אֱלֹקִים",
                "word": "אֱלֹקִים",
                "correct_answer": "God",
                "choices": ["God", "light", "earth", "water"],
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
            result = select_pasuk_first_question("translation", progress={"prefix_level": 1}, adaptive_context={})
            pilot_logging.sync_pilot_served_question(result, practice_type="Learn Mode")

        self.assertIsNotNone(result)
        self.assertEqual(mocked_generate.call_count, 2)
        self.assertEqual(result["pasuk"], active_records[1]["text"])
        self.assertEqual(result["pasuk_id"], active_records[1]["pasuk_id"])
        self.assertEqual(captured_events[0]["scope_membership"], "active_parsed")
        self.assertNotEqual(
            captured_events[0]["pasuk_ref"]["label"],
            pilot_logging.OUTSIDE_ACTIVE_PARSED_LABEL,
        )

    def test_build_followup_question_skips_unmappable_candidate_in_trusted_scope(self):
        active_record = active_pesukim_records()[0]
        progress = {"current_skill": "translation", "prefix_level": 1}
        current_question = {
            "skill": "translation",
            "pasuk": active_record["text"],
            "pasuk_id": active_record["pasuk_id"],
            "selected_word": "בְּרֵאשִׁית",
            "question": "What does בְּרֵאשִׁית mean?",
        }
        bad_followup = {
            "skill": "translation",
            "question": "What does this word mean?",
            "selected_word": "מִחוּץ",
            "correct_answer": "outside",
            "choices": ["outside", "inside", "light", "earth"],
            "pasuk": "outside active pilot block text",
        }
        good_followup = {
            "skill": "translation",
            "question": "What does אֱלֹקִים mean?",
            "selected_word": "אֱלֹקִים",
            "correct_answer": "God",
            "choices": ["God", "created", "earth", "light"],
        }

        with patch.object(question_flow, "analyze_generator_pasuk", return_value=[{"word": "בְּרֵאשִׁית"}]), \
             patch.object(question_flow, "generate_skill_question", side_effect=[bad_followup, good_followup]), \
             patch.object(question_flow, "generate_practice_question") as practice_fallback, \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.build_followup_question(progress, current_question)

        self.assertIsNotNone(result)
        self.assertEqual(result["pasuk"], active_record["text"])
        self.assertEqual(result["pasuk_id"], active_record["pasuk_id"])
        self.assertEqual(result["_assessment_source"], "targeted follow-up from active parsed dataset")
        practice_fallback.assert_not_called()


if __name__ == "__main__":
    unittest.main()
