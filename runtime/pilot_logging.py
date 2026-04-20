from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
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


PILOT_EVENT_LOG_PATH = data_path("pilot/pilot_session_events.jsonl")
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


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def new_pilot_session_id():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"pilot-{timestamp}-{uuid4().hex[:8]}"


def ensure_pilot_session_id():
    session_id = st.session_state.get("pilot_session_id")
    st.session_state.setdefault("pilot_scope_mode", TRUSTED_ACTIVE_SCOPE_MODE)
    st.session_state.setdefault("pilot_trusted_active_scope_session", True)
    if session_id:
        return session_id
    session_id = new_pilot_session_id()
    st.session_state.pilot_session_id = session_id
    st.session_state.pilot_trusted_active_scope_session = True
    return session_id


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


def append_pilot_event(record, *, path=PILOT_EVENT_LOG_PATH):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        return False
    return True


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


def mark_current_question_unclear(question):
    session_id = ensure_pilot_session_id()
    question_log_id = st.session_state.get("pilot_current_question_log_id")
    if not question_log_id:
        return False
    flagged_ids = st.session_state.setdefault("pilot_flagged_question_log_ids", [])
    if question_log_id in flagged_ids:
        return False
    flagged_ids.append(question_log_id)
    st.session_state.pilot_flagged_question_log_ids = flagged_ids
    append_pilot_event(
        build_question_flag_event(
            question,
            session_id=session_id,
            question_log_id=question_log_id,
            flag="unclear",
        )
    )
    return True


def record_teacher_flag_label(question_log_id, label, *, session_id=None, path=PILOT_EVENT_LOG_PATH):
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


def load_pilot_events(*, path=PILOT_EVENT_LOG_PATH):
    if not path.exists():
        return []
    events = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
    return events


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


def build_flagged_review_queue(events, *, max_items=20):
    latest_labels = latest_teacher_labels_by_question(events)
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
        item["teacher_label"] = label_data.get("teacher_label")
        item["labeled_at_utc"] = label_data.get("labeled_at_utc")
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


def build_pilot_summary(sessions, flagged_review_queue):
    served_family_counts = Counter()
    top_repeated_flagged_items = []
    seen_fingerprints = set()

    for session in sessions:
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
    for session in sessions:
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

    return {
        "top_repeated_flagged_items": top_repeated_flagged_items[:5],
        "highest_unclear_rate_sessions": high_unclear_sessions[:5],
        "dominant_served_question_families": dict(served_family_counts.most_common(6)),
        "trusted_scope_violations": trusted_scope_violations,
    }


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

        if event.get("event_type") == "question_served":
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
        session_scope_status = "open_pilot_scope"
        if session["trusted_active_scope_requested"]:
            session_scope_status = (
                "trusted_active_scope"
                if session["trusted_active_scope_session"]
                else "outside_active_scope_detected"
            )
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
                "recent_unclear_flags": session["recent_unclear_flags"][-5:],
                "recent_scope_issues": session["recent_scope_issues"][-5:],
            }
        )
    return normalized


def build_pilot_review_export(*, max_sessions=5, path=PILOT_EVENT_LOG_PATH):
    events = load_pilot_events(path=path)
    sessions = summarize_pilot_sessions(events, max_sessions=max_sessions)
    flagged_review_queue = build_flagged_review_queue(events)
    return {
        "generated_at_utc": utc_now_iso(),
        "scope_id": ACTIVE_ASSESSMENT_SCOPE,
        "log_path": str(path),
        "accounting_model": {
            "served_question_types": "question_served events only",
            "answered_question_types": "question_answered events only",
            "flagged_unclear_question_types": "question_flagged events with flag=unclear only",
        },
        "teacher_flag_labels": list(TEACHER_FLAG_LABELS),
        "session_count": len({event.get("session_id") for event in events if event.get("session_id")}),
        "sessions": sessions,
        "flagged_review_queue": flagged_review_queue,
        "summary": build_pilot_summary(sessions, flagged_review_queue),
    }


def current_session_review(*, path=PILOT_EVENT_LOG_PATH):
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
        "recent_unclear_flags": [],
        "recent_scope_issues": [],
    }
