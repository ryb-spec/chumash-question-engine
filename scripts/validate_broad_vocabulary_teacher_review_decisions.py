from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DECISION_TSV = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_teacher_review_decisions_applied_2026_04_30.tsv"
DECISION_JSON = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_teacher_review_decisions_applied_2026_04_30.json"
ELIGIBILITY_TSV = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.tsv"
ELIGIBILITY_JSON = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.json"
REPORT_MD = ROOT / "data/pipeline_rounds/broad_vocabulary_teacher_review_decisions_applied_2026_04_30.md"
CONTRACT_JSON = ROOT / "data/pipeline_rounds/broad_vocabulary_teacher_review_decisions_applied_2026_04_30.json"
NEXT_PROMPT = ROOT / "data/pipeline_rounds/next_codex_prompt_perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.md"

EXPECTED_DECISIONS = {
    "bsvb_p4_001": "approve_word_level",
    "bsvb_p4_002": "approve_word_level_with_revision",
    "bsvb_p4_003": "hold_for_follow_up",
    "bsvb_p4_004": "hold_for_follow_up",
    "bsvb_p4_005": "approve_word_level",
    "svqcl_p4_001": "approve_for_protected_preview_candidate",
    "svqcl_p4_002": "approve_for_protected_preview_candidate",
    "svqcl_p4_003": "approve_for_protected_preview_candidate",
    "svqcl_p4_004": "approve_with_revision",
    "svqcl_p4_005": "approve_for_protected_preview_candidate",
    "svqcl_p4_006": "approve_for_protected_preview_candidate",
    "svqcl_p4_007": "hold_for_follow_up",
    "svqcl_p4_008": "hold_for_follow_up",
    "svqcl_p4_009": "hold_for_follow_up",
    "svqcl_block_p4_001": "hold_for_follow_up",
    "svqcl_block_p4_002": "hold_for_follow_up",
}

EXPECTED_CLEAN_ELIGIBLE = {
    "svqcl_p4_001",
    "svqcl_p4_002",
    "svqcl_p4_003",
    "svqcl_p4_005",
    "svqcl_p4_006",
}

EXPECTED_REVISION_REQUIRED = {"bsvb_p4_002", "svqcl_p4_004"}
EXPECTED_HELD = {"bsvb_p4_003", "bsvb_p4_004", "svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009"}

FALSE_CONTRACT_FLAGS = [
    "fake_teacher_approval_created",
    "runtime_scope_widened",
    "perek_activated",
    "protected_preview_packet_created",
    "protected_preview_promoted",
    "reviewed_bank_promoted",
    "runtime_questions_created",
    "runtime_content_promoted",
    "scoring_mastery_changed",
    "question_generation_changed",
    "question_selection_changed",
    "question_selection_weighting_changed",
    "source_truth_changed",
    "fake_student_data_created",
    "raw_logs_exposed",
    "validators_weakened",
    "ready_for_runtime_activation",
    "runtime_activation_authorized",
]

FORBIDDEN_PHRASES = [
    "runtime ready",
    "activated perek 4",
    "reviewed bank promoted",
    "runtime content promoted",
    "student-facing content created",
    "mastery proven",
    "raw jsonl",
]

FORBIDDEN_CHANGED_PATHS = {
    "assessment_scope.py",
    "streamlit_app.py",
}

FORBIDDEN_CHANGED_PREFIXES = (
    "runtime/",
    "data/source_texts/",
    "data/gate_2_protected_preview_packets/",
    "data/reviewed_bank/",
)


