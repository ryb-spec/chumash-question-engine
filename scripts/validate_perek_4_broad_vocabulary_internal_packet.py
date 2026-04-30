from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PACKET_TSV = ROOT / "data/gate_2_protected_preview_packets/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.tsv"
PACKET_MD = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.md"
PACKET_JSON = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_protected_preview_packet_2026_04_30.json"
CHECKLIST_MD = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_checklist_2026_04_30.md"
CHECKLIST_TSV = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_internal_review_checklist_2026_04_30.tsv"
OBS_MD = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_observation_template_2026_04_30.md"
OBS_TSV = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_observation_template_2026_04_30.tsv"
EXCLUDED_MD = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_packet_excluded_register_2026_04_30.md"
EXCLUDED_JSON = ROOT / "data/gate_2_protected_preview_packets/reports/bereishis_perek_4_broad_vocabulary_packet_excluded_register_2026_04_30.json"
LINEAGE_MD = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_packet_lineage_reconciliation_2026_04_30.md"
LINEAGE_JSON = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_packet_lineage_reconciliation_2026_04_30.json"
MAIN_MD = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.md"
MAIN_JSON = ROOT / "data/pipeline_rounds/perek_4_broad_vocabulary_internal_protected_preview_packet_v1_2026_04_30.json"
NEXT_PROMPT = ROOT / "data/pipeline_rounds/next_codex_prompt_perek_4_broad_vocabulary_post_preview_decisions_2026_04_30.md"
TEST_FILE = ROOT / "tests/test_perek_4_broad_vocabulary_internal_packet.py"

EXPECTED_INCLUDED = {
    "svqcl_p4_001",
    "svqcl_p4_002",
    "svqcl_p4_003",
    "svqcl_p4_005",
    "svqcl_p4_006",
}
EXCLUDED_CANDIDATES = {"svqcl_p4_004", "svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009"}
EXCLUDED_VOCAB = {"bsvb_p4_003", "bsvb_p4_004"}
EXCLUDED_REVISION = {"bsvb_p4_002", "svqcl_p4_004"}
EXCLUDED_HELD = {"bsvb_p4_003", "bsvb_p4_004", "svqcl_p4_007", "svqcl_p4_008", "svqcl_p4_009"}

FALSE_FLAGS = [
    "runtime_scope_widened",
    "perek_activated",
    "reviewed_bank_promoted",
    "runtime_questions_created",
    "runtime_content_promoted",
    "student_facing_content_created",
    "question_generation_changed",
    "question_selection_changed",
    "question_selection_weighting_changed",
    "scoring_mastery_changed",
    "source_truth_changed",
    "raw_logs_exposed",
    "validators_weakened",
    "fake_teacher_approval_created",
    "fake_observation_evidence_created",
    "ready_for_reviewed_bank_promotion",
    "ready_for_runtime_activation",
    "runtime_activation_authorized",
]

FORBIDDEN_POSITIVE_PHRASES = [
    "runtime ready",
    "activated perek 4",
    "reviewed bank promoted",
    "student-facing content created: yes",
    "mastery proven",
    "observation completed",
    "teacher approved for runtime",
]

FORBIDDEN_CHANGED_PATHS = {"assessment_scope.py", "streamlit_app.py"}
FORBIDDEN_CHANGED_PREFIXES = (
    "runtime/",
    "data/source_texts/",
    "data/reviewed_bank/",
)


