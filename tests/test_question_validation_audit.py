import unittest

import question_validation_audit


class QuestionValidationAuditTests(unittest.TestCase):
    def test_active_scope_summary_reflects_expanded_runtime_boundary(self):
        report = question_validation_audit.build_question_validation_audit()

        self.assertEqual(report["scope_summary"]["scope"], "local_parsed_bereishis_1_1_to_3_8")
        self.assertEqual(report["scope_summary"]["range"]["end"], {"perek": 3, "pasuk": 8})
        self.assertEqual(report["scope_summary"]["pesukim_count"], 64)

    def test_contextual_meaning_validator_rejects_placeholder_translation(self):
        result = question_validation_audit.contextual_meaning_validation_result(
            "מינים",
            {
                "type": "noun",
                "part_of_speech": "noun",
                "translation": "מינים",
                "confidence": "reviewed",
            },
        )

        self.assertFalse(result["valid"])
        self.assertIn("placeholder_translation", result["reason_codes"])

    def test_summarize_skill_rows_counts_rejections_and_no_safe_refs(self):
        rows = [
            {
                "ref": "Bereishis 1:1",
                "token": "ולמראה",
                "valid": False,
                "reason_codes": ["multiple_prefixes"],
                "details": {},
            },
            {
                "ref": "Bereishis 1:2",
                "token": "זרעו",
                "valid": True,
                "reason_codes": [],
                "details": {},
            },
            {
                "ref": "Bereishis 1:2",
                "token": "למינו",
                "valid": False,
                "reason_codes": ["multiple_prefixes", "compound_morphology"],
                "details": {},
            },
        ]

        summary = question_validation_audit.summarize_skill_rows(
            "prefix",
            "Prefix",
            rows,
            ["Bereishis 1:1", "Bereishis 1:2", "Bereishis 1:3"],
        )

        self.assertEqual(summary["total_candidates_seen"], 3)
        self.assertEqual(summary["valid_candidates"], 1)
        self.assertEqual(summary["invalid_candidates"], 2)
        self.assertEqual(summary["valid_percent"], 33.3)
        self.assertEqual(summary["invalid_by_reason"][0], {"reason": "multiple_prefixes", "count": 2})
        self.assertIn({"form": "ולמראה", "count": 1}, summary["most_common_blocked_forms"])
        self.assertEqual(
            summary["pesukim_with_no_safe_candidate_paths"],
            ["Bereishis 1:1", "Bereishis 1:3"],
        )

    def test_render_markdown_includes_core_sections(self):
        report = {
            "scope_summary": {
                "scope": "local_scope",
                "sefer": "Bereishis",
                "range": {
                    "start": {"perek": 1, "pasuk": 1},
                    "end": {"perek": 1, "pasuk": 30},
                },
                "pesukim_count": 30,
            },
            "analysis_errors": [],
            "overall": {
                "top_rejection_reasons": [{"reason": "multiple_prefixes", "count": 4}],
                "most_common_blocked_forms": [{"form": "ולמראה", "count": 3}],
            },
            "skills": [
                {
                    "title": "Prefix",
                    "total_candidates_seen": 10,
                    "valid_candidates": 6,
                    "invalid_candidates": 4,
                    "valid_percent": 60.0,
                    "invalid_by_reason": [{"reason": "multiple_prefixes", "count": 4}],
                    "most_common_blocked_forms": [{"form": "ולמראה", "count": 3}],
                    "pesukim_with_no_safe_candidate_paths": ["Bereishis 1:4"],
                    "sample_pesukim_with_no_safe_candidate_paths": ["Bereishis 1:4"],
                }
            ],
        }

        markdown = question_validation_audit.render_question_validation_markdown(report)

        self.assertIn("# Question Validation Audit", markdown)
        self.assertIn("## Coverage Snapshot", markdown)
        self.assertIn("## Top Rejection Reasons", markdown)
        self.assertIn("## Prefix", markdown)
        self.assertIn("### Pesukim With No Safe Candidate Paths", markdown)


if __name__ == "__main__":
    unittest.main()