def _fail(message: str) -> None:
    raise SystemExit(f"Broad vocabulary teacher review decisions validation failed: {message}")


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _changed_files() -> set[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        _fail("could not inspect git diff")
    return {line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()}


def validate() -> None:
    for path in [DECISION_TSV, DECISION_JSON, ELIGIBILITY_TSV, ELIGIBILITY_JSON, REPORT_MD, CONTRACT_JSON, NEXT_PROMPT]:
        if not path.exists():
            _fail(f"missing required file: {path.relative_to(ROOT)}")

    decision_rows = _rows(DECISION_TSV)
    eligibility_rows = _rows(ELIGIBILITY_TSV)
    decision_json = _json(DECISION_JSON)
    eligibility_json = _json(ELIGIBILITY_JSON)
    contract = _json(CONTRACT_JSON)

    if contract.get("feature_name") != "broad_vocabulary_teacher_review_decisions_applied":
        _fail("unexpected contract feature_name")
    if contract.get("teacher_decisions_created") is not True:
        _fail("teacher_decisions_created must be true")
    if decision_json.get("teacher_decisions_created") is not True:
        _fail("decision JSON must mark teacher decisions created")
    for payload in [decision_json, contract]:
        if payload.get("fake_teacher_approval_created") is not False:
            _fail("fake teacher approval flag must be false")
        if payload.get("reviewed_by") != "Yossi":
            _fail("reviewed_by must be Yossi")
        if payload.get("reviewed_at") != "2026-04-30":
            _fail("reviewed_at must be 2026-04-30")

    for flag in FALSE_CONTRACT_FLAGS:
        if contract.get(flag) is not False:
            _fail(f"{flag} must be false")

    if contract.get("clean_protected_preview_candidate_eligible_count") != 5:
        _fail("clean eligible count must be 5")
    if contract.get("revision_required_count") != 2:
        _fail("revision required count must be 2")
    if contract.get("held_count") != 7:
        _fail("held count must be 7 decision rows")
    if contract.get("word_level_approved_count") != 3:
        _fail("word-level approved count must be 3")
    if contract.get("ready_for_future_protected_preview_candidate_gate") is not True:
        _fail("future candidate gate readiness must be true")

    if len(decision_rows) != 16:
        _fail("decision TSV must contain 16 decision rows")

    decisions_by_source = {row["source_id"]: row for row in decision_rows}
    if set(decisions_by_source) != set(EXPECTED_DECISIONS):
        _fail("decision source set does not match expected Yossi decisions")
    for source_id, expected in EXPECTED_DECISIONS.items():
        actual = decisions_by_source[source_id]["yossi_decision"]
        if actual != expected:
            _fail(f"{source_id} decision must be {expected}, got {actual}")
        if actual in {"", "pending", "needs_teacher_review", "not_applicable"}:
            _fail(f"{source_id} has a blank/pending decision")
        if decisions_by_source[source_id]["reviewed_by"] != "Yossi":
            _fail(f"{source_id} reviewed_by must be Yossi")
        if decisions_by_source[source_id]["reviewed_at"] != "2026-04-30":
            _fail(f"{source_id} reviewed_at must be 2026-04-30")
        if decisions_by_source[source_id]["runtime_status"] != "not_runtime":
            _fail(f"{source_id} runtime_status must remain not_runtime")
        if decisions_by_source[source_id]["reviewed_bank_status"] != "not_reviewed_bank":
            _fail(f"{source_id} reviewed_bank_status must remain not_reviewed_bank")

    if decisions_by_source["bsvb_p4_002"]["protected_preview_candidate_eligibility"] != "revision_required_before_future_gate":
        _fail("צאן word-level row must require revision before future gate")
    if decisions_by_source["svqcl_p4_004"]["protected_preview_candidate_eligibility"] != "revision_required_before_future_gate":
        _fail("צאן translate candidate must require revision before future gate")
    for source_id in ["svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009", "bsvb_p4_003", "bsvb_p4_004"]:
        if decisions_by_source[source_id]["yossi_decision"] != "hold_for_follow_up":
            _fail(f"{source_id} must remain held")

    clean = {row["source_id"] for row in eligibility_rows if row["eligibility_classification"] == "clean_eligible_for_future_protected_preview_candidate_gate"}
    revision = {row["source_id"] for row in eligibility_rows if row["eligibility_classification"] == "revision_required_before_future_gate"}
    held = {row["source_id"] for row in eligibility_rows if row["eligibility_classification"] == "held_for_follow_up"}
    if clean != EXPECTED_CLEAN_ELIGIBLE:
        _fail(f"clean eligibility set mismatch: {sorted(clean)}")
    if revision != EXPECTED_REVISION_REQUIRED:
        _fail("revision-required eligibility set mismatch")
    if held != EXPECTED_HELD:
        _fail("held eligibility set mismatch")
    if clean.intersection(revision | held):
        _fail("revision-required or held rows must not be clean eligible")

    if set(eligibility_json.get("clean_eligible_candidate_ids", [])) != EXPECTED_CLEAN_ELIGIBLE:
        _fail("eligibility JSON clean candidate IDs mismatch")
    if set(eligibility_json.get("revision_required_source_ids", [])) != EXPECTED_REVISION_REQUIRED:
        _fail("eligibility JSON revision IDs mismatch")
    if set(eligibility_json.get("held_source_ids", [])) != EXPECTED_HELD:
        _fail("eligibility JSON held IDs mismatch")

    changed = _changed_files()
    forbidden = changed.intersection(FORBIDDEN_CHANGED_PATHS)
    forbidden.update(path for path in changed if path.startswith(FORBIDDEN_CHANGED_PREFIXES))
    if forbidden:
        _fail(f"forbidden changed paths found: {sorted(forbidden)}")

    scanned_text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [REPORT_MD, CONTRACT_JSON, NEXT_PROMPT, DECISION_JSON, ELIGIBILITY_JSON]
    )
    for phrase in FORBIDDEN_PHRASES:
        if phrase in scanned_text:
            _fail(f"forbidden positive claim found: {phrase}")

    print("Broad vocabulary teacher review decisions validation passed.")


if __name__ == "__main__":
    validate()

