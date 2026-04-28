from __future__ import annotations

import json
import unittest
from pathlib import Path

import scripts.validate_pipeline_rounds as validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "pipeline_rounds" / "round_2_fast_track_pipeline_contract.v1.json"
CHECKLIST = ROOT / "data" / "pipeline_rounds" / "reports" / "round_2_starter_checklist.md"


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


if __name__ == "__main__":
    unittest.main()
