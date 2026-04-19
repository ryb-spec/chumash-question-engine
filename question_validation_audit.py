from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from assessment_scope import active_pesukim_records, active_scope_summary, data_path
from pasuk_flow_generator import (
    analyze_pasuk,
    apply_prefix_metadata,
    apply_suffix_metadata,
    entry_type,
    extract_prefix,
    extract_suffix,
    is_placeholder_translation,
    load_word_bank,
    quiz_eligible,
    usable_translation,
    validate_question_candidate,
)


VALIDATION_DIR = data_path("validation")
AUDIT_MARKDOWN_PATH = VALIDATION_DIR / "question_validation_audit.md"
AUDIT_JSON_PATH = VALIDATION_DIR / "question_validation_audit.json"
REPORT_VERSION = 1
TOP_LIMIT = 10
TRANSLATION_FIELDS = (
    "translation_context",
    "context_translation",
    "translation",
    "translation_literal",
)


def validation_result(valid, reason_codes=None, details=None):
    return {
        "valid": bool(valid),
        "reason_codes": list(reason_codes or []),
        "details": dict(details or {}),
    }


def invalid_result(*reason_codes, **details):
    return validation_result(False, reason_codes=reason_codes, details=details)


def _prefix_forms(entry):
    forms = []
    for item in (entry or {}).get("prefixes") or []:
        if not isinstance(item, dict):
            continue
        form = item.get("form")
        if form and form not in forms:
            forms.append(form)
    legacy = (entry or {}).get("prefix")
    if legacy and legacy not in forms:
        forms.insert(0, legacy)
    return forms


def _suffix_forms(entry):
    forms = []
    for item in (entry or {}).get("suffixes") or []:
        if not isinstance(item, dict):
            continue
        form = item.get("form")
        if form and form not in forms:
            forms.append(form)
    legacy = (entry or {}).get("suffix")
    if legacy and legacy not in forms:
        forms.insert(0, legacy)
    return forms


def _sorted_counter_rows(counter, *, key_name, value_name="count", limit=None):
    items = sorted(counter.items(), key=lambda item: (-item[1], str(item[0])))
    if limit is not None:
        items = items[:limit]
    return [{key_name: key, value_name: count} for key, count in items]


def _scope_ref_label(record):
    ref = record.get("ref", {})
    sefer = ref.get("sefer", "Unknown")
    perek = ref.get("perek", "?")
    pasuk = ref.get("pasuk", "?")
    return f"{sefer} {perek}:{pasuk}"


def _format_scope_range(scope_summary):
    range_data = (scope_summary or {}).get("range") or {}
    start = range_data.get("start") or {}
    end = range_data.get("end") or {}
    if not start or not end:
        return "unknown"
    return f"{start.get('perek')}:{start.get('pasuk')}-{end.get('perek')}:{end.get('pasuk')}"


def _prepare_entry(token, entry, word_bank, *, add_prefix=False, add_suffix=False):
    prepared = dict(entry or {})
    if add_prefix:
        apply_prefix_metadata(token, prepared, word_bank)
    if add_suffix:
        apply_suffix_metadata(token, prepared, word_bank)
    return prepared


def _prefix_candidate_seen(entry, token, word_bank):
    return bool(extract_prefix(token, word_bank) or _prefix_forms(entry))


def _suffix_candidate_seen(entry, token, word_bank):
    return bool(extract_suffix(token) or _suffix_forms(entry))


def _shoresh_candidate_seen(entry, token, word_bank):
    del token, word_bank
    return entry_type(entry) == "verb"


def _tense_candidate_seen(entry, token, word_bank):
    del token, word_bank
    return entry_type(entry) == "verb" or bool((entry or {}).get("tense"))


def _translation_candidate_seen(entry, token, word_bank):
    del word_bank
    if not token:
        return False
    if (entry or {}).get("entity_type") == "grammatical_particle":
        return True
    if (entry or {}).get("part_of_speech") == "particle" or entry_type(entry) == "particle":
        return True
    if any((entry or {}).get(field) not in {None, ""} for field in TRANSLATION_FIELDS):
        return True
    return entry_type(entry) in {"noun", "verb", "adjective", "prep", "preposition", "unknown"}


