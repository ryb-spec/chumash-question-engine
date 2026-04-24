from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from assessment_scope import (
    ACTIVE_ASSESSMENT_SCOPE,
    active_pesukim_records,
    active_scope_metadata,
    get_scope_metadata,
)
from engine.flow_builder import generate_question
from runtime.pilot_logging import (
    PILOT_EVENT_LOG_ENV_VAR,
    build_isolated_pilot_log_path,
    build_pilot_review_export,
    ensure_pilot_log_file,
)
from runtime.question_flow import (
    question_concept_key,
    question_prompt_family,
    question_surface_pattern,
    question_target_family,
)
from torah_parser.word_bank_adapter import normalize_hebrew_key


DEFAULT_HAND_AUDIT_COUNT = 25
DEFAULT_MAX_PILOT_SESSIONS = 20
DEFAULT_OUTPUT_DIR = BASE_DIR / "data" / "validation" / "release_checks"

HAND_AUDIT_LANES = (
    {"lane": "translation", "skills": ("translation",)},
    {"lane": "shoresh", "skills": ("shoresh",)},
    {"lane": "tense", "skills": ("verb_tense", "identify_tense")},
    {
        "lane": "affix",
        "skills": ("identify_prefix_meaning", "identify_suffix_meaning", "identify_pronoun_suffix"),
    },
    {"lane": "part_of_speech", "skills": ("part_of_speech",)},
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_release_check_output_dir(log_path: Path, output_dir: Path | None = None) -> Path:
    return output_dir or (DEFAULT_OUTPUT_DIR / log_path.stem)


def build_release_check_paths(log_path: Path, output_dir: Path | None = None) -> dict[str, Path]:
    directory = build_release_check_output_dir(log_path, output_dir)
    return {
        "output_dir": directory,
        "pilot_review_json": directory / "pilot_review.json",
        "hand_audit_json": directory / "hand_audit.json",
        "hand_audit_markdown": directory / "hand_audit.md",
        "summary_json": directory / "release_check_summary.json",
        "summary_markdown": directory / "release_check_summary.md",
    }


def scope_metadata_for_release_check(scope_id: str | None = None) -> dict:
    requested_scope_id = str(scope_id or ACTIVE_ASSESSMENT_SCOPE).strip() or ACTIVE_ASSESSMENT_SCOPE
    metadata = active_scope_metadata() if requested_scope_id == ACTIVE_ASSESSMENT_SCOPE else get_scope_metadata(requested_scope_id)
    if not metadata:
        raise ValueError(f"Unknown scope_id for release-check hand audit: {requested_scope_id}")
    return metadata


def scope_records_for_release_check(scope_id: str | None = None) -> tuple[dict, list[dict]]:
    metadata = scope_metadata_for_release_check(scope_id)
    resolved_scope_id = metadata.get("scope_id") or ACTIVE_ASSESSMENT_SCOPE
    if resolved_scope_id != ACTIVE_ASSESSMENT_SCOPE:
        raise ValueError(
            "Hand-audit packet generation currently supports the active runtime scope only. "
            f"Requested scope_id={resolved_scope_id}, active scope is {ACTIVE_ASSESSMENT_SCOPE}."
        )
    return metadata, list(active_pesukim_records())


def question_lane_family(question: dict) -> str:
    question_type = str(question.get("question_type") or question.get("skill") or "").strip()
    if question_type in {"translation", "phrase_translation", "word_meaning"}:
        return "translation"
    if question_type == "shoresh":
        return "shoresh"
    if question_type in {"identify_tense", "verb_tense"}:
        return "tense"
    if question_type.startswith("prefix_level_"):
        return "affix"
    if question_type in {
        "identify_prefix_meaning",
        "identify_suffix_meaning",
        "identify_pronoun_suffix",
        "prefix",
        "suffix",
    }:
        return "affix"
    if question_type == "part_of_speech":
        return "part_of_speech"
    return question_type or "unknown"


def question_provenance(question: dict) -> str:
    analysis_source = str(question.get("analysis_source") or "").strip()
    source = str(question.get("source") or "").strip().lower()
    if analysis_source == "active_scope_reviewed_bank" or "reviewed" in source:
        return "reviewed"
    if analysis_source == "active_scope_override" or "override" in source:
        return "override"
    if "gold suppression" in source:
        return "suppressed"
    return "generated"


def ref_label_from_record(record: dict) -> str:
    ref = record.get("ref") or {}
    if ref.get("label"):
        return ref["label"]
    return f"{ref.get('sefer', 'Unknown')} {ref.get('perek', '?')}:{ref.get('pasuk', '?')}"


def unique_candidate_key(question: dict) -> tuple[str, str, str, str, str]:
    return (
        question_lane_family(question),
        str(question.get("question_type") or ""),
        normalize_hebrew_key(str(question.get("selected_word") or question.get("word") or "")),
        str(question.get("correct_answer") or "").strip().lower(),
        str((question.get("pasuk_ref") or {}).get("pasuk_id") or question.get("pasuk_id") or ""),
    )


def exact_duplicate_key(question: dict) -> tuple[str, str, str]:
    return (
        question_prompt_family(question),
        normalize_hebrew_key(str(question.get("selected_word") or question.get("word") or "")),
        str(question.get("correct_answer") or "").strip().lower(),
    )


def strict_duplicate_reason(candidate: dict, selected: list[dict]) -> str | None:
    candidate_lane = question_lane_family(candidate)
    candidate_exact = exact_duplicate_key(candidate)
    candidate_target_family = question_target_family(candidate)
    candidate_concept = question_concept_key(candidate)
    candidate_surface = question_surface_pattern(candidate)

    if any(exact_duplicate_key(item) == candidate_exact for item in selected):
        return "exact_prompt_target_repeat"
    if candidate_target_family and any(
        question_lane_family(item) == candidate_lane and question_target_family(item) == candidate_target_family
        for item in selected
    ):
        return "target_family_repeat"
    if candidate_concept and any(
        question_lane_family(item) == candidate_lane and question_concept_key(item) == candidate_concept
        for item in selected
    ):
        return "concept_repeat"
    if (
        candidate_lane == "shoresh"
        and candidate_surface in {"vav_yod_surface", "vav_tav_surface", "vav_led_surface"}
        and sum(
            1
            for item in selected
            if question_lane_family(item) == "shoresh" and question_surface_pattern(item) == candidate_surface
        )
        >= 2
    ):
        return "shoresh_surface_repeat"
    return None


def relaxed_duplicate_reason(candidate: dict, selected: list[dict]) -> str | None:
    if any(exact_duplicate_key(item) == exact_duplicate_key(candidate) for item in selected):
        return "exact_prompt_target_repeat"
    return None


def top_duplicate_warning_rows(counter: Counter, *, limit: int = 5) -> list[dict]:
    return [{"code": code, "count": count} for code, count in counter.most_common(limit) if count > 0]


def build_hand_audit_duplicate_warnings(questions: list[dict]) -> list[dict]:
    exact_counts = Counter()
    concept_counts = Counter()
    target_counts = Counter()
    for question in questions:
        exact_counts[exact_duplicate_key(question)] += 1
        concept = question_concept_key(question)
        if concept:
            concept_counts[(question_lane_family(question), concept)] += 1
        target = question_target_family(question)
        if target:
            target_counts[(question_lane_family(question), target)] += 1

    warnings = []
    for key, count in exact_counts.items():
        if count > 1:
            warnings.append({"code": "exact_packet_duplicate", "fingerprint": list(key), "count": count})
    for (lane, concept), count in concept_counts.items():
        if count > 1:
            warnings.append({"code": "concept_duplicate_feel", "lane": lane, "concept": concept, "count": count})
    for (lane, target), count in target_counts.items():
        if count > 1:
            warnings.append({"code": "target_duplicate_feel", "lane": lane, "target": target, "count": count})
    return warnings[:10]


def normalize_audit_question(question: dict, lane: str, record: dict, index: int) -> dict:
    normalized = dict(question)
    normalized["audit_lane"] = lane
    normalized["provenance"] = question_provenance(question)
    ref_payload = dict(record.get("ref") or {})
    ref_payload.update(dict(question.get("pasuk_ref") or {}))
    ref_payload.setdefault("label", ref_label_from_record(record))
    ref_payload.setdefault("pasuk_id", question.get("pasuk_id") or record.get("pasuk_id"))
    normalized["pasuk_ref"] = ref_payload
    normalized.setdefault("pasuk_id", record.get("pasuk_id"))
    normalized.setdefault("pasuk", record.get("text"))
    normalized["index"] = index
    normalized["prompt"] = question.get("question") or question.get("question_text") or ""
    normalized["target_word"] = question.get("selected_word") or question.get("word") or ""
    return normalized


def build_lane_candidate_pool(
    *,
    lane: str,
    skills: tuple[str, ...],
    records: list[dict],
    pool_target: int,
    scope_id: str,
) -> tuple[list[dict], list[dict]]:
    candidates: list[dict] = []
    warnings: list[dict] = []
    seen = set()
    skill_index = 0
    for record in records:
        if len(candidates) >= pool_target:
            break
        pasuk_text = record.get("text")
        if not pasuk_text:
            continue
        for _ in range(len(skills)):
            skill = skills[skill_index % len(skills)]
            skill_index += 1
            random.seed(f"release-check|{scope_id}|{lane}|{skill}|{record.get('pasuk_id')}")
            question_kwargs = {}
            if skill == "identify_prefix_meaning":
                question_kwargs["prefix_level"] = 2
            try:
                question = generate_question(skill, pasuk_text, **question_kwargs)
            except ValueError:
                continue
            if not isinstance(question, dict) or question.get("status") == "skipped":
                continue
            normalized = normalize_audit_question(question, lane, record, len(candidates) + 1)
            candidate_key = unique_candidate_key(normalized)
            if candidate_key in seen:
                continue
            seen.add(candidate_key)
            candidates.append(normalized)
            break
    if len(candidates) < min(3, pool_target):
        warnings.append(
            {
                "code": "lane_pool_thin",
                "lane": lane,
                "candidate_count": len(candidates),
                "requested_pool_target": pool_target,
            }
        )
    return candidates, warnings


def find_allowed_candidate_index(pool: list[dict], selected: list[dict], *, strict: bool) -> tuple[int | None, str | None]:
    rejection_counter: Counter = Counter()
    for index, candidate in enumerate(pool):
        reason = strict_duplicate_reason(candidate, selected) if strict else relaxed_duplicate_reason(candidate, selected)
        if reason is None:
            return index, None
        rejection_counter[reason] += 1
    if not rejection_counter:
        return None, None
    return None, rejection_counter.most_common(1)[0][0]


def select_hand_audit_questions(candidate_pools: dict[str, list[dict]], question_count: int) -> tuple[list[dict], list[dict]]:
    selected: list[dict] = []
    warnings: list[dict] = []
    lane_order = [item["lane"] for item in HAND_AUDIT_LANES if candidate_pools.get(item["lane"])]
    if not lane_order:
        return selected, [{"code": "no_supported_lanes", "message": "No hand-audit candidates could be built."}]

    for strict in (True, False):
        while len(selected) < question_count:
            made_progress = False
            for lane in lane_order:
                if len(selected) >= question_count:
                    break
                pool = candidate_pools.get(lane) or []
                if not pool:
                    continue
                index, blocked_reason = find_allowed_candidate_index(pool, selected, strict=strict)
                if index is None:
                    if blocked_reason and strict:
                        warnings.append({"code": "lane_candidate_blocked", "lane": lane, "reason": blocked_reason})
                    continue
                selected.append(pool.pop(index))
                made_progress = True
            if not made_progress:
                break
        if len(selected) >= question_count:
            break
        if strict and len(selected) < question_count:
            warnings.append(
                {
                    "code": "limited_pool_relaxed_fill",
                    "message": "Strict duplicate-feel filtering underfilled the packet, so finalize used relaxed exact-duplicate-only fill.",
                    "selected_count": len(selected),
                    "requested_question_count": question_count,
                }
            )

    if len(selected) < question_count:
        warnings.append(
            {
                "code": "packet_underfilled",
                "selected_count": len(selected),
                "requested_question_count": question_count,
            }
        )
    return selected, warnings


def format_hand_audit_question(question: dict, index: int) -> dict:
    return {
        "index": index,
        "lane": question_lane_family(question),
        "skill": question.get("skill"),
        "question_type": question.get("question_type"),
        "pasuk_ref": question.get("pasuk_ref"),
        "target_word": question.get("target_word") or question.get("selected_word") or question.get("word"),
        "prompt": question.get("prompt") or question.get("question"),
        "choices": list(question.get("choices") or []),
        "correct_answer": question.get("correct_answer"),
        "explanation": question.get("explanation"),
        "provenance": question.get("provenance"),
        "source": question.get("source"),
        "analysis_source": question.get("analysis_source"),
    }


def build_hand_audit_packet(scope_id: str | None = None, question_count: int = DEFAULT_HAND_AUDIT_COUNT) -> dict:
    scope_metadata, records = scope_records_for_release_check(scope_id)
    scope_id = scope_metadata.get("scope_id") or ACTIVE_ASSESSMENT_SCOPE
    positive_count = max(1, int(question_count))
    base_lane_target = max(1, positive_count // max(1, len(HAND_AUDIT_LANES)))
    pool_target = max(8, base_lane_target * 4)
    candidate_pools: dict[str, list[dict]] = {}
    warnings: list[dict] = []

    for lane_spec in HAND_AUDIT_LANES:
        pool, pool_warnings = build_lane_candidate_pool(
            lane=lane_spec["lane"],
            skills=tuple(lane_spec["skills"]),
            records=records,
            pool_target=pool_target,
            scope_id=scope_id,
        )
        if pool:
            candidate_pools[lane_spec["lane"]] = pool
        warnings.extend(pool_warnings)

    selected_questions, selection_warnings = select_hand_audit_questions(candidate_pools, positive_count)
    warnings.extend(selection_warnings)
    duplicate_warnings = build_hand_audit_duplicate_warnings(selected_questions)
    warnings.extend(duplicate_warnings)

    lane_counts = Counter(question_lane_family(question) for question in selected_questions)
    question_type_counts = Counter(str(question.get("question_type") or "unknown") for question in selected_questions)
    provenance_counts = Counter(str(question.get("provenance") or "unknown") for question in selected_questions)
    rendered_questions = [
        format_hand_audit_question(question, index)
        for index, question in enumerate(selected_questions, start=1)
    ]

    return {
        "generated_at_utc": utc_now_iso(),
        "scope": {
            "scope_id": scope_id,
            "sefer": scope_metadata.get("sefer"),
            "range": scope_metadata.get("range"),
            "status": scope_metadata.get("status"),
            "pesukim_count": scope_metadata.get("pesukim_count"),
        },
        "requested_question_count": positive_count,
        "question_count": len(rendered_questions),
        "lane_counts": dict(lane_counts),
        "question_type_counts": dict(question_type_counts),
        "provenance_counts": dict(provenance_counts),
        "duplicate_feel_warning_count": len(duplicate_warnings),
        "warnings": warnings,
        "questions": rendered_questions,
    }


def render_hand_audit_markdown(packet: dict) -> str:
    lines = [
        "# Release Check Hand Audit",
        "",
        f"Generated: {packet.get('generated_at_utc')}",
        f"Scope: {packet.get('scope', {}).get('scope_id')}",
        f"Question count: {packet.get('question_count')}",
        f"Counts by lane: {packet.get('lane_counts')}",
        f"Counts by provenance: {packet.get('provenance_counts')}",
    ]
    warnings = packet.get("warnings") or []
    if warnings:
        lines.append(f"Warnings: {len(warnings)}")
        for warning in warnings[:6]:
            detail = warning.get("message") or warning.get("reason") or warning.get("code")
            lines.append(f"- {detail}")
    else:
        lines.append("Warnings: none")
    for question in packet.get("questions", []):
        lines.extend(
            [
                "",
                f"## {question['index']}. {question.get('lane')} | {(question.get('pasuk_ref') or {}).get('label', 'Unknown reference')}",
                f"- Question type: {question.get('question_type')}",
                f"- Target: {question.get('target_word')}",
                f"- Prompt: {question.get('prompt')}",
            ]
        )
        if question.get("choices"):
            lines.append(f"- Choices: {question.get('choices')}")
        lines.extend(
            [
                f"- Correct: {question.get('correct_answer')}",
                f"- Explanation: {question.get('explanation')}",
                f"- Provenance: {question.get('provenance')}",
                "",
                "Review:",
                "- verdict:",
                "- note:",
            ]
        )
    return "\n".join(lines) + "\n"


def release_gate_checks(release_review_summary: dict) -> list[dict]:
    warnings = set(release_review_summary.get("warning_codes") or [])
    return [
        {
            "code": "fresh_run_only",
            "status": "pass" if release_review_summary.get("fresh_run_only") else "fail",
            "value": bool(release_review_summary.get("fresh_run_only")),
        },
        {
            "code": "mixed_log_clear",
            "status": "pass" if "source_log_not_isolated" not in warnings else "fail",
            "value": "source_log_not_isolated" not in warnings,
        },
        {
            "code": "trusted_scope_violations_clear",
            "status": "pass" if release_review_summary.get("trusted_scope_violation_count", 0) == 0 else "fail",
            "value": release_review_summary.get("trusted_scope_violation_count", 0),
        },
        {
            "code": "served_without_validation_clear",
            "status": "pass" if release_review_summary.get("served_without_validation_flag", 0) == 0 else "fail",
            "value": release_review_summary.get("served_without_validation_flag", 0),
        },
        {
            "code": "unclear_flags_clear",
            "status": "pass" if release_review_summary.get("unclear_flag_count", 0) == 0 else "warn",
            "value": release_review_summary.get("unclear_flag_count", 0),
        },
        {
            "code": "supported_mode_coverage_complete",
            "status": "pass" if release_review_summary.get("supported_mode_coverage_complete") else "fail",
            "value": bool(release_review_summary.get("supported_mode_coverage_complete")),
            "details": {
                "observed_practice_modes": list(release_review_summary.get("observed_practice_modes") or []),
                "missing_practice_modes": list(release_review_summary.get("missing_practice_modes") or []),
            },
        },
    ]


def build_release_check_summary(
    *,
    input_log_path: Path,
    pilot_export: dict,
    hand_audit_packet: dict,
    artifact_paths: dict[str, Path],
) -> dict:
    compact = dict(pilot_export.get("release_review_summary") or {})
    hand_audit_summary = {
        "scope_id": hand_audit_packet.get("scope", {}).get("scope_id"),
        "question_count": hand_audit_packet.get("question_count"),
        "requested_question_count": hand_audit_packet.get("requested_question_count"),
        "lane_counts": dict(hand_audit_packet.get("lane_counts") or {}),
        "provenance_counts": dict(hand_audit_packet.get("provenance_counts") or {}),
        "duplicate_feel_warning_count": hand_audit_packet.get("duplicate_feel_warning_count", 0),
    }
    return {
        "generated_at_utc": utc_now_iso(),
        "input_log_path": str(input_log_path),
        "scope_id": compact.get("scope_id") or hand_audit_summary.get("scope_id") or ACTIVE_ASSESSMENT_SCOPE,
        "artifacts": {
            key: str(path)
            for key, path in artifact_paths.items()
            if key != "output_dir"
        },
        "release_gate_checks": release_gate_checks(compact),
        "pilot_review_summary": compact,
        "hand_audit_summary": hand_audit_summary,
    }


def render_release_check_summary_markdown(summary: dict) -> str:
    pilot = summary.get("pilot_review_summary") or {}
    hand_audit = summary.get("hand_audit_summary") or {}
    checks = summary.get("release_gate_checks") or []
    lines = [
        "# Release Check Summary",
        "",
        f"Generated: {summary.get('generated_at_utc')}",
        f"Scope: {summary.get('scope_id')}",
        f"Pilot log: {summary.get('input_log_path')}",
        "",
        "## Gate Checks",
    ]
    for check in checks:
        lines.append(f"- {check.get('status', 'info').upper()} `{check.get('code')}`: {check.get('value')}")
    lines.extend(
        [
            "",
            "## Pilot Review",
            f"- Session count: {pilot.get('session_count')}",
            f"- Substantive vs shell: {pilot.get('substantive_session_count')} substantive / {pilot.get('shell_session_count')} shell",
            f"- Trusted-scope violations: {pilot.get('trusted_scope_violation_count')}",
            f"- Served without validation: {pilot.get('served_without_validation_flag')}",
            f"- Top unclear items: {pilot.get('top_unclear_items')}",
            f"- Top served question families: {pilot.get('top_served_question_families')}",
            f"- Top rejection codes: {pilot.get('top_pre_serve_rejection_codes')}",
            f"- supported_practice_modes: {pilot.get('supported_practice_modes')}",
            f"- practice_mode_counts: {pilot.get('practice_mode_counts')}",
            f"- observed_practice_modes: {pilot.get('observed_practice_modes')}",
            f"- missing_practice_modes: {pilot.get('missing_practice_modes')}",
            f"- supported_mode_coverage_complete: {pilot.get('supported_mode_coverage_complete')}",
            f"- Warning codes: {pilot.get('warning_codes')}",
            "",
            "## Hand Audit",
            f"- Question count: {hand_audit.get('question_count')} requested {hand_audit.get('requested_question_count')}",
            f"- Counts by lane: {hand_audit.get('lane_counts')}",
            f"- Counts by provenance: {hand_audit.get('provenance_counts')}",
            f"- Duplicate-feel warnings: {hand_audit.get('duplicate_feel_warning_count')}",
            "",
            "## Artifact Paths",
        ]
    )
    for label, path in (summary.get("artifacts") or {}).items():
        lines.append(f"- {label}: {path}")
    return "\n".join(lines) + "\n"


def write_release_check_artifacts(
    *,
    input_log_path: Path,
    pilot_export: dict,
    hand_audit_packet: dict,
    artifact_paths: dict[str, Path],
) -> dict:
    output_dir = artifact_paths["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    artifact_paths["pilot_review_json"].write_text(
        json.dumps(pilot_export, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    artifact_paths["hand_audit_json"].write_text(
        json.dumps(hand_audit_packet, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    artifact_paths["hand_audit_markdown"].write_text(
        render_hand_audit_markdown(hand_audit_packet),
        encoding="utf-8",
    )
    summary = build_release_check_summary(
        input_log_path=input_log_path,
        pilot_export=pilot_export,
        hand_audit_packet=hand_audit_packet,
        artifact_paths=artifact_paths,
    )
    artifact_paths["summary_json"].write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    artifact_paths["summary_markdown"].write_text(
        render_release_check_summary_markdown(summary),
        encoding="utf-8",
    )
    return summary


def prepare_release_check(
    label: str = "",
    *,
    output_dir: Path | None = None,
    scope_id: str | None = None,
    question_count: int = DEFAULT_HAND_AUDIT_COUNT,
) -> None:
    log_path = ensure_pilot_log_file(build_isolated_pilot_log_path(label))
    artifact_paths = build_release_check_paths(log_path, output_dir)
    requested_scope = str(scope_id or ACTIVE_ASSESSMENT_SCOPE).strip() or ACTIVE_ASSESSMENT_SCOPE
    payload = {
        "release_check_id": log_path.stem,
        "isolated_log_path": str(log_path),
        "release_check_output_dir": str(artifact_paths["output_dir"]),
        "scope_id": requested_scope,
        "hand_audit_question_count": int(question_count),
        "powershell_env_command": f"$env:{PILOT_EVENT_LOG_ENV_VAR} = '{log_path}'",
        "streamlit_command": "python -m streamlit run streamlit_app.py",
        "finalize_command": (
            f"python scripts/release_check.py finalize --input \"{log_path}\" "
            f"--output-dir \"{artifact_paths['output_dir']}\" "
            f"--scope-id \"{requested_scope}\" "
            f"--question-count {int(question_count)}"
        ),
        "next_steps": [
            f"$env:{PILOT_EVENT_LOG_ENV_VAR} = '{log_path}'",
            "python -m streamlit run streamlit_app.py",
            (
                f"python scripts/release_check.py finalize --input \"{log_path}\" "
                f"--output-dir \"{artifact_paths['output_dir']}\" "
                f"--scope-id \"{requested_scope}\" "
                f"--question-count {int(question_count)}"
            ),
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def finalize_release_check(
    input_path: Path,
    *,
    output_dir: Path | None = None,
    scope_id: str | None = None,
    question_count: int = DEFAULT_HAND_AUDIT_COUNT,
    max_sessions: int = DEFAULT_MAX_PILOT_SESSIONS,
    session_start_since: str | None = None,
    session_start_until: str | None = None,
    trusted_active_scope_only: bool = False,
    latest_session_only: bool = False,
) -> None:
    resolved_input = Path(input_path)
    artifact_paths = build_release_check_paths(resolved_input, output_dir)
    pilot_export = build_pilot_review_export(
        max_sessions=max_sessions,
        path=resolved_input,
        session_start_since=session_start_since,
        session_start_until=session_start_until,
        scope_id=scope_id,
        trusted_active_scope_only=trusted_active_scope_only,
        latest_session_only=latest_session_only,
    )
    hand_audit_packet = build_hand_audit_packet(scope_id=scope_id, question_count=question_count)
    summary = write_release_check_artifacts(
        input_log_path=resolved_input,
        pilot_export=pilot_export,
        hand_audit_packet=hand_audit_packet,
        artifact_paths=artifact_paths,
    )
    print(
        json.dumps(
            {
                "input_log_path": str(resolved_input),
                "scope_id": scope_id or ACTIVE_ASSESSMENT_SCOPE,
                "output_dir": str(artifact_paths["output_dir"]),
                "artifacts": {
                    key: str(path)
                    for key, path in artifact_paths.items()
                    if key != "output_dir"
                },
                "release_gate_checks": summary.get("release_gate_checks"),
                "pilot_review_summary": summary.get("pilot_review_summary"),
                "hand_audit_summary": summary.get("hand_audit_summary"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare and finalize combined release checks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare", help="Create a fresh isolated pilot target and print the finalize command.")
    prepare_parser.add_argument("--label", default="", help="Optional short label for the isolated pilot file.")
    prepare_parser.add_argument("--output-dir", type=Path, help="Optional release-check output directory.")
    prepare_parser.add_argument("--scope-id", default=ACTIVE_ASSESSMENT_SCOPE, help="Scope id for the hand-audit packet.")
    prepare_parser.add_argument("--question-count", type=int, default=DEFAULT_HAND_AUDIT_COUNT, help="Hand-audit question count.")

    finalize_parser = subparsers.add_parser(
        "finalize",
        help="Write the pilot review export, hand-audit packet, and compact release-check summary in one pass.",
    )
    finalize_parser.add_argument("--input", required=True, type=Path, help="Input pilot event log path.")
    finalize_parser.add_argument("--output-dir", type=Path, help="Optional output directory for release-check artifacts.")
    finalize_parser.add_argument("--scope-id", default=ACTIVE_ASSESSMENT_SCOPE, help="Scope id for pilot review and hand-audit generation.")
    finalize_parser.add_argument("--question-count", type=int, default=DEFAULT_HAND_AUDIT_COUNT, help="Hand-audit question count.")
    finalize_parser.add_argument("--max-sessions", type=int, default=DEFAULT_MAX_PILOT_SESSIONS, help="Number of recent pilot sessions to summarize.")
    finalize_parser.add_argument("--session-start-since", default=None, help="Optional inclusive ISO timestamp filter.")
    finalize_parser.add_argument("--session-start-until", default=None, help="Optional inclusive ISO timestamp filter.")
    finalize_parser.add_argument("--trusted-active-scope-only", action="store_true", help="Include only trusted active-scope pilot sessions.")
    finalize_parser.add_argument("--latest-session-only", action="store_true", help="Review only the latest included session after other filters.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "prepare":
        prepare_release_check(
            args.label,
            output_dir=args.output_dir,
            scope_id=args.scope_id,
            question_count=args.question_count,
        )
        return
    finalize_release_check(
        args.input,
        output_dir=args.output_dir,
        scope_id=args.scope_id,
        question_count=args.question_count,
        max_sessions=args.max_sessions,
        session_start_since=args.session_start_since,
        session_start_until=args.session_start_until,
        trusted_active_scope_only=bool(args.trusted_active_scope_only),
        latest_session_only=bool(args.latest_session_only),
    )


if __name__ == "__main__":
    main()
