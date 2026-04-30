from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PACKET_MD = ROOT / "data/pipeline_rounds/broad_vocabulary_teacher_review_packet_v1_2026_04_30.md"
PACKET_JSON = ROOT / "data/pipeline_rounds/broad_vocabulary_teacher_review_packet_v1_2026_04_30.json"
VOCAB_TSV = ROOT / "data/vocabulary_bank/bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.tsv"
CANDIDATE_TSV = ROOT / "data/question_candidate_lanes/bereishis_perek_4_simple_vocabulary_question_candidates_2026_04_30.tsv"
BLOCKER_TSV = ROOT / "data/question_candidate_lanes/bereishis_perek_4_simple_vocabulary_question_candidate_blockers_2026_04_30.tsv"
SOURCE_CONTRACT = ROOT / "data/pipeline_rounds/simple_vocabulary_question_candidate_lane_v1_2026_04_30.json"
TEST_FILE = ROOT / "tests/test_broad_vocabulary_teacher_review_packet.py"

EXPECTED_FALSE_FLAGS = [
    "teacher_decisions_created",
    "fake_teacher_approval_created",
    "runtime_questions_created",
    "protected_preview_promoted",
    "reviewed_bank_promoted",
    "runtime_content_promoted",
    "runtime_scope_widened",
    "perek_activated",
    "student_facing_content_created",
    "question_generation_changed",
    "question_selection_changed",
    "question_selection_weighting_changed",
    "scoring_mastery_changed",
    "source_truth_changed",
    "fake_student_data_created",
    "raw_logs_exposed",
    "validators_weakened",
    "ready_for_protected_preview_promotion",
    "ready_for_reviewed_bank_promotion",
    "ready_for_runtime_activation",
    "runtime_activation_authorized",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "approved for runtime",
    "runtime ready",
    "reviewed bank promoted",
    "teacher approved",
    "protected preview promoted",
    "activated perek 4",
    "scope widened",
    "mastery proven",
    "raw jsonl",
]

FORBIDDEN_CHANGED_FILES = {
    "assessment_scope.py",
    "streamlit_app.py",
    "runtime/question_flow.py",
    "runtime/scope_exhaustion.py",
    "runtime/attempt_history.py",
}


def _fail(message: str) -> None:
    raise SystemExit(f"Teacher review packet validation failed: {message}")


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _load_json(path: Path) -> dict:
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
    for path in [PACKET_MD, PACKET_JSON, VOCAB_TSV, CANDIDATE_TSV, BLOCKER_TSV, SOURCE_CONTRACT, TEST_FILE]:
        if not path.exists():
            _fail(f"missing required file: {path.relative_to(ROOT)}")

    packet = PACKET_MD.read_text(encoding="utf-8")
    packet_lower = packet.lower()
    contract = _load_json(PACKET_JSON)

    if contract.get("feature_name") != "broad_vocabulary_teacher_review_packet_v1":
        _fail("unexpected feature_name")
    if contract.get("planning_only") is not True:
        _fail("planning_only must be true")
    if contract.get("teacher_review_packet_created") is not True:
        _fail("teacher review packet must be marked created")
    if contract.get("ready_for_teacher_manual_review") is not True:
        _fail("packet should be ready for manual teacher review")

    for flag in EXPECTED_FALSE_FLAGS:
        if contract.get(flag) is not False:
            _fail(f"{flag} must be false")

    if contract.get("word_level_review_items") != 5:
        _fail("word-level item count must be 5")
    if contract.get("simple_question_candidate_review_items") != 9:
        _fail("simple question candidate count must be 9")
    if contract.get("revision_watch_items") != 2:
        _fail("revision/watch count must be 2")
    if contract.get("perek_5_6_status") != "planning_only":
        _fail("Perek 5/6 status must remain planning_only")
    if contract.get("review_decision_fields_blank") is not True:
        _fail("review decision fields must be marked blank")

    vocab_rows = _read_csv(VOCAB_TSV)
    candidate_rows = _read_csv(CANDIDATE_TSV)
    blocker_rows = _read_csv(BLOCKER_TSV)

    vocab_ids = {row["vocabulary_id"] for row in vocab_rows}
    candidate_ids = {row["candidate_id"] for row in candidate_rows}
    blocker_ids = {row["vocabulary_id"] for row in blocker_rows}

    if len(vocab_ids) != 5:
        _fail("expected 5 vocabulary rows")
    if len(candidate_ids) != 9:
        _fail("expected 9 question candidate rows")
    if blocker_ids != {"bsvb_p4_003", "bsvb_p4_004"}:
        _fail("blocker register must include only the two revision/watch vocabulary IDs")

    for vocabulary_id in sorted(vocab_ids):
        if vocabulary_id not in packet:
            _fail(f"packet missing vocabulary ID {vocabulary_id}")
    for candidate_id in sorted(candidate_ids):
        if candidate_id not in packet:
            _fail(f"packet missing candidate ID {candidate_id}")
    for blocker_id in sorted(blocker_ids):
        if blocker_id not in packet:
            _fail(f"packet missing blocker ID {blocker_id}")

    required_packet_phrases = [
        "No response has been filled in by this packet.",
        "Teacher word-level decision",
        "Yossi prompt decision",
        "Revision and watch register",
        "Perek 5 and Perek 6 status",
        "Word-level review is not question approval.",
        "They are not runtime questions.",
    ]
    for phrase in required_packet_phrases:
        if phrase not in packet:
            _fail(f"packet missing required phrase: {phrase}")

    for phrase in FORBIDDEN_POSITIVE_CLAIMS:
        if phrase in packet_lower:
            _fail(f"forbidden positive claim found: {phrase}")

    touched_forbidden = _changed_files().intersection(FORBIDDEN_CHANGED_FILES)
    if touched_forbidden:
        _fail(f"forbidden runtime/scope files changed: {sorted(touched_forbidden)}")

    print("Broad vocabulary teacher review packet validation passed.")


if __name__ == "__main__":
    validate()