def contextual_meaning_validation_result(
    token,
    entry,
    correct_answer=None,
    choices=None,
    choice_entries=None,
):
    del correct_answer, choices, choice_entries

    entry = entry or {}
    if entry.get("entity_type") == "grammatical_particle":
        return invalid_result("grammatical_particle", entity_type=entry.get("entity_type"))

    if entry.get("part_of_speech") == "particle" or entry_type(entry) == "particle":
        return invalid_result("grammatical_particle", part_of_speech=entry.get("part_of_speech"))

    translation_values = [
        entry.get(field)
        for field in TRANSLATION_FIELDS
        if entry.get(field) not in {None, ""}
    ]
    if translation_values and all(is_placeholder_translation(value, token) for value in translation_values):
        return invalid_result("placeholder_translation")

    translation = usable_translation(entry, token)
    if translation is None:
        return invalid_result("no_usable_translation")

    if not quiz_eligible(entry, token, "word_meaning"):
        return invalid_result(
            "low_instructional_value",
            entry_type=entry_type(entry),
            confidence=entry.get("confidence"),
        )

    return validation_result(True, details={"translation": translation})


AUDIT_SKILL_SPECS = (
    {
        "key": "prefix",
        "title": "Prefix",
        "validator_skill": "identify_prefix_meaning",
        "candidate_seen": _prefix_candidate_seen,
        "add_prefix": True,
        "add_suffix": True,
        "selection_validation": True,
    },
    {
        "key": "suffix",
        "title": "Suffix",
        "validator_skill": "identify_suffix_meaning",
        "candidate_seen": _suffix_candidate_seen,
        "add_prefix": True,
        "add_suffix": True,
        "selection_validation": True,
    },
    {
        "key": "shoresh",
        "title": "Shoresh",
        "validator_skill": "shoresh",
        "candidate_seen": _shoresh_candidate_seen,
        "add_prefix": True,
        "add_suffix": True,
        "selection_validation": True,
    },
    {
        "key": "tense",
        "title": "Tense",
        "validator_skill": "verb_tense",
        "candidate_seen": _tense_candidate_seen,
        "add_prefix": True,
        "add_suffix": True,
        "selection_validation": True,
    },
    {
        "key": "translation",
        "title": "Translation / Context",
        "validator": contextual_meaning_validation_result,
        "candidate_seen": _translation_candidate_seen,
        "add_prefix": False,
        "add_suffix": False,
        "selection_validation": False,
    },
)


def _scan_scope_records():
    word_bank, _by_group = load_word_bank()
    scope_rows = []
    analysis_errors = []
    pasuk_refs = []

    for record in active_pesukim_records():
        ref_label = _scope_ref_label(record)
        pasuk_refs.append(ref_label)
        try:
            analyzed = analyze_pasuk(record.get("text", ""), word_bank)
        except Exception as error:  # pragma: no cover - defensive, hard to force safely
            analysis_errors.append({"ref": ref_label, "error": str(error)})
            analyzed = []
        scope_rows.append({"record": record, "ref": ref_label, "items": analyzed})

    return word_bank, tuple(scope_rows), tuple(pasuk_refs), analysis_errors


