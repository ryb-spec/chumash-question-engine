import unittest

from assessment_scope import active_pesukim_records
from engine import flow_builder
from engine.morphology_labels import classify_tense_form
from pasuk_flow_generator import analyze_pasuk as runtime_analyze_pasuk, generate_question


def pasuk_by_ref(perek, pasuk):
    for record in active_pesukim_records():
        ref = record.get("ref", {})
        if ref.get("perek") == perek and ref.get("pasuk") == pasuk:
            return record["text"]
    raise AssertionError(f"Missing active pasuk {perek}:{pasuk}")


def analyzed_override_for_token(perek, pasuk, token):
    pasuk_text = pasuk_by_ref(perek, pasuk)
    analyzed = flow_builder.analyze_pasuk(pasuk_text, {})
    target_key = flow_builder.normalize_hebrew_key(token)
    for item in analyzed:
        if flow_builder.normalize_hebrew_key(item.get("token")) == target_key:
            return pasuk_text, [{"token": item["token"], "entry": item["entry"]}]
    raise AssertionError(f"Missing analyzed token {token} in {perek}:{pasuk}")


def runtime_analysis_entry_for_token(perek, pasuk, token):
    pasuk_text = pasuk_by_ref(perek, pasuk)
    target_key = flow_builder.normalize_hebrew_key(token)
    for item in runtime_analyze_pasuk(pasuk_text):
        item_token = item.get("word") or item.get("token") or item.get("surface")
        if flow_builder.normalize_hebrew_key(item_token) != target_key:
            continue
        analyses = list(item.get("analyses") or [])
        for analysis in analyses:
            if analysis.get("confidence") != "generated_alternate":
                return analysis
        if analyses:
            return analyses[0]
    raise AssertionError(f"Missing runtime analysis token {token} in {perek}:{pasuk}")


