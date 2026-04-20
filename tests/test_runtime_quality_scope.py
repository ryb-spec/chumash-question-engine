import unittest
from unittest.mock import patch
import json
from pathlib import Path

import streamlit as st

import runtime.question_flow as question_flow
import runtime.session_state as session_state
import streamlit_app
from assessment_scope import active_pesukim_records
from pasuk_flow_generator import generate_pasuk_flow, generate_question, is_placeholder_translation


def newly_active_scope_pesukim():
    return [
        record["text"]
        for record in active_pesukim_records()
        if record.get("ref", {}).get("perek") == 1
        and 21 <= record.get("ref", {}).get("pasuk", 0) <= 30
    ]


def promoted_scope_pesukim():
    return [
        record["text"]
        for record in active_pesukim_records()
        if (
            record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk", 0) == 31
        )
        or (
            record.get("ref", {}).get("perek") == 2
            and 1 <= record.get("ref", {}).get("pasuk", 0) <= 9
        )
    ]


class ActiveRuntimeQualityTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()
        st.session_state.asked_tokens = []
        st.session_state.asked_question_ids = []
        st.session_state.asked_pasuks = []
        st.session_state.recent_pesukim = []
        st.session_state.recent_phrases = []
        st.session_state.recent_question_formats = []
        st.session_state.recent_prefixes = []
        st.session_state.recent_features = []
        st.session_state.feature_fallback_message = ""

    def test_newly_active_flows_avoid_duplicate_question_prompts(self):
        for pasuk in newly_active_scope_pesukim():
            flow = generate_pasuk_flow(pasuk)
            prompts = [question.get("question") for question in flow.get("questions", [])]
            self.assertEqual(
                len(prompts),
                len(set(prompts)),
                f"Repeated prompt found in flow for {pasuk}",
            )

    def test_newly_active_translation_like_questions_avoid_placeholder_answers(self):
        translation_like_types = {
            "translation",
            "phrase_meaning",
            "phrase_translation",
            "subject_identification",
        }

        for pasuk in newly_active_scope_pesukim():
            flow = generate_pasuk_flow(pasuk)
            for question in flow.get("questions", []):
                if question.get("question_type") not in translation_like_types:
                    continue

                token = question.get("selected_word") or question.get("word")
                self.assertFalse(
                    is_placeholder_translation(question.get("correct_answer"), token),
                    f"Weak translation output for {token} in {pasuk}",
                )
                self.assertEqual(len(question.get("choices", [])), 4)
                self.assertEqual(len(set(question.get("choices", []))), 4)
                self.assertFalse(
                    any(
                        is_placeholder_translation(choice, token)
                        for choice in question.get("choices", [])
                    ),
                    f"Placeholder distractor found for {token} in {pasuk}",
                )

    def test_promoted_scope_translation_like_questions_avoid_placeholder_answers(self):
        translation_like_types = {
            "translation",
            "phrase_meaning",
            "phrase_translation",
            "subject_identification",
        }

        for pasuk in promoted_scope_pesukim():
            flow = generate_pasuk_flow(pasuk)
            self.assertGreaterEqual(len(flow.get("questions", [])), 3)
            for question in flow.get("questions", []):
                if question.get("question_type") not in translation_like_types:
                    continue

                token = question.get("selected_word") or question.get("word")
                self.assertFalse(
                    is_placeholder_translation(question.get("correct_answer"), token),
                    f"Weak promoted-scope translation output for {token} in {pasuk}",
                )
                self.assertEqual(len(question.get("choices", [])), 4)
                self.assertEqual(len(set(question.get("choices", []))), 4)
                self.assertFalse(
                    any(
                        is_placeholder_translation(choice, token)
                        for choice in question.get("choices", [])
                    ),
                    f"Placeholder promoted-scope distractor found for {token} in {pasuk}",
                )

    def test_promoted_scope_phrase_questions_translate_cleanly_or_skip_honestly(self):
        supported = 0
        for pasuk in promoted_scope_pesukim():
            question = generate_question("phrase_translation", pasuk)
            if question.get("status") == "skipped":
                self.assertEqual(
                    question.get("reason"),
                    "No quiz-ready phrase target found in this pasuk.",
                )
                continue

            supported += 1
            answer = question.get("correct_answer", "")
            token = question.get("selected_word") or question.get("word")
            self.assertFalse(
                is_placeholder_translation(answer, token),
                f"Weak promoted-scope phrase answer for {token} in {pasuk}",
            )
            self.assertNotIn("God and ", answer)
            self.assertNotIn("the LORD and ", answer)
            self.assertNotIn("God making", answer)
            self.assertNotIn("the LORD God making", answer)

        self.assertGreaterEqual(supported, 1)

    def test_active_scope_known_weak_phrase_fragments_skip_honestly(self):
        weak_refs = {(1, 15), (2, 1)}

        for record in active_pesukim_records():
            ref = record.get("ref", {})
            key = (ref.get("perek"), ref.get("pasuk"))
            if key not in weak_refs:
                continue

            question = generate_question("phrase_translation", record["text"])
            self.assertEqual(question.get("status"), "skipped")
            self.assertEqual(
                question.get("reason"),
                "No quiz-ready phrase target found in this pasuk.",
            )

    def test_active_scope_overrides_recover_selected_role_and_phrase_questions(self):
        expected = {
            (1, 1): {
                "subject_identification": "God",
                "phrase_translation": "God created",
            },
            (1, 3): {
                "subject_identification": "God",
                "phrase_translation": "and God said",
            },
            (1, 4): {
                "subject_identification": "God",
                "object_identification": "the light",
                "phrase_translation": "and God saw the light",
            },
            (1, 7): {
                "subject_identification": "God",
                "object_identification": "the expanse",
                "phrase_translation": "and God made the expanse",
            },
            (1, 16): {
                "object_identification": "the two great lights",
            },
            (1, 17): {
                "object_identification": "them",
            },
            (1, 27): {
                "object_identification": "the man",
            },
            (2, 3): {
                "object_identification": "the seventh day",
                "phrase_translation": "and God blessed the seventh day",
            },
            (2, 2): {
                "object_identification": "His work",
            },
            (2, 7): {
                "subject_identification": "the LORD God",
                "object_identification": "the man",
                "phrase_translation": "and the LORD God formed the man",
            },
            (2, 8): {
                "subject_identification": "the LORD God",
                "object_identification": "a garden",
                "phrase_translation": "and the LORD God planted a garden in Eden",
            },
            (2, 9): {
                "object_identification": "every tree",
            },
        }

        for record in active_pesukim_records():
            ref = record.get("ref", {})
            key = (ref.get("perek"), ref.get("pasuk"))
            if key not in expected:
                continue

            for skill, answer in expected[key].items():
                question = generate_question(skill, record["text"])
                self.assertNotEqual(question.get("status"), "skipped")
                self.assertEqual(question.get("correct_answer"), answer)
                self.assertEqual(question.get("analysis_source"), "active_scope_override")

    def test_active_scope_verb_tense_filters_known_nonfinite_article_forms(self):
        expected_bad = {
            (1, 16): "הַמְּאֹרֹת",
            (1, 21): "הָרֹמֶשֶׂת",
        }

        for record in active_pesukim_records():
            ref = record.get("ref", {})
            key = (ref.get("perek"), ref.get("pasuk"))
            if key not in expected_bad:
                continue

            question = generate_question("verb_tense", record["text"])
            self.assertNotEqual(question.get("status"), "skipped")
            self.assertNotEqual(question.get("selected_word"), expected_bad[key])
            self.assertNotIn(expected_bad[key], question.get("explanation", ""))

    def test_promoted_scope_translation_reviews_remain_needs_review(self):
        reviews = json.loads(
            Path("data/translation_reviews.json").read_text(encoding="utf-8")
        )["reviews"]
        promoted_pasuks = {
            "bereishis_1_31",
            "bereishis_2_4",
            "bereishis_2_7",
            "bereishis_2_8",
            "bereishis_2_9",
        }
        enriched = [
            review
            for review in reviews
            if review.get("pasuk_id") in promoted_pasuks
            and review.get("authority_source") == "local_data_enrichment"
        ]

        self.assertTrue(enriched)
        self.assertTrue(all(review.get("review_status") == "needs_review" for review in enriched))
        self.assertTrue(all(review.get("approved_context") is None for review in enriched))

    def test_active_scope_role_and_morpheme_questions_use_specific_wording(self):
        saw_subject = False
        saw_object = False
        saw_prefix_suffix = False

        for pasuk in [record["text"] for record in active_pesukim_records()]:
            subject_question = generate_question("subject_identification", pasuk)
            if subject_question.get("status") != "skipped":
                saw_subject = True
                self.assertIn("doing the action in", subject_question.get("question", ""))
                self.assertIn(subject_question.get("action_token", ""), subject_question.get("question", ""))
                self.assertIn(subject_question.get("action_token", ""), subject_question.get("explanation", ""))

            object_question = generate_question("object_identification", pasuk)
            if object_question.get("status") != "skipped":
                saw_object = True
                self.assertIn("receives the action in", object_question.get("question", ""))
                self.assertIn(object_question.get("action_token", ""), object_question.get("question", ""))
                self.assertNotEqual(object_question.get("question"), "What does this word mean?")
                self.assertIn("receiv", object_question.get("explanation", "").lower())

            flow = generate_pasuk_flow(pasuk)
            for question in flow.get("questions", []):
                if question.get("question_type") != "prefix_suffix":
                    continue
                saw_prefix_suffix = True
                morpheme_type = question.get("morpheme_type")
                morpheme_form = question.get("morpheme_form")
                self.assertIn(morpheme_type, {"prefix", "suffix"})
                self.assertIn(morpheme_type, question.get("question", ""))
                self.assertIn(morpheme_form, question.get("question", ""))
                self.assertIn(morpheme_type, question.get("explanation", ""))
                self.assertNotEqual(
                    question.get("question"),
                    f"What does {question.get('selected_word')} add?",
                )

        self.assertTrue(saw_subject)
        self.assertTrue(saw_object)
        self.assertTrue(saw_prefix_suffix)

    def test_role_questions_use_resolved_roles_or_skip_honestly(self):
        genesis_1_1 = next(
            record["text"]
            for record in active_pesukim_records()
            if record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk") == 1
        )
        genesis_1_2 = next(
            record["text"]
            for record in active_pesukim_records()
            if record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk") == 2
        )
        genesis_1_26 = next(
            record["text"]
            for record in active_pesukim_records()
            if record.get("ref", {}).get("perek") == 1
            and record.get("ref", {}).get("pasuk") == 26
        )

        recovered = generate_question("subject_identification", genesis_1_1)
        self.assertNotEqual(recovered.get("status"), "skipped")
        self.assertEqual(recovered.get("correct_answer"), "God")
        self.assertEqual(recovered.get("analysis_source"), "active_scope_override")

        skipped = generate_question("subject_identification", genesis_1_2)
        self.assertEqual(skipped.get("status"), "skipped")
        self.assertIn("action anchor", skipped.get("reason", "").lower())

        supported = generate_question("subject_identification", genesis_1_26)
        self.assertNotEqual(supported.get("status"), "skipped")
        self.assertEqual(supported.get("action_token"), "וַיֹּאמֶר")
        self.assertIn("וַיֹּאמֶר", supported.get("question", ""))

    def test_build_followup_question_falls_back_when_same_question_repeats(self):
        progress = {"current_skill": "translation", "prefix_level": 1}
        question = {
            "skill": "translation",
            "pasuk": "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
            "selected_word": "בְּרֵאשִׁית",
            "question": "What does בְּרֵאשִׁית mean?",
        }
        stale_followup = {
            "skill": "translation",
            "question": "What does בְּרֵאשִׁית mean?",
            "selected_word": "בְּרֵאשִׁית",
            "correct_answer": "in the beginning",
            "choices": ["in the beginning", "created", "God", "earth"],
        }
        fallback_question = {
            "skill": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "in the beginning", "earth", "light"],
        }

        with patch.object(question_flow, "analyze_generator_pasuk", return_value=[{"word": "בְּרֵאשִׁית"}]), \
             patch.object(question_flow, "generate_skill_question", return_value=stale_followup), \
             patch.object(question_flow, "generate_practice_question", return_value=dict(fallback_question)), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.build_followup_question(progress, question)

        self.assertEqual(result["selected_word"], "בָּרָא")
        self.assertEqual(result["_assessment_source"], "fallback follow-up from active parsed dataset")
        self.assertEqual(result["_cache_status"], "fallback follow-up regenerated after the current error")

    def test_select_pasuk_first_question_uses_feature_fallback_instead_of_stalling(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        ready_rows = [
            {
                "pasuk": "לָאוֹר",
                "word": "לָאוֹר",
                "feature": "prefix",
                "prefix": "ל",
            }
        ]
        blocked_prefix_question = {
            "skill": "prefix",
            "question_type": "prefix",
            "question": "What is the prefix in לָאוֹר?",
            "selected_word": "לָאוֹר",
            "correct_answer": "ל",
            "choices": ["ל", "ב", "מ", "ו"],
            "prefix": "ל",
        }

        st.session_state.recent_features = ["prefix", "translation", "prefix", "verb", "suffix"]
        st.session_state.recent_prefixes = ["ל", "ל"]

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "generate_skill_question", return_value=dict(blocked_prefix_question)), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.select_pasuk_first_question("prefix", progress={"prefix_level": 1})

        self.assertEqual(result["selected_word"], "לָאוֹר")
        self.assertEqual(
            st.session_state.feature_fallback_message,
            "Feature repetition fallback used after 10 attempts.",
        )

    def test_generate_mastery_question_caps_opening_mechanical_questions(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        st.session_state.practice_type = "Learn Mode"
        st.session_state.recent_features = [
            "translation",
            "prefix",
            "translation",
            "suffix",
            "part_of_speech",
        ]
        st.session_state.recent_morpheme_families = ["prefix_letter", "suffix_meaning"]
        st.session_state.recent_question_groups = [
            "other",
            "mechanical",
            "other",
            "mechanical",
            "other",
        ]

        progress = {"current_skill": "identify_verb_marker", "prefix_level": 1}
        verb_question = {
            "skill": "identify_verb_marker",
            "question_type": "identify_verb_marker",
            "question": "What does the first letter ו add?",
            "selected_word": "וַיְהִי",
            "correct_answer": "and",
            "choices": ["and", "will", "he", "the"],
            "pasuk": "verb_pasuk",
        }
        translation_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
            "pasuk": "translation_pasuk",
        }

        def ready_rows(skill):
            if skill == "identify_verb_marker":
                return [{"pasuk": "verb_pasuk"}]
            if skill == "translation":
                return [{"pasuk": "translation_pasuk"}]
            return []

        def generate_question(skill, candidate_source, **kwargs):
            if skill == "identify_verb_marker":
                return dict(verb_question)
            if skill == "translation":
                return dict(translation_question)
            return None

        with patch.object(question_flow, "get_skill_ready_pasuks", side_effect=ready_rows), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.generate_mastery_question(progress)

        self.assertEqual(result["skill"], "translation")
        self.assertEqual(result["pasuk"], "translation_pasuk")
        self.assertTrue(result["_debug_trace"]["variety_guard_applied"])
        self.assertEqual(
            result["_debug_trace"]["variety_guard_source"],
            "identify_verb_marker",
        )

    def test_generate_mastery_question_blocks_back_to_back_morpheme_family(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        st.session_state.practice_type = "Learn Mode"
        st.session_state.recent_features = ["translation", "verb"]
        st.session_state.recent_morpheme_families = ["verb_marker"]
        st.session_state.recent_question_groups = ["other", "mechanical"]

        progress = {"current_skill": "identify_verb_marker", "prefix_level": 1}
        verb_question = {
            "skill": "identify_verb_marker",
            "question_type": "identify_verb_marker",
            "question": "What does the first letter ו add?",
            "selected_word": "וַיֹּאמֶר",
            "correct_answer": "and",
            "choices": ["and", "will", "he", "the"],
            "pasuk": "verb_pasuk",
        }
        translation_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does אֱלֹקִים mean?",
            "selected_word": "אֱלֹקִים",
            "correct_answer": "God",
            "choices": ["God", "created", "light", "earth"],
            "pasuk": "translation_pasuk",
        }

        def ready_rows(skill):
            if skill == "identify_verb_marker":
                return [{"pasuk": "verb_pasuk"}]
            if skill == "translation":
                return [{"pasuk": "translation_pasuk"}]
            return []

        def generate_question(skill, candidate_source, **kwargs):
            if skill == "identify_verb_marker":
                return dict(verb_question)
            if skill == "translation":
                return dict(translation_question)
            return None

        with patch.object(question_flow, "get_skill_ready_pasuks", side_effect=ready_rows), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.generate_mastery_question(progress)

        self.assertEqual(result["skill"], "translation")
        self.assertTrue(result["_debug_trace"]["variety_guard_applied"])

    def test_generate_mastery_question_blocks_excessive_morpheme_lane_looping(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        st.session_state.practice_type = "Learn Mode"
        st.session_state.recent_features = [
            "prefix",
            "translation",
            "suffix",
            "translation",
            "part_of_speech",
            "translation",
        ]
        st.session_state.recent_morpheme_families = [
            "prefix_letter",
            "suffix_meaning",
        ]
        st.session_state.recent_question_groups = [
            "mechanical",
            "other",
            "mechanical",
            "other",
            "other",
            "other",
        ]

        progress = {"current_skill": "identify_verb_marker", "prefix_level": 1}
        verb_question = {
            "skill": "identify_verb_marker",
            "question_type": "identify_verb_marker",
            "question": "What does the first letter ו add?",
            "selected_word": "וַיַּרְא",
            "correct_answer": "and",
            "choices": ["and", "will", "he", "the"],
            "pasuk": "verb_pasuk",
        }
        translation_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does אוֹר mean?",
            "selected_word": "אוֹר",
            "correct_answer": "light",
            "choices": ["light", "God", "water", "day"],
            "pasuk": "translation_pasuk",
        }

        def ready_rows(skill):
            if skill == "identify_verb_marker":
                return [{"pasuk": "verb_pasuk"}]
            if skill == "translation":
                return [{"pasuk": "translation_pasuk"}]
            return []

        def generate_question(skill, candidate_source, **kwargs):
            if skill == "identify_verb_marker":
                return dict(verb_question)
            if skill == "translation":
                return dict(translation_question)
            return None

        with patch.object(question_flow, "get_skill_ready_pasuks", side_effect=ready_rows), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.generate_mastery_question(progress)

        self.assertEqual(result["skill"], "translation")
        self.assertTrue(result["_debug_trace"]["variety_guard_applied"])

    def test_generate_mastery_question_sequences_short_run_from_warmup_to_context(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        st.session_state.practice_type = "Learn Mode"

        progress = {"current_skill": "identify_prefix_meaning", "prefix_level": 1}
        mechanical_question = {
            "skill": "identify_prefix_meaning",
            "question_type": "prefix_level_2_identify_prefix_meaning",
            "question": "What does the prefix mean?",
            "selected_word": "לָאוֹר",
            "correct_answer": "to / for",
            "choices": ["to / for", "in", "from", "the"],
            "pasuk": "prefix_pasuk",
        }
        translation_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
            "pasuk": "translation_pasuk",
        }
        context_question = {
            "skill": "phrase_translation",
            "question_type": "phrase_translation",
            "question": "What does this phrase mean?",
            "selected_word": "וַיֹּאמֶר אֱלֹקִים",
            "correct_answer": "God said",
            "choices": ["God said", "God saw", "light was", "there was evening"],
            "pasuk": "context_pasuk",
        }

        def ready_rows(skill):
            if skill == "identify_prefix_meaning":
                return [{"pasuk": "prefix_pasuk"}]
            if skill == "translation":
                return [{"pasuk": "translation_pasuk"}]
            if skill == "phrase_translation":
                return [{"pasuk": "context_pasuk"}]
            return []

        def generate_question(skill, candidate_source, **kwargs):
            if skill == "identify_prefix_meaning":
                return dict(mechanical_question)
            if skill == "translation":
                return dict(translation_question)
            if skill == "phrase_translation":
                return dict(context_question)
            return None

        with patch.object(question_flow, "get_skill_ready_pasuks", side_effect=ready_rows), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            st.session_state.questions_answered = 0
            st.session_state.recent_instructional_groups = []
            warmup = streamlit_app.generate_mastery_question(progress)

            st.session_state.questions_answered = 3
            st.session_state.recent_instructional_groups = ["mechanical", "meaning", "mechanical"]
            middle = streamlit_app.generate_mastery_question(progress)

            st.session_state.questions_answered = 7
            st.session_state.recent_instructional_groups = ["mechanical", "meaning", "meaning", "verb_building"]
            late = streamlit_app.generate_mastery_question(progress)

        self.assertEqual(warmup["skill"], "identify_prefix_meaning")
        self.assertEqual(warmup["_debug_trace"]["sequencing_stage"], "warmup")

        self.assertEqual(middle["skill"], "translation")
        self.assertEqual(middle["_debug_trace"]["sequencing_stage"], "meaning_build")
        self.assertEqual(middle["_debug_trace"]["sequencing_selected_group"], "meaning")

        self.assertEqual(late["skill"], "phrase_translation")
        self.assertEqual(late["_debug_trace"]["sequencing_stage"], "context_ramp")
        self.assertEqual(late["_debug_trace"]["sequencing_selected_group"], "context")

    def test_generate_mastery_question_moves_out_of_tense_family_after_missed_tense(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        st.session_state.practice_type = "Learn Mode"
        st.session_state.pending_tense_contrast_followup = True

        progress = {"current_skill": "identify_tense", "prefix_level": 1}
        tense_question = {
            "skill": "identify_tense",
            "question_type": "identify_tense",
            "question": "What form is shown?",
            "selected_word": "וַיַּרְא",
            "correct_answer": "past",
            "choices": ["past", "future", "present", "to do form"],
            "pasuk": "tense_pasuk",
        }
        translation_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
            "pasuk": "translation_pasuk",
        }

        def ready_rows(skill):
            if skill == "identify_tense":
                return [{"pasuk": "tense_pasuk"}]
            if skill == "translation":
                return [{"pasuk": "translation_pasuk"}]
            return []

        def generate_question(skill, candidate_source, **kwargs):
            if skill == "identify_tense":
                return dict(tense_question)
            if skill == "translation":
                return dict(translation_question)
            return None

        with patch.object(question_flow, "get_skill_ready_pasuks", side_effect=ready_rows), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.generate_mastery_question(progress)

        self.assertEqual(result["skill"], "translation")
        self.assertFalse(st.session_state.pending_tense_contrast_followup)
        self.assertEqual(
            result["_debug_trace"]["transition_reason"],
            "A short tense contrast was shown, so the run moved back into broader variety.",
        )

    def test_select_pasuk_first_question_binds_lamor_to_active_scope_in_trusted_mode(self):
        st.session_state.pilot_scope_mode = "trusted_active_scope"
        active_record = next(
            record for record in active_pesukim_records()
            if "לָאוֹר" in record.get("text", "")
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
        generated_question = {
            "skill": "identify_prefix_meaning",
            "question_type": "prefix_level_3_apply_prefix_meaning",
            "question": "What does לָאוֹר mean?",
            "selected_word": "לָאוֹר",
            "word": "לָאוֹר",
            "pasuk": "לָאוֹר",
            "correct_answer": "to / for light",
            "choices": ["to / for light", "in the light", "and light", "the light"],
            "prefix": "ל",
        }

        with patch.object(question_flow, "get_skill_ready_pasuks", return_value=ready_rows), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", return_value=dict(generated_question)), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.select_pasuk_first_question(
                "identify_prefix_meaning",
                progress={"prefix_level": 3},
            )

        self.assertEqual(result["selected_word"], "לָאוֹר")
        self.assertEqual(result["pasuk"], active_record["text"])
        self.assertEqual(result["pasuk_id"], active_record["pasuk_id"])
        self.assertEqual(
            result["pasuk_ref"]["label"],
            f"{active_record['ref']['sefer']} {active_record['ref']['perek']}:{active_record['ref']['pasuk']}",
        )

    def test_generate_mastery_question_caps_tense_family_in_short_run(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        st.session_state.practice_type = "Learn Mode"
        st.session_state.questions_answered = 6
        st.session_state.recent_questions = [
            {"skill": "identify_tense"},
            {"skill": "translation"},
            {"skill": "verb_tense"},
            {"skill": "shoresh"},
            {"skill": "identify_tense"},
        ]
        st.session_state.recent_instructional_groups = ["verb_building", "meaning", "verb_building", "meaning"]

        progress = {"current_skill": "identify_tense", "prefix_level": 1}
        tense_question = {
            "skill": "identify_tense",
            "question_type": "identify_tense",
            "question": "What form is shown?",
            "selected_word": "וַיַּרְא",
            "correct_answer": "past",
            "choices": ["past", "future", "present", "to do form"],
            "pasuk": "tense_pasuk",
        }
        translation_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
            "pasuk": "translation_pasuk",
        }

        def ready_rows(skill):
            if skill == "identify_tense":
                return [{"pasuk": "tense_pasuk"}]
            if skill == "translation":
                return [{"pasuk": "translation_pasuk"}]
            return []

        def generate_question(skill, candidate_source, **kwargs):
            if skill == "identify_tense":
                return dict(tense_question)
            if skill == "translation":
                return dict(translation_question)
            return None

        with patch.object(question_flow, "get_skill_ready_pasuks", side_effect=ready_rows), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.generate_mastery_question(progress)

        self.assertEqual(result["skill"], "translation")
        self.assertEqual(result["_debug_trace"]["sequencing_stage"], "context_ramp")

    def test_generate_mastery_question_caps_broader_grammar_taxonomy_family(self):
        st.session_state.pilot_scope_mode = "open_pilot_scope"
        st.session_state.practice_type = "Learn Mode"
        st.session_state.questions_answered = 7
        st.session_state.recent_questions = [
            {"skill": "identify_tense"},
            {"skill": "translation"},
            {"skill": "part_of_speech"},
            {"skill": "shoresh"},
            {"skill": "verb_tense"},
        ]
        st.session_state.recent_instructional_groups = ["verb_building", "meaning", "meaning", "context"]

        progress = {"current_skill": "part_of_speech", "prefix_level": 1}
        grammar_question = {
            "skill": "part_of_speech",
            "question_type": "part_of_speech",
            "question": "What kind of word is אוֹר?",
            "selected_word": "אוֹר",
            "correct_answer": "naming word",
            "choices": ["naming word", "action word", "small helper word", "direction word"],
            "pasuk": "grammar_pasuk",
        }
        translation_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does בָּרָא mean?",
            "selected_word": "בָּרָא",
            "correct_answer": "created",
            "choices": ["created", "light", "earth", "water"],
            "pasuk": "translation_pasuk",
        }

        def ready_rows(skill):
            if skill == "part_of_speech":
                return [{"pasuk": "grammar_pasuk"}]
            if skill == "translation":
                return [{"pasuk": "translation_pasuk"}]
            return []

        def generate_question(skill, candidate_source, **kwargs):
            if skill == "part_of_speech":
                return dict(grammar_question)
            if skill == "translation":
                return dict(translation_question)
            return None

        with patch.object(question_flow, "get_skill_ready_pasuks", side_effect=ready_rows), \
             patch.object(question_flow, "analyze_generator_pasuk", side_effect=lambda pasuk: pasuk), \
             patch.object(question_flow, "generate_skill_question", side_effect=generate_question), \
             patch.object(session_state, "record_selected_pasuk"), \
             patch.object(session_state, "record_question_feature"), \
             patch.object(session_state, "record_question_prefix"):
            result = streamlit_app.generate_mastery_question(progress)

        self.assertEqual(result["skill"], "translation")
        self.assertEqual(
            result["_debug_trace"]["transition_reason"],
            "Learn Mode moved back to clearer word work before more grammar labels.",
        )


if __name__ == "__main__":
    unittest.main()
