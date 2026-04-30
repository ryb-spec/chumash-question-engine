from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOCAB_TSV = ROOT / "data" / "vocabulary_bank" / "bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.tsv"
CANDIDATE_TSV = ROOT / "data" / "question_candidate_lanes" / "bereishis_perek_4_simple_vocabulary_question_candidates_2026_04_30.tsv"
CANDIDATE_JSON = ROOT / "data" / "question_candidate_lanes" / "bereishis_perek_4_simple_vocabulary_question_candidates_2026_04_30.json"
BLOCKER_TSV = ROOT / "data" / "question_candidate_lanes" / "bereishis_perek_4_simple_vocabulary_question_candidate_blockers_2026_04_30.tsv"
BLOCKER_JSON = ROOT / "data" / "question_candidate_lanes" / "bereishis_perek_4_simple_vocabulary_question_candidate_blockers_2026_04_30.json"
REPORT_MD = ROOT / "data" / "pipeline_rounds" / "simple_vocabulary_question_candidate_lane_v1_2026_04_30.md"
CONTRACT_JSON = ROOT / "data" / "pipeline_rounds" / "simple_vocabulary_question_candidate_lane_v1_2026_04_30.json"
NEXT_PROMPT = ROOT / "data" / "pipeline_rounds" / "next_codex_prompt_broad_vocabulary_teacher_review_packet_2026_04_30.md"

ALLOWED_LANES = {
    "translate_hebrew_to_english",
    "identify_hebrew_from_english",
    "find_word_in_pasuk",
    "classify_basic_part_of_speech",
}
FORBIDDEN_LANES = {
    "tense",
    "shoresh_identification",
    "prefix_suffix_analysis",
    "phrase_translation",
    "rashi",
    "inference",
    "conceptual_comprehension",
    "context_sensitive_meaning",
    "pasuk_level_translation",
    "dikduk_morphology",
    "gender_number_person",
    "vav_hahipuch",
}
REQUIRED_CANDIDATE_COLUMNS = {
    "candidate_id",
    "vocabulary_id",
    "sefer",
    "perek",
    "pasuk",
    "pasuk_ref",
    "hebrew_word",
    "normalized_hebrew",
    "display_hebrew",
    "english_gloss",
    "skill_category",
    "vocabulary_safety_classification",
    "allowed_question_lane",
    "candidate_prompt_template",
    "teacher_review_prompt_preview",
    "expected_answer",
    "expected_answer_source",
    "distractor_policy",
    "source_evidence_artifacts",
    "candidate_status",
    "teacher_review_status",
    "protected_preview_status",
    "reviewed_bank_status",
    "runtime_status",
    "blocker_reason",
    "revision_note",
    "safety_notes",
    "allowed_next_use",
}


