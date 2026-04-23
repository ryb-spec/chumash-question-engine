import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from assessment_scope import ACTIVE_ASSESSMENT_SCOPE
from scripts import release_check


class ReleaseCheckScriptTests(unittest.TestCase):
    def test_prepare_release_check_prints_finalize_command_and_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pilot_session_events_20260422T010000Z_release-check.jsonl"
            output_dir = Path(tmpdir) / "release-check-output"
            with patch.object(release_check, "build_isolated_pilot_log_path", return_value=log_path):
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    release_check.prepare_release_check(
                        "release-check",
                        output_dir=output_dir,
                        question_count=12,
                    )

        payload = json.loads(buffer.getvalue())
        self.assertEqual(payload["isolated_log_path"], str(log_path))
        self.assertEqual(payload["release_check_output_dir"], str(output_dir))
        self.assertIn("finalize_command", payload)
        self.assertIn(str(log_path), payload["finalize_command"])
        self.assertIn(str(output_dir), payload["finalize_command"])
        self.assertIn(f'--scope-id "{ACTIVE_ASSESSMENT_SCOPE}"', payload["finalize_command"])
        self.assertIn("--question-count 12", payload["finalize_command"])

    def test_finalize_release_check_writes_all_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pilot_session_events_20260422T011500Z_release-check.jsonl"
            log_path.write_text(
                json.dumps(
                    {
                        "event_type": "question_served",
                        "timestamp_utc": "2026-04-22T01:15:00+00:00",
                        "session_id": "pilot-release",
                        "question_log_id": "q1",
                        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
                        "trusted_scope_mode": "trusted_active_scope",
                        "trusted_active_scope_requested": True,
                        "trusted_active_scope_session": True,
                        "practice_type": "Learn Mode",
                        "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                        "scope_membership": "active_parsed",
                        "question_type": "translation",
                        "selected_word": "אֱלֹקִים",
                        "correct_answer": "God",
                        "served_status": "served",
                        "debug_pre_serve_validation_passed": True,
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            output_dir = Path(tmpdir) / "release-check"
            hand_audit_packet = {
                "generated_at_utc": "2026-04-22T01:20:00+00:00",
                "scope": {
                    "scope_id": ACTIVE_ASSESSMENT_SCOPE,
                    "range": {"start": {"perek": 1, "pasuk": 1}, "end": {"perek": 3, "pasuk": 8}},
                },
                "requested_question_count": 2,
                "question_count": 2,
                "lane_counts": {"translation": 1, "shoresh": 1},
                "question_type_counts": {"translation": 1, "shoresh": 1},
                "provenance_counts": {"reviewed": 1, "generated": 1},
                "duplicate_feel_warning_count": 0,
                "warnings": [],
                "questions": [
                    {
                        "index": 1,
                        "lane": "translation",
                        "skill": "translation",
                        "question_type": "translation",
                        "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                        "target_word": "אֱלֹקִים",
                        "prompt": "What does אֱלֹקִים mean?",
                        "choices": ["God", "earth", "light", "dust"],
                        "correct_answer": "God",
                        "explanation": "אֱלֹקִים means 'God'.",
                        "provenance": "reviewed",
                        "source": "active scope reviewed bank",
                        "analysis_source": "active_scope_reviewed_bank",
                    },
                    {
                        "index": 2,
                        "lane": "shoresh",
                        "skill": "shoresh",
                        "question_type": "shoresh",
                        "pasuk_ref": {"label": "Bereishis 1:3", "pasuk_id": "bereishis_1_3"},
                        "target_word": "וַיֹּאמֶר",
                        "prompt": "What is the shoresh of וַיֹּאמֶר?",
                        "choices": ["אמר", "ראה", "היה", "בדל"],
                        "correct_answer": "אמר",
                        "explanation": "The shoresh is אמר.",
                        "provenance": "generated",
                        "source": "generated skill question",
                        "analysis_source": None,
                    },
                ],
            }

            with patch.object(release_check, "build_hand_audit_packet", return_value=hand_audit_packet):
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    release_check.finalize_release_check(
                        log_path,
                        output_dir=output_dir,
                        scope_id=ACTIVE_ASSESSMENT_SCOPE,
                        question_count=2,
                    )

            payload = json.loads(buffer.getvalue())
            self.assertEqual(payload["output_dir"], str(output_dir))
            artifact_paths = payload["artifacts"]
            for path in artifact_paths.values():
                self.assertTrue(Path(path).exists(), path)

            summary = json.loads((output_dir / "release_check_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["pilot_review_summary"]["session_count"], 1)
            self.assertEqual(summary["hand_audit_summary"]["question_count"], 2)
            self.assertEqual(summary["hand_audit_summary"]["lane_counts"], {"translation": 1, "shoresh": 1})

            hand_audit_markdown = (output_dir / "hand_audit.md").read_text(encoding="utf-8")
            self.assertIn("# Release Check Hand Audit", hand_audit_markdown)
            self.assertIn("Review:", hand_audit_markdown)

    def test_build_hand_audit_packet_returns_structured_balanced_sample(self):
        packet = release_check.build_hand_audit_packet(question_count=10)

        self.assertEqual(packet["scope"]["scope_id"], ACTIVE_ASSESSMENT_SCOPE)
        self.assertEqual(packet["question_count"], 10)
        self.assertEqual(sum(packet["lane_counts"].values()), 10)
        self.assertGreaterEqual(len(packet["lane_counts"]), 4)
        self.assertTrue(set(packet["lane_counts"]).issubset({"translation", "shoresh", "tense", "affix", "part_of_speech"}))
        self.assertTrue(packet["questions"])
        exact_keys = {
            (
                question["question_type"],
                question["target_word"],
                question["correct_answer"],
                question["pasuk_ref"]["pasuk_id"],
            )
            for question in packet["questions"]
        }
        self.assertEqual(len(exact_keys), len(packet["questions"]))
        for question in packet["questions"]:
            self.assertTrue(question["prompt"])
            self.assertTrue(question["correct_answer"])
            self.assertIn(question["provenance"], {"reviewed", "generated", "override", "suppressed"})


if __name__ == "__main__":
    unittest.main()