def _fail(message: str) -> None:
    raise SystemExit(f"Perek 4 broad vocabulary internal packet validation failed: {message}")


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
    required = [
        PACKET_TSV,
        PACKET_MD,
        PACKET_JSON,
        CHECKLIST_MD,
        CHECKLIST_TSV,
        OBS_MD,
        OBS_TSV,
        EXCLUDED_MD,
        EXCLUDED_JSON,
        LINEAGE_MD,
        LINEAGE_JSON,
        MAIN_MD,
        MAIN_JSON,
        NEXT_PROMPT,
        TEST_FILE,
    ]
    for path in required:
        if not path.exists():
            _fail(f"missing required file: {path.relative_to(ROOT)}")

    packet_rows = _rows(PACKET_TSV)
    checklist_rows = _rows(CHECKLIST_TSV)
    observation_rows = _rows(OBS_TSV)
    packet_json = _json(PACKET_JSON)
    main_json = _json(MAIN_JSON)
    excluded_json = _json(EXCLUDED_JSON)
    lineage_json = _json(LINEAGE_JSON)

    packet_ids = {row["source_candidate_id"] for row in packet_rows}
    if packet_ids != EXPECTED_INCLUDED:
        _fail(f"packet candidate IDs mismatch: {sorted(packet_ids)}")
    if len(packet_rows) != 5:
        _fail("packet must contain exactly five rows")
    if packet_ids.intersection(EXCLUDED_CANDIDATES):
        _fail("excluded candidate entered packet")
    if {row["vocabulary_id"] for row in packet_rows}.intersection(EXCLUDED_VOCAB):
        _fail("excluded vocabulary row entered packet")

    for row in packet_rows:
        if row["runtime_status"] != "not_runtime":
            _fail(f"{row['packet_item_id']} must be not_runtime")
        if row["reviewed_bank_status"] != "not_reviewed_bank":
            _fail(f"{row['packet_item_id']} must be not_reviewed_bank")
        if row["student_facing_status"] != "not_student_facing":
            _fail(f"{row['packet_item_id']} must be not_student_facing")
        if row["distractor_policy"] != "no_distractors_needed":
            _fail(f"{row['packet_item_id']} must not create distractors")
        if "answer_choice" in row or "distractors" in row:
            _fail("packet must not include answer choices or distractor columns")

    if len(checklist_rows) != 5:
        _fail("review checklist must contain five rows")
    for row in checklist_rows:
        if row["reviewer_decision"] not in {"", "pending"}:
            _fail("review checklist decisions must be blank/pending")

    if len(observation_rows) != 5:
        _fail("observation template must contain five rows")
    observation_fields = [
        "observed",
        "reviewer_name",
        "observation_date",
        "setting",
        "student_or_group_context_optional",
        "did_prompt_make_sense",
        "did_expected_answer_match_teacher_intent",
        "student_confusion_observed",
        "issue_category",
        "recommended_decision",
        "notes",
    ]
    for row in observation_rows:
        for field in observation_fields:
            if row[field] != "":
                _fail("observation template fields must remain blank")

    for payload in [packet_json, main_json]:
        included = set(payload.get("included_candidate_ids", []))
        if included != EXPECTED_INCLUDED:
            _fail("JSON included candidate IDs mismatch")
        if set(payload.get("excluded_revision_required_ids", [])) != EXCLUDED_REVISION:
            _fail("JSON revision-required exclusions mismatch")
        if set(payload.get("excluded_held_ids", [])) != EXCLUDED_HELD:
            _fail("JSON held exclusions mismatch")

    if packet_json.get("protected_preview_packet_created") is not True:
        _fail("packet JSON must mark internal protected-preview packet created")
    if main_json.get("packet_created") is not True:
        _fail("main JSON must mark packet_created true")
    if main_json.get("protected_preview_packet_created") is not True:
        _fail("main JSON must mark protected_preview_packet_created true")
    if main_json.get("internal_review_checklist_created") is not True:
        _fail("main JSON must mark checklist created")
    if main_json.get("observation_template_created") is not True:
        _fail("main JSON must mark observation template created")
    if main_json.get("lineage_reconciliation_created") is not True:
        _fail("main JSON must mark lineage reconciliation created")

    for flag in FALSE_FLAGS:
        if main_json.get(flag) is not False:
            _fail(f"{flag} must be false")

    if set(excluded_json.get("excluded_revision_required_ids", [])) != EXCLUDED_REVISION:
        _fail("excluded register revision IDs mismatch")
    if set(excluded_json.get("excluded_held_ids", [])) != EXCLUDED_HELD:
        _fail("excluded register held IDs mismatch")
    if lineage_json.get("broad_vocabulary_packet_complements_prior_work") is not True:
        _fail("lineage must say broad packet complements prior work")
    if lineage_json.get("supersedes_prior_packet_work") is not False:
        _fail("lineage must not supersede prior work")

    lineage_text = LINEAGE_MD.read_text(encoding="utf-8").lower()
    for phrase in ["source-discovery", "limited protected-preview", "broad safe vocabulary", "candidate gate"]:
        if phrase not in lineage_text:
            _fail(f"lineage report missing {phrase}")

    changed = _changed_files()
    forbidden = changed.intersection(FORBIDDEN_CHANGED_PATHS)
    forbidden.update(path for path in changed if path.startswith(FORBIDDEN_CHANGED_PREFIXES))
    if forbidden:
        _fail(f"forbidden changed paths found: {sorted(forbidden)}")

    scanned = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [PACKET_MD, PACKET_JSON, CHECKLIST_MD, OBS_MD, EXCLUDED_MD, EXCLUDED_JSON, LINEAGE_MD, MAIN_MD, MAIN_JSON, NEXT_PROMPT]
    )
    for phrase in FORBIDDEN_POSITIVE_PHRASES:
        if phrase in scanned:
            _fail(f"forbidden positive claim found: {phrase}")

    print("Perek 4 broad vocabulary internal packet validation passed.")


if __name__ == "__main__":
    validate()

