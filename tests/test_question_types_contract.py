import unittest
from unittest.mock import patch

import engine.flow_builder as flow_builder
from assessment_scope import active_pesukim_records, active_scope_override_for_pasuk_id
from pasuk_flow_generator import (
    CONTROLLED_TENSE_CHOICES,
    analyze_pasuk,
    generate_pasuk_flow,
    generate_question,
    load_word_bank,
)
from torah_parser.word_bank_adapter import normalize_hebrew_key


def pasuk_by_ref(perek, pasuk):
    for record in active_pesukim_records():
        ref = record.get("ref", {})
        if ref.get("perek") == perek and ref.get("pasuk") == pasuk:
            return record["text"]
    raise AssertionError(f"Missing active pasuk {perek}:{pasuk}")


class QuestionTypeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.word_bank, _ = load_word_bank()

    def test_subject_identification_can_use_active_scope_override_when_parser_fails_closed(self):
        pasuk = pasuk_by_ref(1, 1)
        question = generate_question("subject_identification", pasuk)

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("skill"), "subject_identification")
        self.assertEqual(question.get("selected_word"), "אֱלֹקִים")
        self.assertEqual(question.get("correct_answer"), "God")
        self.assertEqual(question.get("action_token"), "בָּרָא")
        self.assertIn(
            question.get("analysis_source"),
            {"active_scope_override", "active_scope_reviewed_bank"},
        )
        self.assertEqual(question.get("override_pasuk_id"), "bereishis_1_1")

    def test_subject_identification_uses_role_layer_when_supported(self):
        pasuk = pasuk_by_ref(1, 3)
        question = generate_question("subject_identification", pasuk)
        self.assertNotEqual(question.get("status"), "skipped")

        analyzed = analyze_pasuk(pasuk, self.word_bank)
        subject_item = next(
            item for item in analyzed if item["token"] == question["selected_word"]
        )
        action_item = next(
            item for item in analyzed if item["token"] == question["action_token"]
        )

        self.assertEqual(subject_item["entry"].get("semantic_group"), "divine")
        self.assertEqual(subject_item["entry"].get("role_hint"), "subject_candidate")
        self.assertEqual(action_item["entry"].get("part_of_speech"), "verb")
        self.assertIn(
            question.get("analysis_source"),
            {"active_scope_override", "active_scope_reviewed_bank"},
        )
        self.assertIn("Who is doing the action in", question.get("question", ""))
        self.assertIn(question["action_token"], question.get("question", ""))
        self.assertIn(question["action_token"], question.get("explanation", ""))
        self.assertEqual(question.get("role_focus"), "subject")

    def test_verb_tense_choices_follow_runtime_labels(self):
        allowed = {
            "past",
            "future",
            "present",
            "to do form",
        }

        for ref in ((1, 3), (1, 9), (1, 14), (1, 17), (2, 10), (2, 15), (2, 17)):
            pasuk = pasuk_by_ref(*ref)
            question = generate_question("verb_tense", pasuk)
            if question.get("status") == "skipped":
                continue
            self.assertIn(question["correct_answer"], allowed)
            self.assertTrue(set(question["choices"]).issubset(allowed))
            self.assertEqual(len(question["choices"]), 4)
            self.assertEqual(len(set(question["choices"])), 4)
            self.assertNotIn("past narrative", question["choices"])
            self.assertNotIn("short future form", question["choices"])
            self.assertNotIn("not a verb", question["choices"])

    def test_identify_tense_uses_only_taught_labels(self):
        allowed = {"past", "future", "present", "to do form"}

        question = generate_question("identify_tense", pasuk_by_ref(1, 3))

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertTrue(set(question.get("choices", [])).issubset(allowed))
        self.assertNotIn("infinitive", question.get("choices", []))
        self.assertNotIn("past narrative", question.get("choices", []))
        self.assertNotIn("short future form", question.get("choices", []))
        self.assertNotIn("not a verb", question.get("choices", []))

    def test_part_of_speech_uses_cohort_safe_word_kind_labels(self):
        analyzed_override = [
            {
                "token": "בָּרָא",
                "entry": {
                    "word": "בָּרָא",
                    "translation": "created",
                    "type": "verb",
                    "part_of_speech": "verb",
                    "semantic_group": "action",
                    "entity_type": "verb",
                },
            },
            {
                "token": "אוֹר",
                "entry": {
                    "word": "אוֹר",
                    "translation": "light",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "object",
                    "entity_type": "common_noun",
                },
            },
        ]

        question = generate_question(
            "part_of_speech",
            "בָּרָא אוֹר",
            analyzed_override=analyzed_override,
        )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(
            question.get("question"),
            f"What kind of word is {question.get('selected_word')}?",
        )
        self.assertIn(question.get("correct_answer"), {"action word", "naming word"})
        self.assertEqual(
            set(question.get("choices", [])),
            {"action word", "naming word", "small helper word", "direction word"},
        )
        self.assertIn(question.get("word_gloss"), {"created", "light"})
        self.assertNotIn("part of speech", question.get("question", "").lower())
        self.assertNotIn("particle", " ".join(question.get("choices", [])).lower())
        self.assertNotIn("prep", " ".join(question.get("choices", [])).lower())

    def test_non_verb_surface_is_rejected_for_verb_tense(self):
        question = generate_question("verb_tense", "בְּצַלְמֵנוּ")

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("verb tense", question.get("reason", "").lower())

    def test_article_led_nonfinite_surfaces_are_rejected_for_verb_tense(self):
        for token in ("הָרֹמֶשֶׂת", "הַמְּאֹרֹת"):
            question = generate_question("verb_tense", token)

            self.assertEqual(question.get("status"), "skipped")
            self.assertIsNone(question.get("choices"))
            self.assertIn("verb tense", question.get("reason", "").lower())

    def test_unsupported_skill_returns_structured_skip(self):
        pasuk = pasuk_by_ref(1, 13)
        question = generate_question("subject_identification", pasuk)

        self.assertEqual(question.get("status"), "skipped")
        self.assertFalse(question.get("supported"))
        self.assertEqual(question.get("skill"), "subject_identification")
        self.assertEqual(question.get("pasuk"), pasuk)
        self.assertIn("subject", question.get("reason", "").lower())
        self.assertIsNone(question.get("selected_word"))

    def test_active_scope_override_does_not_apply_outside_active_scope(self):
        question = generate_question(
            "subject_identification",
            "בְּרֵאשִׁית בָּרָא אֱלֹקִים",
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIsNone(question.get("analysis_source"))
        self.assertIsNone(question.get("override_pasuk_id"))

    def test_flow_generation_stays_valid_when_skill_is_skipped(self):
        pasuk = pasuk_by_ref(1, 24)
        flow = generate_pasuk_flow(pasuk)

        self.assertEqual(flow.get("pasuk"), pasuk)
        self.assertGreaterEqual(len(flow.get("questions", [])), 3)
        self.assertIn("skipped", flow)
        self.assertIn(
            "subject_identification",
            {item.get("skill") for item in flow.get("skipped", [])},
        )
        self.assertNotIn(
            "subject_identification",
            {item.get("question_type") for item in flow.get("questions", [])},
        )

    def test_object_identification_skips_ambiguous_translation_like_case(self):
        pasuk = pasuk_by_ref(1, 1)
        question = generate_question("object_identification", pasuk)

        self.assertEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("skill"), "object_identification")
        self.assertNotEqual(question.get("question"), "What does this word mean?")

    def test_object_identification_supported_case_uses_role_language(self):
        analyzed_pasuk = [
            {
                "token": "וַיִּתֵּן",
                "entry": {
                    "word": "וַיִּתֵּן",
                    "translation": "and gave",
                    "type": "verb",
                    "part_of_speech": "verb",
                    "semantic_group": "action",
                    "role_hint": "unknown",
                    "entity_type": "verb",
                    "tense": "past",
                    "shoresh": "נתן",
                },
            },
            {
                "token": "מֹשֶׁה",
                "entry": {
                    "word": "מֹשֶׁה",
                    "translation": "Moshe",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "person",
                    "role_hint": "subject_candidate",
                    "entity_type": "person",
                },
            },
            {
                "token": "אֶת",
                "entry": {
                    "word": "אֶת",
                    "translation": "[direct object marker]",
                    "type": "particle",
                    "part_of_speech": "particle",
                    "semantic_group": "unknown",
                    "role_hint": "object_candidate",
                    "entity_type": "grammatical_particle",
                },
            },
            {
                "token": "סֵפֶר",
                "entry": {
                    "word": "סֵפֶר",
                    "translation": "a book",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "object",
                    "role_hint": "object_candidate",
                    "entity_type": "common_noun",
                },
            },
        ]

        question = generate_question(
            "object_identification",
            "וַיִּתֵּן מֹשֶׁה אֶת סֵפֶר",
            analyzed_override=analyzed_pasuk,
        )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("action_token"), "וַיִּתֵּן")
        self.assertEqual(question.get("role_focus"), "direct_object")
        self.assertEqual(question.get("correct_answer"), "a book")
        self.assertEqual(
            question.get("question"),
            "What receives the action in וַיִּתֵּן?",
        )
        self.assertIn("receives the action", question.get("explanation", ""))

    def test_object_identification_can_use_active_scope_override(self):
        pasuk = pasuk_by_ref(2, 3)
        question = generate_question("object_identification", pasuk)

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "יוֹם הַשְּׁבִיעִי")
        self.assertEqual(question.get("correct_answer"), "the seventh day")
        self.assertEqual(question.get("action_token"), "וַיְבָרֶךְ")
        self.assertIn(
            question.get("analysis_source"),
            {"active_scope_override", "active_scope_reviewed_bank"},
        )

    def test_object_identification_can_use_active_scope_override_for_clean_first_clause(self):
        pasuk = pasuk_by_ref(1, 4)
        question = generate_question("object_identification", pasuk)

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "הָאוֹר")
        self.assertEqual(question.get("correct_answer"), "the light")
        self.assertEqual(question.get("action_token"), "וַיַּרְא")
        self.assertIn(
            question.get("analysis_source"),
            {"active_scope_override", "active_scope_reviewed_bank"},
        )

    def test_object_identification_recovers_additional_gold_aligned_override_cases(self):
        expected = {
            (1, 16): "the two great lights",
            (1, 17): "them",
            (1, 27): "the man",
            (2, 2): "His work",
            (2, 9): "every tree",
        }

        for ref, answer in expected.items():
            question = generate_question("object_identification", pasuk_by_ref(*ref))
            self.assertNotEqual(question.get("status"), "skipped")
            self.assertEqual(question.get("correct_answer"), answer)
            self.assertIn(
                question.get("analysis_source"),
                {"active_scope_override", "active_scope_reviewed_bank"},
            )
            self.assertEqual(question.get("role_focus"), "direct_object")

    def test_phrase_translation_skips_known_weak_active_scope_fragment(self):
        pasuk = pasuk_by_ref(1, 15)
        question = generate_question("phrase_translation", pasuk)

        self.assertEqual(question.get("status"), "skipped")
        self.assertEqual(
            question.get("reason"),
            "This clause is not treated as a quiz-ready phrase target.",
        )

    def test_phrase_translation_prefers_full_role_backed_clause_when_available(self):
        analyzed_pasuk = [
            {
                "token": "וַיְבָרֶךְ",
                "entry": {
                    "word": "וַיְבָרֶךְ",
                    "translation": "and blessed",
                    "type": "verb",
                    "part_of_speech": "verb",
                    "semantic_group": "action",
                    "role_hint": "unknown",
                    "entity_type": "verb",
                },
            },
            {
                "token": "אֹתָם",
                "entry": {
                    "word": "אֹתָם",
                    "translation": "them",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "object",
                    "role_hint": "object_candidate",
                    "entity_type": "pronoun",
                },
            },
            {
                "token": "אֱלֹקִים",
                "entry": {
                    "word": "אֱלֹקִים",
                    "translation": "God",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "divine",
                    "role_hint": "subject_candidate",
                    "entity_type": "divine_being",
                },
            },
        ]

        question = generate_question(
            "phrase_translation",
            "וַיְבָרֶךְ אֹתָם אֱלֹקִים",
            analyzed_override=analyzed_pasuk,
        )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "וַיְבָרֶךְ אֹתָם אֱלֹקִים")
        self.assertEqual(question.get("correct_answer"), "and God blessed them")
        self.assertNotIn("God and blessed", question.get("choices", []))
        self.assertNotIn("and blessed God", question.get("choices", []))
        self.assertNotIn("and he God blessed", question.get("choices", []))

    def test_phrase_translation_can_use_active_scope_preferred_phrase_override(self):
        pasuk = pasuk_by_ref(2, 7)
        question = generate_question("phrase_translation", pasuk)

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(
            question.get("selected_word"),
            "וַיִּיצֶר יְהוָה אֱלֹהִים אֶת הָאָדָם",
        )
        self.assertEqual(question.get("correct_answer"), "and the LORD God formed the man")
        self.assertIn(
            question.get("analysis_source"),
            {"active_scope_override", "active_scope_reviewed_bank"},
        )

    def test_phrase_translation_can_use_active_scope_preferred_phrase_override_for_god_said_clause(self):
        pasuk = pasuk_by_ref(1, 3)
        question = generate_question("phrase_translation", pasuk)

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "וַיֹּאמֶר אֱלֹקִים")
        self.assertEqual(question.get("correct_answer"), "and God said")
        self.assertIn(
            question.get("analysis_source"),
            {"active_scope_override", "active_scope_reviewed_bank"},
        )

    def test_phrase_translation_can_use_backfilled_overrides_for_bereishis_2_11_to_2_14(self):
        expected = {
            (2, 11): "the name of the first is Pishon",
            (2, 12): "and the gold of that land is good",
            (2, 13): "and the name of the second river is Gichon",
            (2, 14): "and the fourth river is Phrat",
        }

        for ref, answer in expected.items():
            question = generate_question("phrase_translation", pasuk_by_ref(*ref))
            self.assertNotEqual(question.get("status"), "skipped")
            self.assertEqual(question.get("correct_answer"), answer)
            self.assertIn(
                question.get("analysis_source"),
                {"active_scope_override", "active_scope_reviewed_bank"},
            )

    def test_student_facing_translation_prefers_contextual_reviewed_targets_and_keeps_divine_choices_consistent(self):
        standalone_word_question = generate_question("translation", "??????????")
        standalone_formed_question = generate_question("translation", "?????????")
        divine_question = generate_question("translation", pasuk_by_ref(3, 3))
        created_translation = generate_question("translation", pasuk_by_ref(1, 1))
        created_phrase = generate_question("phrase_translation", pasuk_by_ref(1, 1))
        made_phrase = generate_question("phrase_translation", pasuk_by_ref(1, 16))
        formed_phrase = generate_question("phrase_translation", pasuk_by_ref(2, 7))

        self.assertEqual(standalone_word_question.get("status"), "skipped")
        self.assertEqual(standalone_formed_question.get("status"), "skipped")
        self.assertEqual(divine_question.get("correct_answer"), "you will die")
        self.assertEqual(divine_question.get("selected_word"), "תְּמֻתוּן")
        self.assertNotIn("God", divine_question.get("choices", []))
        self.assertNotIn("the LORD", divine_question.get("choices", []))
        self.assertEqual(created_translation.get("question_type"), "phrase_translation")
        self.assertEqual(created_translation.get("correct_answer"), "God created")
        self.assertEqual(created_phrase.get("question_type"), "phrase_translation")
        self.assertEqual(created_phrase.get("correct_answer"), "God created")
        self.assertEqual(made_phrase.get("correct_answer"), "and God made the two great lights")
        self.assertEqual(formed_phrase.get("correct_answer"), "and the LORD God formed the man")
        self.assertNotIn("the LORD the LORD", " ".join(formed_phrase.get("choices", [])))
        self.assertNotIn("God God", " ".join(formed_phrase.get("choices", [])))

    def test_vayehi_style_hayah_forms_are_not_standalone_translation_targets(self):
        entry = {
            "word": "וַיְהִי",
            "surface": "וַיְהִי",
            "type": "verb",
            "part_of_speech": "verb",
            "shoresh": "היה",
            "tense": "vav_consecutive_past",
            "translation_literal": "and it was",
            "translation_context": "and there was",
        }

        self.assertFalse(flow_builder.standalone_translation_target(entry, "וַיְהִי"))
        self.assertEqual(flow_builder.instructional_value(entry, "translation"), "low")

    def test_bereishis_1_31_translation_does_not_serve_vayehi_as_plain_word_meaning(self):
        with patch.object(flow_builder, "pick_word_for_skill", return_value="וַיְהִי"):
            question = generate_question("translation", pasuk_by_ref(1, 31))

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertNotEqual(question.get("selected_word"), "וַיְהִי")
        self.assertNotIn("וַיְהִי", question.get("question", ""))

    def test_translation_uses_same_family_verb_distractors_instead_of_random_nouns(self):
        target_entry = {
            "word": "וַיִּיצֶר",
            "translation": "formed",
            "type": "verb",
            "part_of_speech": "verb",
            "semantic_group": "action",
            "role_hint": "unknown",
            "entity_type": "verb",
            "group": "verb_action",
            "shoresh": "יצר",
            "tense": "vav_consecutive_past",
            "source_refs": ["bereishis_2_7"],
        }
        made_entry = {
            "word": "וַיַּעַשׂ",
            "translation": "made",
            "type": "verb",
            "part_of_speech": "verb",
            "semantic_group": "action",
            "role_hint": "unknown",
            "entity_type": "verb",
            "group": "verb_action",
            "shoresh": "עשה",
            "tense": "vav_consecutive_past",
            "source_refs": ["bereishis_1_16"],
        }
        saw_entry = {
            "word": "וַיַּרְא",
            "translation": "saw",
            "type": "verb",
            "part_of_speech": "verb",
            "semantic_group": "action",
            "role_hint": "unknown",
            "entity_type": "verb",
            "group": "verb_action",
            "shoresh": "ראה",
            "tense": "vav_consecutive_past",
            "source_refs": ["bereishis_1_4"],
        }
        called_entry = {
            "word": "וַיִּקְרָא",
            "translation": "called",
            "type": "verb",
            "part_of_speech": "verb",
            "semantic_group": "action",
            "role_hint": "unknown",
            "entity_type": "verb",
            "group": "verb_action",
            "shoresh": "קרא",
            "tense": "vav_consecutive_past",
            "source_refs": ["bereishis_1_5"],
        }
        noun_entries = [
            {
                "word": "אוֹר",
                "translation": "light",
                "type": "noun",
                "part_of_speech": "noun",
                "semantic_group": "object",
                "role_hint": "unknown",
                "entity_type": "common_noun",
                "group": "noun_object",
                "source_refs": ["bereishis_1_3"],
            },
            {
                "word": "אֶרֶץ",
                "translation": "earth",
                "type": "noun",
                "part_of_speech": "noun",
                "semantic_group": "place",
                "role_hint": "unknown",
                "entity_type": "common_noun",
                "group": "noun_object",
                "source_refs": ["bereishis_1_1"],
            },
            {
                "word": "מַיִם",
                "translation": "water",
                "type": "noun",
                "part_of_speech": "noun",
                "semantic_group": "object",
                "role_hint": "unknown",
                "entity_type": "common_noun",
                "group": "noun_object",
                "source_refs": ["bereishis_1_2"],
            },
        ]
        word_bank = {
            entry["word"]: entry
            for entry in [target_entry, made_entry, saw_entry, called_entry, *noun_entries]
        }
        by_group = {
            "verb_action": [target_entry, made_entry, saw_entry, called_entry],
            "noun_object": noun_entries,
        }

        with patch.object(flow_builder, "load_word_bank", return_value=(word_bank, by_group)):
            question = generate_question(
                "translation",
                "וַיִּיצֶר",
                analyzed_override=[{"token": "וַיִּיצֶר", "entry": dict(target_entry)}],
            )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("correct_answer"), "and he formed")
        wrong_answers = {
            choice for choice in question.get("choices", [])
            if choice != question.get("correct_answer")
        }
        self.assertEqual(
            wrong_answers,
            {"and he made", "and he saw", "and he called"},
        )
        self.assertNotIn("light", question.get("choices", []))
        self.assertNotIn("earth", question.get("choices", []))
        self.assertNotIn("water", question.get("choices", []))

    def test_phrase_translation_choices_stay_phrase_like_and_same_family(self):
        question = generate_question("phrase_translation", pasuk_by_ref(1, 4))

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("correct_answer"), "and God saw the light")
        self.assertTrue(all(choice.startswith("and ") for choice in question.get("choices", [])))
        self.assertTrue(all(len(choice.split()) >= 3 for choice in question.get("choices", [])))

    def test_active_scope_verb_tense_reroutes_away_from_known_bad_targets(self):
        expected_bad = {
            (1, 16): "הַמְּאֹרֹת",
            (1, 21): "הָרֹמֶשֶׂת",
        }

        for ref, bad_token in expected_bad.items():
            question = generate_question("verb_tense", pasuk_by_ref(*ref))

            self.assertNotEqual(question.get("status"), "skipped")
            self.assertNotEqual(question.get("selected_word"), bad_token)
            self.assertIn(question.get("correct_answer"), {
                "past",
                "future",
                "present",
                "to do form",
            })

    def test_active_scope_verb_tense_avoids_false_surface_only_verb_in_bereishis_1_1(self):
        question = generate_question("verb_tense", pasuk_by_ref(1, 1))

        if question.get("status") == "skipped":
            self.assertIn("verb tense", question.get("reason", "").lower())
        else:
            self.assertNotEqual(question.get("selected_word"), "בְּרֵאשִׁית")
            self.assertIn(question.get("correct_answer"), {"past", "future", "present", "to do form"})

    def test_active_scope_identify_tense_avoids_false_surface_only_verb_in_bereishis_1_2(self):
        question = generate_question("identify_tense", pasuk_by_ref(1, 2))

        if question.get("status") == "skipped":
            self.assertIn("verb tense", question.get("reason", "").lower())
        else:
            self.assertNotEqual(question.get("selected_word"), "מְרַחֶפֶת")
            self.assertIn(question.get("correct_answer"), {"past", "future", "present", "to do form"})

    def test_active_scope_part_of_speech_avoids_false_action_word_in_bereishis_1_1(self):
        question = generate_question("part_of_speech", pasuk_by_ref(1, 1))

        if question.get("status") == "skipped":
            self.assertIn("noun or verb target", question.get("reason", "").lower())
        else:
            self.assertNotEqual(question.get("selected_word"), "בְּרֵאשִׁית")
            self.assertIn(question.get("correct_answer"), {"action word", "naming word"})

    def test_vav_consecutive_forms_are_not_simple_prefix_meaning_targets(self):
        analyzed_override = [
            {
                "token": "וַיְהִי",
                "entry": {
                    "word": "וַיְהִי",
                    "surface": "וַיְהִי",
                    "type": "verb",
                    "part_of_speech": "verb",
                    "shoresh": "היה",
                    "tense": "vav_consecutive_past",
                    "translation_literal": "and it was",
                    "translation_context": "and there was",
                    "prefixes": [
                        {"form": "ו", "type": "verb_prefix_vav_consecutive", "translation": "and"}
                    ],
                    "prefix": "ו",
                    "prefix_meaning": "and",
                },
            }
        ]

        question = generate_question(
            "identify_prefix_meaning",
            "וַיְהִי",
            analyzed_override=analyzed_override,
            prefix_level=2,
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertEqual(
            question.get("reason"),
            "No usable prefixed word found in this pasuk.",
        )

    def test_reviewed_translation_keeps_arum_in_bereishis_3_1_as_crafty_not_naked(self):
        question = generate_question("translation", pasuk_by_ref(3, 1))

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("analysis_source"), "active_scope_reviewed_bank")
        self.assertEqual(question.get("selected_word"), "עָרוּם")
        self.assertEqual(question.get("correct_answer"), "crafty")
        self.assertNotIn("naked", question.get("choices", []))

    def test_tense_questions_do_not_emit_structurally_weird_answer_banks(self):
        for skill in ("verb_tense", "identify_tense"):
            question = generate_question(skill, pasuk_by_ref(2, 2))

            self.assertNotEqual(question.get("status"), "skipped")
            self.assertEqual(len(question.get("choices", [])), 4)
            self.assertEqual(len(set(question.get("choices", []))), 4)
            self.assertNotIn("not a verb", question.get("choices", []))
            self.assertNotIn("past narrative", question.get("choices", []))
            self.assertNotIn("short future form", question.get("choices", []))

    def test_active_scope_override_records_exist_for_curated_pasuks(self):
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_1_1"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_1_3"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_1_4"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_1_7"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_2_7"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_2_11"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_2_12"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_2_13"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_2_14"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_2_15"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_2_16"))
        self.assertIsNotNone(active_scope_override_for_pasuk_id("bereishis_2_17"))
        self.assertIsNone(active_scope_override_for_pasuk_id("bereishis_99_1"))


if __name__ == "__main__":
    unittest.main()
