import unittest

import assessment_scope
from corpus_promotion import (
    apply_promotion_to_manifest,
    evaluate_next_source_block,
)


class CorpusPromotionTests(unittest.TestCase):
    def test_current_repo_has_no_next_contiguous_block_after_active_scope(self):
        result = evaluate_next_source_block(block_size=10)

        self.assertEqual(result["current_active_scope"], assessment_scope.ACTIVE_ASSESSMENT_SCOPE)
        self.assertEqual(result["status"], "no_next_block")
        self.assertFalse(result["promoted"])
        self.assertIn("does not contain a contiguous block", result["reason"])

    def test_active_scope_remains_unchanged_when_no_promotion_occurs(self):
        before = assessment_scope.active_scope_summary()
        result = evaluate_next_source_block(block_size=10)
        after = assessment_scope.active_scope_summary()

        self.assertEqual(result["status"], "no_next_block")
        self.assertEqual(before["scope"], after["scope"])
        self.assertEqual(before["range"], after["range"])
        self.assertEqual(before["pesukim_count"], after["pesukim_count"])

    def test_manifest_active_scope_updates_correctly_if_promotion_is_applied(self):
        manifest = {
            "source_corpora": [
                {
                    "corpus_id": "source_demo",
                    "range": {"start": {"perek": 1, "pasuk": 1}, "end": {"perek": 1, "pasuk": 20}},
                    "pesukim_count": 20,
                }
            ],
            "parsed_corpora": [
                {
                    "corpus_id": "parsed_demo",
                    "range": {"start": {"perek": 1, "pasuk": 1}, "end": {"perek": 1, "pasuk": 20}},
                    "pesukim_count": 20,
                    "status": "active_candidate",
                }
            ],
            "scopes": [
                {
                    "scope_id": "local_parsed_bereishis_1_1_to_1_20",
                    "sefer": "Bereishis",
                    "range": {"start": {"perek": 1, "pasuk": 1}, "end": {"perek": 1, "pasuk": 20}},
                    "pesukim_count": 20,
                    "status": "active",
                    "supported_runtime": True,
                    "source_corpus_id": "source_demo",
                    "parsed_corpus_id": "parsed_demo",
                }
            ],
        }
        evaluation = {
            "next_block": {
                "range": {
                    "start": {"sefer": "Bereishis", "perek": 1, "pasuk": 21},
                    "end": {"sefer": "Bereishis", "perek": 1, "pasuk": 30},
                },
                "pesukim_count": 10,
            },
            "readiness": {
                "readiness_recommendation": "active_candidate",
            },
        }

        updated = apply_promotion_to_manifest(manifest, evaluation)
        active_scope = updated["scopes"][0]

        self.assertEqual(active_scope["scope_id"], "local_parsed_bereishis_1_1_to_1_30")
        self.assertEqual(active_scope["range"]["end"], {"perek": 1, "pasuk": 30})
        self.assertEqual(active_scope["pesukim_count"], 30)
        self.assertEqual(updated["parsed_corpora"][0]["status"], "active")


if __name__ == "__main__":
    unittest.main()
