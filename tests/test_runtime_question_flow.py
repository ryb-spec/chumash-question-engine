import unittest

from runtime.question_flow import (
    candidate_quality_breakdown,
    display_context_policy,
    question_signature,
    recent_question_repeat_reason,
)


class RuntimeQuestionFlowTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
