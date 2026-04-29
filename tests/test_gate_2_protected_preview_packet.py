from __future__ import annotations

import csv
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import scripts.validate_gate_2_protected_preview_packet as validator


class Gate2ProtectedPreviewPacketTests(unittest.TestCase):
    def test_validator_passes(self):
        summary = validator.validate_gate_2_protected_preview_packet()
        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["row_count"], 14)
        self.assertEqual(summary["family_counts"], {"basic_noun_recognition": 14})
        self.assertEqual(summary["perek_summaries"]["perek_2"]["row_count"], 10)
        self.assertEqual(summary["perek_summaries"]["perek_3"]["row_count"], 4)

    def test_perek_2_packet_tsv_exists_and_has_10_rows(self):
        fields, rows = validator.load_tsv(validator.TSV)
        self.assertEqual(fields, validator.REQUIRED_COLUMNS)
        self.assertEqual(len(rows), 10)

    def test_perek_2_excluded_rows_absent(self):
        _, rows = validator.load_tsv(validator.TSV)
        _, candidates = validator.load_tsv(validator.CAND)
        by_id = {row["protected_preview_candidate_id"]: row for row in candidates}
        gate_ids = {
            by_id[row["protected_preview_candidate_id"]]["gate_2_input_candidate_id"]
            for row in rows
        }
        self.assertFalse(gate_ids.intersection(validator.EXCLUDED_GATE2))

    def test_perek_3_packet_file_exists_and_has_exact_4_rows(self):
        fields, rows = validator.load_tsv(validator.P3_TSV)
        self.assertEqual(fields, validator.REQUIRED_COLUMNS)
        self.assertEqual(len(rows), 4)

    def test_perek_3_packet_id_set_is_exactly_approved_ids(self):
        _, rows = validator.load_tsv(validator.P3_TSV)
        candidate_ids = {row["protected_preview_candidate_id"] for row in rows}
        self.assertEqual(candidate_ids, validator.EXPECTED_P3_APPROVED)

    def test_perek_3_packet_excludes_revision_and_followup_ids(self):
        _, rows = validator.load_tsv(validator.P3_TSV)
        candidate_ids = {row["protected_preview_candidate_id"] for row in rows}
        self.assertFalse(candidate_ids.intersection(validator.P3_REVISION))
        self.assertFalse(candidate_ids.intersection(validator.P3_FOLLOWUP))
        self.assertFalse(candidate_ids.intersection(validator.P3_EXCLUDED))

    def test_downstream_gates_false_and_decisions_blank(self):
        for packet in (validator.TSV, validator.P3_TSV):
            _, rows = validator.load_tsv(packet)
            for row in rows:
                for gate in validator.GATES:
                    self.assertEqual(row[gate], "false")
                self.assertEqual(row["yossi_internal_preview_decision"], "")
                self.assertEqual(row["yossi_internal_preview_notes"], "")
                self.assertEqual(row["internal_packet_status"], "internal_protected_preview_packet_only")
                self.assertEqual(row["internal_preview_review_status"], "needs_internal_review")

    def test_reports_exist(self):
        for path in (
            validator.README,
            validator.PACKET,
            validator.GEN,
            validator.COMPLETE,
            validator.EXCLUDED,
            validator.P3_REPORT,
            validator.P3_REVIEW_CHECKLIST,
            validator.P3_REVIEW_CHECKLIST_TSV,
            validator.P3_REVIEW_DECISIONS_APPLIED,
            validator.P3_REVIEW_DECISIONS_APPLIED_TSV,
            validator.P3_ITEM_004_REVISION_PLAN,
            validator.P3_ITEM_004_REVISION_PLAN_TSV,
            validator.P3_LIMITED_READINESS,
            validator.P3_LIMITED_READINESS_TSV,
            validator.P3_BLOCKED_REGISTER,
            validator.P3_BLOCKED_REGISTER_TSV,
            validator.P3_OBSERVATION_TEMPLATE,
            validator.P3_OBSERVATION_TEMPLATE_TSV,
            validator.P3_REVIEWER_HANDOFF,
            validator.P3_REVIEWER_HANDOFF_TSV,
            validator.P3_OBSERVATION_INTAKE,
            validator.P3_OBSERVATION_INTAKE_TSV,
            validator.P3_OBSERVATION_INTAKE_INSTRUCTIONS,
            validator.P3_COMPLETION_DASHBOARD,
            validator.P3_COMPLETION_DASHBOARD_JSON,
            validator.P3_RISK_REGISTER,
            validator.P3_RISK_REGISTER_TSV,
            validator.P3_FINAL_HANDOFF_INDEX,
            validator.P3_TO_P4_LAUNCH_GATE,
            validator.P3_TO_P4_LAUNCH_GATE_JSON,
            validator.P4_SOURCE_DISCOVERY_PROMPT,
            validator.P3_STATUS_INDEX,
        ):
            self.assertTrue(path.exists(), path)

    def test_perek_3_packet_report_names_inclusions_and_exclusions(self):
        text = validator.P3_REPORT.read_text(encoding="utf-8")
        for candidate_id in validator.EXPECTED_P3_APPROVED:
            self.assertIn(candidate_id, text)
        self.assertIn("All 4 `approve_with_revision` items are excluded", text)
        self.assertIn("All 2 `needs_follow_up` items are excluded", text)
        self.assertIn("Included approved rows: 4", text)
        self.assertIn("Excluded revision rows: 4", text)
        self.assertIn("Excluded follow-up rows: 2", text)
        self.assertIn("No Perek 3 runtime activation", text)
        self.assertIn("No reviewed-bank promotion", text)

    def test_perek_3_review_checklist_exists_and_names_approved_ids_only(self):
        text = validator.P3_REVIEW_CHECKLIST.read_text(encoding="utf-8")
        for candidate_id in validator.EXPECTED_P3_APPROVED:
            self.assertIn(candidate_id, text)
            self.assertIn(f" / {candidate_id}", text)
        for candidate_id in validator.P3_EXCLUDED:
            self.assertNotIn(f" / {candidate_id}", text)

    def test_perek_3_review_checklist_is_review_only_and_blank(self):
        text = validator.P3_REVIEW_CHECKLIST.read_text(encoding="utf-8")
        required_phrases = [
            "This is not runtime content.",
            "This is not reviewed-bank content.",
            "This is not student-facing content.",
            "This does not apply decisions.",
            "This does not activate or promote anything.",
            "approve_for_limited_post_preview_iteration",
            "approve_with_revision",
            "needs_follow_up",
            "reject_for_broader_use",
            "source_only",
            "Are two עֵץ items too repetitive",
            "Reviewer decision: ",
            "Reviewer notes: ",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, text)

    def test_perek_3_review_checklist_has_one_card_per_packet_item(self):
        text = validator.P3_REVIEW_CHECKLIST.read_text(encoding="utf-8")
        _, rows = validator.load_tsv(validator.P3_TSV)
        for row in rows:
            heading = f"### {row['protected_preview_packet_item_id']} / {row['protected_preview_candidate_id']}"
            self.assertEqual(text.count(heading), 1)

    def test_perek_3_review_checklist_tsv_records_applied_decisions_only(self):
        fields, rows = validator.load_tsv(validator.P3_REVIEW_CHECKLIST_TSV)
        self.assertEqual(fields, validator.REVIEW_CHECKLIST_COLUMNS)
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["candidate_id"] for row in rows}, validator.EXPECTED_P3_APPROVED)
        decisions = {row["candidate_id"]: row["reviewer_decision"] for row in rows}
        self.assertEqual(decisions["g2ppcand_p3_004"], "approve_with_revision")
        self.assertEqual(
            {candidate_id for candidate_id, decision in decisions.items() if decision == "approve_for_limited_post_preview_iteration"},
            {"g2ppcand_p3_003", "g2ppcand_p3_007", "g2ppcand_p3_008"},
        )
        for row in rows:
            self.assertEqual(row["runtime_allowed"], "false")
            self.assertEqual(row["reviewed_bank_allowed"], "false")
            self.assertEqual(row["student_facing_allowed"], "false")
            self.assertTrue(row["reviewer_decision"])
            self.assertTrue(row["reviewer_notes"])
            if row["candidate_id"] == "g2ppcand_p3_004":
                self.assertIn("repetition/session-balance", row["revision_required"])
            for field in ("reviewer_name", "review_date"):
                self.assertEqual(row[field], "")

    def test_perek_3_applied_review_decisions_report_and_tsv_exist(self):
        self.assertTrue(validator.P3_REVIEW_DECISIONS_APPLIED.exists())
        self.assertTrue(validator.P3_REVIEW_DECISIONS_APPLIED_TSV.exists())
        text = validator.P3_REVIEW_DECISIONS_APPLIED.read_text(encoding="utf-8")
        self.assertIn("Decision summary", text)
        self.assertIn("repetition/session-balance", text)
        self.assertIn("No runtime activation", text)
        self.assertIn("No reviewed-bank promotion", text)
        self.assertIn("No item content revision", text)

    def test_perek_3_applied_review_decisions_tsv_counts_and_gates(self):
        fields, rows = validator.load_tsv(validator.P3_REVIEW_DECISIONS_APPLIED_TSV)
        self.assertEqual(fields, validator.APPLIED_REVIEW_COLUMNS)
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["candidate_id"] for row in rows}, validator.EXPECTED_P3_APPROVED)
        decisions = [row["reviewer_decision"] for row in rows]
        self.assertEqual(decisions.count("approve_for_limited_post_preview_iteration"), 3)
        self.assertEqual(decisions.count("approve_with_revision"), 1)
        revision_rows = [row for row in rows if row["reviewer_decision"] == "approve_with_revision"]
        self.assertEqual([row["candidate_id"] for row in revision_rows], ["g2ppcand_p3_004"])
        self.assertIn("repetition/session-balance", revision_rows[0]["required_revision"])
        for row in rows:
            for gate in validator.APPLIED_REVIEW_GATE_COLUMNS:
                self.assertEqual(row[gate], "false")

    def test_perek_3_item_004_revision_plan_exists_and_is_planning_only(self):
        text = validator.P3_ITEM_004_REVISION_PLAN.read_text(encoding="utf-8")
        self.assertIn("planning artifact only", text)
        self.assertIn("g2ppcand_p3_004", text)
        self.assertIn("g2ppacket_p3_002", text)
        self.assertIn("repetition/session-balance", text)
        self.assertIn("It does not revise the item.", text)
        self.assertIn("It does not apply a new decision.", text)
        self.assertIn("No runtime activation", text)
        self.assertIn("No reviewed-bank promotion", text)
        self.assertIn("No student-facing content creation", text)
        self.assertIn("broader use blocked", text)
        for candidate_id in validator.EXPECTED_P3_APPROVED - {"g2ppcand_p3_004"}:
            self.assertNotIn(f"Candidate: `{candidate_id}`", text)

    def test_perek_3_item_004_revision_plan_tsv_is_one_row_and_blocked(self):
        fields, rows = validator.load_tsv(validator.P3_ITEM_004_REVISION_PLAN_TSV)
        self.assertEqual(fields, validator.REVISION_PLAN_COLUMNS)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["packet_item_id"], "g2ppacket_p3_002")
        self.assertEqual(row["candidate_id"], "g2ppcand_p3_004")
        self.assertEqual(row["current_decision"], "approve_with_revision")
        self.assertIn("repetition/session-balance", row["revision_issue"])
        self.assertEqual(row["broader_use_blocked"], "true")
        self.assertEqual(row["runtime_allowed"], "false")
        self.assertEqual(row["reviewed_bank_allowed"], "false")
        self.assertEqual(row["student_facing_allowed"], "false")

    def test_perek_3_limited_readiness_report_exists_and_explains_three_item_lane(self):
        text = validator.P3_LIMITED_READINESS.read_text(encoding="utf-8")
        self.assertIn("Internal-only limited post-preview iteration readiness", text)
        self.assertIn("Why only 3 items", text)
        self.assertIn("No runtime activation", text)
        self.assertIn("No reviewed-bank promotion", text)
        self.assertIn("No student-facing content creation", text)
        self.assertIn("No protected-preview packet creation", text)
        for candidate_id in validator.EXPECTED_P3_LIMITED_READINESS:
            self.assertIn(candidate_id, text)
        self.assertIn("g2ppcand_p3_004", text)
        self.assertIn("blocked from broader use", text)
        self.assertIn("not rejected, not revised, not promoted", text)

    def test_perek_3_limited_readiness_tsv_has_exact_three_clean_items(self):
        fields, rows = validator.load_tsv(validator.P3_LIMITED_READINESS_TSV)
        self.assertEqual(fields, validator.LIMITED_READINESS_COLUMNS)
        self.assertEqual(len(rows), 3)
        self.assertEqual({row["candidate_id"] for row in rows}, validator.EXPECTED_P3_LIMITED_READINESS)
        self.assertNotIn("g2ppcand_p3_004", {row["candidate_id"] for row in rows})
        for row in rows:
            self.assertEqual(row["applied_review_decision"], "approve_for_limited_post_preview_iteration")
            self.assertEqual(row["limited_iteration_ready"], "true")
            self.assertEqual(row["post_iteration_decision"], "")
            for gate in validator.LIMITED_READINESS_GATE_COLUMNS:
                self.assertEqual(row[gate], "false")

    def test_perek_3_blocked_register_contains_only_item_004(self):
        text = validator.P3_BLOCKED_REGISTER.read_text(encoding="utf-8")
        self.assertIn("Blocked from broader use register", text)
        self.assertIn("g2ppcand_p3_004", text)
        self.assertIn("repetition/session-balance", text)
        self.assertIn("broader_use_blocked=true", text)
        self.assertIn("This item is not rejected.", text)
        self.assertIn("This item is not revised by this task.", text)
        self.assertIn("This item is not approved for broader use.", text)
        fields, rows = validator.load_tsv(validator.P3_BLOCKED_REGISTER_TSV)
        self.assertEqual(fields, validator.BLOCKED_REGISTER_COLUMNS)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["packet_item_id"], "g2ppacket_p3_002")
        self.assertEqual(row["candidate_id"], "g2ppcand_p3_004")
        self.assertEqual(row["current_decision"], "approve_with_revision")
        self.assertIn("repetition/session-balance", row["block_reason"])
        self.assertEqual(row["related_duplicate_item"], "g2ppcand_p3_003")
        self.assertEqual(row["broader_use_blocked"], "true")
        self.assertEqual(row["runtime_allowed"], "false")
        self.assertEqual(row["reviewed_bank_allowed"], "false")
        self.assertEqual(row["student_facing_allowed"], "false")

    def test_perek_3_observation_template_has_three_active_items_and_blank_fields(self):
        text = validator.P3_OBSERVATION_TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("Limited post-preview observation template", text)
        for candidate_id in validator.EXPECTED_P3_LIMITED_READINESS:
            self.assertIn(candidate_id, text)
        self.assertNotIn("### g2ppacket_p3_002 / g2ppcand_p3_004", text)
        fields, rows = validator.load_tsv(validator.P3_OBSERVATION_TEMPLATE_TSV)
        self.assertEqual(fields, validator.OBSERVATION_TEMPLATE_COLUMNS)
        self.assertEqual(len(rows), 3)
        self.assertEqual({row["candidate_id"] for row in rows}, validator.EXPECTED_P3_LIMITED_READINESS)
        self.assertNotIn("g2ppcand_p3_004", {row["candidate_id"] for row in rows})
        for row in rows:
            for field in validator.OBSERVATION_BLANK_COLUMNS:
                self.assertEqual(row[field], "")

    def test_perek_3_reviewer_handoff_exists_and_covers_three_active_items(self):
        text = validator.P3_REVIEWER_HANDOFF.read_text(encoding="utf-8")
        self.assertIn("limited post-preview reviewer handoff", text)
        self.assertIn("Reviewer instructions", text)
        self.assertIn("Observation fields must remain blank until real observations are recorded.", text)
        for candidate_id in validator.EXPECTED_P3_LIMITED_READINESS:
            self.assertIn(candidate_id, text)
        self.assertIn("g2ppcand_p3_004", text)
        self.assertIn("blocked and should not be used in this limited review lane", text)
        self.assertNotIn("### g2ppacket_p3_002 / g2ppcand_p3_004", text)

    def test_perek_3_reviewer_handoff_safety_boundary_language(self):
        text = validator.P3_REVIEWER_HANDOFF.read_text(encoding="utf-8")
        required_phrases = [
            "Not runtime.",
            "Not reviewed bank.",
            "Not student-facing.",
            "Does not apply decisions.",
            "Does not revise items.",
            "Does not activate or promote content.",
            "No runtime activation",
            "No Perek 3 runtime activation",
            "No reviewed-bank promotion",
            "No protected-preview packet creation",
            "No student-facing content creation",
            "No item content revision",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, text)

    def test_perek_3_reviewer_handoff_checklist_tsv_is_blank_three_item_sheet(self):
        fields, rows = validator.load_tsv(validator.P3_REVIEWER_HANDOFF_TSV)
        self.assertEqual(fields, validator.REVIEWER_HANDOFF_COLUMNS)
        self.assertEqual(len(rows), 3)
        self.assertEqual({row["candidate_id"] for row in rows}, validator.EXPECTED_P3_LIMITED_READINESS)
        self.assertNotIn("g2ppcand_p3_004", {row["candidate_id"] for row in rows})
        for row in rows:
            for field in validator.REVIEWER_HANDOFF_BLANK_COLUMNS:
                self.assertEqual(row[field], "")

    def test_perek_3_observation_intake_exists_and_is_blank_three_item_sheet(self):
        text = validator.P3_OBSERVATION_INTAKE.read_text(encoding="utf-8")
        instructions = validator.P3_OBSERVATION_INTAKE_INSTRUCTIONS.read_text(encoding="utf-8")
        self.assertIn("observation intake", text)
        self.assertIn("These are future recommendation values only.", text)
        self.assertIn("They are not applied by this task.", text)
        self.assertIn("A later explicit decision-application task is required", text)
        self.assertIn("g2ppcand_p3_004", text)
        self.assertIn("not an active observation item", text)
        for decision in (
            "keep_limited_iteration",
            "revise_before_next_iteration",
            "needs_follow_up",
            "reject_for_broader_use",
            "candidate_for_future_reviewed_bank_consideration",
        ):
            self.assertIn(decision, instructions)
        fields, rows = validator.load_tsv(validator.P3_OBSERVATION_INTAKE_TSV)
        self.assertEqual(fields, validator.OBSERVATION_INTAKE_COLUMNS)
        self.assertEqual(len(rows), 3)
        self.assertEqual({row["candidate_id"] for row in rows}, validator.EXPECTED_P3_LIMITED_READINESS)
        self.assertNotIn("g2ppcand_p3_004", {row["candidate_id"] for row in rows})
        for row in rows:
            for field in validator.OBSERVATION_INTAKE_BLANK_COLUMNS:
                self.assertEqual(row[field], "")

    def test_perek_3_completion_dashboard_counts_are_closed(self):
        text = validator.P3_COMPLETION_DASHBOARD.read_text(encoding="utf-8")
        self.assertIn("Observed rows: 0", text)
        self.assertIn("Runtime-ready rows: 0", text)
        self.assertIn("Reviewed-bank-ready rows: 0", text)
        self.assertIn("Student-facing rows: 0", text)
        self.assertIn("No observation decisions applied", text)
        payload = json.loads(validator.P3_COMPLETION_DASHBOARD_JSON.read_text(encoding="utf-8"))
        self.assertEqual(payload["counts"]["original_internal_packet_rows"], 4)
        self.assertEqual(payload["counts"]["active_limited_readiness_rows"], 3)
        self.assertEqual(payload["counts"]["blocked_rows"], 1)
        self.assertEqual(payload["counts"]["observed_rows"], 0)
        self.assertEqual(payload["counts"]["runtime_ready_rows"], 0)
        self.assertEqual(payload["counts"]["reviewed_bank_ready_rows"], 0)
        self.assertEqual(payload["counts"]["student_facing_rows"], 0)
        self.assertFalse(payload["safety_state"]["runtime_activation"])
        self.assertFalse(payload["safety_state"]["reviewed_bank_promotion"])

    def test_perek_3_risk_register_contains_expected_closed_gate_risks(self):
        text = validator.P3_RISK_REGISTER.read_text(encoding="utf-8")
        self.assertIn("Duplicate `עֵץ` / session-balance risk", text)
        self.assertIn("Small sample size risk", text)
        self.assertIn("Narrow skill-family risk", text)
        self.assertIn("No actual observation data yet", text)
        self.assertIn("No reviewed-bank approval", text)
        self.assertIn("No runtime approval", text)
        fields, rows = validator.load_tsv(validator.P3_RISK_REGISTER_TSV)
        self.assertEqual(fields, validator.RISK_REGISTER_COLUMNS)
        self.assertTrue(any("Duplicate עֵץ" in row["risk_name"] for row in rows))
        for row in rows:
            self.assertEqual(row["runtime_allowed"], "false")
            self.assertEqual(row["reviewed_bank_allowed"], "false")
            self.assertEqual(row["student_facing_allowed"], "false")

    def test_perek_3_to_perek_4_launch_gate_is_source_discovery_only(self):
        text = validator.P3_TO_P4_LAUNCH_GATE.read_text(encoding="utf-8")
        self.assertIn("Go for Perek 4 source-discovery only.", text)
        self.assertIn("No for Perek 4 runtime activation.", text)
        self.assertIn("No for Perek 4 reviewed-bank promotion.", text)
        self.assertIn("No for Perek 4 student-facing content.", text)
        self.assertIn("does not create Perek 4 candidates", text)
        payload = json.loads(validator.P3_TO_P4_LAUNCH_GATE_JSON.read_text(encoding="utf-8"))
        self.assertEqual(payload["go_no_go_recommendation"]["perek_4_source_discovery_only"], "go")
        self.assertEqual(payload["go_no_go_recommendation"]["perek_4_runtime_activation"], "no")
        self.assertEqual(payload["go_no_go_recommendation"]["perek_4_reviewed_bank_promotion"], "no")
        self.assertEqual(payload["go_no_go_recommendation"]["perek_4_student_facing_content"], "no")

    def test_perek_4_source_discovery_prompt_is_review_only(self):
        text = validator.P4_SOURCE_DISCOVERY_PROMPT.read_text(encoding="utf-8")
        self.assertIn("source-to-skill discovery only", text)
        self.assertIn("review-only safe candidate inventory", text)
        self.assertIn("avoid runtime", text)
        self.assertIn("avoid reviewed-bank promotion", text)
        self.assertIn("avoid student-facing content", text)
        self.assertIn("avoid packet creation unless explicitly asked later", text)
        self.assertIn("include duplicate-token/session-balance warnings", text)
        self.assertIn("Keep every row review-only and fail-closed.", text)

    def test_perek_3_final_handoff_index_links_key_artifacts(self):
        text = validator.P3_FINAL_HANDOFF_INDEX.read_text(encoding="utf-8")
        for path in (
            validator.P3_CAND,
            validator.P3_STATUS_INDEX,
            validator.P3_TSV,
            validator.P3_REPORT,
            validator.P3_REVIEW_CHECKLIST,
            validator.P3_REVIEW_CHECKLIST_TSV,
            validator.P3_REVIEW_DECISIONS_APPLIED,
            validator.P3_REVIEW_DECISIONS_APPLIED_TSV,
            validator.P3_ITEM_004_REVISION_PLAN,
            validator.P3_ITEM_004_REVISION_PLAN_TSV,
            validator.P3_LIMITED_READINESS,
            validator.P3_LIMITED_READINESS_TSV,
            validator.P3_BLOCKED_REGISTER,
            validator.P3_BLOCKED_REGISTER_TSV,
            validator.P3_OBSERVATION_TEMPLATE,
            validator.P3_OBSERVATION_TEMPLATE_TSV,
            validator.P3_REVIEWER_HANDOFF,
            validator.P3_REVIEWER_HANDOFF_TSV,
            validator.P3_OBSERVATION_INTAKE,
            validator.P3_OBSERVATION_INTAKE_TSV,
            validator.P3_OBSERVATION_INTAKE_INSTRUCTIONS,
            validator.P3_COMPLETION_DASHBOARD,
            validator.P3_RISK_REGISTER,
            validator.P3_TO_P4_LAUNCH_GATE,
            validator.P4_SOURCE_DISCOVERY_PROMPT,
        ):
            self.assertIn(validator.rel(path), text)
        self.assertIn("Active limited-review lane: 3 items.", text)
        self.assertIn("Blocked item: 1.", text)
        self.assertIn("Runtime-ready: 0.", text)
        self.assertIn("Reviewed-bank-ready: 0.", text)
        self.assertIn("Student-facing: 0.", text)

    def test_perek_3_status_index_says_packet_exists_and_gates_closed(self):
        text = validator.P3_STATUS_INDEX.read_text(encoding="utf-8")
        self.assertIn("historical pre-decision artifact", text)
        self.assertIn("applied-decision report is the current status source", text)
        self.assertIn("four-item internal protected-preview packet now exists", text)
        self.assertIn("Internal review decisions are recorded", text)
        self.assertIn("g2ppcand_p3_004", text)
        self.assertIn("repetition/session-balance", text)
        self.assertIn("planning-only revision plan", text)
        self.assertIn("three-item limited post-preview iteration readiness lane exists", text)
        self.assertIn("blocked broader-use register keeps `g2ppcand_p3_004` out of the limited readiness lane", text)
        self.assertIn("Future observation decisions must be recorded in a later explicit task", text)
        self.assertIn("limited post-preview reviewer handoff", text)
        self.assertIn("observation intake", text)
        self.assertIn("completion status dashboard", text)
        self.assertIn("risk register", text)
        self.assertIn("Perek 4 source-discovery only", text)
        self.assertIn("No Perek 3 runtime activation", text)
        self.assertIn("No reviewed-bank promotion", text)
        self.assertIn("No student-facing content", text)
        self.assertIn("`approve_for_internal_protected_preview_packet`: 4", text)
        self.assertIn("`approve_with_revision`: 4", text)
        self.assertIn("`needs_follow_up`: 2", text)

    def test_hebrew_integrity(self):
        for packet in (validator.TSV, validator.P3_TSV):
            _, rows = validator.load_tsv(packet)
            self.assertTrue(
                all(validator.has_hebrew(row["hebrew_token"]) and validator.has_hebrew(row["hebrew_phrase"]) for row in rows)
            )
        text = validator.PACKET.read_text(encoding="utf-8") + validator.EXCLUDED.read_text(encoding="utf-8")
        self.assertNotIn("??", text)

    def test_validator_rejects_extra_perek_3_candidate_id(self):
        _, rows = validator.load_tsv(validator.P3_TSV)
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir) / "bad_p3_packet.tsv"
            with tmp_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=validator.REQUIRED_COLUMNS, delimiter="\t", lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows + [rows[0]])
            errors: list[str] = []
            validator.validate_packet_spec(
                name="bad_perek_3",
                packet_tsv=tmp_path,
                candidate_tsv=validator.P3_CAND,
                expected_count=4,
                expected_candidate_ids=validator.EXPECTED_P3_APPROVED,
                excluded_gate_ids=set(),
                excluded_candidate_ids=validator.P3_EXCLUDED,
                errors=errors,
                family_counts=Counter(),
            )
            self.assertTrue(any("exactly 4 rows" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
