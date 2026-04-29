from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data" / "gate_2_protected_preview_candidates"
README = DIR / "README.md"
TSV = DIR / "bereishis_perek_2_protected_preview_candidates.tsv"
REPORTS = DIR / "reports"
PACKET = REPORTS / "bereishis_perek_2_protected_preview_candidate_review_packet.md"
REPORT = REPORTS / "bereishis_perek_2_protected_preview_candidate_generation_report.md"
EXCLUDED_REPORT = REPORTS / "bereishis_perek_2_protected_preview_candidate_excluded_preserved_report.md"
APPLIED_REPORT = REPORTS / "bereishis_perek_2_protected_preview_candidate_yossi_review_applied.md"
DRAFT_TSV = ROOT / "data" / "gate_2_controlled_draft_generation" / "bereishis_perek_2_controlled_draft.tsv"

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
REVIEW_FIELDS = [
    "protected_preview_review_status",
    "answer_key_review_status",
    "distractor_review_status",
    "hebrew_rendering_review_status",
    "context_display_review_status",
]
GATES = ["protected_preview_allowed", "reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed"]
REVISION = {"g2p2_001", "g2p2_010", "g2p2_012", "g2p2_013"}
FOLLOWUP = {"g2p2_011", "g2p2_015"}
EXCLUDED = {"g2p2_004", "g2p2_005", "g2p2_008", "g2p2_018"} | REVISION | FOLLOWUP
DECISION = "approve_for_internal_protected_preview_packet"
STATUS = "yossi_approved_for_internal_protected_preview_packet"
HEBREW_RE = re.compile(r"[\u0590-\u05FF]")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def validate_gate_2_protected_preview_candidates() -> dict[str, object]:
    errors: list[str] = []
    for path in (README, TSV, PACKET, REPORT, EXCLUDED_REPORT, APPLIED_REPORT, DRAFT_TSV):
        if not path.exists():
            errors.append(f"missing protected-preview candidate artifact: {rel(path)}")
    if errors:
        return {"valid": False, "errors": errors}

    fields, rows = load_tsv(TSV)
    if fields != REQUIRED_COLUMNS:
        errors.append("candidate TSV columns do not match required schema")
    if len(rows) != 10:
        errors.append(f"candidate TSV must have exactly 10 rows, found {len(rows)}")

    _, drafts = load_tsv(DRAFT_TSV)
    approved = {
        row["controlled_draft_item_id"]: row
        for row in drafts
        if row.get("yossi_draft_decision") == "approve_draft_item"
        and row.get("draft_review_status") == "yossi_draft_approved"
    }
    included: set[str] = set()
    decisions: Counter[str] = Counter()

    for row in rows:
        cid = row.get("protected_preview_candidate_id", "?")
        did = row.get("controlled_draft_item_id", "")
        gid = row.get("gate_2_input_candidate_id", "")
        included.add(did)
        decisions[row.get("yossi_protected_preview_decision", "")] += 1
        draft = approved.get(did)
        if not draft:
            errors.append(f"{cid}: must link to approved controlled draft")
        else:
            for source_field, target_field in (
                ("draft_prompt", "prompt"),
                ("controlled_draft_item_id", "controlled_draft_item_id"),
                ("gate_2_input_candidate_id", "gate_2_input_candidate_id"),
                ("source_ref", "source_ref"),
                ("approved_family", "approved_family"),
                ("hebrew_token", "hebrew_token"),
                ("hebrew_phrase", "hebrew_phrase"),
                ("answer_choices", "answer_choices"),
                ("expected_answer", "expected_answer"),
                ("correct_answer", "correct_answer"),
                ("explanation", "explanation"),
                ("source_evidence_note", "source_evidence_note"),
                ("caution_note", "caution_note"),
                ("draft_review_status", "draft_review_status"),
            ):
                if row.get(target_field, "") != draft.get(source_field, ""):
                    errors.append(f"{cid}: {target_field} must match draft row")
        if gid in EXCLUDED:
            errors.append(f"{cid}: skipped/follow-up/excluded row included")
        if row.get("approved_family") != "basic_noun_recognition":
            errors.append(f"{cid}: unsafe family included")
        if row.get("protected_preview_candidate_status") != STATUS:
            errors.append(f"{cid}: status must be {STATUS}")
        for field in REVIEW_FIELDS:
            if row.get(field) != "needs_yossi_review":
                errors.append(f"{cid}: {field} must be needs_yossi_review")
        for field in GATES:
            if row.get(field) != "false":
                errors.append(f"{cid}: {field} must be false")
        if row.get("yossi_protected_preview_decision") != DECISION:
            errors.append(f"{cid}: Yossi decision must be {DECISION}")
        if "internal protected-preview packet only" not in row.get("yossi_protected_preview_notes", ""):
            errors.append(f"{cid}: Yossi note must preserve internal-only boundary")
        for field in ("hebrew_token", "hebrew_phrase"):
            value = row.get(field, "")
            if not HEBREW_RE.search(value):
                errors.append(f"{cid}: {field} must contain Hebrew")
            if "???" in value or "×" in value or "Ö" in value:
                errors.append(f"{cid}: {field} contains corruption")

    if included != set(approved):
        errors.append("candidate rows must exactly match approved controlled drafts")
    if decisions.get(DECISION, 0) != 10:
        errors.append(f"exactly 10 rows must have {DECISION}")

    text = "\n".join(path.read_text(encoding="utf-8") for path in (README, PACKET, REPORT, EXCLUDED_REPORT, APPLIED_REPORT))
    for phrase in ("not protected-preview release", "not reviewed-bank", "not runtime", "not student-facing", "All gates closed"):
        if phrase not in text:
            errors.append(f"missing safety phrase: {phrase}")
    for phrase in (
        "approved_for_preview",
        "protected_preview_ready",
        "reviewed_bank_ready",
        "runtime_ready",
        "approved_for_reviewed_bank",
        "approved_for_runtime",
        "approved_for_student_facing",
    ):
        if phrase in text:
            errors.append(f"forbidden release/readiness phrase appears: {phrase}")
    excluded_text = EXCLUDED_REPORT.read_text(encoding="utf-8")
    for gid in REVISION | FOLLOWUP:
        if gid not in excluded_text:
            errors.append(f"excluded-preserved report missing {gid}")
    for bad in ("???", "×", "Ö"):
        if bad in text:
            errors.append(f"artifacts contain corrupt phrase: {bad}")

    return {
        "valid": not errors,
        "errors": errors,
        "candidate_path": rel(TSV),
        "row_count": len(rows),
        "decision_counts": dict(decisions),
        "family_counts": dict(Counter(row.get("approved_family", "") for row in rows)),
    }


def main() -> int:
    summary = validate_gate_2_protected_preview_candidates()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
