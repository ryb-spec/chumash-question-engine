import unittest

from pasuk_flow_generator import generate_question
from torah_parser.disambiguate import annotate_role_layer


class RoleLayerTests(unittest.TestCase):
    def test_single_verb_clause_resolves_main_verb_and_subject(self):
        analyzed = [
            {
                "token": "וַיֹּאמֶר",
                "entry": {
                    "word": "וַיֹּאמֶר",
                    "translation": "said",
                    "type": "verb",
                    "part_of_speech": "verb",
                    "semantic_group": "action",
                    "role_hint": "unknown",
                    "entity_type": "verb",
                },
            },
            {
                "token": "אֱלֹהִים",
                "entry": {
                    "word": "אֱלֹהִים",
                    "translation": "God",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "divine",
                    "role_hint": "subject_candidate",
                    "entity_type": "divine_being",
                },
            },
        ]

        annotated, layer = annotate_role_layer(analyzed)

        self.assertEqual(layer["status"], "resolved")
        self.assertEqual(layer["main_verb_index"], 0)
        self.assertEqual(layer["subject_index"], 1)
        self.assertEqual(annotated[0]["role_data"]["clause_role"], "verb")
        self.assertEqual(annotated[1]["role_data"]["clause_role"], "subject")

    def test_role_layer_distinguishes_direct_object_and_recipient(self):
        analyzed = [
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
            {
                "token": "לְאַהֲרֹן",
                "entry": {
                    "word": "לְאַהֲרֹן",
                    "translation": "Aharon",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "person",
                    "role_hint": "subject_candidate",
                    "entity_type": "person",
                    "prefix": "ל",
                },
            },
        ]

        annotated, layer = annotate_role_layer(analyzed)

        self.assertEqual(layer["status"], "resolved")
        self.assertEqual(layer["subject_index"], 1)
        self.assertEqual(layer["direct_object_index"], 3)
        self.assertEqual(layer["recipient_index"], 4)
        self.assertEqual(annotated[3]["role_data"]["clause_role"], "direct_object")
        self.assertEqual(annotated[4]["role_data"]["clause_role"], "recipient")
        self.assertEqual(
            [(phrase["phrase_role"], phrase["text"]) for phrase in layer["prepositional_phrases"]],
            [("recipient", "לְאַהֲרֹן")],
        )

        question = generate_question(
            "object_identification",
            "וַיִּתֵּן מֹשֶׁה אֶת סֵפֶר לְאַהֲרֹן",
            analyzed_override=analyzed,
        )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("role_focus"), "recipient")
        self.assertEqual(question.get("action_token"), "וַיִּתֵּן")
        self.assertEqual(question.get("correct_answer"), "Aharon")
        self.assertEqual(question.get("question"), "Who receives the action in וַיִּתֵּן?")

    def test_role_layer_extracts_source_and_destination_phrases_for_phrase_questions(self):
        analyzed = [
            {
                "token": "וַיֵּלֶךְ",
                "entry": {
                    "word": "וַיֵּלֶךְ",
                    "translation": "and went",
                    "type": "verb",
                    "part_of_speech": "verb",
                    "semantic_group": "action",
                    "role_hint": "unknown",
                    "entity_type": "verb",
                },
            },
            {
                "token": "אַבְרָם",
                "entry": {
                    "word": "אַבְרָם",
                    "translation": "Avram",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "person",
                    "role_hint": "subject_candidate",
                    "entity_type": "person",
                },
            },
            {
                "token": "מֵאֶרֶץ",
                "entry": {
                    "word": "מֵאֶרֶץ",
                    "translation": "land",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "place",
                    "role_hint": "unknown",
                    "entity_type": "common_noun",
                    "prefix": "מ",
                },
            },
            {
                "token": "לָעִיר",
                "entry": {
                    "word": "לָעִיר",
                    "translation": "city",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "place",
                    "role_hint": "unknown",
                    "entity_type": "common_noun",
                    "prefix": "ל",
                },
            },
        ]

        _, layer = annotate_role_layer(analyzed)

        self.assertEqual(
            [(phrase["phrase_role"], phrase["text"]) for phrase in layer["prepositional_phrases"]],
            [("source", "מֵאֶרֶץ"), ("destination", "לָעִיר")],
        )

        question = generate_question(
            "phrase_translation",
            "וַיֵּלֶךְ אַבְרָם מֵאֶרֶץ לָעִיר",
            analyzed_override=analyzed,
        )

        self.assertNotEqual(question.get("status"), "skipped")
        self.assertEqual(question.get("selected_word"), "מֵאֶרֶץ לָעִיר")
        self.assertEqual(question.get("correct_answer"), "from land to city")

    def test_ambiguous_multiple_verbs_skip_role_backed_questions(self):
        analyzed = [
            {
                "token": "וַיֹּאמֶר",
                "entry": {
                    "word": "וַיֹּאמֶר",
                    "translation": "said",
                    "type": "verb",
                    "part_of_speech": "verb",
                    "semantic_group": "action",
                    "role_hint": "unknown",
                    "entity_type": "verb",
                },
            },
            {
                "token": "אֱלֹהִים",
                "entry": {
                    "word": "אֱלֹהִים",
                    "translation": "God",
                    "type": "noun",
                    "part_of_speech": "noun",
                    "semantic_group": "divine",
                    "role_hint": "subject_candidate",
                    "entity_type": "divine_being",
                },
            },
            {
                "token": "וַיַּעַשׂ",
                "entry": {
                    "word": "וַיַּעַשׂ",
                    "translation": "and made",
                    "type": "verb",
                    "part_of_speech": "verb",
                    "semantic_group": "action",
                    "role_hint": "unknown",
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
                    "role_hint": "object_candidate",
                    "entity_type": "common_noun",
                },
            },
        ]

        _, layer = annotate_role_layer(analyzed)
        self.assertEqual(layer["status"], "ambiguous_main_verbs")

        question = generate_question(
            "subject_identification",
            "וַיֹּאמֶר אֱלֹהִים וַיַּעַשׂ אוֹר",
            analyzed_override=analyzed,
        )

        self.assertEqual(question.get("status"), "skipped")
        self.assertIn("action anchor", question.get("reason", "").lower())

        phrase_question = generate_question(
            "phrase_translation",
            "וַיֹּאמֶר אֱלֹהִים וַיַּעַשׂ אוֹר",
            analyzed_override=analyzed,
        )

        self.assertEqual(phrase_question.get("status"), "skipped")
        self.assertEqual(
            phrase_question.get("reason"),
            "No quiz-ready phrase target found in this pasuk.",
        )


if __name__ == "__main__":
    unittest.main()
