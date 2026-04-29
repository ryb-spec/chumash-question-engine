from __future__ import annotations

import json
import unittest
from pathlib import Path

import scripts.validate_pipeline_rounds as validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "pipeline_rounds" / "round_2_fast_track_pipeline_contract.v1.json"
CHECKLIST = ROOT / "data" / "pipeline_rounds" / "reports" / "round_2_starter_checklist.md"
PEREK2_SOURCE_AUDIT = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_1_source_readiness_audit.md"
)
PEREK2_GATE1_REPORT = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_1_source_enrichment_eligibility_report.md"
)
PEREK2_GATE1_ENRICHMENT_DECISION_STATUS = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_1_enrichment_decision_status_report.md"
)
PEREK2_GATE2_CANDIDATE_POOL_SUMMARY = (
    ROOT / "data" / "pipeline_rounds" / "reports" / "bereishis_perek_2_gate_2_candidate_pool_summary.md"
)


class PipelineRoundsTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_pipeline_rounds()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["gate_count"], 4)

    def test_contract_json_exists_and_has_four_gates(self):
        self.assertTrue(CONTRACT.exists())
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        gate_ids = {gate["gate_id"] for gate in contract["gate_definitions"]}
        self.assertEqual(gate_ids, validator.REQUIRED_GATES)

    def test_prompt_templates_exist(self):
        for path in validator.PROMPTS:
            self.assertTrue(path.exists())
            text = path.read_text(encoding="utf-8")
            for placeholder in validator.PROMPT_PLACEHOLDERS:
                self.assertIn(placeholder, text)

    def test_stop_conditions_present(self):
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertIn("hebrew_corruption", contract["stop_conditions"])
        self.assertIn("missing_batch_balance_table", contract["stop_conditions"])

    def test_safety_gate_defaults_are_closed(self):
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        for field in validator.CLOSED_GATE_FIELDS:
            self.assertIs(contract["safety_gate_defaults"][field], False)

    def test_verb_form_remains_deferred(self):
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertIn("basic_verb_form_recognition", contract["deferred_families"])

    def test_round_2_checklist_exists(self):
        self.assertTrue(CHECKLIST.exists())
        text = CHECKLIST.read_text(encoding="utf-8")
        self.assertIn("Round 2 Starter Checklist", text)
        self.assertIn("Stop conditions", text)

    def test_perek2_gate1_reports_exist(self):
        self.assertTrue(PEREK2_SOURCE_AUDIT.exists())
        self.assertTrue(PEREK2_GATE1_REPORT.exists())
        text = PEREK2_GATE1_REPORT.read_text(encoding="utf-8")
        self.assertIn("Bereishis Perek 2 Gate 1", text)
        self.assertIn("Enrichment candidate counts", text)
        self.assertIn("Question-eligibility decisions and approved input-candidate planning are not ready", text)

    def test_perek2_compressed_review_packet_is_registered(self):
        summary = validator.validate_pipeline_rounds()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(
            summary["perek2_compressed_review_packet_path"],
            "data/source_skill_enrichment/reports/bereishis_perek_2_enrichment_compressed_yossi_review_packet.md",
        )
        self.assertTrue(validator.PEREK2_COMPRESSED_REVIEW_PACKET.exists())
        self.assertTrue(validator.PEREK2_COMPRESSED_REVIEW_SUMMARY.exists())
        text = validator.PEREK2_COMPRESSED_REVIEW_PACKET.read_text(encoding="utf-8")
        self.assertIn("raw candidate count: 1083", text)
        self.assertIn("no safety gates opened", text)
        self.assertIn("This is enrichment review only.", text)

    def test_perek2_clean_group_review_packet_is_registered(self):
        summary = validator.validate_pipeline_rounds()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(
            summary["perek2_clean_group_review_packet_path"],
            "data/source_skill_enrichment/reports/bereishis_perek_2_clean_group_yossi_review_packet.md",
        )
        self.assertTrue(validator.PEREK2_CLEAN_GROUP_REVIEW_PACKET.exists())
        self.assertTrue(validator.PEREK2_CLEAN_GROUP_REVIEW_SUMMARY.exists())
        self.assertTrue(validator.PEREK2_CLEAN_GROUP_APPLIED_REPORT.exists())
        text = validator.PEREK2_CLEAN_GROUP_REVIEW_PACKET.read_text(encoding="utf-8")
        applied_text = validator.PEREK2_CLEAN_GROUP_APPLIED_REPORT.read_text(encoding="utf-8")
        self.assertIn("groups reviewed: 69", text)
        self.assertIn("raw candidates covered: 191", text)
        self.assertIn("This is enrichment review only", text)
        self.assertIn("verified groups: 31", applied_text)
        self.assertIn("verified raw candidates: 91", applied_text)

    def test_perek2_gate1_decision_status_and_candidate_pool_are_registered(self):
        summary = validator.validate_pipeline_rounds()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(
            summary["perek2_gate1_enrichment_decision_status_path"],
            "data/pipeline_rounds/reports/bereishis_perek_2_gate_1_enrichment_decision_status_report.md",
        )
        self.assertEqual(
            summary["perek2_gate2_candidate_pool_summary_path"],
            "data/pipeline_rounds/reports/bereishis_perek_2_gate_2_candidate_pool_summary.md",
        )
        self.assertTrue(PEREK2_GATE1_ENRICHMENT_DECISION_STATUS.exists())
        self.assertTrue(PEREK2_GATE2_CANDIDATE_POOL_SUMMARY.exists())
        status_text = PEREK2_GATE1_ENRICHMENT_DECISION_STATUS.read_text(encoding="utf-8")
        pool_text = PEREK2_GATE2_CANDIDATE_POOL_SUMMARY.read_text(encoding="utf-8")
        for phrase in (
            "31 token-split clean noun standards groups",
            "91 raw token-split standards candidates",
            "38 clean vocabulary/noun and clean shoresh groups",
            "100 raw vocabulary/shoresh candidates",
            "only the 91 verified token-split clean noun standards raw candidates",
            "no follow-up groups",
            "no morphology",
            "no verb forms",
            "no prefix/preposition",
            "no direct-object-marker",
            "no shoresh",
            "no phrase-level standards",
        ):
            self.assertIn(phrase, status_text)
        self.assertIn("This is not a Gate 2 batch selection", pool_text)
        self.assertIn("No input-candidate batch TSV was created", pool_text)


if __name__ == "__main__":
    unittest.main()