def _read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise AssertionError(f"missing TSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader)


def _read_json(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing JSON: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _assert_false(payload: dict, fields: list[str]) -> None:
    for field in fields:
        if payload.get(field) is not False:
            raise AssertionError(f"{field} must be false")


def _changed_files() -> set[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return {line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()}


def validate() -> None:
    vocab_rows = _read_tsv(VOCAB_TSV)
    candidate_rows = _read_tsv(CANDIDATE_TSV)
    blocker_rows = _read_tsv(BLOCKER_TSV)
    candidate_payload = _read_json(CANDIDATE_JSON)
    blocker_payload = _read_json(BLOCKER_JSON)
    contract = _read_json(CONTRACT_JSON)
    for path in [REPORT_MD, NEXT_PROMPT]:
        if not path.exists():
            raise AssertionError(f"missing artifact: {path}")

    if not candidate_rows:
        raise AssertionError("candidate TSV must not be empty")
    missing_columns = REQUIRED_CANDIDATE_COLUMNS - set(candidate_rows[0])
    if missing_columns:
        raise AssertionError(f"candidate TSV missing columns: {sorted(missing_columns)}")

    vocab_ids = {row["vocabulary_id"] for row in vocab_rows}
    for row in candidate_rows:
        if row["vocabulary_id"] not in vocab_ids:
            raise AssertionError(f"candidate maps to unknown vocabulary_id: {row['vocabulary_id']}")
        if row["perek"] != "4":
            raise AssertionError("only Perek 4 candidates may be included")
        if row["allowed_question_lane"] not in ALLOWED_LANES:
            raise AssertionError(f"unsupported lane: {row['allowed_question_lane']}")
        if row["allowed_question_lane"] in FORBIDDEN_LANES:
            raise AssertionError(f"forbidden lane used: {row['allowed_question_lane']}")
        if row["runtime_status"] != "not_runtime":
            raise AssertionError("candidate runtime status must be not_runtime")
        if row["reviewed_bank_status"] != "not_reviewed_bank":
            raise AssertionError("candidate reviewed-bank status must remain closed")
        if row["protected_preview_status"] not in {"not_promoted", "blocked"}:
            raise AssertionError("protected-preview status must not be promoted")
        if row["teacher_review_status"] not in {"needs_teacher_review", "blocked"}:
            raise AssertionError("teacher review status must be needs_teacher_review or blocked")
        if row["distractor_policy"] not in {
            "no_distractors_needed",
            "use_only_bank_verified_same_perek_words",
            "use_only_teacher_approved_distractors_later",
            "blocked_until_distractors_reviewed",
        }:
            raise AssertionError("invalid distractor policy")
        if "|" in row["distractor_policy"]:
            raise AssertionError("distractor policy must not contain invented distractors")

    if any(row["perek"] in {"5", "6"} for row in candidate_rows):
        raise AssertionError("Perek 5/6 candidates must not be included")
    if {row["vocabulary_id"] for row in blocker_rows} != {"bsvb_p4_003", "bsvb_p4_004"}:
        raise AssertionError("blocker register must include the two Perek 4 revision-needed rows")
    if blocker_payload.get("blocker_count") != 2:
        raise AssertionError("blocker JSON count must be 2")
    if candidate_payload.get("candidate_count") != len(candidate_rows):
        raise AssertionError("candidate JSON count must match TSV")

    _assert_false(
        contract,
        [
            "runtime_questions_created",
            "protected_preview_promoted",
            "reviewed_bank_promoted",
            "runtime_content_promoted",
            "runtime_scope_widened",
            "perek_activated",
            "question_generation_changed",
            "question_selection_changed",
            "question_selection_weighting_changed",
            "scoring_mastery_changed",
            "source_truth_changed",
            "fake_teacher_approval_created",
            "fake_student_data_created",
            "raw_logs_exposed",
            "validators_weakened",
            "ready_for_protected_preview_promotion",
            "ready_for_reviewed_bank_promotion",
            "ready_for_runtime_activation",
            "runtime_activation_authorized",
        ],
    )
    if contract.get("question_candidates_created") is not True:
        raise AssertionError("contract must record question candidates")
    if contract.get("ready_for_teacher_review_packet") is not True:
        raise AssertionError("contract must be ready for teacher review packet")
    if contract.get("perek_5_6_status") != "planning_only":
        raise AssertionError("Perek 5/6 status must remain planning_only")

    changed_files = _changed_files()
    forbidden_changed = {"assessment_scope.py", "streamlit_app.py", "runtime/question_flow.py", "engine/flow_builder.py"}
    touched_forbidden = sorted(changed_files & forbidden_changed)
    if touched_forbidden:
        raise AssertionError(f"forbidden runtime/scope files changed: {touched_forbidden}")

    artifact_text = "\n".join(
        path.read_text(encoding="utf-8-sig").lower()
        for path in [CANDIDATE_TSV, CANDIDATE_JSON, BLOCKER_TSV, BLOCKER_JSON, REPORT_MD, CONTRACT_JSON, NEXT_PROMPT]
    )
    for phrase in [
        "approved for runtime",
        "runtime ready",
        "reviewed bank promoted",
        "teacher approved",
        "protected preview promoted",
        "activated perek 4",
        "scope widened",
        "mastery proven",
        "raw jsonl",
    ]:
        if phrase in artifact_text:
            raise AssertionError(f"forbidden language found: {phrase}")
    if "safety confirmation" not in REPORT_MD.read_text(encoding="utf-8-sig").lower():
        raise AssertionError("report must contain safety confirmation")

    print("Simple vocabulary question candidate lane validation passed.")


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:  # pragma: no cover
        print(f"Simple vocabulary question candidate lane validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
