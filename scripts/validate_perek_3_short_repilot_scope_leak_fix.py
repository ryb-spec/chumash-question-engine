from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FIX_REPORT = ROOT / "data/pipeline_rounds/perek_3_short_repilot_scope_leak_fix_report_2026_04_29.md"
ENFORCEMENT_MD = ROOT / "data/pipeline_rounds/perek_3_short_repilot_enforcement_plan_2026_04_29.md"
ENFORCEMENT_JSON = ROOT / "data/pipeline_rounds/perek_3_short_repilot_enforcement_plan_2026_04_29.json"
PEREK_4_GATE_MD = ROOT / "data/pipeline_rounds/perek_3_short_repilot_to_perek_4_ready_gate_2026_04_29.md"
PEREK_4_GATE_JSON = ROOT / "data/pipeline_rounds/perek_3_short_repilot_to_perek_4_ready_gate_2026_04_29.json"
ACTIVE_REVIEWED_QUESTIONS = ROOT / "data/active_scope_reviewed_questions.json"

REQUIRED_FILES = (
    FIX_REPORT,
    ENFORCEMENT_MD,
    ENFORCEMENT_JSON,
    PEREK_4_GATE_MD,
    PEREK_4_GATE_JSON,
    ACTIVE_REVIEWED_QUESTIONS,
)

PREFIX_QUESTION_TYPE = "prefix_level_1_identify_prefix_letter"
STALE_PREFIX_PREFIX = "What is the prefix in "
BAISHTO = "בְּאִשְׁתּוֹ"
BAISHTO_NEW_PROMPT = f"In {BAISHTO}, which beginning letter is the prefix?"

FORBIDDEN_PATTERNS = (
    "runtime_allowed=true",
    "runtime_allowed: true",
    "approved_for_runtime",
    "promoted_to_runtime",
    '"perek_4_activated": true',
    '"runtime_scope_widened": true',
    '"reviewed_bank_runtime_promoted": true',
    "Perek 4 is active",
    "Perek 4 is activated",
    "activate Perek 4 now",
    "invented observation",
    "synthetic observation",
)


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _load_json(path: Path, errors: list[str]) -> dict:
    try:
        payload = json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"{_relative(path)} is invalid JSON: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{_relative(path)} must be a JSON object")
        return {}
    return payload


def _require_bool(payload: dict, key: str, expected: bool, errors: list[str], path: Path) -> None:
    if payload.get(key) is not expected:
        errors.append(f"{_relative(path)} must set {key} to {expected}")


def _prefix_prompt_summary(errors: list[str]) -> dict:
    payload = _load_json(ACTIVE_REVIEWED_QUESTIONS, errors)
    questions = payload.get("questions", []) if isinstance(payload, dict) else []
    if not isinstance(questions, list):
        errors.append("data/active_scope_reviewed_questions.json must contain a questions list")
        return {
            "stale_prefix_rows": [],
            "baishto_rows": [],
            "perek_4_rows": [],
        }

    stale_prefix_rows = []
    baishto_rows = []
    perek_4_rows = []
    for question in questions:
        if not isinstance(question, dict):
            continue
        if str(question.get("pasuk_id") or "").startswith("bereishis_4_"):
            perek_4_rows.append(question.get("reviewed_id"))
        if question.get("question_type") != PREFIX_QUESTION_TYPE:
            continue
        fields = {
            "question": str(question.get("question") or ""),
            "question_text": str(question.get("question_text") or ""),
        }
        if any(value.startswith(STALE_PREFIX_PREFIX) for value in fields.values()):
            stale_prefix_rows.append(
                {
                    "reviewed_id": question.get("reviewed_id"),
                    "word": question.get("selected_word") or question.get("word"),
                    "question": fields["question"],
                    "question_text": fields["question_text"],
                }
            )
        if (question.get("selected_word") or question.get("word")) == BAISHTO:
            baishto_rows.append(question)

    return {
        "stale_prefix_rows": stale_prefix_rows,
        "baishto_rows": baishto_rows,
        "perek_4_rows": perek_4_rows,
    }


