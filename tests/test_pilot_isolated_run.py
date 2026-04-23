import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts import pilot_isolated_run


class PilotIsolatedRunTests(unittest.TestCase):
    def test_prepare_run_prints_exact_review_command(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pilot_session_events_20260421T190000Z_fast-check.jsonl"
            with patch.object(pilot_isolated_run, "build_isolated_pilot_log_path", return_value=log_path):
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    pilot_isolated_run.prepare_run("fast-check")

        payload = json.loads(buffer.getvalue())
        self.assertEqual(payload["isolated_log_path"], str(log_path))
        self.assertIn("review_command", payload)
        self.assertIn(str(log_path), payload["review_command"])
        self.assertIn("next_steps", payload)

    def test_review_run_writes_default_export_path_and_prints_compact_summary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pilot_session_events_20260421T190500Z_fast-check.jsonl"
            log_path.write_text(
                json.dumps(
                    {
                        "event_type": "question_served",
                        "timestamp_utc": "2026-04-21T19:05:00+00:00",
                        "session_id": "pilot-fast",
                        "question_log_id": "q1",
                        "scope_id": "local_parsed_bereishis_1_1_to_2_25",
                        "trusted_scope_mode": "trusted_active_scope",
                        "trusted_active_scope_requested": True,
                        "trusted_active_scope_session": True,
                        "practice_type": "Learn Mode",
                        "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                        "scope_membership": "active_parsed",
                        "question_type": "translation",
                        "selected_word": "בְּרֵאשִׁית",
                        "correct_answer": "in the beginning",
                        "served_status": "served",
                        "debug_pre_serve_validation_passed": True,
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            export_dir = Path(tmpdir) / "exports"
            with patch.object(pilot_isolated_run, "DEFAULT_EXPORT_DIR", export_dir):
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    pilot_isolated_run.review_run(log_path, None, 20)
                payload = json.loads(buffer.getvalue())
                export_path = export_dir / f"{log_path.stem}_review.json"
                self.assertEqual(payload["export_path"], str(export_path))
                self.assertTrue(export_path.exists())

        self.assertIn("release_review_summary", payload)
        self.assertEqual(payload["release_review_summary"]["session_count"], 1)
        self.assertEqual(payload["release_review_summary"]["top_served_question_families"], {"translation": 1})


if __name__ == "__main__":
    unittest.main()