def audit_skill_rows(skill_spec, scope_rows, word_bank):
    candidates = []
    for scope_row in scope_rows:
        for item in scope_row.get("items", []):
            token = item.get("token")
            entry = item.get("entry") or {}
            if not skill_spec["candidate_seen"](entry, token, word_bank):
                continue
            candidates.append(
                {
                    "ref": scope_row["ref"],
                    "pasuk_id": scope_row["record"].get("pasuk_id"),
                    "token": token,
                    "entry": _prepare_entry(
                        token,
                        entry,
                        word_bank,
                        add_prefix=skill_spec.get("add_prefix", False),
                        add_suffix=skill_spec.get("add_suffix", False),
                    ),
                }
            )

    selection_choice_entries = {}
    if skill_spec.get("selection_validation"):
        for candidate in candidates:
            selection_choice_entries.setdefault(candidate["token"], candidate["entry"])

    rows = []
    for candidate in candidates:
        if skill_spec.get("validator_skill"):
            choice_entries = None
            correct_answer = None
            if skill_spec.get("selection_validation"):
                choice_entries = dict(selection_choice_entries)
                choice_entries[candidate["token"]] = candidate["entry"]
                correct_answer = candidate["token"]
            result = validate_question_candidate(
                skill_spec["validator_skill"],
                candidate["token"],
                candidate["entry"],
                correct_answer=correct_answer,
                choice_entries=choice_entries,
            )
        else:
            result = skill_spec["validator"](candidate["token"], candidate["entry"])

        rows.append(
            {
                "ref": candidate["ref"],
                "pasuk_id": candidate["pasuk_id"],
                "token": candidate["token"],
                "valid": bool(result.get("valid")),
                "reason_codes": list(result.get("reason_codes") or []),
                "details": dict(result.get("details") or {}),
            }
        )

    return rows


def summarize_skill_rows(skill_key, title, rows, all_pasuk_refs):
    invalid_rows = [row for row in rows if not row.get("valid")]
    valid_rows = [row for row in rows if row.get("valid")]
    invalid_by_reason = Counter()
    blocked_forms = Counter()
    valid_forms = {row["token"] for row in valid_rows}

    for row in invalid_rows:
        reasons = row.get("reason_codes") or ["invalid_question"]
        invalid_by_reason.update(reasons)
        if row["token"] not in valid_forms:
            blocked_forms[row["token"]] += 1

    valid_refs = {row["ref"] for row in valid_rows}
    no_safe_refs = [ref for ref in all_pasuk_refs if ref not in valid_refs]

    total_candidates_seen = len(rows)
    valid_candidates = len(valid_rows)
    invalid_candidates = len(invalid_rows)
    valid_percent = round((valid_candidates / total_candidates_seen) * 100, 1) if total_candidates_seen else 0.0

    return {
        "skill": skill_key,
        "title": title,
        "total_candidates_seen": total_candidates_seen,
        "valid_candidates": valid_candidates,
        "invalid_candidates": invalid_candidates,
        "valid_percent": valid_percent,
        "invalid_by_reason": _sorted_counter_rows(
            invalid_by_reason,
            key_name="reason",
            limit=TOP_LIMIT,
        ),
        "most_common_blocked_forms": _sorted_counter_rows(
            blocked_forms,
            key_name="form",
            limit=TOP_LIMIT,
        ),
        "forms_without_safe_candidate_paths": _sorted_counter_rows(
            blocked_forms,
            key_name="form",
        ),
        "pesukim_with_no_safe_candidate_paths": no_safe_refs,
        "sample_pesukim_with_no_safe_candidate_paths": no_safe_refs[:TOP_LIMIT],
    }


def summarize_overall(skill_summaries):
    reason_counter = Counter()
    blocked_counter = Counter()

    for summary in skill_summaries:
        for item in summary.get("invalid_by_reason", []):
            reason_counter[item["reason"]] += item["count"]
        for item in summary.get("forms_without_safe_candidate_paths", []):
            blocked_counter[item["form"]] += item["count"]

    return {
        "top_rejection_reasons": _sorted_counter_rows(
            reason_counter,
            key_name="reason",
            limit=TOP_LIMIT,
        ),
        "most_common_blocked_forms": _sorted_counter_rows(
            blocked_counter,
            key_name="form",
            limit=TOP_LIMIT,
        ),
    }


