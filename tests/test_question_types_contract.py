import unittest

from assessment_scope import active_pesukim_records
from pasuk_flow_generator import (
    CONTROLLED_TENSE_CHOICES,
    analyze_pasuk,
    generate_pasuk_flow,
    generate_question,
    load_word_bank,
)


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

    def test_subject_identification_uses_semantic_fields(self):
        pasuk = pasuk_by_ref(1, 1)
        question = generate_question("subject_identification", pasuk)
        self.assertNotEqual(question.get("status"), "skipped")

        analyzed = analyze_pasuk(pasuk, self.word_bank)
        subject_item = next(
            item for item in analyzed if item["token"] == question["selected_word"]
        )

        self.assertEqual(subject_item["entry"].get("group"), "unknown")
        self.assertEqual(subject_item["entry"].get("semantic_group"), "divine")
        self.assertEqual(subject_item["entry"].get("role_hint"), "subject_candidate")

    def test_verb_tense_choices_follow_runtime_labels(self):
        allowed = set(CONTROLLED_TENSE_CHOICES) | {"not a verb"}

        for ref in ((1, 3), (1, 9), (1, 14), (1, 17)):
            pasuk = pasuk_by_ref(*ref)
            question = generate_question("verb_tense", pasuk)
            if question.get("status") == "skipped":
                continue
            self.assertIn(question["correct_answer"], allowed)
            self.assertTrue(set(question["choices"]).issubset(allowed))

    def test_unsupported_skill_returns_structured_skip(self):
        pasuk = pasuk_by_ref(1, 13)
        question = generate_question("subject_identification", pasuk)

        self.assertEqual(question.get("status"), "skipped")
        self.assertFalse(question.get("supported"))
        self.assertEqual(question.get("skill"), "subject_identification")
        self.assertEqual(question.get("pasuk"), pasuk)
        self.assertIn("subject", question.get("reason", "").lower())
        self.assertIsNone(question.get("selected_word"))

    def test_flow_generation_stays_valid_when_skill_is_skipped(self):
        pasuk = pasuk_by_ref(1, 13)
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


if __name__ == "__main__":
    unittest.main()