class TenseMorphologyQuestionTests(unittest.TestCase):
    def test_classify_tense_form_marks_vihi_as_future_style_with_conjunction(self):
        details = classify_tense_form("future_jussive", token="וִיהִי")

        self.assertEqual(details["raw_code"], "future_jussive")
        self.assertEqual(details["displayed_label"], "future")
        self.assertEqual(details["base_conjugation"], "imperfect")
        self.assertEqual(details["vav_prefix_type"], "conjunction")
        self.assertEqual(details["display_phrase"], "a future-style form")
        self.assertIn("future", details["accepted_answer_aliases"])
        self.assertIn("future_jussive", details["accepted_answer_aliases"])

    def test_classify_tense_form_keeps_converted_imperfect_past_style(self):
        details = classify_tense_form("vav_consecutive_past", token="וַיֹּאמֶר")

        self.assertEqual(details["displayed_label"], "past")
        self.assertEqual(details["base_conjugation"], "converted_imperfect")
        self.assertEqual(details["vav_prefix_type"], "consecutive")
        self.assertEqual(details["display_phrase"], "a past-style form")

    def test_classify_tense_form_leaves_plain_future_without_vav_unchanged(self):
        details = classify_tense_form("future", token="תֵרָאֶה")

        self.assertEqual(details["displayed_label"], "future")
        self.assertEqual(details["base_conjugation"], "imperfect")
        self.assertEqual(details["vav_prefix_type"], "")
        self.assertEqual(details["display_phrase"], "the future form")

    def test_bereishis_1_6_identify_tense_uses_future_style_copy_for_vihi(self):
        question = generate_question("identify_tense", pasuk_by_ref(1, 6))

        self.assertEqual(question.get("selected_word"), "וִיהִי")
        self.assertEqual(question.get("question"), "What tense or verb form is this word?")
        self.assertNotEqual(question.get("question"), "What form is shown?")
        self.assertEqual(question.get("correct_answer"), "future")
        self.assertEqual(question.get("tense_code"), "future_jussive")
        self.assertEqual(question.get("word_gloss"), "and let it be")
        self.assertEqual(question.get("base_conjugation"), "imperfect")
        self.assertEqual(question.get("vav_prefix_type"), "conjunction")
        self.assertIn("future", question.get("accepted_answer_aliases", []))
        self.assertIn("future_jussive", question.get("accepted_answer_aliases", []))
        self.assertIn("future-style form", question.get("explanation", ""))
        self.assertIn(question.get("correct_answer"), question.get("choices", []))

    def test_bereishis_1_9_identify_tense_uses_future_style_copy_for_veteraeh(self):
        pasuk, analyzed_override = analyzed_override_for_token(1, 9, "וְתֵרָאֶה")
        question = generate_question("identify_tense", pasuk, analyzed_override=analyzed_override)

        self.assertEqual(question.get("selected_word"), "וְתֵרָאֶה")
        self.assertEqual(question.get("correct_answer"), "future")
        self.assertEqual(question.get("tense_code"), "future_jussive")
        self.assertEqual(question.get("word_gloss"), "and let it appear")
        self.assertEqual(question.get("base_conjugation"), "imperfect")
        self.assertEqual(question.get("vav_prefix_type"), "conjunction")
        self.assertIn("future-style form", question.get("explanation", ""))
        self.assertIn(question.get("correct_answer"), question.get("choices", []))

    def test_bereishis_1_3_identify_tense_keeps_vayehi_as_past_style(self):
        pasuk, analyzed_override = analyzed_override_for_token(1, 3, "וַיְהִי")
        question = generate_question("identify_tense", pasuk, analyzed_override=analyzed_override)

        self.assertEqual(question.get("selected_word"), "וַיְהִי")
        self.assertEqual(question.get("correct_answer"), "past")
        self.assertEqual(question.get("tense_code"), "vav_consecutive_past")
        self.assertEqual(question.get("word_gloss"), "and there was")
        self.assertEqual(question.get("base_conjugation"), "converted_imperfect")
        self.assertEqual(question.get("vav_prefix_type"), "consecutive")
        self.assertIn("past-style form", question.get("explanation", ""))

    def test_identify_tense_keeps_plain_future_question_unchanged_without_vav(self):
        analyzed_override = [
            {
                "token": "תֵרָאֶה",
                "entry": {
                    "word": "תֵרָאֶה",
                    "translation": "it will appear",
                    "translation_literal": "it will appear",
                    "translation_context": "it will appear",
                    "type": "verb",
                    "part_of_speech": "verb",
                    "confidence": "reviewed",
                    "tense": "future",
                    "shoresh": "ראה",
                    "semantic_group": "action",
                    "entity_type": "verb",
                },
            }
        ]

        question = generate_question("identify_tense", "תֵרָאֶה", analyzed_override=analyzed_override)

        self.assertEqual(question.get("selected_word"), "תֵרָאֶה")
        self.assertEqual(question.get("correct_answer"), "future")
        self.assertEqual(question.get("tense_code"), "future")
        self.assertFalse(question.get("vav_prefix_type"))
        self.assertIn("the future form", question.get("explanation", ""))
        self.assertNotIn("future-style form", question.get("explanation", ""))

    def test_runtime_analysis_supports_backfilled_infinitive_token(self):
        entry = runtime_analysis_entry_for_token(2, 4, "עֲשׂוֹת")

        self.assertEqual(entry.get("part_of_speech"), "verb")
        self.assertEqual(entry.get("shoresh"), "עשה")
        self.assertEqual(entry.get("tense"), "infinitive")

    def test_runtime_analysis_supports_backfilled_vayikach_token(self):
        entry = runtime_analysis_entry_for_token(2, 21, "וַיִּקַּח")

        self.assertEqual(entry.get("part_of_speech"), "verb")
        self.assertEqual(entry.get("shoresh"), "לקח")
        self.assertEqual(entry.get("tense"), "vav_consecutive_past")


if __name__ == "__main__":
    unittest.main()
