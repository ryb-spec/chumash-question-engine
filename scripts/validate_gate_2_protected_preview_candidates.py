from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data" / "gate_2_protected_preview_candidates"
REPORTS = DIR / "reports"
README = DIR / "README.md"

TSV = DIR / "bereishis_perek_2_protected_preview_candidates.tsv"
PACKET = REPORTS / "bereishis_perek_2_protected_preview_candidate_review_packet.md"
GENERATION_REPORT = REPORTS / "bereishis_perek_2_protected_preview_candidate_generation_report.md"
EXCLUDED_REPORT = REPORTS / "bereishis_perek_2_protected_preview_candidate_excluded_preserved_report.md"
REVIEW_APPLIED_REPORT = REPORTS / "bereishis_perek_2_protected_preview_candidate_yossi_review_applied.md"
CONTROLLED_DRAFT = ROOT / "data" / "gate_2_controlled_draft_generation" / "bereishis_perek_2_controlled_draft.tsv"

PEREK3_TSV = DIR / "bereishis_perek_3_protected_preview_candidates.tsv"
PEREK3_PACKET = REPORTS / "bereishis_perek_3_protected_preview_candidate_review_packet.md"
PEREK3_SOURCE_READINESS_REPORT = REPORTS / "bereishis_perek_3_protected_preview_candidate_source_readiness_report.md"
PEREK3_REVIEW_APPLIED_REPORT = REPORTS / "bereishis_perek_3_protected_preview_candidate_yossi_review_applied.md"
PEREK3_SOURCE_MAPS = [
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_3_1_to_3_7_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_3_8_to_3_16_source_to_skill_map.tsv",
    ROOT / "data" / "verified_source_skill_maps" / "bereishis_3_17_to_3_24_source_to_skill_map.tsv",
]
PEREK3_FORBIDDEN_PACKET = ROOT / "data" / "gate_2_protected_preview_packets" / "bereishis_perek_3_internal_protected_preview_packet.tsv"

REQUIRED_COLUMNS = [
    "protected_preview_candidate_id",
    "controlled_draft_item_id",
    "gate_2_input_candidate_id",
    "source_ref",
    "approved_family",
    "hebrew_token",
    "hebrew_phrase",
    "prompt",
    "answer_choices",
    "expected_answer",
    "correct_answer",
    "explanation",
    "source_evidence_note",
    "caution_note",
    "draft_review_status",
    "protected_preview_candidate_status",
    "protected_preview_review_status",
    "answer_key_review_status",
    "distractor_review_status",
    "hebrew_rendering_review_status",
    "context_display_review_status",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "runtime_allowed",
    "student_facing_allowed",
    "yossi_protected_preview_decision",
    "yossi_protected_preview_notes",
]

P2_APPROVED_STATUS = "yossi_approved_for_internal_protected_preview_packet"
P2_APPROVED_DECISION = "approve_for_internal_protected_preview_packet"
P3_REVISION_STATUS = "yossi_approved_with_revision_before_internal_protected_preview_packet"
P3_FOLLOW_UP_STATUS = "needs_follow_up"
NEEDS_YOSSI_REVIEW = "needs_yossi_review"
CLOSED_GATES = [
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "runtime_allowed",
    "student_facing_allowed",
]
REVIEW_STATUS_COLUMNS = [
    "protected_preview_review_status",
    "answer_key_review_status",
    "distractor_review_status",
    "hebrew_rendering_review_status",
    "context_display_review_status",
]
P3_EXPECTED_DECISION_COUNTS = {
    "approve_for_internal_protected_preview_packet": 4,
    "approve_with_revision": 4,
    "needs_follow_up": 2,
    "reject_for_preview": 0,
    "source_only": 0,
}
P3_EXPECTED_STATUS_BY_DECISION = {
    "approve_for_internal_protected_preview_packet": P2_APPROVED_STATUS,
    "approve_with_revision": P3_REVISION_STATUS,
    "needs_follow_up": P3_FOLLOW_UP_STATUS,
}
FORBIDDEN_P3_STATUS_FRAGMENTS = [
    "reviewed_bank_ready",
    "runtime_ready",
    "approved_for_reviewed_bank",
    "approved_for_runtime",
    "approved_for_student_facing",
]


