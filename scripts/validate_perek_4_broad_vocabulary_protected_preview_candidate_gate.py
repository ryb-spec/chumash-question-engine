from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GATE_TSV = ROOT / "data/protected_preview_candidate_gates/bereishis_perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.tsv"
GATE_JSON = ROOT / "data/protected_preview_candidate_gates/bereishis_perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.json"
REPORT_MD = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.md"
CONTRACT_JSON = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_protected_preview_candidate_gate_2026_04_30.json"
ELIGIBILITY_TSV = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.tsv"
ELIGIBILITY_JSON = ROOT / "data/teacher_review_decisions/bereishis_perek_4_broad_vocabulary_future_gate_eligibility_register_2026_04_30.json"
TEST_FILE = ROOT / "tests/test_perek_4_broad_vocabulary_protected_preview_candidate_gate.py"

EXPECTED_CLEAN = {
    "svqcl_p4_001",
    "svqcl_p4_002",
    "svqcl_p4_003",
    "svqcl_p4_005",
    "svqcl_p4_006",
}
EXPECTED_REVISION = {"bsvb_p4_002", "svqcl_p4_004"}
EXPECTED_HELD = {"bsvb_p4_003", "bsvb_p4_004", "svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009"}

FALSE_FLAGS = [
    "protected_preview_packet_created",
    "protected_preview_promoted",
    "reviewed_bank_promoted",
    "runtime_questions_created",
    "runtime_content_promoted",
    "runtime_scope_widened",
    "perek_activated",
    "student_facing_content_created",
    "scoring_mastery_changed",
    "question_generation_changed",
    "question_selection_changed",
    "question_selection_weighting_changed",
    "source_truth_changed",
    "fake_teacher_approval_created",
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
    "student-facing content created: yes",
    "mastery proven",
    "raw jsonl",
]

FORBIDDEN_CHANGED_PATHS = {"assessment_scope.py", "streamlit_app.py"}
FORBIDDEN_CHANGED_PREFIXES = (
    "runtime/",
    "data/source_texts/",
    "data/gate_2_protected_preview_packets/",
    "data/reviewed_bank/",
)


def _fail(message: str) -> None:
    raise SystemExit(f"Perek 4 broad vocabulary protected-preview candidate gate validation failed: {message}")


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
    for path in [GATE_TSV, GATE_JSON, REPORT_MD, CONTRACT_JSON, ELIGIBILITY_TSV, ELIGIBILITY_JSON, TEST_FILE]:
        if not path.exists():
            _fail(f"missing required file: {path.relative_to(ROOT)}")

    gate_rows = _rows(GATE_TSV)
    gate_json = _json(GATE_JSON)
    contract = _json(CONTRACT_JSON)
    eligibility_rows = _rows(ELIGIBILITY_TSV)
    eligibility_json = _json(ELIGIBILITY_JSON)

    if contract.get("feature_name") != "perek_4_broad_vocabulary_protected_preview_candidate_gate_v1":
        _fail("unexpected feature_name")
    if contract.get("candidate_gate_created") is not True:
        _fail("candidate_gate_created must be true")
    if gate_json.get("candidate_gate_created") is not True:
        _fail("gate JSON must mark candidate gate created")
    if contract.get("clean_candidate_count") != 5:
        _fail("clean candidate count must be 5")

    for payload in [contract, gate_json]:
        for flag in FALSE_FLAGS:
            if payload.get(flag) is not False:
                _fail(f"{flag} must be false in {payload.get('feature_name') or payload.get('gate_name')}")

    candidate_ids = {row["candidate_id"] for row in gate_rows}
    if candidate_ids != EXPECTED_CLEAN:
        _fail(f"gate candidate set mismatch: {sorted(candidate_ids)}")
    if set(contract.get("clean_candidate_ids", [])) != EXPECTED_CLEAN:
        _fail("contract clean_candidate_ids mismatch")
    if set(gate_json.get("clean_candidate_ids", [])) != EXPECTED_CLEAN:
        _fail("gate JSON clean_candidate_ids mismatch")

    eligibility_clean = {
        row["source_id"]
        for row in eligibility_rows
        if row["eligibility_classification"] == "clean_eligible_for_future_protected_preview_candidate_gate"
    }
    if eligibility_clean != EXPECTED_CLEAN:
        _fail("source eligibility register clean set mismatch")
    if set(eligibility_json.get("clean_eligible_candidate_ids", [])) != EXPECTED_CLEAN:
        _fail("source eligibility JSON clean set mismatch")

    if candidate_ids.intersection(EXPECTED_REVISION | EXPECTED_HELD):
        _fail("revision-required or held rows leaked into candidate gate")
    if set(contract.get("revision_required_source_ids", [])) != EXPECTED_REVISION:
        _fail("contract revision-required set mismatch")
    if set(contract.get("held_source_ids", [])) != EXPECTED_HELD:
        _fail("contract held set mismatch")

    for row in gate_rows:
        if row["runtime_status"] != "not_runtime":
            _fail(f"{row['candidate_id']} runtime_status must be not_runtime")
        if row["reviewed_bank_status"] != "not_reviewed_bank":
            _fail(f"{row['candidate_id']} reviewed_bank_status must be not_reviewed_bank")
        if row["protected_preview_packet_status"] != "not_created":
            _fail(f"{row['candidate_id']} must not create protected-preview packet")
        if row["blocked_revision_required"] != "false":
            _fail(f"{row['candidate_id']} must not be revision-required")
        if row["blocked_held"] != "false":
            _fail(f"{row['candidate_id']} must not be held")

    report = REPORT_MD.read_text(encoding="utf-8")
    for source_id in EXPECTED_CLEAN | EXPECTED_REVISION | EXPECTED_HELD:
        if source_id not in report:
            _fail(f"report missing source ID {source_id}")
    if "Safety confirmation" not in report:
        _fail("report missing safety confirmation")

    changed = _changed_files()
    forbidden = changed.intersection(FORBIDDEN_CHANGED_PATHS)
    forbidden.update(path for path in changed if path.startswith(FORBIDDEN_CHANGED_PREFIXES))
    if forbidden:
        _fail(f"forbidden changed paths found: {sorted(forbidden)}")

    scanned = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [REPORT_MD, CONTRACT_JSON, GATE_JSON]
    )
    for phrase in FORBIDDEN_PHRASES:
        if phrase in scanned:
            _fail(f"forbidden positive claim found: {phrase}")

    print("Perek 4 broad vocabulary protected-preview candidate gate validation passed.")


if __name__ == "__main__":
    validate()
