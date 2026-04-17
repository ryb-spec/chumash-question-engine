import unittest

from adaptive_engine import evaluate_skill_progression


class AdaptiveSkillSelectionTests(unittest.TestCase):
    def test_clustered_errors_trigger_reteach_route(self):
        decision = evaluate_skill_progression(
            current_skill="identify_prefix_meaning",
            answered_skill="identify_prefix_meaning",
            skill_state={
                "score": 48,
                "current_streak": 0,
                "challenge_streak": 0,
                "mastered": False,
                "last_12_results": [True, False, False, False],
                "error_counts": {"prefix_error": 2},
            },
            is_correct=False,
            skill_order=[
                "identify_prefix_meaning",
                "identify_suffix_meaning",
                "identify_pronoun_suffix",
            ],
            skill_label="How words are built",
            next_skill_label="How words are built",
        )

        self.assertEqual(decision["route"], "reteach_same_skill")
        self.assertEqual(decision["target_skill"], "identify_prefix_meaning")
        self.assertEqual(decision["selection_mode"], "reteach")

    def test_mastered_skill_advances_normally(self):
        decision = evaluate_skill_progression(
            current_skill="identify_prefix_meaning",
            answered_skill="identify_prefix_meaning",
            skill_state={
                "score": 95,
                "current_streak": 5,
                "challenge_streak": 3,
                "mastered": True,
                "last_12_results": [True] * 12,
                "error_counts": {},
            },
            is_correct=True,
            skill_order=[
                "identify_prefix_meaning",
                "identify_suffix_meaning",
                "identify_pronoun_suffix",
            ],
            skill_label="How words are built",
            next_skill_label="How words are built",
        )

        self.assertEqual(decision["route"], "advance")
        self.assertEqual(decision["target_skill"], "identify_suffix_meaning")


if __name__ == "__main__":
    unittest.main()
