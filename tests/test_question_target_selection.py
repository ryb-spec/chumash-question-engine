import unittest

from assessment_scope import (
    active_pasuk_text_set,
    active_pasuk_texts,
)
from pasuk_flow_generator import generate_question


TARGETED_SKILLS = [
    "translation",
    "part_of_speech",
    "verb_tense",
    "shoresh",
    "subject_identification",
    "object_identification",
    "phrase_translation",
]


class QuestionTargetSelectionTests(unittest.TestCase):
    def test_generated_targets_come_from_current_pasuk(self):
        for pasuk in active_pasuk_texts():
            pasuk_tokens = pasuk.split()
            for skill in TARGETED_SKILLS:
                question = generate_question(skill, pasuk)
                if question.get("status") == "skipped":
                    continue

                self.assertEqual(question.get("pasuk"), pasuk)
                selected = question.get("selected_word") or question.get("word")
                self.assertIsNotNone(selected, f"Missing target for {skill} in {pasuk!r}")
                for token in selected.split():
                    self.assertIn(
                        token,
                        pasuk_tokens,
                        f"{skill} targeted {selected!r} outside the current pasuk",
                    )

    def test_generate_question_from_active_pool_stays_in_active_dataset(self):
        pasuk_pool = list(active_pasuk_texts())

        for skill in ("translation", "verb_tense", "subject_identification"):
            question = generate_question(skill, pasuk_pool)
            self.assertNotEqual(question.get("status"), "skipped")
            self.assertIn(question.get("pasuk"), active_pasuk_text_set())


if __name__ == "__main__":
    unittest.main()
