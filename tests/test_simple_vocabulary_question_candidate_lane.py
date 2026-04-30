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
CONTRACT_JSON = ROOT / "data" / "pipeline_rounds" / "simple_vocabulary_question_candidate_lane_v1_2026_04_30.json"
NEXT_PROMPT = ROOT / "data" / "pipeline_rounds" / "next_codex_prompt_broad_vocabulary_teacher_review_packet_2026_04_30.md"


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_candidate_tsv_and_json_parse():
    rows = _read_tsv(CANDIDATE_TSV)
    payload = json.loads(CANDIDATE_JSON.read_text(encoding="utf-8-sig"))
    assert len(rows) == 9
    assert payload["candidate_count"] == 9


def test_blocker_tsv_and_json_parse():
    rows = _read_tsv(BLOCKER_TSV)
    payload = json.loads(BLOCKER_JSON.read_text(encoding="utf-8-sig"))
    assert len(rows) == 2
    assert payload["blocker_count"] == 2


def test_contract_json_parses_and_keeps_safety_flags_closed():
    payload = json.loads(CONTRACT_JSON.read_text(encoding="utf-8-sig"))
    assert payload["question_candidates_created"] is True
    assert payload["runtime_questions_created"] is False
    assert payload["protected_preview_promoted"] is False
    assert payload["reviewed_bank_promoted"] is False
    assert payload["runtime_scope_widened"] is False
    assert payload["perek_activated"] is False
    assert payload["runtime_activation_authorized"] is False


def test_all_candidate_vocabulary_ids_exist_in_broad_bank():
    vocab_ids = {row["vocabulary_id"] for row in _read_tsv(VOCAB_TSV)}
    candidate_ids = {row["vocabulary_id"] for row in _read_tsv(CANDIDATE_TSV)}
    assert candidate_ids <= vocab_ids
    assert candidate_ids == {"bsvb_p4_001", "bsvb_p4_002", "bsvb_p4_005"}


def test_candidates_are_perek_4_only_and_no_perek_5_6_rows():
    rows = _read_tsv(CANDIDATE_TSV)
    assert {row["perek"] for row in rows} == {"4"}
    assert not any(row["vocabulary_id"].startswith("bsvb_p5_6") for row in rows)


def test_only_allowed_simple_lanes_are_used():
    rows = _read_tsv(CANDIDATE_TSV)
    lanes = {row["allowed_question_lane"] for row in rows}
    assert lanes == {
        "translate_hebrew_to_english",
        "find_word_in_pasuk",
        "classify_basic_part_of_speech",
    }


def test_forbidden_lanes_do_not_appear():
    text = CANDIDATE_TSV.read_text(encoding="utf-8-sig").lower()
    for forbidden in [
        "tense",
        "shoresh",
        "prefix",
        "suffix",
        "phrase_translation",
        "rashi",
        "inference",
        "conceptual",
        "pasuk_level_translation",
        "vav_hahipuch",
    ]:
        assert forbidden not in text


def test_no_runtime_reviewed_bank_or_protected_preview_promotion():
    rows = _read_tsv(CANDIDATE_TSV)
    assert {row["runtime_status"] for row in rows} == {"not_runtime"}
    assert {row["reviewed_bank_status"] for row in rows} == {"not_reviewed_bank"}
    assert {row["protected_preview_status"] for row in rows} == {"not_promoted"}


def test_teacher_review_status_is_not_pre_approved():
    rows = _read_tsv(CANDIDATE_TSV)
    assert {row["teacher_review_status"] for row in rows} == {"needs_teacher_review"}
    assert "teacher approved" not in CANDIDATE_TSV.read_text(encoding="utf-8-sig").lower()


def test_distractor_policy_does_not_contain_invented_distractors():
    rows = _read_tsv(CANDIDATE_TSV)
    assert {row["distractor_policy"] for row in rows} == {"no_distractors_needed"}
    assert not any("|" in row["distractor_policy"] for row in rows)


def test_blocker_register_includes_revision_needed_rows():
    rows = _read_tsv(BLOCKER_TSV)
    assert {row["vocabulary_id"] for row in rows} == {"bsvb_p4_003", "bsvb_p4_004"}
    assert {row["runtime_status"] for row in rows} == {"not_runtime"}
    assert {row["protected_preview_status"] for row in rows} == {"blocked"}


def test_next_codex_prompt_exists():
    assert NEXT_PROMPT.exists()
    text = NEXT_PROMPT.read_text(encoding="utf-8-sig")
    assert "feature/broad-vocabulary-teacher-review-packet-v1" in text
    assert "Do not create teacher decisions" in text


def test_validator_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_simple_vocabulary_question_candidate_lane.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert "Simple vocabulary question candidate lane validation passed." in result.stdout
