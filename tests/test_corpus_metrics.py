import unittest

from corpus_metrics import EVALUATED_SKILLS, evaluate_staged_corpus_readiness
from torah_parser.export_bank import build_parsed_corpus_artifacts


SAMPLE_SOURCE_CORPUS = {
    "metadata": {
        "title": "Sample Bereishis Source",
        "range": "1:1-1:3",
        "format": "sefer,perek,pasuk,text",
    },
    "pesukim": [
        {
            "sefer": "Bereishis",
            "perek": 1,
            "pasuk": 1,
            "text": "בְּרֵאשִׁית בָּרָא אֱלֹקִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ",
        },
        {
            "sefer": "Bereishis",
            "perek": 1,
            "pasuk": 2,
            "text": "וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ וְחֹשֶׁךְ עַל פְּנֵי תְהוֹם",
        },
        {
            "sefer": "Bereishis",
            "perek": 1,
            "pasuk": 3,
            "text": "וַיֹּאמֶר אֱלֹקִים יְהִי אוֹר וַיְהִי אוֹר",
        },
    ],
}


class CorpusMetricsTests(unittest.TestCase):
    def test_readiness_metrics_compute_on_representative_staged_sample(self):
        bundle = build_parsed_corpus_artifacts(
            SAMPLE_SOURCE_CORPUS,
            corpus_id="sample_bereishis_metrics",
            status="parsed",
        )

        metrics = evaluate_staged_corpus_readiness(bundle)

        self.assertEqual(metrics["structural_summary"]["pesukim_count"], 3)
        self.assertGreater(metrics["structural_summary"]["token_count"], 0)
        self.assertIn(metrics["readiness_recommendation"], {"not_ready", "review_needed", "active_candidate"})
        self.assertEqual(metrics["scope_under_evaluation"]["sefer"], "Bereishis")
        self.assertEqual(metrics["scope_under_evaluation"]["bundle_status"], "staged")
        self.assertEqual(
            metrics["lifecycle"]["promotion_gate"],
            "only active_candidate bundles may be promoted into the active runtime",
        )

    def test_per_skill_support_metrics_behave_sensibly_on_sample_bundle(self):
        bundle = build_parsed_corpus_artifacts(SAMPLE_SOURCE_CORPUS)
        metrics = evaluate_staged_corpus_readiness(bundle)

        self.assertEqual(set(metrics["per_skill_support"].keys()), set(EVALUATED_SKILLS))
        self.assertGreaterEqual(metrics["per_skill_support"]["translation"]["supported_pesukim"], 0)
        self.assertGreaterEqual(metrics["per_skill_support"]["verb_tense"]["support_rate"], 0.0)
        self.assertLessEqual(metrics["per_skill_support"]["translation"]["support_rate"], 1.0)
        self.assertLessEqual(metrics["per_skill_support"]["verb_tense"]["support_rate"], 1.0)
        self.assertGreaterEqual(metrics["per_skill_support"]["shoresh"]["support_rate"], 0.0)
        self.assertLessEqual(metrics["per_skill_support"]["shoresh"]["support_rate"], 1.0)
        self.assertFalse(metrics["staged_reviewed_support"]["available"])


if __name__ == "__main__":
    unittest.main()
