from __future__ import annotations

import json
import unittest
from pathlib import Path

import scripts.validate_question_template_wording_policy as validator


ROOT = Path(__file__).resolve().parents[1]
DOC_POLICY_PATH = ROOT / "docs" / "question_templates" / "perek_1_approved_input_candidate_wording_policy.md"
JSON_POLICY_PATH = ROOT / "data" / "question_eligibility_audits" / "question_template_wording_policy.v1.json"
YOSSI_PACKET_PATH = (
    ROOT / "data" / "question_eligibility_audits" / "reports" / "perek_1_approved_input_candidate_wording_policy_yossi_review_packet.md"
)
POLICY_REPORT_PATH = ROOT / "data" / "question_eligibility_audits" / "reports" / "perek_1_question_template_wording_policy_report.md"
APPLIED_REPORT_PATH = (
    ROOT / "data" / "question_eligibility_audits" / "reports" / "perek_1_approved_input_candidate_wording_policy_yossi_review_applied.md"
)
README_PATH = ROOT / "data" / "question_eligibility_audits" / "README.md"
ET = "\u05d0\u05ea"


class QuestionTemplateWordingPolicyTests(unittest.TestCase):
    def load_policy(self):
        with JSON_POLICY_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def test_validator_passes(self):
        summary = validator.validate_question_template_wording_policy()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(
            summary["policy_markdown_path"],
            "docs/question_templates/perek_1_approved_input_candidate_wording_policy.md",
        )
        self.assertEqual(
            summary["policy_json_path"],
            "data/question_eligibility_audits/question_template_wording_policy.v1.json",
        )
        self.assertEqual(summary["approved_family_policy_count"], 4)

    def test_artifacts_exist(self):
        self.assertTrue(DOC_POLICY_PATH.exists())
        self.assertTrue(JSON_POLICY_PATH.exists())
        self.assertTrue(YOSSI_PACKET_PATH.exists())
        self.assertTrue(POLICY_REPORT_PATH.exists())
        self.assertTrue(APPLIED_REPORT_PATH.exists())

    def test_json_allowed_and_deferred_families_are_correct(self):
        policy = self.load_policy()
        self.assertEqual(set(policy["allowed_families"]), validator.ALLOWED_FAMILIES)
        self.assertIn("basic_verb_form_recognition", policy["deferred_families"])
        self.assertEqual(policy["family_rules"]["basic_verb_form_recognition"]["status"], "deferred")
        approved = [
            family
            for family in validator.ALLOWED_FAMILIES
            if policy["family_rules"][family]["family_policy_review_status"] == "yossi_family_policy_approved"
        ]
        self.assertEqual(len(approved), 4)
        self.assertEqual(policy["family_rules"]["basic_verb_form_recognition"]["family_policy_review_status"], "deferred")

    def test_no_actual_questions_or_answer_payloads_are_created(self):
        policy = self.load_policy()
        self.assertIn("generated_question", policy["forbidden_output_types"])
        self.assertIn("answer_choice_set", policy["forbidden_output_types"])
        self.assertIn("answer_key", policy["forbidden_output_types"])
        text = DOC_POLICY_PATH.read_text(encoding="utf-8")
        self.assertIn("non-final template shells only", text)
        self.assertIn("Do not generate answer choices in this task.", text)
        self.assertIn("This policy is not itself permission to generate questions", text)

    def test_safety_gates_remain_closed(self):
        policy = self.load_policy()
        defaults = policy["safety_gate_defaults"]
        self.assertEqual(defaults["question_allowed"], "needs_review")
        self.assertFalse(defaults["protected_preview_allowed"])
        self.assertFalse(defaults["reviewed_bank_allowed"])
        self.assertFalse(defaults["runtime_allowed"])
        self.assertFalse(defaults["student_use_allowed"])
        for family in validator.ALLOWED_FAMILIES:
            rules = policy["family_rules"][family]
            self.assertFalse(rules["future_template_allowed"])
            self.assertFalse(rules["protected_preview_allowed"])
            self.assertFalse(rules["reviewed_bank_allowed"])
            self.assertFalse(rules["runtime_allowed"])
        verb_rules = policy["family_rules"]["basic_verb_form_recognition"]
        self.assertFalse(verb_rules["future_template_allowed"])
        self.assertFalse(verb_rules["protected_preview_allowed"])
        self.assertFalse(verb_rules["reviewed_bank_allowed"])
        self.assertFalse(verb_rules["runtime_allowed"])

    def test_et_rules_require_function_not_translation_wording(self):
        text = DOC_POLICY_PATH.read_text(encoding="utf-8")
        self.assertIn(f"Ask about the function of `{ET}` as a direct-object marker.", text)
        self.assertIn(f'Do not ask "What does {ET} mean?" as if it has a simple English translation.', text)
        self.assertIn(f'Do not translate `{ET}` as "the."', text)
        self.assertIn(f'Do not translate `{ET}` as "with."', text)
        policy = self.load_policy()
        cautions = policy["family_rules"]["direct_object_marker_recognition"]["required_cautions"]
        self.assertIn("must use function wording", cautions)
        self.assertIn("must require future exact wording review", cautions)

    def test_yossi_packet_exists_and_contains_decision_fields(self):
        text = YOSSI_PACKET_PATH.read_text(encoding="utf-8")
        self.assertIn("This packet does not approve questions", text)
        self.assertIn("Recorded decision: `approve_family_policy`", text)
        self.assertIn("Recorded decision: `keep_deferred`", text)
        self.assertIn("approve_family_policy", text)
        self.assertIn("approve_with_revision", text)
        self.assertIn("block_family_for_now", text)

    def test_applied_report_records_family_policy_decisions_and_safety(self):
        text = APPLIED_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("families reviewed: 5", text)
        self.assertIn("approved family policies: 4", text)
        self.assertIn("deferred family policies: 1", text)
        self.assertIn("direct_object_marker_recognition", text)
        self.assertIn("basic_verb_form_recognition", text)
        self.assertIn("no questions generated", text)
        self.assertIn("no answer choices generated", text)
        self.assertIn("no answer keys generated", text)
        self.assertIn("no protected-preview input list created", text)

    def test_readme_links_are_present(self):
        text = README_PATH.read_text(encoding="utf-8")
        self.assertIn("docs/question_templates/perek_1_approved_input_candidate_wording_policy.md", text)
        self.assertIn("question_template_wording_policy.v1.json", text)
        self.assertIn("perek_1_approved_input_candidate_wording_policy_yossi_review_packet.md", text)
        self.assertIn("perek_1_question_template_wording_policy_report.md", text)
        self.assertIn("perek_1_approved_input_candidate_wording_policy_yossi_review_applied.md", text)


if __name__ == "__main__":
    unittest.main()
