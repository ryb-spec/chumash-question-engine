import unittest

import assessment_scope
from corpus_metrics import evaluate_staged_corpus_readiness
from torah_parser.export_bank import build_parsed_corpus_artifacts


WEAK_SOURCE_CORPUS = {
    "metadata": {
        "title": "Weak Sample Source",
        "range": "1:1-1:1",
        "format": "sefer,perek,pasuk,text",
    },
    "pesukim": [
        {
            "sefer": "Bereishis",
            "perek": 1,
            "pasuk": 1,
            "text": "אֵת אֵת אֵת",
        }
    ],
}


class CorpusReadinessTests(unittest.TestCase):
    def test_weak_staged_chunks_are_not_recommended_as_active_candidates(self):
        bundle = build_parsed_corpus_artifacts(
            WEAK_SOURCE_CORPUS,
            corpus_id="weak_chunk",
            status="parsed",
        )

        metrics = evaluate_staged_corpus_readiness(bundle)

        self.assertEqual(metrics["generation_summary"]["stable_flow_pesukim"], 0)
        self.assertNotEqual(metrics["readiness_recommendation"], "active_candidate")
        self.assertIn(metrics["readiness_recommendation"], {"not_ready", "review_needed"})

    def test_readiness_evaluation_does_not_change_active_runtime_scope(self):
        original_scope = assessment_scope.ACTIVE_ASSESSMENT_SCOPE
        original_contract = assessment_scope.active_runtime_contract()
        bundle = build_parsed_corpus_artifacts(
            WEAK_SOURCE_CORPUS,
            corpus_id="weak_chunk",
            status="parsed",
        )

        metrics = evaluate_staged_corpus_readiness(bundle)

        self.assertEqual(assessment_scope.ACTIVE_ASSESSMENT_SCOPE, original_scope)
        self.assertEqual(
            assessment_scope.active_runtime_contract()["active_scope"],
            original_contract["active_scope"],
        )
        self.assertEqual(
            metrics["scope_under_evaluation"]["active_runtime_scope_unchanged"],
            original_scope,
        )
        self.assertEqual(metrics["scope_under_evaluation"]["bundle_status"], "staged")


if __name__ == "__main__":
    unittest.main()
