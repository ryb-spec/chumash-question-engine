import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import streamlit as st

from assessment_scope import active_pesukim_records
from runtime import pilot_logging


class PilotLoggingTests(unittest.TestCase):
    def setUp(self):
        st.session_state.clear()

    def test_sync_pilot_served_question_logs_once_for_same_visible_question(self):
        active_record = active_pesukim_records()[0]
        question = {
            "skill": "translation",
            "question_type": "word_meaning",
            "question": "What does this word mean?",
            "selected_word": "בראשית",
            "correct_answer": "in the beginning",
            "pasuk": active_record["text"],
            "pasuk_id": active_record["pasuk_id"],
        }

        with patch.object(pilot_logging, "append_pilot_event", return_value=True) as append_mock:
            first_log_id = pilot_logging.sync_pilot_served_question(
                question,
                practice_type="Learn Mode",
            )
            second_log_id = pilot_logging.sync_pilot_served_question(
                question,
                practice_type="Learn Mode",
            )
            third_log_id = pilot_logging.sync_pilot_served_question(
                question,
                practice_type="Pasuk Flow",
                flow_label="Bereishis 1:1 - Guided pasuk",
                flow_step=1,
            )

        self.assertEqual(first_log_id, second_log_id)
        self.assertNotEqual(first_log_id, third_log_id)
        self.assertEqual(append_mock.call_count, 2)
        self.assertTrue(st.session_state.get("pilot_session_id"))
        self.assertTrue(st.session_state.get("pilot_trusted_active_scope_session"))

    def test_sync_pilot_served_question_uses_active_pasuk_id_for_trusted_scope(self):
        active_record = active_pesukim_records()[0]
        question = {
            "skill": "translation",
            "question_type": "word_meaning",
            "question": "What does this word mean?",
            "selected_word": "בראשית",
            "correct_answer": "in the beginning",
            "pasuk": "mismatched text should not matter when pasuk_id is present",
            "pasuk_id": active_record["pasuk_id"],
        }

        captured_events = []

        with patch.object(
            pilot_logging,
            "append_pilot_event",
            side_effect=lambda event, **kwargs: captured_events.append(event) or True,
        ):
            pilot_logging.sync_pilot_served_question(question, practice_type="Learn Mode")

        self.assertEqual(len(captured_events), 1)
        served_event = captured_events[0]
        self.assertEqual(served_event["scope_membership"], "active_parsed")
        self.assertEqual(
            served_event["pasuk_ref"]["label"],
            f"{active_record['ref']['sefer']} {active_record['ref']['perek']}:{active_record['ref']['pasuk']}",
        )
        self.assertTrue(served_event["trusted_active_scope_session"])

    def test_sync_pilot_served_question_marks_outside_scope_session_non_trusted(self):
        question = {
            "skill": "translation",
            "question_type": "word_meaning",
            "question": "What does this word mean?",
            "selected_word": "מחוץ",
            "correct_answer": "outside",
            "pasuk": "outside active pilot block text",
        }

        captured_events = []

        with patch.object(
            pilot_logging,
            "append_pilot_event",
            side_effect=lambda event, **kwargs: captured_events.append(event) or True,
        ):
            pilot_logging.sync_pilot_served_question(question, practice_type="Learn Mode")

        self.assertEqual(len(captured_events), 1)
        served_event = captured_events[0]
        self.assertEqual(served_event["scope_membership"], "outside_active_parsed")
        self.assertEqual(
            served_event["pasuk_ref"]["label"],
            pilot_logging.OUTSIDE_ACTIVE_PARSED_LABEL,
        )
        self.assertFalse(served_event["trusted_active_scope_session"])
        self.assertFalse(st.session_state.get("pilot_trusted_active_scope_session"))

    def test_mark_current_question_unclear_is_idempotent(self):
        st.session_state.pilot_session_id = "pilot-test"
        st.session_state.pilot_current_question_log_id = "question-1"
        st.session_state.pilot_flagged_question_log_ids = []
        question = {
            "skill": "phrase_translation",
            "question_type": "phrase_meaning",
            "question": "What does this phrase mean?",
            "selected_word": "ויאמר אלהים",
            "pasuk": "ויאמר אלהים יהי אור",
        }

        with patch.object(pilot_logging, "append_pilot_event", return_value=True) as append_mock:
            self.assertTrue(pilot_logging.mark_current_question_unclear(question))
            self.assertFalse(pilot_logging.mark_current_question_unclear(question))

        self.assertTrue(pilot_logging.question_is_flagged_unclear())
        self.assertEqual(append_mock.call_count, 1)

    def test_mark_current_question_unclear_saves_optional_student_note(self):
        st.session_state.pilot_session_id = "pilot-test"
        st.session_state.pilot_current_question_log_id = "question-2"
        st.session_state.pilot_flagged_question_log_ids = []
        question = {
            "skill": "phrase_translation",
            "question_type": "phrase_meaning",
            "question": "What does this phrase mean?",
            "selected_word": "וַיֹּאמֶר אֱלֹהִים",
            "pasuk": "וַיֹּאמֶר אֱלֹהִים יְהִי אוֹר",
        }
        captured_events = []

        with patch.object(
            pilot_logging,
            "append_pilot_event",
            side_effect=lambda event, **kwargs: captured_events.append(event) or True,
        ):
            self.assertTrue(
                pilot_logging.mark_current_question_unclear(
                    question,
                    note_text="wording felt confusing",
                )
            )

        self.assertEqual(len(captured_events), 1)
        self.assertEqual(captured_events[0]["student_note"], "wording felt confusing")
        self.assertEqual(
            st.session_state.get("pilot_flagged_question_notes", {}).get("question-2"),
            "wording felt confusing",
        )

    def test_mark_current_question_unclear_allows_blank_student_note(self):
        st.session_state.pilot_session_id = "pilot-test"
        st.session_state.pilot_current_question_log_id = "question-3"
        st.session_state.pilot_flagged_question_log_ids = []
        question = {
            "skill": "translation",
            "question_type": "word_meaning",
            "question": "What does this word mean?",
            "selected_word": "בְּרֵאשִׁית",
            "pasuk": active_pesukim_records()[0]["text"],
        }
        captured_events = []

        with patch.object(
            pilot_logging,
            "append_pilot_event",
            side_effect=lambda event, **kwargs: captured_events.append(event) or True,
        ):
            self.assertTrue(pilot_logging.mark_current_question_unclear(question, note_text="   "))

        self.assertEqual(len(captured_events), 1)
        self.assertIsNone(captured_events[0].get("student_note"))

    def test_record_teacher_flag_label_and_note_persist_to_export_queue(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pilot_events.jsonl"
            events = [
                {
                    "event_type": "question_flagged",
                    "timestamp_utc": "2026-04-19T12:00:06+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_9",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "word_meaning",
                    "question_text": "What does this word mean?",
                    "selected_word": "בראשית",
                    "flag": "unclear",
                    "student_note": "translation felt unclear",
                },
            ]
            path.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            self.assertTrue(
                pilot_logging.record_teacher_flag_label(
                    "q1",
                    "unclear wording",
                    session_id="pilot-a",
                    path=path,
                )
            )
            self.assertTrue(
                pilot_logging.record_teacher_flag_note(
                    "q1",
                    "Need cleaner distractors for this item.",
                    session_id="pilot-a",
                    path=path,
                )
            )
            export = pilot_logging.build_pilot_review_export(max_sessions=5, path=path)

        self.assertEqual(export["teacher_flag_labels"], list(pilot_logging.TEACHER_FLAG_LABELS))
        queue_item = export["flagged_review_queue"][0]
        self.assertEqual(queue_item["question_log_id"], "q1")
        self.assertEqual(queue_item["teacher_label"], "unclear wording")
        self.assertEqual(queue_item["teacher_note"], "Need cleaner distractors for this item.")
        self.assertEqual(queue_item["student_note"], "translation felt unclear")
        self.assertEqual(queue_item["session_id"], "pilot-a")

    def test_build_pilot_review_export_summarizes_recent_sessions_and_review_queue(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pilot_events.jsonl"
            events = [
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-19T12:00:00+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_9",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "word_meaning",
                    "served_status": "served",
                },
                {
                    "event_type": "question_answered",
                    "timestamp_utc": "2026-04-19T12:00:05+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_9",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "word_meaning",
                    "is_correct": True,
                    "response_time_ms": 4200.0,
                },
                {
                    "event_type": "question_flagged",
                    "timestamp_utc": "2026-04-19T12:00:06+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_9",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "word_meaning",
                    "question_text": "What does this word mean?",
                    "selected_word": "בראשית",
                    "flag": "unclear",
                    "student_note": "Too many close answers",
                },
                {
                    "event_type": "question_labeled",
                    "timestamp_utc": "2026-04-19T12:00:07+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_9",
                    "teacher_label": "bad distractors",
                },
                {
                    "event_type": "question_noted",
                    "timestamp_utc": "2026-04-19T12:00:08+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_9",
                    "note_role": "teacher",
                    "note_text": "Tighten the distractor set for this cohort.",
                },
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-19T11:00:00+00:00",
                    "session_id": "pilot-b",
                    "question_log_id": "q2",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_9",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": False,
                    "practice_type": "Practice Mode",
                    "pasuk_ref": {"label": pilot_logging.OUTSIDE_ACTIVE_PARSED_LABEL, "pasuk_id": None},
                    "scope_membership": "outside_active_parsed",
                    "question_type": "subject_identification",
                    "question_text": "Who is doing the action?",
                    "selected_word": "unknown",
                    "served_status": "served",
                },
                {
                    "event_type": "question_flagged",
                    "timestamp_utc": "2026-04-19T11:00:03+00:00",
                    "session_id": "pilot-b",
                    "question_log_id": "q2",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_9",
                    "pasuk_ref": {"label": pilot_logging.OUTSIDE_ACTIVE_PARSED_LABEL, "pasuk_id": None},
                    "scope_membership": "outside_active_parsed",
                    "question_type": "subject_identification",
                    "question_text": "Who is doing the action?",
                    "selected_word": "unknown",
                    "flag": "unclear",
                },
            ]
            path.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            export = pilot_logging.build_pilot_review_export(max_sessions=5, path=path)

        self.assertEqual(export["session_count"], 2)
        self.assertEqual(
            export["accounting_model"],
            {
                "served_question_types": "question_served events only",
                "answered_question_types": "question_answered events only",
                "flagged_unclear_question_types": "question_flagged events with flag=unclear only",
            },
        )
        self.assertEqual(export["teacher_flag_labels"], list(pilot_logging.TEACHER_FLAG_LABELS))

        latest = export["sessions"][0]
        self.assertEqual(latest["session_id"], "pilot-a")
        self.assertEqual(latest["served_questions"], 1)
        self.assertEqual(latest["answered_questions"], 1)
        self.assertEqual(latest["correct_answers"], 1)
        self.assertEqual(latest["flagged_unclear"], 1)
        self.assertEqual(latest["average_response_time_ms"], 4200.0)
        self.assertEqual(latest["practice_types"], {"Learn Mode": 1})
        self.assertEqual(latest["session_scope_status"], "trusted_active_scope")
        self.assertEqual(latest["served_question_types"], {"word_meaning": 1})
        self.assertEqual(latest["answered_question_types"], {"word_meaning": 1})
        self.assertEqual(latest["flagged_unclear_question_types"], {"word_meaning": 1})
        self.assertEqual(latest["served_question_type_total"], latest["served_questions"])
        self.assertEqual(latest["answered_question_type_total"], latest["answered_questions"])
        self.assertEqual(latest["flagged_unclear_question_type_total"], latest["flagged_unclear"])
        self.assertEqual(latest["served_pasuk_refs"], {"Bereishis 1:1": 1})
        self.assertEqual(latest["served_active_scope_questions"], 1)
        self.assertEqual(latest["served_outside_active_scope_questions"], 0)
        self.assertEqual(latest["recent_unclear_flags"][0]["question_log_id"], "q1")
        self.assertEqual(latest["recent_unclear_flags"][0]["session_id"], "pilot-a")
        self.assertEqual(latest["recent_unclear_flags"][0]["student_note"], "Too many close answers")

        older = export["sessions"][1]
        self.assertEqual(older["session_id"], "pilot-b")
        self.assertEqual(older["session_scope_status"], "outside_active_scope_detected")
        self.assertFalse(older["trusted_active_scope_session"])
        self.assertEqual(older["served_question_types"], {"subject_identification": 1})
        self.assertEqual(older["answered_question_types"], {})
        self.assertEqual(older["flagged_unclear_question_types"], {"subject_identification": 1})
        self.assertEqual(older["served_outside_active_scope_questions"], 1)
        self.assertEqual(
            older["recent_scope_issues"][0]["pasuk_ref"],
            pilot_logging.OUTSIDE_ACTIVE_PARSED_LABEL,
        )

        queue = export["flagged_review_queue"]
        self.assertEqual(len(queue), 2)
        queue_by_id = {item["question_log_id"]: item for item in queue}
        self.assertEqual(queue_by_id["q1"]["pasuk_ref"], "Bereishis 1:1")
        self.assertEqual(queue_by_id["q1"]["teacher_label"], "bad distractors")
        self.assertEqual(queue_by_id["q1"]["teacher_note"], "Tighten the distractor set for this cohort.")
        self.assertEqual(queue_by_id["q1"]["student_note"], "Too many close answers")
        self.assertEqual(queue_by_id["q1"]["question_text"], "What does this word mean?")
        self.assertEqual(queue_by_id["q2"]["session_id"], "pilot-b")
        self.assertEqual(queue_by_id["q2"]["pasuk_ref"], pilot_logging.OUTSIDE_ACTIVE_PARSED_LABEL)

        summary = export["summary"]
        self.assertEqual(
            summary["dominant_served_question_families"],
            {"word_meaning": 1, "subject_identification": 1},
        )
        self.assertEqual(summary["top_repeated_flagged_items"][0]["question_type"], "subject_identification")
        self.assertEqual(
            {item["session_id"] for item in summary["highest_unclear_rate_sessions"][:2]},
            {"pilot-a", "pilot-b"},
        )
        self.assertEqual(summary["trusted_scope_violations"][0]["session_id"], "pilot-b")

    def test_export_loads_older_flagged_entries_without_notes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pilot_events.jsonl"
            events = [
                {
                    "event_type": "question_flagged",
                    "timestamp_utc": "2026-04-19T12:00:06+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_9",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "word_meaning",
                    "question_text": "What does this word mean?",
                    "selected_word": "בראשית",
                    "flag": "unclear",
                },
            ]
            path.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            export = pilot_logging.build_pilot_review_export(max_sessions=5, path=path)

        queue_item = export["flagged_review_queue"][0]
        self.assertIsNone(queue_item.get("student_note"))
        self.assertIsNone(queue_item.get("teacher_note"))


if __name__ == "__main__":
    unittest.main()