def _read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise AssertionError(f"Missing TSV: {path}")
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def _require_columns(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise AssertionError(f"No rows in {path}")
    missing = [col for col in REQUIRED_COLUMNS if col not in rows[0]]
    if missing:
        raise AssertionError(f"{path} missing columns: {missing}")
    extras = [col for col in rows[0] if col not in REQUIRED_COLUMNS]
    if extras:
        raise AssertionError(f"{path} has unexpected columns: {extras}")


def _has_hebrew(text: str) -> bool:
    return any("\u0590" <= ch <= "\u05ff" for ch in text)


def _check_no_placeholder_corruption(rows: list[dict[str, str]], path: Path) -> None:
    bad_fragments = ["???", "TBD", "PLACEHOLDER", "REPLACE_ME"]
    for row in rows:
        joined = "\t".join(row.values())
        if any(fragment in joined for fragment in bad_fragments):
            raise AssertionError(f"Placeholder/corruption marker found in {path}: {row.get('protected_preview_candidate_id')}")
        if not _has_hebrew(row.get("hebrew_token", "")):
            raise AssertionError(f"Missing real Hebrew token in {path}: {row.get('protected_preview_candidate_id')}")
        if not _has_hebrew(row.get("hebrew_phrase", "")):
            raise AssertionError(f"Missing real Hebrew phrase in {path}: {row.get('protected_preview_candidate_id')}")


def _load_controlled_drafts() -> dict[str, dict[str, str]]:
    return {row["controlled_draft_item_id"]: row for row in _read_tsv(CONTROLLED_DRAFT)}


def _load_perek3_source_refs() -> dict[str, list[str]]:
    refs: dict[str, list[str]] = {}
    for path in PEREK3_SOURCE_MAPS:
        if not path.exists():
            raise AssertionError(f"Missing Perek 3 source map: {path}")
        for row in _read_tsv(path):
            ref = row.get("ref", "")
            phrase = (
                row.get("hebrew_word_or_phrase")
                or row.get("hebrew_phrase")
                or row.get("source_hebrew")
                or row.get("hebrew")
                or ""
            )
            status = row.get("extraction_review_status", "")
            if status != "yossi_extraction_verified":
                continue
            refs.setdefault(ref, []).append(phrase)
    return refs


def _validate_perek2_candidates() -> tuple[list[dict[str, str]], dict[str, object]]:
    for path in [README, TSV, PACKET, GENERATION_REPORT, EXCLUDED_REPORT, REVIEW_APPLIED_REPORT]:
        if not path.exists():
            raise AssertionError(f"Missing Perek 2 protected-preview candidate artifact: {path}")

    rows = _read_tsv(TSV)
    _require_columns(TSV, rows)
    if len(rows) != 10:
        raise AssertionError(f"Expected 10 Perek 2 candidate rows, found {len(rows)}")
    _check_no_placeholder_corruption(rows, TSV)

    drafts = _load_controlled_drafts()
    for row in rows:
        cid = row["protected_preview_candidate_id"]
        draft_id = row["controlled_draft_item_id"]
        if draft_id not in drafts:
            raise AssertionError(f"Perek 2 candidate {cid} does not link to controlled draft {draft_id}")
        if drafts[draft_id].get("draft_review_status") != "yossi_draft_approved":
            raise AssertionError(f"Perek 2 candidate {cid} links to unapproved controlled draft {draft_id}")
        if row["protected_preview_candidate_status"] != P2_APPROVED_STATUS:
            raise AssertionError(f"Unexpected Perek 2 candidate status for {cid}: {row['protected_preview_candidate_status']}")
        if row["yossi_protected_preview_decision"] != P2_APPROVED_DECISION:
            raise AssertionError(f"Unexpected Perek 2 Yossi decision for {cid}: {row['yossi_protected_preview_decision']}")
        for col in CLOSED_GATES:
            if row[col] != "false":
                raise AssertionError(f"Perek 2 candidate {cid} opened {col}: {row[col]}")

    return rows, {
        "row_count": len(rows),
        "family_counts": dict(Counter(row["approved_family"] for row in rows)),
        "decision_counts": dict(Counter(row["yossi_protected_preview_decision"] for row in rows)),
    }


def _validate_perek3_candidates() -> tuple[list[dict[str, str]], dict[str, object]]:
    for path in [PEREK3_TSV, PEREK3_PACKET, PEREK3_SOURCE_READINESS_REPORT, PEREK3_REVIEW_APPLIED_REPORT]:
        if not path.exists():
            raise AssertionError(f"Missing Perek 3 protected-preview candidate artifact: {path}")
    if PEREK3_FORBIDDEN_PACKET.exists():
        raise AssertionError(f"Perek 3 final/internal packet must not exist for this decision-application task: {PEREK3_FORBIDDEN_PACKET}")

    rows = _read_tsv(PEREK3_TSV)
    _require_columns(PEREK3_TSV, rows)
    if len(rows) != 10:
        raise AssertionError(f"Expected 10 Perek 3 candidate rows, found {len(rows)}")
    _check_no_placeholder_corruption(rows, PEREK3_TSV)

    source_refs = _load_perek3_source_refs()
    seen_ids: set[str] = set()
    for row in rows:
        cid = row["protected_preview_candidate_id"]
        if cid in seen_ids:
            raise AssertionError(f"Duplicate Perek 3 candidate id: {cid}")
        seen_ids.add(cid)
        if not cid.startswith("g2ppcand_p3_"):
            raise AssertionError(f"Unexpected Perek 3 candidate id: {cid}")
        if not row["source_ref"].startswith("Bereishis 3:"):
            raise AssertionError(f"Perek 3 candidate has non-Perek 3 ref: {cid} / {row['source_ref']}")
        if row["source_ref"] not in source_refs:
            raise AssertionError(f"Perek 3 candidate {cid} is not backed by a verified source map ref: {row['source_ref']}")
        phrases_for_ref = source_refs[row["source_ref"]]
        if row["hebrew_phrase"] not in phrases_for_ref and not any(row["hebrew_token"] in phrase for phrase in phrases_for_ref):
            raise AssertionError(f"Perek 3 candidate {cid} phrase/token not found in verified source maps")
        if row["approved_family"] != "basic_noun_recognition":
            raise AssertionError(f"Perek 3 candidate {cid} uses non-conservative family: {row['approved_family']}")
        decision = row["yossi_protected_preview_decision"]
        expected_status = P3_EXPECTED_STATUS_BY_DECISION.get(decision)
        if expected_status is None:
            raise AssertionError(f"Perek 3 candidate {cid} has unexpected Yossi decision: {decision}")
        if row["protected_preview_candidate_status"] != expected_status:
            raise AssertionError(f"Perek 3 candidate {cid} has wrong status for {decision}: {row['protected_preview_candidate_status']}")
        if not row["yossi_protected_preview_notes"].strip():
            raise AssertionError(f"Perek 3 candidate {cid} is missing Yossi notes")
        if row["draft_review_status"] != NEEDS_YOSSI_REVIEW:
            raise AssertionError(f"Perek 3 candidate {cid} draft review status should remain pending")
        for col in REVIEW_STATUS_COLUMNS:
            if row[col] != NEEDS_YOSSI_REVIEW:
                raise AssertionError(f"Perek 3 candidate {cid} has non-pending {col}: {row[col]}")
        for col in CLOSED_GATES:
            if row[col] != "false":
                raise AssertionError(f"Perek 3 candidate {cid} opened {col}: {row[col]}")
        joined_status = "|".join([
            row["protected_preview_candidate_status"],
            row["yossi_protected_preview_decision"],
            row["yossi_protected_preview_notes"],
        ])
        if any(fragment in joined_status for fragment in FORBIDDEN_P3_STATUS_FRAGMENTS):
            raise AssertionError(f"Perek 3 candidate {cid} contains forbidden runtime/reviewed-bank approval language")
        for required_text_col in ["explanation", "source_evidence_note", "caution_note"]:
            if not row[required_text_col].strip():
                raise AssertionError(f"Perek 3 candidate {cid} missing {required_text_col}")
        if "verified Perek 3 source-to-skill" not in row["source_evidence_note"]:
            raise AssertionError(f"Perek 3 candidate {cid} missing explicit source-to-skill evidence note")
        if "not protected-preview approval" not in row["caution_note"]:
            raise AssertionError(f"Perek 3 candidate {cid} missing fail-closed caution note")

    decision_counts = Counter(row["yossi_protected_preview_decision"] for row in rows)
    for decision, expected_count in P3_EXPECTED_DECISION_COUNTS.items():
        if decision_counts.get(decision, 0) != expected_count:
            raise AssertionError(f"Perek 3 expected {expected_count} {decision} rows, found {decision_counts.get(decision, 0)}")

    applied_text = PEREK3_REVIEW_APPLIED_REPORT.read_text(encoding="utf-8")
    required_applied_phrases = [
        "Yossi decisions were applied",
        "`approve_for_internal_protected_preview_packet`: 4",
        "`approve_with_revision`: 4",
        "`needs_follow_up`: 2",
        "This is not runtime approval.",
        "This is not reviewed-bank approval.",
        "This is not student-facing approval.",
        "No final protected-preview packet was created.",
    ]
    for phrase in required_applied_phrases:
        if phrase not in applied_text:
            raise AssertionError(f"Perek 3 applied report missing phrase: {phrase}")

    readme_text = README.read_text(encoding="utf-8")
    if "bereishis_perek_3_protected_preview_candidate_yossi_review_applied.md" not in readme_text:
        raise AssertionError("Perek 3 decision-applied report is not discoverable from candidate README")

    return rows, {
        "perek3_row_count": len(rows),
        "perek3_family_counts": dict(Counter(row["approved_family"] for row in rows)),
        "perek3_status_counts": dict(Counter(row["protected_preview_candidate_status"] for row in rows)),
        "perek3_decision_counts": dict(decision_counts),
    }


def validate_gate_2_protected_preview_candidates() -> dict[str, object]:
    p2_rows, p2_summary = _validate_perek2_candidates()
    p3_rows, p3_summary = _validate_perek3_candidates()
    summary: dict[str, object] = {
        **p2_summary,
        **p3_summary,
        "total_candidate_rows": len(p2_rows) + len(p3_rows),
    }
    return summary


if __name__ == "__main__":
    print(json.dumps(validate_gate_2_protected_preview_candidates(), ensure_ascii=False, indent=2, sort_keys=True))
