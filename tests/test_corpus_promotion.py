import unittest

import assessment_scope
from corpus_promotion import (
    apply_promotion_to_manifest,
    evaluate_next_source_block,
    find_next_source_block,
)
from torah_parser.export_bank import load_source_corpora


class CorpusPromotionTests(unittest.TestCase):
    def test_current_repo_exposes_the_next_review_needed_block_after_3_8_without_promoting_it(self):
        result = evaluate_next_source_block(block_size=10)

        self.assertEqual(result["current_active_scope"], assessment_scope.ACTIVE_ASSESSMENT_SCOPE)
        self.assertEqual(result["status"], "evaluated")
        self.assertFalse(result["promoted"])
        self.assertEqual(result["source_declared_range"], "1:1-3:16")
        self.assertEqual(result["next_block"]["status"], "found")
        self.assertEqual(
            result["next_block"]["range"],
            {
                "start": {"sefer": "Bereishis", "perek": 3, "pasuk": 9},
                "end": {"sefer": "Bereishis", "perek": 3, "pasuk": 16},
            },
        )
        self.assertEqual(
            result["source_actual_range"]["end"],
            {"sefer": "Bereishis", "perek": 3, "pasuk": 16},
        )
        self.assertEqual(result["source_pesukim_count"], 72)
        self.assertEqual(result["evaluation_source"], "existing_staged_bundle")
        self.assertEqual(result["readiness"]["readiness_recommendation"], "active_candidate")
        self.assertEqual(
            result["readiness"]["structural_summary"]["tokens_with_placeholder_context_count"],
            0,
        )
        self.assertEqual(result["readiness"]["generation_summary"]["stable_flow_pesukim"], 8)
        self.assertEqual(result["readiness"]["per_skill_support"]["shoresh"]["supported_pesukim"], 8)
        self.assertEqual(
            result["readiness"]["staged_reviewed_support"]["skill_supported_pesukim"]["phrase_translation"],
            8,
        )
        self.assertEqual(
            result["readiness"]["staged_reviewed_support"]["lane_supported_pesukim"]["role"],
            7,
        )
        self.assertEqual(
            [blocker["code"] for blocker in result["readiness"]["diagnostic_summary"]["blocker_categories"]],
            [],
        )

    def test_active_scope_remains_unchanged_when_the_next_block_is_only_staged(self):
        before = assessment_scope.active_scope_summary()
        result = evaluate_next_source_block(block_size=10)
        after = assessment_scope.active_scope_summary()

        self.assertEqual(result["status"], "evaluated")
        self.assertFalse(result["promoted"])
        self.assertEqual(before["scope"], after["scope"])
        self.assertEqual(before["range"], after["range"])
        self.assertEqual(before["pesukim_count"], after["pesukim_count"])

    def test_combined_source_files_expose_new_contiguous_block_after_bereishis_1_30(self):
        source_corpus = load_source_corpora(
            [
                "data/source/bereishis_1_1_to_1_30.json",
                "data/source/bereishis_1_31_to_2_9.json",
            ]
        )

        result = find_next_source_block(
            source_corpus,
            active_scope={
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 1, "pasuk": 1},
                    "end": {"perek": 1, "pasuk": 30},
                },
            },
            block_size=10,
        )

        self.assertEqual(result["status"], "found")
        self.assertEqual(result["pesukim_count"], 10)
        self.assertEqual(result["range"]["start"], {"sefer": "Bereishis", "perek": 1, "pasuk": 31})
        self.assertEqual(result["range"]["end"], {"sefer": "Bereishis", "perek": 2, "pasuk": 9})

    def test_combined_source_files_expose_next_contiguous_block_after_2_9(self):
        source_corpus = load_source_corpora(
            [
                "data/source/bereishis_1_1_to_1_30.json",
                "data/source/bereishis_1_31_to_2_9.json",
                "data/source/bereishis_2_10_to_2_17.json",
            ]
        )

        result = find_next_source_block(
            source_corpus,
            active_scope={
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 1, "pasuk": 1},
                    "end": {"perek": 2, "pasuk": 9},
                },
            },
            block_size=10,
        )

        self.assertEqual(result["status"], "found")
        self.assertEqual(result["pesukim_count"], 8)
        self.assertEqual(result["range"]["start"], {"sefer": "Bereishis", "perek": 2, "pasuk": 10})
        self.assertEqual(result["range"]["end"], {"sefer": "Bereishis", "perek": 2, "pasuk": 17})

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

    def test_review_needed_chunk_is_not_promoted_automatically(self):
        manifest = {
            "source_corpora": [{"corpus_id": "source_demo", "status": "source"}],
            "parsed_corpora": [{"corpus_id": "parsed_demo", "status": "review_needed"}],
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
                "readiness_recommendation": "review_needed",
            },
        }

        with self.assertRaisesRegex(ValueError, "not an active_candidate"):
            apply_promotion_to_manifest(manifest, evaluation)


if __name__ == "__main__":
    unittest.main()
