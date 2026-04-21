from __future__ import annotations

import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from time import perf_counter
from uuid import uuid4

import streamlit as st

from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    active_pasuk_record_for_question,
    active_pasuk_record_for_text,
    active_pasuk_ref_payload,
    data_path,
)


PILOT_EVENT_LOG_ENV_VAR = "CHUMASH_PILOT_EVENT_LOG_PATH"
DEFAULT_PILOT_EVENT_LOG_PATH = data_path("pilot/pilot_session_events.jsonl")
PILOT_EVENT_LOG_PATH = DEFAULT_PILOT_EVENT_LOG_PATH
PILOT_SESSION_QUERY_PARAM = "pilot_session_id"
TRUSTED_ACTIVE_SCOPE_MODE = "trusted_active_scope"
OUTSIDE_ACTIVE_PARSED_LABEL = "not in active parsed dataset"
TEACHER_FLAG_LABELS = (
    "wrong morphology",
    "bad distractors",
    "too repetitive",
    "wrong pasuk",
    "unclear wording",
    "other",
)
STUDENT_FLAG_NOTE_MAX_LENGTH = 120
TEACHER_FLAG_NOTE_MAX_LENGTH = 280


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def resolve_pilot_event_log_path(path=None):
    if path:
        return Path(path)
    configured_path = os.environ.get(PILOT_EVENT_LOG_ENV_VAR, "").strip()
    if configured_path:
        return Path(configured_path)
    return DEFAULT_PILOT_EVENT_LOG_PATH


def _pilot_run_slug(label=""):
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", str(label or "").strip()).strip("-").lower()
    return cleaned[:40]


def build_isolated_pilot_log_path(label="", *, base_dir=None):
    runs_dir = Path(base_dir) if base_dir else data_path("pilot/runs")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = _pilot_run_slug(label)
    stem = f"pilot_session_events_{stamp}"
    if slug:
        stem = f"{stem}_{slug}"
    path = runs_dir / f"{stem}.jsonl"
    suffix = 1
    while path.exists():
        path = runs_dir / f"{stem}_{suffix}.jsonl"
        suffix += 1
    return path


def ensure_pilot_log_file(path=None):
    resolved_path = resolve_pilot_event_log_path(path)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    if not resolved_path.exists():
        resolved_path.write_text("", encoding="utf-8")
    return resolved_path