def build_question_validation_audit():
    word_bank, scope_rows, pasuk_refs, analysis_errors = _scan_scope_records()
    skill_summaries = []

    for skill_spec in AUDIT_SKILL_SPECS:
        rows = audit_skill_rows(skill_spec, scope_rows, word_bank)
        skill_summaries.append(
            summarize_skill_rows(
                skill_spec["key"],
                skill_spec["title"],
                rows,
                pasuk_refs,
            )
        )

    return {
        "report_version": REPORT_VERSION,
        "scope_summary": active_scope_summary(),
        "analysis_errors": analysis_errors,
        "skills": skill_summaries,
        "overall": summarize_overall(skill_summaries),
    }


def _markdown_count_lines(items, label, field, *, limit=TOP_LIMIT):
    if not items:
        return [f"- No {label.lower()}."]
    lines = []
    for item in items[:limit]:
        lines.append(f"- `{item[label]}`: {item[field]}")
    return lines


def render_question_validation_markdown(report):
    scope_summary = report.get("scope_summary") or {}
    lines = [
        "# Question Validation Audit",
        "",
        "## Scope",
        "",
        f"- Active scope: `{scope_summary.get('scope', 'unknown')}`",
        f"- Sefer: {scope_summary.get('sefer', 'unknown')}",
        f"- Range: {_format_scope_range(scope_summary)}",
        f"- Pesukim in active scope: {scope_summary.get('pesukim_count', 0)}",
        "",
        "## Coverage Snapshot",
        "",
        "| Skill | Total Seen | Valid | Invalid | Valid % |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for summary in report.get("skills", []):
        lines.append(
            f"| {summary['title']} | {summary['total_candidates_seen']} | "
            f"{summary['valid_candidates']} | {summary['invalid_candidates']} | "
            f"{summary['valid_percent']}% |"
        )

    lines.extend(
        [
            "",
            "## Top Rejection Reasons",
            "",
            *_markdown_count_lines(
                report.get("overall", {}).get("top_rejection_reasons", []),
                "reason",
                "count",
            ),
            "",
            "## Most Common Blocked Forms",
            "",
            *_markdown_count_lines(
                report.get("overall", {}).get("most_common_blocked_forms", []),
                "form",
                "count",
            ),
            "",
        ]
    )

    if report.get("analysis_errors"):
        lines.extend(
            [
                "## Analysis Errors",
                "",
                *[
                    f"- `{item['ref']}`: {item['error']}"
                    for item in report.get("analysis_errors", [])
                ],
                "",
            ]
        )

    for summary in report.get("skills", []):
        lines.extend(
            [
                f"## {summary['title']}",
                "",
                f"- Total candidates seen: {summary['total_candidates_seen']}",
                f"- Valid candidates: {summary['valid_candidates']}",
                f"- Invalid candidates: {summary['invalid_candidates']}",
                f"- Valid coverage: {summary['valid_percent']}%",
                f"- Pesukim with no safe candidate paths: {len(summary['pesukim_with_no_safe_candidate_paths'])}",
                "",
                "### Invalid by Reason",
                "",
                *_markdown_count_lines(summary.get("invalid_by_reason", []), "reason", "count"),
                "",
                "### Most Common Blocked Forms",
                "",
                *_markdown_count_lines(summary.get("most_common_blocked_forms", []), "form", "count"),
                "",
                "### Pesukim With No Safe Candidate Paths",
                "",
            ]
        )
        if summary.get("sample_pesukim_with_no_safe_candidate_paths"):
            lines.extend(
                [
                    f"- `{ref}`"
                    for ref in summary.get("sample_pesukim_with_no_safe_candidate_paths", [])
                ]
            )
        else:
            lines.append("- None.")
        lines.append("")

    return "\n".join(lines)


def write_question_validation_audit(report=None):
    report = report or build_question_validation_audit()
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_JSON_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    AUDIT_MARKDOWN_PATH.write_text(
        render_question_validation_markdown(report),
        encoding="utf-8",
    )
    return {
        "json_path": AUDIT_JSON_PATH,
        "markdown_path": AUDIT_MARKDOWN_PATH,
        "report": report,
    }
