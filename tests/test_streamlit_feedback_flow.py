import unittest

from question_ui import build_feedback_context, build_learning_context


class StreamlitFeedbackFlowTests(unittest.TestCase):
    def test_learning_context_for_learn_mode_is_clear_and_guided(self):
        context = build_learning_context(
            practice_type="Learn Mode",
            skill_label="Word Meaning",
            current_skill_label="Word Meaning",
            next_skill_label="Verb Tense",
            source_label="Bereishis 1:3",
            focus_tip="Look at the strongest clue before you guess.",
        )

        self.assertIn("currently working on word meaning", context["why_this_question"].lower())
        self.assertIn("verb tense", context["what_happens_next"].lower())
        self.assertIn("strongest clue", context["what_to_focus_on"].lower())

    def test_feedback_context_for_incorrect_answer_includes_confusion_and_next_step(self):
        question = {
            "question_type": "verb_tense",
            "skill": "verb_tense",
            "correct_answer": "vav_consecutive_past",
            "explanation": "The form is read as vav_consecutive_past here.",
        }
        feedback = build_feedback_context(
            question=question,
            selected_answer="future",
            is_correct=False,
            clue_text="The verb form points to narrative past here.",
            practice_type="Learn Mode",
            skill_label="Verb Tense",
            next_skill_label="Subject Identification",
        )

        self.assertEqual(feedback["title"], "Incorrect")
        self.assertIn("verb form", feedback["clue_that_mattered"].lower())
        self.assertTrue(feedback["likely_confusion"])
        self.assertIn("one more verb tense item", feedback["what_comes_next"].lower())
        self.assertEqual(feedback["followup"]["route"], "retry_similar")


if __name__ == "__main__":
    unittest.main()