def write_pilot_review_export(
    output_path,
    *,
    max_sessions=5,
    path=None,
    session_start_since=None,
    session_start_until=None,
    scope_id=None,
    trusted_active_scope_only=False,
):
    resolved_output_path = Path(output_path)
    export = build_pilot_review_export(
        max_sessions=max_sessions,
        path=path,
        session_start_since=session_start_since,
        session_start_until=session_start_until,
        scope_id=scope_id,
        trusted_active_scope_only=trusted_active_scope_only,
    )
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_output_path.write_text(
        json.dumps(export, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return resolved_output_path


def new_pilot_session_id():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"pilot-{timestamp}-{uuid4().hex[:8]}"


def _pilot_query_params_proxy():
    try:
        return st.query_params
    except Exception:
        return None


def _pilot_query_param_value(key):
    query_params = _pilot_query_params_proxy()
    if query_params is None:
        return None
    try:
        value = query_params.get(key)
    except Exception:
        return None
    if isinstance(value, (list, tuple)):
        value = value[0] if value else None
    cleaned = str(value or "").strip()
    return cleaned or None


def _set_pilot_query_param(key, value):
    query_params = _pilot_query_params_proxy()
    if query_params is None:
        return False
    try:
        query_params[key] = str(value)
    except Exception:
        return False
    return True


def _clear_pilot_query_param(key):
    query_params = _pilot_query_params_proxy()
    if query_params is None:
        return False
    try:
        if key in query_params:
            del query_params[key]
            return True
    except Exception:
        try:
            query_params.pop(key, None)
            return True
        except Exception:
            return False
    return False


def persisted_pilot_session_id():
    return _pilot_query_param_value(PILOT_SESSION_QUERY_PARAM)


def persist_pilot_session_id(session_id):
    if not session_id:
        return False
    return _set_pilot_query_param(PILOT_SESSION_QUERY_PARAM, session_id)


def clear_pilot_session_persistence():
    return _clear_pilot_query_param(PILOT_SESSION_QUERY_PARAM)


def build_session_lifecycle_event(*, session_id, lifecycle, reason=""):
    return {
        "event_type": "session_lifecycle",
        "timestamp_utc": utc_now_iso(),
        "session_id": session_id,
        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "lifecycle": lifecycle,
        "reason": reason,
        "trusted_scope_mode": pilot_scope_mode(),
        "trusted_active_scope_requested": trusted_active_scope_requested(),
        "trusted_active_scope_session": trusted_active_scope_session(),
    }


def ensure_pilot_session_id():
    session_id = st.session_state.get("pilot_session_id")
    st.session_state.setdefault("pilot_scope_mode", TRUSTED_ACTIVE_SCOPE_MODE)
    st.session_state.setdefault("pilot_trusted_active_scope_session", True)
    st.session_state.setdefault("pilot_session_origin", "")
    if session_id:
        return session_id
    persisted_session_id = persisted_pilot_session_id()
    if persisted_session_id:
        st.session_state.pilot_session_id = persisted_session_id
        st.session_state.pilot_trusted_active_scope_session = True
        st.session_state.pilot_session_origin = "resumed"
        append_pilot_event(
            build_session_lifecycle_event(
                session_id=persisted_session_id,
                lifecycle="resumed",
                reason="browser_refresh_or_streamlit_reconnect",
            )
        )
        return persisted_session_id
    session_id = new_pilot_session_id()
    st.session_state.pilot_session_id = session_id
    st.session_state.pilot_trusted_active_scope_session = True
    st.session_state.pilot_session_origin = "started"
    persist_pilot_session_id(session_id)
    append_pilot_event(
        build_session_lifecycle_event(
            session_id=session_id,
            lifecycle="started",
            reason="runtime_initialized",
        )
    )
    return session_id


def end_pilot_session(*, reason="explicit_restart"):
    session_id = st.session_state.get("pilot_session_id") or persisted_pilot_session_id()
    if not session_id:
        clear_pilot_session_persistence()
        return False
    append_pilot_event(
        build_session_lifecycle_event(
            session_id=session_id,
            lifecycle="ended",
            reason=reason,
        )
    )
    clear_pilot_session_persistence()
    st.session_state.pilot_session_id = None
    st.session_state.pilot_session_origin = ""
    st.session_state.pilot_current_question_signature = ""
    st.session_state.pilot_current_question_log_id = None
    st.session_state.pilot_current_question_started_at = None
    return True


def pilot_scope_mode():
    return st.session_state.get("pilot_scope_mode", TRUSTED_ACTIVE_SCOPE_MODE)


def trusted_active_scope_requested():
    return pilot_scope_mode() == TRUSTED_ACTIVE_SCOPE_MODE


def trusted_active_scope_session():
    if not trusted_active_scope_requested():
        return False
    return bool(st.session_state.get("pilot_trusted_active_scope_session", True))


def outside_active_parsed_ref():
    return {
        "label": OUTSIDE_ACTIVE_PARSED_LABEL,
        "pasuk_id": None,
    }


def active_pasuk_ref_for_text(pasuk_text):
    record = active_pasuk_record_for_text(pasuk_text)
    if not record:
        return outside_active_parsed_ref()
    return active_pasuk_ref_payload(record)


def active_pasuk_ref_for_question(question):
    record = active_pasuk_record_for_question(question)
    if not record:
        return outside_active_parsed_ref()
    return active_pasuk_ref_payload(record)


def scope_membership_for_ref(pasuk_ref):
    if (pasuk_ref or {}).get("pasuk_id"):
        return "active_parsed"
    return "outside_active_parsed"


def note_trusted_scope_violation():
    if trusted_active_scope_requested():
        st.session_state.pilot_trusted_active_scope_session = False


def question_log_signature(question, *, practice_type="", flow_label="", flow_step=None):
    return json.dumps(
        {
            "practice_type": practice_type or "",
            "flow_label": flow_label or "",
            "flow_step": flow_step,
            "pasuk": question.get("pasuk"),
            "question": question.get("question"),
            "skill": question.get("skill"),
            "question_type": question.get("question_type"),
            "selected_word": question.get("selected_word"),
            "word": question.get("word"),
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def append_pilot_event(record, *, path=None):
    resolved_path = resolve_pilot_event_log_path(path)
    try:
        resolved_path.parent.mkdir(parents=True, exist_ok=True)
        with resolved_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        return False
    return True


def clean_optional_note(text, *, max_length):
    cleaned = " ".join(str(text or "").split()).strip()
    if not cleaned:
        return None
    return cleaned[:max_length]


def build_question_served_event(
    question,
    *,
    session_id,
    question_log_id,
    practice_type="",
    flow_label="",
    flow_step=None,
):
    pasuk_ref = active_pasuk_ref_for_question(question)
    scope_membership = scope_membership_for_ref(pasuk_ref)
    debug_trace = question.get("_debug_trace") or {}
    if scope_membership != "active_parsed":
        note_trusted_scope_violation()
    return {
        "event_type": "question_served",
        "timestamp_utc": utc_now_iso(),
        "session_id": session_id,
        "question_log_id": question_log_id,
        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "practice_type": practice_type or "",
        "flow_label": flow_label or "",
        "flow_step": flow_step,
        "pasuk_ref": pasuk_ref,
        "scope_membership": scope_membership,
        "trusted_scope_mode": pilot_scope_mode(),
        "trusted_active_scope_requested": trusted_active_scope_requested(),
        "trusted_active_scope_session": trusted_active_scope_session(),
        "skill": question.get("skill"),
        "question_type": question.get("question_type"),
        "standard": question.get("standard"),
        "question_text": question.get("question"),
        "selected_word": question.get("selected_word"),
        "word": question.get("word"),
        "correct_answer": question.get("correct_answer"),
        "source": question.get("source"),
        "analysis_source": question.get("analysis_source"),
        "question_generation_ms": question.get("question_generation_ms"),
        "served_status": "suppressed" if question.get("status") == "skipped" else "served",
        "skip_reason": question.get("reason"),
        "debug_fallback_path": debug_trace.get("fallback_path", ""),
        "debug_transition_reason": debug_trace.get("transition_reason", ""),
        "debug_candidate_filter_reasons": list(debug_trace.get("candidate_filter_reasons") or []),
        "debug_rejection_counts": dict(debug_trace.get("rejection_counts") or {}),
        "debug_pre_serve_validation_passed": bool(debug_trace.get("pre_serve_validation_passed")),
        "debug_pre_serve_validation_path": debug_trace.get("pre_serve_validation_path", ""),
        "debug_pre_serve_validation_codes": list(debug_trace.get("pre_serve_validation_codes") or []),
        "debug_reuse_mode": debug_trace.get("reuse_mode", ""),
        "debug_variety_guard_applied": bool(debug_trace.get("variety_guard_applied")),
        "debug_variety_guard_source": debug_trace.get("variety_guard_source", ""),
        "debug_selection_mode": debug_trace.get("selection_mode", ""),
    }


def build_question_answered_event(
    question,
    *,
    session_id,
    question_log_id,
    selected_answer,
    is_correct,
    response_time_ms,
):
    pasuk_ref = active_pasuk_ref_for_question(question)
    return {
        "event_type": "question_answered",
        "timestamp_utc": utc_now_iso(),
        "session_id": session_id,
        "question_log_id": question_log_id,
        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "pasuk_ref": pasuk_ref,
        "scope_membership": scope_membership_for_ref(pasuk_ref),
        "trusted_scope_mode": pilot_scope_mode(),
        "trusted_active_scope_requested": trusted_active_scope_requested(),
        "trusted_active_scope_session": trusted_active_scope_session(),
        "skill": question.get("skill"),
        "question_type": question.get("question_type"),
        "question_text": question.get("question"),
        "selected_word": question.get("selected_word"),
        "correct_answer": question.get("correct_answer"),
        "user_answer": selected_answer,
        "is_correct": bool(is_correct),
        "response_time_ms": response_time_ms,
        "analysis_source": question.get("analysis_source"),
    }


def build_question_flag_event(question, *, session_id, question_log_id, flag="unclear"):
    pasuk_ref = active_pasuk_ref_for_question(question)
    return {
        "event_type": "question_flagged",
        "timestamp_utc": utc_now_iso(),
        "session_id": session_id,
        "question_log_id": question_log_id,
        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "pasuk_ref": pasuk_ref,
        "scope_membership": scope_membership_for_ref(pasuk_ref),
        "trusted_scope_mode": pilot_scope_mode(),
        "trusted_active_scope_requested": trusted_active_scope_requested(),
        "trusted_active_scope_session": trusted_active_scope_session(),
        "skill": question.get("skill"),
        "question_type": question.get("question_type"),
        "question_text": question.get("question"),
        "selected_word": question.get("selected_word"),
        "flag": flag,
    }


def build_question_label_event(*, session_id, question_log_id, label):
    return {
        "event_type": "question_labeled",
        "timestamp_utc": utc_now_iso(),
        "session_id": session_id,
        "question_log_id": question_log_id,
        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "teacher_label": label,
    }


def build_question_note_event(*, session_id, question_log_id, note_role, note_text):
    return {
        "event_type": "question_noted",
        "timestamp_utc": utc_now_iso(),
        "session_id": session_id,
        "question_log_id": question_log_id,
        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "note_role": note_role,
        "note_text": note_text,
    }


def sync_pilot_served_question(question, *, practice_type="", flow_label="", flow_step=None):
    session_id = ensure_pilot_session_id()
    signature = question_log_signature(
        question,
        practice_type=practice_type,
        flow_label=flow_label,
        flow_step=flow_step,
    )
    if st.session_state.get("pilot_current_question_signature") == signature:
        return st.session_state.get("pilot_current_question_log_id")

    question_log_id = f"question-{uuid4().hex[:12]}"
    st.session_state.pilot_current_question_signature = signature
    st.session_state.pilot_current_question_log_id = question_log_id
    st.session_state.pilot_current_question_started_at = perf_counter()
    append_pilot_event(
        build_question_served_event(
            question,
            session_id=session_id,
            question_log_id=question_log_id,
            practice_type=practice_type,
            flow_label=flow_label,
            flow_step=flow_step,
        )
    )
    return question_log_id


def record_pilot_answer(question, selected_answer, is_correct):
    session_id = ensure_pilot_session_id()
    question_log_id = st.session_state.get("pilot_current_question_log_id") or f"question-{uuid4().hex[:12]}"
    started_at = st.session_state.get("pilot_current_question_started_at")
    response_time_ms = None
    if started_at is not None:
        response_time_ms = round((perf_counter() - started_at) * 1000, 1)
    append_pilot_event(
        build_question_answered_event(
            question,
            session_id=session_id,
            question_log_id=question_log_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            response_time_ms=response_time_ms,
        )
    )
    return response_time_ms


def question_is_flagged_unclear():
    question_log_id = st.session_state.get("pilot_current_question_log_id")
    flagged_ids = st.session_state.setdefault("pilot_flagged_question_log_ids", [])
    return bool(question_log_id and question_log_id in flagged_ids)


def mark_current_question_unclear(question, note_text=""):
    session_id = ensure_pilot_session_id()
    question_log_id = st.session_state.get("pilot_current_question_log_id")
    if not question_log_id:
        return False
    flagged_ids = st.session_state.setdefault("pilot_flagged_question_log_ids", [])
    flagged_notes = st.session_state.setdefault("pilot_flagged_question_notes", {})
    if question_log_id in flagged_ids:
        return False
    cleaned_note = clean_optional_note(note_text, max_length=STUDENT_FLAG_NOTE_MAX_LENGTH)
    flagged_ids.append(question_log_id)
    st.session_state.pilot_flagged_question_log_ids = flagged_ids
    if cleaned_note:
        flagged_notes[question_log_id] = cleaned_note
        st.session_state.pilot_flagged_question_notes = flagged_notes
    append_pilot_event(
        {
            **build_question_flag_event(
                question,
                session_id=session_id,
                question_log_id=question_log_id,
                flag="unclear",
            ),
            "student_note": cleaned_note,
        }
    )
    return True


def record_teacher_flag_label(question_log_id, label, *, session_id=None, path=None):
    if label not in TEACHER_FLAG_LABELS:
        return False
    if not question_log_id:
        return False
    return append_pilot_event(
        build_question_label_event(
            session_id=session_id or ensure_pilot_session_id(),
            question_log_id=question_log_id,
            label=label,
        ),
        path=path,
    )


def record_teacher_flag_note(question_log_id, note_text, *, session_id=None, path=None):
    cleaned_note = clean_optional_note(note_text, max_length=TEACHER_FLAG_NOTE_MAX_LENGTH)
    if not question_log_id or not cleaned_note:
        return False
    return append_pilot_event(
        build_question_note_event(
            session_id=session_id or ensure_pilot_session_id(),
            question_log_id=question_log_id,
            note_role="teacher",
            note_text=cleaned_note,
        ),
        path=path,
    )


def load_pilot_events(*, path=None):
    resolved_path = resolve_pilot_event_log_path(path)
    if not resolved_path.exists():
        return []
    events = []
    with resolved_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
    return events


def parse_pilot_timestamp(value):
    cleaned = str(value or "").strip()
    if not cleaned:
        return None
    try:
        return datetime.fromisoformat(cleaned)
    except ValueError:
        return None


def session_start_times(events):
    starts = {}
    for event in events:
        session_id = event.get("session_id")
        timestamp = parse_pilot_timestamp(event.get("timestamp_utc"))
        if not session_id or timestamp is None:
            continue
        current = starts.get(session_id)
        if current is None or timestamp < current:
            starts[session_id] = timestamp
    return starts


def _normalize_review_filter_timestamp(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return parse_pilot_timestamp(value)


def filter_pilot_events(
    events,
    *,
    session_start_since=None,
    session_start_until=None,
    scope_id=None,
    trusted_active_scope_only=False,
):
    session_start_since = _normalize_review_filter_timestamp(session_start_since)
    session_start_until = _normalize_review_filter_timestamp(session_start_until)
    scope_id = str(scope_id or "").strip() or None
    source_events = list(events or [])
    starts = session_start_times(source_events)

    trusted_session_ids = set()
    if trusted_active_scope_only:
        for event in source_events:
            event_scope_mode = event.get("trusted_scope_mode")
            if bool(event.get("trusted_active_scope_requested")) or bool(event.get("trusted_active_scope_session")):
                trusted_session_ids.add(event.get("session_id"))
            elif event_scope_mode == TRUSTED_ACTIVE_SCOPE_MODE:
                trusted_session_ids.add(event.get("session_id"))

    filtered = []
    for event in source_events:
        event_session_id = event.get("session_id")
        session_started_at = starts.get(event_session_id)
        event_timestamp = parse_pilot_timestamp(event.get("timestamp_utc"))
        effective_timestamp = session_started_at or event_timestamp

        if session_start_since is not None and effective_timestamp is not None and effective_timestamp < session_start_since:
            continue
        if session_start_until is not None and effective_timestamp is not None and effective_timestamp > session_start_until:
            continue
        if scope_id and (event.get("scope_id") or "") != scope_id:
            continue
        if trusted_active_scope_only and event_session_id not in trusted_session_ids:
            continue
        filtered.append(event)

    return filtered


def _event_scope_ids(events):
    return sorted({event.get("scope_id") for event in events if event.get("scope_id")})


def _session_start_range(events):
    starts = sorted(session_start_times(events).values())
    if not starts:
        return {"first": None, "last": None}
    return {
        "first": starts[0].isoformat(),
        "last": starts[-1].isoformat(),
    }


def _is_isolated_pilot_log_path(path):
    resolved_path = resolve_pilot_event_log_path(path)
    return resolved_path.parent.name == "runs"


def _review_warnings(
    source_events,
    filtered_events,
    *,
    resolved_path,
    session_start_since=None,
    session_start_until=None,
    scope_id=None,
    trusted_active_scope_only=False,
):
    warnings = []
    source_scope_ids = _event_scope_ids(source_events)
    source_session_range = _session_start_range(source_events)
    excluded_count = max(0, len(source_events) - len(filtered_events))

    if not _is_isolated_pilot_log_path(resolved_path):
        warnings.append(
            {
                "code": "source_log_not_isolated",
                "message": "This review was built from a non-isolated pilot log path. Older sessions may be present unless filters were applied.",
            }
        )
    if len(source_scope_ids) > 1:
        warnings.append(
            {
                "code": "source_log_multiple_scope_ids",
                "message": f"This source log contains multiple scope ids: {', '.join(source_scope_ids)}.",
            }
        )
    first_start = source_session_range.get("first")
    last_start = source_session_range.get("last")
    if first_start and last_start and first_start[:10] != last_start[:10]:
        warnings.append(
            {
                "code": "source_log_multiple_session_dates",
                "message": f"This source log spans multiple session start dates ({first_start[:10]} to {last_start[:10]}).",
            }
        )
    if excluded_count:
        warnings.append(
            {
                "code": "filters_excluded_source_events",
                "message": f"The active review filters excluded {excluded_count} source events from the selected artifact.",
            }
        )
    if session_start_since or session_start_until or scope_id or trusted_active_scope_only:
        warnings.append(
            {
                "code": "review_filters_applied",
                "message": "This review artifact was generated with explicit filters. Use the included review_window metadata when interpreting counts.",
            }
        )
    return warnings


def build_validation_signal_summary(events, *, example_limit=5):
    served_events = [
        event for event in events
        if event.get("event_type") == "question_served"
    ]
    rejection_counts = Counter()
    missing_validation_examples = []

    for event in served_events:
        for code, count in (event.get("debug_rejection_counts") or {}).items():
            rejection_counts[code] += count
        if event.get("served_status") == "served" and not event.get("debug_pre_serve_validation_passed"):
            if len(missing_validation_examples) < example_limit:
                missing_validation_examples.append(
                    {
                        "session_id": event.get("session_id"),
                        "question_log_id": event.get("question_log_id"),
                        "question_type": event.get("question_type"),
                        "selected_word": event.get("selected_word"),
                        "pasuk_ref": (event.get("pasuk_ref") or {}).get("label"),
                    }
                )

    served_with_validation_flag = sum(
        1
        for event in served_events
        if event.get("served_status") == "served" and event.get("debug_pre_serve_validation_passed")
    )
    served_without_validation_flag = sum(
        1
        for event in served_events
        if event.get("served_status") == "served" and not event.get("debug_pre_serve_validation_passed")
    )
    return {
        "served_with_validation_flag": served_with_validation_flag,
        "served_without_validation_flag": served_without_validation_flag,
        "served_without_validation_examples": missing_validation_examples,
        "top_pre_serve_rejection_codes": [
            {"code": code, "count": count}
            for code, count in rejection_counts.most_common(8)
        ],
    }


def latest_teacher_labels_by_question(events):
    labels = {}
    for event in events:
        if event.get("event_type") != "question_labeled":
            continue
        question_log_id = event.get("question_log_id")
        if not question_log_id:
            continue
        labels[question_log_id] = {
            "teacher_label": event.get("teacher_label"),
            "labeled_at_utc": event.get("timestamp_utc"),
            "session_id": event.get("session_id"),
        }
    return labels


def latest_teacher_notes_by_question(events):
    notes = {}
    for event in events:
        if event.get("event_type") != "question_noted" or event.get("note_role") != "teacher":
            continue
        question_log_id = event.get("question_log_id")
        if not question_log_id:
            continue
        notes[question_log_id] = {
            "teacher_note": event.get("note_text"),
            "noted_at_utc": event.get("timestamp_utc"),
            "session_id": event.get("session_id"),
        }
    return notes


def build_flagged_review_queue(events, *, max_items=20):
    latest_labels = latest_teacher_labels_by_question(events)
    latest_notes = latest_teacher_notes_by_question(events)
    flagged_items = []
    fingerprint_counts = Counter()

    for event in events:
        if event.get("event_type") != "question_flagged" or event.get("flag") != "unclear":
            continue
        item = {
            "session_id": event.get("session_id"),
            "question_log_id": event.get("question_log_id"),
            "timestamp_utc": event.get("timestamp_utc"),
            "pasuk_ref": (event.get("pasuk_ref") or {}).get("label"),
            "question_type": event.get("question_type"),
            "question_text": event.get("question_text"),
            "selected_word": event.get("selected_word"),
            "scope_membership": event.get("scope_membership"),
            "student_note": event.get("student_note"),
        }
        fingerprint = (
            item["pasuk_ref"],
            item["question_type"],
            item["question_text"],
            item["selected_word"],
        )
        item["fingerprint"] = fingerprint
        fingerprint_counts[fingerprint] += 1
        flagged_items.append(item)

    for item in flagged_items:
        label_data = latest_labels.get(item["question_log_id"], {})
        note_data = latest_notes.get(item["question_log_id"], {})
        item["teacher_label"] = label_data.get("teacher_label")
        item["labeled_at_utc"] = label_data.get("labeled_at_utc")
        item["teacher_note"] = note_data.get("teacher_note")
        item["teacher_noted_at_utc"] = note_data.get("noted_at_utc")
        item["repeat_count"] = fingerprint_counts[item["fingerprint"]]
        item.pop("fingerprint", None)

    flagged_items.sort(
        key=lambda item: (
            item.get("repeat_count", 0),
            item.get("timestamp_utc") or "",
        ),
        reverse=True,
    )
    return flagged_items[:max_items]


def build_pilot_summary(sessions, flagged_review_queue, *, validation_signals=None):
    served_family_counts = Counter()
    top_repeated_flagged_items = []
    seen_fingerprints = set()
    substantive_sessions = [session for session in sessions if session.get("is_substantive_session")]

    for session in substantive_sessions:
        served_family_counts.update(session.get("served_question_types", {}))

    for item in flagged_review_queue:
        fingerprint = (
            item.get("pasuk_ref"),
            item.get("question_type"),
            item.get("question_text"),
            item.get("selected_word"),
        )
        if fingerprint in seen_fingerprints:
            continue
        seen_fingerprints.add(fingerprint)
        top_repeated_flagged_items.append(
            {
                "pasuk_ref": item.get("pasuk_ref"),
                "question_type": item.get("question_type"),
                "question_text": item.get("question_text"),
                "selected_word": item.get("selected_word"),
                "repeat_count": item.get("repeat_count", 1),
                "teacher_label": item.get("teacher_label"),
            }
        )

    top_repeated_flagged_items.sort(
        key=lambda item: (-item.get("repeat_count", 0), item.get("question_type") or "", item.get("pasuk_ref") or "")
    )

    high_unclear_sessions = []
    for session in substantive_sessions:
        served = session.get("served_questions", 0) or 0
        flagged = session.get("flagged_unclear", 0) or 0
        unclear_rate = round(flagged / served, 2) if served else 0.0
        high_unclear_sessions.append(
            {
                "session_id": session.get("session_id"),
                "unclear_rate": unclear_rate,
                "flagged_unclear": flagged,
                "served_questions": served,
                "practice_types": session.get("practice_types", {}),
            }
        )
    high_unclear_sessions.sort(
        key=lambda item: (-item["unclear_rate"], -item["flagged_unclear"], item["session_id"] or "")
    )

    trusted_scope_violations = [
        {
            "session_id": session.get("session_id"),
            "served_outside_active_scope_questions": session.get("served_outside_active_scope_questions", 0),
            "recent_scope_issues": session.get("recent_scope_issues", []),
        }
        for session in sessions
        if session.get("session_scope_status") == "outside_active_scope_detected"
    ]

    summary = {
        "top_repeated_flagged_items": top_repeated_flagged_items[:5],
        "top_flagged_unclear_items": top_repeated_flagged_items[:5],
        "highest_unclear_rate_sessions": high_unclear_sessions[:5],
        "dominant_served_question_families": dict(served_family_counts.most_common(6)),
        "top_served_question_families": dict(served_family_counts.most_common(6)),
        "trusted_scope_violations": trusted_scope_violations,
        "substantive_session_count": len(substantive_sessions),
        "shell_session_count": sum(1 for session in sessions if session.get("is_shell_session")),
    }
    if validation_signals:
        summary["served_without_validation_signals"] = {
            "served_with_validation_flag": validation_signals.get("served_with_validation_flag", 0),
            "served_without_validation_flag": validation_signals.get("served_without_validation_flag", 0),
            "served_without_validation_examples": list(
                validation_signals.get("served_without_validation_examples") or []
            ),
        }
        summary["top_pre_serve_rejection_codes"] = list(
            validation_signals.get("top_pre_serve_rejection_codes") or []
        )
    return summary


def summarize_pilot_sessions(events, *, max_sessions=5):
    sessions = {}
    for event in events:
        event_scope_mode = event.get("trusted_scope_mode") or TRUSTED_ACTIVE_SCOPE_MODE
        trusted_requested = bool(
            event.get(
                "trusted_active_scope_requested",
                event_scope_mode == TRUSTED_ACTIVE_SCOPE_MODE,
            )
        )
        session = sessions.setdefault(
            event.get("session_id"),
            {
                "session_id": event.get("session_id"),
                "scope_id": event.get("scope_id"),
                "trusted_scope_mode": event_scope_mode,
                "trusted_active_scope_requested": trusted_requested,
                "trusted_active_scope_session": True if trusted_requested else False,
                "started_at_utc": event.get("timestamp_utc"),
                "last_event_at_utc": event.get("timestamp_utc"),
                "served_questions": 0,
                "answered_questions": 0,
                "correct_answers": 0,
                "incorrect_answers": 0,
                "flagged_unclear": 0,
                "suppressed_or_skipped": 0,
                "served_active_scope_questions": 0,
                "served_outside_active_scope_questions": 0,
                "practice_types": Counter(),
                "served_question_types": Counter(),
                "answered_question_types": Counter(),
                "flagged_unclear_question_types": Counter(),
                "served_pasuk_refs": Counter(),
                "response_times_ms": [],
                "recent_unclear_flags": [],
                "recent_scope_issues": [],
                "lifecycle_events": Counter(),
                "lifecycle_reasons": [],
            },
        )
        timestamp = event.get("timestamp_utc")
        if timestamp and timestamp < session["started_at_utc"]:
            session["started_at_utc"] = timestamp
        if timestamp and timestamp > session["last_event_at_utc"]:
            session["last_event_at_utc"] = timestamp

        question_type = event.get("question_type")
        pasuk_ref = (event.get("pasuk_ref") or {}).get("label")
        has_scope_signal = bool(event.get("scope_membership")) or bool(event.get("pasuk_ref"))
        scope_membership = event.get("scope_membership") or scope_membership_for_ref(event.get("pasuk_ref"))
        if event.get("trusted_active_scope_session") is False:
            session["trusted_active_scope_session"] = False
        if trusted_requested and has_scope_signal and scope_membership != "active_parsed":
            session["trusted_active_scope_session"] = False

        if event.get("event_type") == "session_lifecycle":
            lifecycle = event.get("lifecycle")
            if lifecycle:
                session["lifecycle_events"][lifecycle] += 1
            if event.get("reason"):
                session["lifecycle_reasons"].append(event.get("reason"))
        elif event.get("event_type") == "question_served":
            session["served_questions"] += 1
            practice_type = event.get("practice_type")
            if practice_type:
                session["practice_types"][practice_type] += 1
            if question_type:
                session["served_question_types"][question_type] += 1
            if pasuk_ref:
                session["served_pasuk_refs"][pasuk_ref] += 1
            if scope_membership == "active_parsed":
                session["served_active_scope_questions"] += 1
            else:
                session["served_outside_active_scope_questions"] += 1
                session["recent_scope_issues"].append(
                    {
                        "pasuk_ref": pasuk_ref,
                        "question_type": question_type,
                        "question_text": event.get("question_text"),
                        "selected_word": event.get("selected_word"),
                    }
                )
            if event.get("served_status") != "served":
                session["suppressed_or_skipped"] += 1
        elif event.get("event_type") == "question_answered":
            session["answered_questions"] += 1
            if question_type:
                session["answered_question_types"][question_type] += 1
            if event.get("is_correct"):
                session["correct_answers"] += 1
            else:
                session["incorrect_answers"] += 1
            response_ms = event.get("response_time_ms")
            if isinstance(response_ms, (int, float)):
                session["response_times_ms"].append(response_ms)
        elif event.get("event_type") == "question_flagged" and event.get("flag") == "unclear":
            session["flagged_unclear"] += 1
            if question_type:
                session["flagged_unclear_question_types"][question_type] += 1
            session["recent_unclear_flags"].append(
                {
                    "question_log_id": event.get("question_log_id"),
                    "session_id": event.get("session_id"),
                    "pasuk_ref": pasuk_ref,
                    "question_type": event.get("question_type"),
                    "question_text": event.get("question_text"),
                    "selected_word": event.get("selected_word"),
                    "student_note": event.get("student_note"),
                }
            )

    ordered = sorted(
        sessions.values(),
        key=lambda item: item.get("last_event_at_utc") or "",
        reverse=True,
    )[:max_sessions]

    normalized = []
    for session in ordered:
        response_times = session.pop("response_times_ms")
        served_question_types = dict(session["served_question_types"])
        answered_question_types = dict(session["answered_question_types"])
        flagged_unclear_question_types = dict(session["flagged_unclear_question_types"])
        served_pasuk_refs = dict(session["served_pasuk_refs"])
        lifecycle_events = dict(session.pop("lifecycle_events"))
        lifecycle_reasons = session.pop("lifecycle_reasons")[-5:]
        session_scope_status = "open_pilot_scope"
        if session["trusted_active_scope_requested"]:
            session_scope_status = (
                "trusted_active_scope"
                if session["trusted_active_scope_session"]
                else "outside_active_scope_detected"
            )
        is_shell_session = (
            session["answered_questions"] == 0
            and session["flagged_unclear"] == 0
            and session["served_questions"] <= 1
        )
        shell_session_reason = ""
        if is_shell_session:
            if session["served_questions"] == 0:
                shell_session_reason = "startup_only"
            elif session["served_questions"] == 1:
                shell_session_reason = "single_question_no_answer"
        is_substantive_session = not is_shell_session
        normalized.append(
            {
                **session,
                "average_response_time_ms": round(mean(response_times), 1) if response_times else None,
                "practice_types": dict(session["practice_types"]),
                "served_question_types": served_question_types,
                "served_question_type_total": sum(served_question_types.values()),
                "answered_question_types": answered_question_types,
                "answered_question_type_total": sum(answered_question_types.values()),
                "flagged_unclear_question_types": flagged_unclear_question_types,
                "flagged_unclear_question_type_total": sum(flagged_unclear_question_types.values()),
                "served_pasuk_refs": served_pasuk_refs,
                "session_scope_status": session_scope_status,
                "session_lifecycle_events": lifecycle_events,
                "session_lifecycle_reasons": lifecycle_reasons,
                "session_origin": (
                    "resumed"
                    if lifecycle_events.get("resumed")
                    else ("started" if lifecycle_events.get("started") else "legacy_or_inferred")
                ),
                "is_shell_session": is_shell_session,
                "shell_session_reason": shell_session_reason,
                "is_substantive_session": is_substantive_session,
                "recent_unclear_flags": session["recent_unclear_flags"][-5:],
                "recent_scope_issues": session["recent_scope_issues"][-5:],
            }
        )
    return normalized


def build_pilot_review_export(
    *,
    max_sessions=5,
    path=None,
    session_start_since=None,
    session_start_until=None,
    scope_id=None,
    trusted_active_scope_only=False,
):
    resolved_path = resolve_pilot_event_log_path(path)
    source_events = load_pilot_events(path=resolved_path)
    events = filter_pilot_events(
        source_events,
        session_start_since=session_start_since,
        session_start_until=session_start_until,
        scope_id=scope_id,
        trusted_active_scope_only=trusted_active_scope_only,
    )
    sessions = summarize_pilot_sessions(events, max_sessions=max_sessions)
    flagged_review_queue = build_flagged_review_queue(events)
    validation_signals = build_validation_signal_summary(events)
    source_session_ids = {event.get("session_id") for event in source_events if event.get("session_id")}
    included_session_ids = {event.get("session_id") for event in events if event.get("session_id")}
    included_scope_ids = _event_scope_ids(events)
    review_scope_id = (str(scope_id or "").strip() or None)
    if not review_scope_id and len(included_scope_ids) == 1:
        review_scope_id = included_scope_ids[0]
    review_warnings = _review_warnings(
        source_events,
        events,
        resolved_path=resolved_path,
        session_start_since=session_start_since,
        session_start_until=session_start_until,
        scope_id=scope_id,
        trusted_active_scope_only=trusted_active_scope_only,
    )
    if review_scope_id and review_scope_id != ACTIVE_ASSESSMENT_SCOPE:
        review_warnings.append(
            {
                "code": "runtime_scope_differs_from_review_scope",
                "message": (
                    f"The current runtime scope is {ACTIVE_ASSESSMENT_SCOPE}, "
                    f"but this review artifact is scoped to {review_scope_id}."
                ),
            }
        )
    review_window = {
        "session_start_since_utc": (
            _normalize_review_filter_timestamp(session_start_since).isoformat()
            if _normalize_review_filter_timestamp(session_start_since) is not None
            else None
        ),
        "session_start_until_utc": (
            _normalize_review_filter_timestamp(session_start_until).isoformat()
            if _normalize_review_filter_timestamp(session_start_until) is not None
            else None
        ),
        "scope_id": str(scope_id or "").strip() or None,
        "trusted_active_scope_only": bool(trusted_active_scope_only),
        "source_event_count": len(source_events),
        "included_event_count": len(events),
        "excluded_event_count": max(0, len(source_events) - len(events)),
        "source_session_count": len(source_session_ids),
        "included_session_count": len(included_session_ids),
        "source_scope_ids": _event_scope_ids(source_events),
        "included_scope_ids": included_scope_ids,
        "source_session_start_range_utc": _session_start_range(source_events),
        "included_session_start_range_utc": _session_start_range(events),
        "source_log_is_isolated_run": _is_isolated_pilot_log_path(resolved_path),
        "fresh_run_only": _is_isolated_pilot_log_path(resolved_path),
        "warnings": review_warnings,
    }
    return {
        "generated_at_utc": utc_now_iso(),
        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "runtime_scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "review_scope_id": review_scope_id,
        "review_scope_ids": included_scope_ids,
        "log_path": str(resolved_path),
        "configured_log_env_var": PILOT_EVENT_LOG_ENV_VAR,
        "review_window": review_window,
        "accounting_model": {
            "served_question_types": "question_served events only",
            "answered_question_types": "question_answered events only",
            "flagged_unclear_question_types": "question_flagged events with flag=unclear only",
        },
        "teacher_flag_labels": list(TEACHER_FLAG_LABELS),
        "student_flag_note_max_length": STUDENT_FLAG_NOTE_MAX_LENGTH,
        "teacher_flag_note_max_length": TEACHER_FLAG_NOTE_MAX_LENGTH,
        "session_count": len(included_session_ids),
        "substantive_session_count": sum(1 for session in sessions if session.get("is_substantive_session")),
        "shell_session_count": sum(1 for session in sessions if session.get("is_shell_session")),
        "sessions": sessions,
        "flagged_review_queue": flagged_review_queue,
        "summary": build_pilot_summary(
            sessions,
            flagged_review_queue,
            validation_signals=validation_signals,
        ),
    }


def current_session_review(*, path=None):
    session_id = st.session_state.get("pilot_session_id")
    if not session_id:
        return None
    export = build_pilot_review_export(max_sessions=20, path=path)
    for session in export["sessions"]:
        if session.get("session_id") == session_id:
            return session
    return {
        "session_id": session_id,
        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "trusted_scope_mode": pilot_scope_mode(),
        "trusted_active_scope_requested": trusted_active_scope_requested(),
        "trusted_active_scope_session": trusted_active_scope_session(),
        "session_scope_status": (
            "trusted_active_scope"
            if trusted_active_scope_requested() and trusted_active_scope_session()
            else (
                "outside_active_scope_detected"
                if trusted_active_scope_requested()
                else "open_pilot_scope"
            )
        ),
        "served_questions": 0,
        "answered_questions": 0,
        "correct_answers": 0,
        "incorrect_answers": 0,
        "flagged_unclear": 0,
        "suppressed_or_skipped": 0,
        "served_active_scope_questions": 0,
        "served_outside_active_scope_questions": 0,
        "practice_types": {},
        "served_question_types": {},
        "served_question_type_total": 0,
        "answered_question_types": {},
        "answered_question_type_total": 0,
        "flagged_unclear_question_types": {},
        "flagged_unclear_question_type_total": 0,
        "served_pasuk_refs": {},
        "average_response_time_ms": None,
        "session_lifecycle_events": {},
        "session_lifecycle_reasons": [],
        "session_origin": st.session_state.get("pilot_session_origin") or "legacy_or_inferred",
        "is_shell_session": True,
        "shell_session_reason": "startup_only",
        "is_substantive_session": False,
        "recent_unclear_flags": [],
        "recent_scope_issues": [],
    }
