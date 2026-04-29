from __future__ import annotations

import json
import unittest
from pathlib import Path

import scripts.validate_protected_preview_input_list_planning_policy as validator


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "data" / "question_eligibility_audits"
DOC_POLICY_PATH = ROOT / "docs" / "question_templates" / "perek_1_protected_preview_input_list_planning_policy.md"
JSON_POLICY_PATH = AUDIT_DIR / "protected_preview_input_list_planning_policy.v1.json"
REPORT_PATH = AUDIT_DIR / "reports" / "perek_1_protected_preview_input_list_planning_policy_report.md"
YOSSI_PACKET_PATH = AUDIT_DIR / "reports" / "perek_1_protected_preview_input_list_planning_policy_yossi_review_packet.md"
APPLIED_REPORT_PATH = AUDIT_DIR / "reports" / "perek_1_protected_preview_input_list_planning_policy_yossi_review_applied.md"
README_PATH = AUDIT_DIR / "README.md"


class ProtectedPreviewInputListPlanningPolicyTests(unittest.TestCase):
    def load_policy(self):
        with JSON_POLICY_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def test_validator_passes(self):
        summary = validator.validate_protected_preview_input_list_planning_policy()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["actual_input_row_count"], 0)
        self.assertEqual(summary["batch_balance_required_field_count"], 7)

    def test_artifacts_exist(self):
        self.assertTrue(DOC_POLICY_PATH.exists())
        self.assertTrue(JSON_POLICY_PATH.exists())
        self.assertTrue(REPORT_PATH.exists())
        self.assertTrue(YOSSI_PACKET_PATH.exists())
        self.assertTrue(APPLIED_REPORT_PATH.exists())

    def test_json_status_and_families(self):
        policy = self.load_policy()
        self.assertEqual(policy["status"], "planning_policy_only")
        self.assertEqual(policy["planning_policy_review_status"], "yossi_approved_with_revision")
        self.assertEqual(policy["review_decision"], "approve_with_revision")
        self.assertTrue(policy["future_input_list_planning_may_proceed"])
        self.assertEqual(set(policy["allowed_families"]), validator.ALLOWED_FAMILIES)
        self.assertIn("basic_verb_form_recognition", policy["deferred_families"])
        self.assertIn("basic_verb_form_recognition", policy["excluded_families"])

    def test_batch_balance_table_is_required(self):
        policy = self.load_policy()
        self.assertTrue(policy["batch_balance_table_required"])
        self.assertTrue(validator.REQUIRED_BATCH_BALANCE_FIELDS.issubset(set(policy["batch_balance_required_fields"])))
        self.assertIn("count by family", policy["review_notes"])
        self.assertIn("direct-object-marker", policy["review_notes"])
        self.assertIn("shoresh", policy["review_notes"])

    def test_required_future_input_fields_exist(self):
        policy = self.load_policy()
        self.assertTrue(validator.REQUIRED_FUTURE_FIELDS.issubset(set(policy["required_future_input_fields"])))

    def test_no_actual_input_list_rows_or_question_payloads_exist(self):
        policy = self.load_policy()
        self.assertEqual(policy["actual_input_rows"], [])
        self.assertIn("actual_questions", policy["forbidden_outputs"])
        self.assertIn("answer_choices", policy["forbidden_outputs"])
        self.assertIn("answer_keys", policy["forbidden_outputs"])
        list_files = [
            path
            for path in AUDIT_DIR.rglob("*")
            if path.is_file()
            and "planning_policy" not in path.name
            and "protected_preview_input_list" in path.name
            and path.suffix.lower() in {".tsv", ".csv", ".json", ".jsonl"}
        ]
        self.assertEqual(list_files, [])

    def test_first_batch_rules_exist(self):
        policy = self.load_policy()
        rules = policy["first_batch_balance_rules"]
        self.assertEqual(rules["total_suggested_size"], "20-30")
        self.assertEqual(rules["prioritize_risk_level"], "low")
        self.assertIn("basic_verb_form_recognition", rules["exclude_families"])

    def test_safety_gates_remain_closed(self):
        policy = self.load_policy()
        defaults = policy["default_future_input_statuses"]
        self.assertEqual(defaults["teacher_wording_review_status"], "needs_review")
        self.assertEqual(defaults["protected_preview_candidate_status"], "planning_only")
        self.assertFalse(defaults["protected_preview_allowed"])
        self.assertFalse(defaults["reviewed_bank_allowed"])
        self.assertFalse(defaults["runtime_allowed"])
        self.assertFalse(defaults["student_facing_allowed"])

    def test_yossi_packet_exists_and_readme_links_are_present(self):
        packet = YOSSI_PACKET_PATH.read_text(encoding="utf-8")
        self.assertIn("approve_planning_policy", packet)
        self.assertIn("Recorded decision: `approve_with_revision`", packet)
        self.assertIn("batch balance table", packet)
        self.assertIn("All verb-form rows remain deferred.", packet)
        applied = APPLIED_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("`approve_with_revision`", applied)
        self.assertIn("batch balance table", applied)
        self.assertIn("no input list created", applied)
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn("docs/question_templates/perek_1_protected_preview_input_list_planning_policy.md", readme)
        self.assertIn("protected_preview_input_list_planning_policy.v1.json", readme)
        self.assertIn("perek_1_protected_preview_input_list_planning_policy_report.md", readme)
        self.assertIn("perek_1_protected_preview_input_list_planning_policy_yossi_review_packet.md", readme)
        self.assertIn("perek_1_protected_preview_input_list_planning_policy_yossi_review_applied.md", readme)
        self.assertIn("Decision: `approve_with_revision`", readme)


if __name__ == "__main__":
    unittest.main()