def validate() -> dict:
    errors: list[str] = []
    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {_relative(path)}")
    if errors:
        return {"ok": False, "errors": errors}

    enforcement = _load_json(ENFORCEMENT_JSON, errors)
    gate = _load_json(PEREK_4_GATE_JSON, errors)
    prompt_summary = _prefix_prompt_summary(errors)

    for key in (
        "old_prefix_wording_leak_addressed",
        "stale_prefix_prompt_fixed_in_active_reviewed_bank",
        "phrase_translation_leak_guarded_by_validator",
        "ready_for_clean_short_repilot",
        "perek_4_teacher_review_packet_allowed_after_clean_short_repilot",
        "clean_short_repilot_required_before_perek_4_teacher_review_packet",
    ):
        _require_bool(enforcement, key, True, errors, ENFORCEMENT_JSON)
    for key in (
        "runtime_scope_widened",
        "perek_4_activated",
        "runtime_enforced",
        "data_enforced",
        "phrase_translation_leak_addressed_by_runtime_filter",
        "reviewed_bank_runtime_promoted",
        "source_truth_changed",
        "question_selection_changed",
        "fake_data_created",
    ):
        _require_bool(enforcement, key, False, errors, ENFORCEMENT_JSON)
    if enforcement.get("enforcement_type") != "manual":
        errors.append("enforcement_type must remain manual for this narrow scope-leak fix")
    if enforcement.get("manual_scope_watch_required") is not True:
        errors.append("manual_scope_watch_required must remain true")

    for key in (
        "scope_leak_fix_completed",
        "stale_prefix_prompt_fixed",
        "phrase_translation_validator_guard_added",
        "clean_short_repilot_still_required",
        "explicit_yossi_override_required_to_skip_clean_short_repilot",
        "perek_4_teacher_review_packet_allowed_after_clean_short_repilot",
    ):
        _require_bool(gate, key, True, errors, PEREK_4_GATE_JSON)
    for key in (
        "clean_short_repilot_closure",
        "full_perek_3_closure_allowed_now",
        "perek_3_full_closure_go",
        "perek_3_runtime_expansion_go",
        "perek_4_teacher_review_packet_go",
        "perek_4_activated",
        "perek_4_runtime_activation_go",
        "perek_4_reviewed_bank_promotion_go",
        "perek_4_student_facing_go",
        "runtime_scope_widened",
        "reviewed_bank_promoted",
        "source_truth_changed",
        "fake_data_created",
    ):
        _require_bool(gate, key, False, errors, PEREK_4_GATE_JSON)

    if prompt_summary["stale_prefix_rows"]:
        errors.append(
            "active reviewed-bank prefix rows still use stale wording: "
            + ", ".join(str(row.get("reviewed_id")) for row in prompt_summary["stale_prefix_rows"])
        )
    if not prompt_summary["baishto_rows"]:
        errors.append("בְּאִשְׁתּוֹ prefix item must still be present in active reviewed-bank data")
    for row in prompt_summary["baishto_rows"]:
        if row.get("question") != BAISHTO_NEW_PROMPT:
            errors.append("בְּאִשְׁתּוֹ question field must use revised prefix wording")
        if row.get("question_text") != BAISHTO_NEW_PROMPT:
            errors.append("בְּאִשְׁתּוֹ question_text field must use revised prefix wording")
        if row.get("correct_answer") != "ב":
            errors.append("בְּאִשְׁתּוֹ correct answer must remain ב")
        if row.get("question_type") != PREFIX_QUESTION_TYPE:
            errors.append("בְּאִשְׁתּוֹ question_type must remain prefix_level_1_identify_prefix_letter")
    if prompt_summary["perek_4_rows"]:
        errors.append("active reviewed-bank data must not include Bereishis Perek 4 rows")

    fix_text = _read_text(FIX_REPORT)
    enforcement_text = _read_text(ENFORCEMENT_MD)
    gate_text = _read_text(PEREK_4_GATE_MD)
    for required in (
        "What is the prefix in <word>?",
        "In <word>, which beginning letter is the prefix?",
        "phrase_translation",
        "manual plus validator guard",
        "Another short re-pilot is still required",
        "Perek 4 teacher-review packet work may proceed only after a clean short Perek 3 re-pilot or an explicit Yossi override",
    ):
        if required not in fix_text:
            errors.append(f"scope leak fix report missing required phrase: {required}")
    for required in (
        "old_prefix_wording_leak_addressed: true",
        "phrase_translation_leak_guarded_by_validator: true",
        "manual_scope_watch_required: true",
        "Perek 4 activated: false",
        "Runtime scope widened: false",
    ):
        if required not in enforcement_text:
            errors.append(f"enforcement plan missing required phrase: {required}")
    for required in (
        "Scope leak fix completed: true.",
        "Clean short re-pilot still required: true.",
        "Perek 4 teacher-review packet may proceed only after a clean short re-pilot or explicit Yossi override.",
        "Perek 4 runtime activation",
    ):
        if required not in gate_text:
            errors.append(f"Perek 3-to-Perek 4 gate missing required phrase: {required}")

    for path in (FIX_REPORT, ENFORCEMENT_MD, ENFORCEMENT_JSON, PEREK_4_GATE_MD, PEREK_4_GATE_JSON):
        text = _read_text(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                errors.append(f"{_relative(path)} contains forbidden claim: {pattern}")

    return {
        "ok": not errors,
        "errors": errors,
        "stale_prefix_row_count": len(prompt_summary["stale_prefix_rows"]),
        "baishto_row_count": len(prompt_summary["baishto_rows"]),
        "perek_4_row_count": len(prompt_summary["perek_4_rows"]),
    }


def main() -> int:
    result = validate()
    if not result["ok"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        return 1
    print("Perek 3 short re-pilot scope leak fix validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
