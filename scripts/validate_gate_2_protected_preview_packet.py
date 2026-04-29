from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data" / "gate_2_protected_preview_packets"
REPORTS = DIR / "reports"
README = DIR / "README.md"
TSV = DIR / "bereishis_perek_2_internal_protected_preview_packet.tsv"
PACKET = REPORTS / "bereishis_perek_2_internal_protected_preview_packet.md"
GEN = REPORTS / "bereishis_perek_2_internal_protected_preview_packet_generation_report.md"
COMPLETE = REPORTS / "bereishis_perek_2_round_2_completion_report.md"
EXCLUDED = REPORTS / "bereishis_perek_2_internal_protected_preview_packet_excluded_preserved_report.md"
CAND = ROOT / "data" / "gate_2_protected_preview_candidates" / "bereishis_perek_2_protected_preview_candidates.tsv"

REQUIRED_COLUMNS = [
    "protected_preview_packet_item_id",
    "protected_preview_candidate_id",
    "controlled_draft_item_id",
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
    "internal_packet_status",
    "internal_preview_review_status",
    "reviewed_bank_allowed",
    "runtime_allowed",
    "student_facing_allowed",
    "post_preview_review_status",
    "yossi_internal_preview_decision",
    "yossi_internal_preview_notes",
]
GATES = ["reviewed_bank_allowed", "runtime_allowed", "student_facing_allowed"]
REVISION = {"g2p2_001", "g2p2_010", "g2p2_012", "g2p2_013"}
FOLLOWUP = {"g2p2_011", "g2p2_015"}
EXCLUDED_GATE2 = REVISION | FOLLOWUP | {"g2p2_004", "g2p2_005", "g2p2_008", "g2p2_018"}
DECISION = "approve_for_internal_protected_preview_packet"
STATUS = "yossi_approved_for_internal_protected_preview_packet"
HEBREW_RE = re.compile(r"[\u0590-\u05FF]")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def has_hebrew(value: str) -> bool:
    return bool(HEBREW_RE.search(value or ""))


def bad_phrase(text: str, phrase: str) -> bool:
    for line in text.lower().splitlines():
        if phrase in line and not any(
            marker in line
            for marker in ("not ", "no ", "false", "closed", "does not", "still requires", "requires post-preview", "remain excluded")
        ):
            return True
    return False


def validate_gate_2_protected_preview_packet() -> dict[str, object]:
    errors: list[str] = []
    for path in (README, TSV, PACKET, GEN, COMPLETE, EXCLUDED, CAND):
        if not path.exists():
            errors.append(f"missing internal packet artifact: {rel(path)}")
    if errors:
        return {"valid": False, "errors": errors}

    fields, rows = load_tsv(TSV)
    if fields != REQUIRED_COLUMNS:
        errors.append("internal packet TSV columns do not match required schema")
    if len(rows) != 10:
        errors.append(f"internal packet TSV must have exactly 10 rows, found {len(rows)}")

    _, candidate_rows = load_tsv(CAND)
    approved = {
        row["protected_preview_candidate_id"]: row
        for row in candidate_rows
        if row.get("yossi_protected_preview_decision") == DECISION
        and row.get("protected_preview_candidate_status") == STATUS
    }
    included: set[str] = set()
    family_counts: Counter[str] = Counter()

    for row in rows:
        rid = row.get("protected_preview_packet_item_id", "?")
        candidate_id = row.get("protected_preview_candidate_id", "")
        included.add(candidate_id)
        family_counts[row.get("approved_family", "")] += 1
        source = approved.get(candidate_id)
        if not source:
            errors.append(f"{rid}: must link to approved protected-preview candidate")
        else:
            for field in (
                "protected_preview_candidate_id",
                "controlled_draft_item_id",
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
            ):
                if row.get(field, "") != source.get(field, ""):
                    errors.append(f"{rid}: {field} must match source candidate")
            if source.get("gate_2_input_candidate_id") in EXCLUDED_GATE2:
                errors.append(f"{rid}: excluded Gate 2 row included")
        if row.get("approved_family") != "basic_noun_recognition":
            errors.append(f"{rid}: unsafe family included")
        if row.get("internal_packet_status") != "internal_protected_preview_packet_only":
            errors.append(f"{rid}: internal_packet_status must be internal_protected_preview_packet_only")
        if row.get("internal_preview_review_status") != "needs_internal_review":
            errors.append(f"{rid}: internal_preview_review_status must be needs_internal_review")
        if row.get("post_preview_review_status") != "not_started":
            errors.append(f"{rid}: post_preview_review_status must be not_started")
        for gate in GATES:
            if row.get(gate) != "false":
                errors.append(f"{rid}: {gate} must be false")
        if row.get("yossi_internal_preview_decision") or row.get("yossi_internal_preview_notes"):
            errors.append(f"{rid}: internal preview decision fields must be blank")
        if not has_hebrew(row.get("hebrew_token", "")) or not has_hebrew(row.get("hebrew_phrase", "")):
            errors.append(f"{rid}: must contain real Hebrew")
        if any(bad in "\t".join(row.values()) for bad in ("???", "×", "Ö")):
            errors.append(f"{rid}: contains placeholder corruption")

    if included != set(approved):
        errors.append("internal packet rows must exactly match approved protected-preview candidates")

    text = "\n".join(path.read_text(encoding="utf-8") for path in (README, PACKET, GEN, COMPLETE, EXCLUDED))
    for phrase in (
        "internal protected-preview packet only",
        "Packet item count: 10",
        "Perek 2 is complete",
        "Reviewed-bank entries created: 0",
        "Runtime changes: 0",
        "Student-facing content: 0",
    ):
        if phrase not in text:
            errors.append(f"required phrase missing: {phrase}")
    for gid in REVISION | FOLLOWUP:
        if gid not in text:
            errors.append(f"excluded report missing {gid}")
    for phrase in (
        "reviewed_bank_ready",
        "runtime_ready",
        "approved_for_reviewed_bank",
        "approved_for_runtime",
        "approved_for_student_facing",
    ):
        if bad_phrase(text, phrase):
            errors.append(f"forbidden phrase appears without clear negation: {phrase}")
    if "??" in text or "×" in text or "Ö" in text:
        errors.append("packet reports contain placeholder corruption")

    readme = README.read_text(encoding="utf-8")
    for path in (TSV, PACKET, GEN, COMPLETE, EXCLUDED):
        if rel(path) not in readme:
            errors.append(f"README must link {rel(path)}")

    return {
        "valid": not errors,
        "errors": errors,
        "packet_path": rel(TSV),
        "row_count": len(rows),
        "family_counts": dict(family_counts),
    }


def main() -> int:
    summary = validate_gate_2_protected_preview_packet()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
