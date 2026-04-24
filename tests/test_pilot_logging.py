import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import streamlit as st

from assessment_scope import active_pesukim_records
from runtime import pilot_logging


class FakeQueryParams(dict):
    pass


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
        self.assertEqual(append_mock.call_count, 3)
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

        served_events = [event for event in captured_events if event.get("event_type") == "question_served"]
        self.assertEqual(len(served_events), 1)
        served_event = served_events[0]
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

        served_events = [event for event in captured_events if event.get("event_type") == "question_served"]
        self.assertEqual(len(served_events), 1)
        served_event = served_events[0]
        self.assertEqual(served_event["scope_membership"], "outside_active_parsed")
        self.assertEqual(
            served_event["pasuk_ref"]["label"],
            pilot_logging.OUTSIDE_ACTIVE_PARSED_LABEL,
        )
        self.assertFalse(served_event["trusted_active_scope_session"])
        self.assertFalse(st.session_state.get("pilot_trusted_active_scope_session"))

    def test_build_question_served_event_includes_dikduk_foundation_fields(self):
        active_record = active_pesukim_records()[0]
        question = {
            "skill": "translation",
            "question_type": "word_meaning",
            "question": "What does this word mean?",
            "selected_word": "בְּרֵאשִׁית",
            "correct_answer": "in the beginning",
            "pasuk": active_record["text"],
            "pasuk_id": active_record["pasuk_id"],
            "dikduk_foundation": {
                "used": True,
                "repeat_key": "vocab:vocab_bereshit",
                "pattern_ids": ["pat_verb_future_tav_ambiguous"],
                "rule_ids": ["rule_verb_future_tav_ambiguous"],
                "confusion_pattern_ids": ["conf_tav_future_ambiguity"],
                "weak_standalone_translation": False,
                "ambiguous_without_context": True,
            },
        }

        event = pilot_logging.build_question_served_event(
            question,
            session_id="pilot-test",
            question_log_id="q-foundation",
        )

        self.assertTrue(event["dikduk_foundation_used"])
        self.assertEqual(event["dikduk_foundation_repeat_key"], "vocab:vocab_bereshit")
        self.assertEqual(event["dikduk_foundation_pattern_ids"], ["pat_verb_future_tav_ambiguous"])
        self.assertEqual(event["dikduk_foundation_rule_ids"], ["rule_verb_future_tav_ambiguous"])
        self.assertEqual(event["dikduk_foundation_confusion_pattern_ids"], ["conf_tav_future_ambiguity"])
        self.assertFalse(event["dikduk_foundation_weak_standalone_translation"])
        self.assertTrue(event["dikduk_foundation_ambiguous_without_context"])

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
        self.assertEqual(latest["session_origin"], "legacy_or_inferred")
        self.assertFalse(latest["is_shell_session"])
        self.assertTrue(latest["is_substantive_session"])
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
        self.assertEqual(older["session_origin"], "legacy_or_inferred")
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

    def test_resolve_pilot_event_log_path_supports_env_override(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            configured_path = Path(tmpdir) / "isolated_events.jsonl"
            explicit_path = Path(tmpdir) / "explicit_events.jsonl"

            with patch.dict(
                "os.environ",
                {pilot_logging.PILOT_EVENT_LOG_ENV_VAR: str(configured_path)},
                clear=False,
            ):
                self.assertEqual(
                    pilot_logging.resolve_pilot_event_log_path(),
                    configured_path,
                )
                self.assertEqual(
                    pilot_logging.resolve_pilot_event_log_path(explicit_path),
                    explicit_path,
                )

    def test_write_pilot_review_export_reads_only_specified_input_log(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            first_log = base / "first.jsonl"
            second_log = base / "second.jsonl"
            output_path = base / "review.json"

            first_events = [
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T10:00:00+00:00",
                    "session_id": "pilot-one",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "served_status": "served",
                },
            ]
            second_events = [
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T11:00:00+00:00",
                    "session_id": "pilot-two",
                    "question_log_id": "q2",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Practice Mode",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "shoresh",
                    "served_status": "served",
                },
            ]
            first_log.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in first_events) + "\n",
                encoding="utf-8",
            )
            second_log.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in second_events) + "\n",
                encoding="utf-8",
            )

            pilot_logging.write_pilot_review_export(output_path, path=second_log, max_sessions=5)
            export = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(export["session_count"], 1)
        self.assertEqual(export["sessions"][0]["session_id"], "pilot-two")
        self.assertEqual(export["log_path"], str(second_log))

    def test_build_isolated_pilot_log_path_and_file_creation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            runs_dir = Path(tmpdir)
            first_path = pilot_logging.build_isolated_pilot_log_path("Fresh Check", base_dir=runs_dir)
            created_path = pilot_logging.ensure_pilot_log_file(first_path)
            second_path = pilot_logging.build_isolated_pilot_log_path("Fresh Check", base_dir=runs_dir)

            self.assertEqual(created_path, first_path)
            self.assertTrue(created_path.exists())
            self.assertEqual(created_path.read_text(encoding="utf-8"), "")
            self.assertNotEqual(first_path, second_path)
            self.assertIn("fresh-check", first_path.stem)

    def test_refresh_resume_keeps_same_pilot_session_id(self):
        query_params = FakeQueryParams()
        lifecycle_events = []

        with patch.object(
            pilot_logging,
            "_pilot_query_params_proxy",
            return_value=query_params,
        ), patch.object(
            pilot_logging,
            "append_pilot_event",
            side_effect=lambda event, **kwargs: lifecycle_events.append(event) or True,
        ):
            first_session_id = pilot_logging.ensure_pilot_session_id()
            st.session_state.clear()
            resumed_session_id = pilot_logging.ensure_pilot_session_id()

        self.assertEqual(first_session_id, resumed_session_id)
        self.assertEqual(query_params[pilot_logging.PILOT_SESSION_QUERY_PARAM], first_session_id)
        self.assertEqual(
            [event.get("lifecycle") for event in lifecycle_events if event.get("event_type") == "session_lifecycle"],
            ["started", "resumed"],
        )

    def test_repeated_reruns_do_not_generate_new_pilot_session_id(self):
        query_params = FakeQueryParams()
        lifecycle_events = []

        with patch.object(
            pilot_logging,
            "_pilot_query_params_proxy",
            return_value=query_params,
        ), patch.object(
            pilot_logging,
            "append_pilot_event",
            side_effect=lambda event, **kwargs: lifecycle_events.append(event) or True,
        ):
            first_session_id = pilot_logging.ensure_pilot_session_id()
            second_session_id = pilot_logging.ensure_pilot_session_id()
            third_session_id = pilot_logging.ensure_pilot_session_id()

        self.assertEqual(first_session_id, second_session_id)
        self.assertEqual(second_session_id, third_session_id)
        self.assertEqual(
            [event.get("lifecycle") for event in lifecycle_events if event.get("event_type") == "session_lifecycle"],
            ["started"],
        )

    def test_answering_multiple_questions_in_one_sitting_stays_in_one_session(self):
        first_record = active_pesukim_records()[0]
        second_record = active_pesukim_records()[1]
        first_question = {
            "skill": "translation",
            "question_type": "translation",
            "question": "What does this word mean?",
            "selected_word": "בְּרֵאשִׁית",
            "correct_answer": "in the beginning",
            "pasuk": first_record["text"],
            "pasuk_id": first_record["pasuk_id"],
        }
        second_question = {
            "skill": "shoresh",
            "question_type": "shoresh",
            "question": "What is the shoresh?",
            "selected_word": "בָּרָא",
            "correct_answer": "ברא",
            "pasuk": second_record["text"],
            "pasuk_id": second_record["pasuk_id"],
        }
        events = []

        with patch.object(
            pilot_logging,
            "append_pilot_event",
            side_effect=lambda event, **kwargs: events.append(event) or True,
        ):
            pilot_logging.sync_pilot_served_question(first_question, practice_type="Learn Mode")
            pilot_logging.record_pilot_answer(first_question, "in the beginning", True)
            pilot_logging.sync_pilot_served_question(second_question, practice_type="Learn Mode")
            pilot_logging.record_pilot_answer(second_question, "ברא", True)

        session_ids = {
            event.get("session_id")
            for event in events
            if event.get("event_type") in {"question_served", "question_answered"}
        }
        self.assertEqual(len(session_ids), 1)

    def test_true_restart_creates_new_pilot_session_id(self):
        query_params = FakeQueryParams()
        lifecycle_events = []

        with patch.object(
            pilot_logging,
            "_pilot_query_params_proxy",
            return_value=query_params,
        ), patch.object(
            pilot_logging,
            "append_pilot_event",
            side_effect=lambda event, **kwargs: lifecycle_events.append(event) or True,
        ):
            first_session_id = pilot_logging.ensure_pilot_session_id()
            self.assertTrue(pilot_logging.end_pilot_session(reason="restart_assessment"))
            st.session_state.clear()
            second_session_id = pilot_logging.ensure_pilot_session_id()

        self.assertNotEqual(first_session_id, second_session_id)
        self.assertEqual(query_params[pilot_logging.PILOT_SESSION_QUERY_PARAM], second_session_id)
        self.assertEqual(
            [event.get("lifecycle") for event in lifecycle_events if event.get("event_type") == "session_lifecycle"],
            ["started", "ended", "started"],
        )

    def test_export_marks_empty_startup_sessions_as_shells_not_substantive_runs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pilot_events.jsonl"
            events = [
                {
                    "event_type": "session_lifecycle",
                    "timestamp_utc": "2026-04-21T10:00:00+00:00",
                    "session_id": "pilot-shell",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "lifecycle": "started",
                    "reason": "runtime_initialized",
                },
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T10:00:01+00:00",
                    "session_id": "pilot-shell",
                    "question_log_id": "q-shell",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "served_status": "served",
                },
                {
                    "event_type": "session_lifecycle",
                    "timestamp_utc": "2026-04-21T10:05:00+00:00",
                    "session_id": "pilot-real",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "lifecycle": "started",
                    "reason": "runtime_initialized",
                },
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T10:05:01+00:00",
                    "session_id": "pilot-real",
                    "question_log_id": "q-real",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "shoresh",
                    "served_status": "served",
                },
                {
                    "event_type": "question_answered",
                    "timestamp_utc": "2026-04-21T10:05:10+00:00",
                    "session_id": "pilot-real",
                    "question_log_id": "q-real",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "shoresh",
                    "is_correct": True,
                    "response_time_ms": 3200.0,
                },
            ]
            path.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            export = pilot_logging.build_pilot_review_export(max_sessions=5, path=path)

        sessions_by_id = {session["session_id"]: session for session in export["sessions"]}
        self.assertEqual(export["session_count"], 2)
        self.assertEqual(export["substantive_session_count"], 1)
        self.assertEqual(export["shell_session_count"], 1)
        self.assertEqual(export["summary"]["substantive_session_count"], 1)
        self.assertEqual(export["summary"]["shell_session_count"], 1)
        self.assertTrue(sessions_by_id["pilot-shell"]["is_shell_session"])
        self.assertEqual(sessions_by_id["pilot-shell"]["shell_session_reason"], "single_question_no_answer")
        self.assertFalse(sessions_by_id["pilot-shell"]["is_substantive_session"])
        self.assertTrue(sessions_by_id["pilot-real"]["is_substantive_session"])

    def test_build_pilot_review_export_surfaces_fresh_run_validation_signals(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "runs" / "pilot_session_events_isolated.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            events = [
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T12:00:00+00:00",
                    "session_id": "pilot-one",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "selected_word": "×‘Ö¼Ö°×¨Öµ××©×Ö´×™×ª",
                    "question_text": "What does ×‘Ö¼Ö°×¨Öµ××©×Ö´×™×ª mean?",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": True,
                    "debug_rejection_counts": {
                        "invalid_tense_target": 2,
                        "duplicate_distractors": 1,
                    },
                },
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T12:03:00+00:00",
                    "session_id": "pilot-two",
                    "question_log_id": "q2",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "identify_tense",
                    "selected_word": "×•Ö·×™Ö¼Ö¹××žÖ¶×¨",
                    "question_text": "What form is shown?",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": False,
                    "debug_rejection_counts": {
                        "invalid_tense_target": 1,
                    },
                },
                {
                    "event_type": "question_flagged",
                    "timestamp_utc": "2026-04-21T12:03:30+00:00",
                    "session_id": "pilot-two",
                    "question_log_id": "q2",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "identify_tense",
                    "question_text": "What form is shown?",
                    "selected_word": "×•Ö·×™Ö¼Ö¹××žÖ¶×¨",
                    "flag": "unclear",
                },
            ]
            path.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            export = pilot_logging.build_pilot_review_export(max_sessions=5, path=path)

        self.assertEqual(export["review_window"]["source_log_is_isolated_run"], True)
        self.assertEqual(export["review_window"]["fresh_run_only"], True)
        self.assertEqual(export["review_scope_id"], "local_parsed_bereishis_1_1_to_2_17")
        warning_codes = {item["code"] for item in export["review_window"]["warnings"]}
        if pilot_logging.ACTIVE_ASSESSMENT_SCOPE == "local_parsed_bereishis_1_1_to_2_17":
            self.assertEqual(export["review_window"]["warnings"], [])
        else:
            self.assertEqual(warning_codes, {"runtime_scope_differs_from_review_scope"})
        self.assertEqual(export["summary"]["served_without_validation_signals"]["served_with_validation_flag"], 1)
        self.assertEqual(export["summary"]["served_without_validation_signals"]["served_without_validation_flag"], 1)
        self.assertEqual(
            export["summary"]["top_pre_serve_rejection_codes"][0],
            {"code": "invalid_tense_target", "count": 3},
        )
        self.assertEqual(
            export["summary"]["top_served_question_families"],
            {"translation": 1, "identify_tense": 1},
        )
        self.assertEqual(
            export["summary"]["top_flagged_unclear_items"][0]["question_type"],
            "identify_tense",
        )

    def test_build_pilot_review_export_can_filter_by_session_start_scope_and_trusted_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pilot_events.jsonl"
            events = [
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T10:00:00+00:00",
                    "session_id": "pilot-old",
                    "question_log_id": "q-old",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": True,
                },
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T12:00:00+00:00",
                    "session_id": "pilot-keep",
                    "question_log_id": "q-keep",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "shoresh",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": True,
                },
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T13:00:00+00:00",
                    "session_id": "pilot-open",
                    "question_log_id": "q-open",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_17",
                    "trusted_scope_mode": "open_pilot_scope",
                    "trusted_active_scope_requested": False,
                    "trusted_active_scope_session": False,
                    "practice_type": "Practice Mode",
                    "pasuk_ref": {"label": "Bereishis 1:3", "pasuk_id": "bereishis_1_3"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": True,
                },
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T14:00:00+00:00",
                    "session_id": "pilot-other-scope",
                    "question_log_id": "q-other",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_25",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 2:20", "pasuk_id": "bereishis_2_20"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": True,
                },
            ]
            path.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            export = pilot_logging.build_pilot_review_export(
                max_sessions=5,
                path=path,
                session_start_since="2026-04-21T11:00:00+00:00",
                session_start_until="2026-04-21T13:30:00+00:00",
                scope_id="local_parsed_bereishis_1_1_to_2_17",
                trusted_active_scope_only=True,
            )

        self.assertEqual(export["session_count"], 1)
        self.assertEqual(export["sessions"][0]["session_id"], "pilot-keep")
        self.assertEqual(export["review_window"]["source_session_count"], 4)
        self.assertEqual(export["review_window"]["included_session_count"], 1)
        self.assertEqual(export["review_window"]["excluded_event_count"], 3)
        warning_codes = {item["code"] for item in export["review_window"]["warnings"]}
        self.assertIn("source_log_not_isolated", warning_codes)
        self.assertIn("source_log_multiple_scope_ids", warning_codes)
        self.assertIn("filters_excluded_source_events", warning_codes)
        self.assertIn("review_filters_applied", warning_codes)
        if pilot_logging.ACTIVE_ASSESSMENT_SCOPE != "local_parsed_bereishis_1_1_to_2_17":
            self.assertIn("runtime_scope_differs_from_review_scope", warning_codes)
        self.assertEqual(export["review_window"]["scope_id"], "local_parsed_bereishis_1_1_to_2_17")
        self.assertEqual(export["review_scope_id"], "local_parsed_bereishis_1_1_to_2_17")
        self.assertTrue(export["review_window"]["trusted_active_scope_only"])

    def test_build_pilot_review_export_can_limit_to_latest_session_only(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pilot_events.jsonl"
            events = [
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T10:00:00+00:00",
                    "session_id": "pilot-old",
                    "question_log_id": "q-old",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_25",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "selected_word": "בְּרֵאשִׁית",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": True,
                },
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T12:00:00+00:00",
                    "session_id": "pilot-new",
                    "question_log_id": "q-new",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_25",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "shoresh",
                    "selected_word": "וְהָאָרֶץ",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": True,
                },
            ]
            path.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            export = pilot_logging.build_pilot_review_export(
                max_sessions=5,
                path=path,
                latest_session_only=True,
            )

        self.assertEqual(export["session_count"], 1)
        self.assertEqual(export["sessions"][0]["session_id"], "pilot-new")
        self.assertTrue(export["review_window"]["latest_session_only"])
        self.assertEqual(export["review_window"]["latest_included_session_ids"], ["pilot-new"])
        warning_codes = {item["code"] for item in export["review_window"]["warnings"]}
        self.assertIn("review_filters_applied", warning_codes)
        self.assertIn("latest_session_only_applied", warning_codes)

    def test_write_pilot_review_export_forwards_latest_session_only_filter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pilot_events.jsonl"
            output_path = Path(tmpdir) / "review.json"
            events = [
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T10:00:00+00:00",
                    "session_id": "pilot-old",
                    "question_log_id": "q-old",
                    "scope_id": "local_parsed_bereishis_1_1_to_3_8",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:1", "pasuk_id": "bereishis_1_1"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": True,
                },
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T12:00:00+00:00",
                    "session_id": "pilot-new",
                    "question_log_id": "q-new",
                    "scope_id": "local_parsed_bereishis_1_1_to_3_8",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "shoresh",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": True,
                },
            ]
            path.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            pilot_logging.write_pilot_review_export(
                output_path,
                path=path,
                max_sessions=5,
                latest_session_only=True,
            )
            export = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(export["session_count"], 1)
        self.assertEqual(export["sessions"][0]["session_id"], "pilot-new")
        self.assertTrue(export["review_window"]["latest_session_only"])

    def test_build_pilot_review_export_includes_compact_release_review_summary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pilot_events.jsonl"
            events = [
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T12:00:00+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q1",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_25",
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
                {
                    "event_type": "question_served",
                    "timestamp_utc": "2026-04-21T12:01:00+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q2",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_25",
                    "trusted_scope_mode": "trusted_active_scope",
                    "trusted_active_scope_requested": True,
                    "trusted_active_scope_session": True,
                    "practice_type": "Learn Mode",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "selected_word": "אֱלֹקִים",
                    "correct_answer": "God",
                    "served_status": "served",
                    "debug_pre_serve_validation_passed": False,
                    "debug_rejection_counts": {"recent_target_repeat": 2},
                },
                {
                    "event_type": "question_flagged",
                    "timestamp_utc": "2026-04-21T12:01:30+00:00",
                    "session_id": "pilot-a",
                    "question_log_id": "q2",
                    "scope_id": "local_parsed_bereishis_1_1_to_2_25",
                    "pasuk_ref": {"label": "Bereishis 1:2", "pasuk_id": "bereishis_1_2"},
                    "scope_membership": "active_parsed",
                    "question_type": "translation",
                    "question_text": "What does אֱלֹקִים mean?",
                    "selected_word": "אֱלֹקִים",
                    "flag": "unclear",
                },
            ]
            path.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            export = pilot_logging.build_pilot_review_export(max_sessions=5, path=path)

        compact = export["release_review_summary"]
        self.assertEqual(compact["scope_id"], "local_parsed_bereishis_1_1_to_2_25")
        self.assertEqual(compact["session_count"], 1)
        self.assertEqual(compact["served_without_validation_flag"], 1)
        self.assertEqual(compact["unclear_flag_count"], 1)
        self.assertEqual(compact["top_served_question_families"], {"translation": 2})
        self.assertEqual(compact["top_pre_serve_rejection_codes"], [{"code": "recent_target_repeat", "count": 2}])
        self.assertEqual(
            compact["supported_practice_modes"],
            ["Learn Mode", "Practice Mode", "Pasuk Flow"],
        )
        self.assertEqual(
            compact["practice_mode_counts"],
            {"Learn Mode": 2, "Practice Mode": 0, "Pasuk Flow": 0},
        )
        self.assertEqual(compact["observed_practice_modes"], ["Learn Mode"])
        self.assertEqual(compact["missing_practice_modes"], ["Practice Mode", "Pasuk Flow"])
        self.assertFalse(compact["supported_mode_coverage_complete"])
        self.assertEqual(compact["repeated_target_feel"]["repeated_target_warning_count"], 1)
        self.assertEqual(compact["repeated_target_feel"]["top_repeated_targets"][0]["target"], "אֱלֹקִים")
        self.assertIn("source_log_not_isolated", compact["warning_codes"])


if __name__ == "__main__":
    unittest.main()
