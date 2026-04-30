from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PACKET_MD = ROOT / "data/pipeline_rounds/broad_vocabulary_teacher_review_packet_v1_2026_04_30.md"
PACKET_JSON = ROOT / "data/pipeline_rounds/broad_vocabulary_teacher_review_packet_v1_2026_04_30.json"
VOCAB_TSV = ROOT / "data/vocabulary_bank/bereishis_perek_4_broad_safe_vocabulary_bank_2026_04_30.tsv"
CANDIDATE_TSV = ROOT / "data/question_candidate_lanes/bereishis_perek_4_simple_vocabulary_question_candidates_2026_04_30.tsv"
BLOCKER_TSV = ROOT / "data/question_candidate_lanes/bereishis_perek_4_simple_vocabulary_question_candidate_blockers_2026_04_30.tsv"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_review_packet_contract_parses_and_keeps_gates_closed() -> None:
    contract = json.loads(PACKET_JSON.read_text(encoding="utf-8"))

    assert contract["feature_name"] == "broad_vocabulary_teacher_review_packet_v1"
    assert contract["planning_only"] is True
    assert contract["teacher_review_packet_created"] is True
    assert contract["teacher_decisions_created"] is False
    assert contract["fake_teacher_approval_created"] is False
    assert contract["runtime_questions_created"] is False
    assert contract["protected_preview_promoted"] is False
    assert contract["reviewed_bank_promoted"] is False
    assert contract["runtime_content_promoted"] is False
    assert contract["runtime_scope_widened"] is False
    assert contract["perek_activated"] is False
    assert contract["ready_for_runtime_activation"] is False
    assert contract["runtime_activation_authorized"] is False


def test_review_packet_counts_match_source_artifacts() -> None:
    contract = json.loads(PACKET_JSON.read_text(encoding="utf-8"))

    assert contract["word_level_review_items"] == len(_rows(VOCAB_TSV)) == 5
    assert contract["simple_question_candidate_review_items"] == len(_rows(CANDIDATE_TSV)) == 9
    assert contract["revision_watch_items"] == len(_rows(BLOCKER_TSV)) == 2
    assert contract["perek_5_6_status"] == "planning_only"


def test_packet_contains_all_vocabulary_candidate_and_blocker_ids() -> None:
    packet = PACKET_MD.read_text(encoding="utf-8")

    for row in _rows(VOCAB_TSV):
        assert row["vocabulary_id"] in packet
    for row in _rows(CANDIDATE_TSV):
        assert row["candidate_id"] in packet
    for row in _rows(BLOCKER_TSV):
        assert row["vocabulary_id"] in packet


def test_packet_has_blank_teacher_review_fields_not_decisions() -> None:
    packet = PACKET_MD.read_text(encoding="utf-8")
    lower = packet.lower()

    assert "No response has been filled in by this packet." in packet
    assert "Teacher word-level decision" in packet
    assert "Yossi prompt decision" in packet
    assert "____" in packet
    assert "teacher approved" not in lower
    assert "approved for runtime" not in lower
    assert "runtime ready" not in lower
    assert "mastery proven" not in lower


def test_packet_keeps_perek_5_6_planning_only() -> None:
    packet = PACKET_MD.read_text(encoding="utf-8")

    assert "Perek 5 and Perek 6 status" in packet
    assert "planning-only" in packet
    assert "not mixed into the Perek 4 review lane" in packet


def test_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_broad_vocabulary_teacher_review_packet.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Broad vocabulary teacher review packet validation passed." in result.stdout

