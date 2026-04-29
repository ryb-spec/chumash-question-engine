from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYER_DIR = ROOT / "data" / "gate_2_input_planning"
README = LAYER_DIR / "README.md"
PROPOSAL_TSV = LAYER_DIR / "bereishis_perek_2_gate_2_input_planning_proposal.tsv"
BALANCE_REPORT = LAYER_DIR / "reports" / "bereishis_perek_2_gate_2_input_planning_balance_report.md"
YOSSI_REVIEW_MD = LAYER_DIR / "reports" / "bereishis_perek_2_gate_2_yossi_review_sheet.md"
YOSSI_REVIEW_CSV = LAYER_DIR / "reports" / "bereishis_perek_2_gate_2_yossi_review_sheet.csv"
PROPOSAL_REPORT = LAYER_DIR / "reports" / "bereishis_perek_2_gate_2_input_planning_proposal_report.md"
REVIEW_APPLIED_REPORT = LAYER_DIR / "reports" / "bereishis_perek_2_gate_2_yossi_review_applied.md"
TEMPLATE_PLANNING_READINESS_REPORT = (
    LAYER_DIR / "reports" / "bereishis_perek_2_gate_2_template_planning_readiness_report.md"
)
TOKEN_SPLIT_SOURCE = (
    ROOT
    / "data"
    / "source_skill_enrichment"
    / "standards_candidates"
    / "bereishis_perek_2_token_split_standards_candidates.tsv"
)
CLEAN_GROUP_CROSSWALK = (
    ROOT
    / "data"
    / "source_skill_enrichment"
    / "reports"
    / "bereishis_perek_2_clean_group_raw_crosswalk.tsv"
)

REQUIRED_COLUMNS = [
    "gate_2_input_candidate_id",
    "source_candidate_file",
    "source_candidate_id",
    "source_ref",
    "hebrew_token",
    "hebrew_phrase",
    "approved_family",
    "canonical_skill_id",
    "canonical_standard_anchor",
    "enrichment_review_status",
    "selection_reason",
    "risk_level",
    "risk_reasons",
    "teacher_review_status",
    "answer_key_review_status",
    "distractor_review_status",
    "context_display_review_status",
    "hebrew_rendering_review_status",
    "gate_2_candidate_status",
    "question_allowed",
    "protected_preview_allowed",
    "reviewed_bank_allowed",
    "runtime_allowed",
    "student_facing_allowed",
    "yossi_gate_2_decision",
    "yossi_gate_2_notes",
]
REVIEW_COLUMNS = [
    "gate_2_input_candidate_id",
    "source_ref",
    "hebrew_token",
    "hebrew_phrase",
    "approved_family",
    "canonical_skill_id",
    "selection_reason",
    "risk_level",
    "teacher_review_status",
    "answer_key_review_status",
    "distractor_review_status",
    "context_display_review_status",
    "hebrew_rendering_review_status",
    "yossi_gate_2_decision",
    "yossi_notes",
]
REVIEW_STATUS_FIELDS = [
    "teacher_review_status",
    "answer_key_review_status",
    "distractor_review_status",
    "context_display_review_status",
    "hebrew_rendering_review_status",
]
GATE_FIELDS = {
    "question_allowed": "needs_review",
    "protected_preview_allowed": "false",
    "reviewed_bank_allowed": "false",
    "runtime_allowed": "false",
    "student_facing_allowed": "false",
}
EXPECTED_DECISION_COUNTS = {
    "approve_for_template_planning": 14,
    "approve_with_revision": 4,
    "needs_follow_up": 2,
    "block_for_now": 0,
    "source_only": 0,
}
EXPECTED_STATUS_BY_DECISION = {
    "approve_for_template_planning": "yossi_approved_for_template_planning",
    "approve_with_revision": "yossi_approved_with_revision_before_template_planning",
    "needs_follow_up": "needs_follow_up",
}
REVISION_NOTE_PHRASES = {
    "g2p2_004": ("field", "not article/prefix recognition"),
    "g2p2_005": ("land/earth", "no prefix/article question"),
    "g2p2_008": ("base noun river", "no vav/prefix recognition"),
    "g2p2_018": ("side/rib", "no article recognition"),
}
FOLLOW_UP_NOTE_PHRASES = {
    "g2p2_011": ("uncommon word", "school vocabulary"),
    "g2p2_015": ("helper opposite him", "teacher wording"),
}
FORBIDDEN_COLUMNS = {
    "question",
    "prompt",
    "draft_prompt",
    "answer_choices",
    "answer_key",
    "expected_answer",
    "correct_answer",
    "distractors",
    "distractor_options",
}
HEBREW_RE = re.compile(r"[\u0590-\u05FF]")
EXPECTED_SOURCE_FILE = "data/source_skill_enrichment/standards_candidates/bereishis_perek_2_token_split_standards_candidates.tsv"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def validate_gate_2_input_planning() -> dict[str, object]:
    errors: list[str] = []
    for path in (
        README,
        PROPOSAL_TSV,
        BALANCE_REPORT,
        YOSSI_REVIEW_MD,
        YOSSI_REVIEW_CSV,
        PROPOSAL_REPORT,
        REVIEW_APPLIED_REPORT,
        TEMPLATE_PLANNING_READINESS_REPORT,
    ):
        if not path.exists():
            errors.append(f"missing Gate 2 input-planning artifact: {rel(path)}")
    if errors:
        return {"valid": False, "errors": errors}

    fields, rows = load_tsv(PROPOSAL_TSV)
    if fields != REQUIRED_COLUMNS:
        errors.append("Gate 2 proposal TSV columns do not match required schema")
    if not 20 <= len(rows) <= 24:
        errors.append(f"Gate 2 proposal row count must be between 20 and 24, found {len(rows)}")
    if FORBIDDEN_COLUMNS.intersection(fields):
        errors.append(f"Gate 2 proposal includes forbidden question/answer columns: {sorted(FORBIDDEN_COLUMNS.intersection(fields))}")

    _, source_rows = load_tsv(TOKEN_SPLIT_SOURCE)
    source_by_id = {row["candidate_id"]: row for row in source_rows}
    with CLEAN_GROUP_CROSSWALK.open("r", encoding="utf-8", newline="") as handle:
        crosswalk_rows = list(csv.DictReader(handle, delimiter="\t"))
    verified_ids = {
        row["source_candidate_id"]
        for row in crosswalk_rows
        if row.get("source_candidate_file") == EXPECTED_SOURCE_FILE
        and row.get("category") == "token_split_clean_noun_standards"
        and row.get("recommended_yossi_decision") == "verified"
    }
    follow_up_ids = {
        row["source_candidate_id"]
        for row in crosswalk_rows
        if row.get("recommended_yossi_decision") == "needs_follow_up"
    }

    seen_ids: set[str] = set()
    for row in rows:
        context = row.get("gate_2_input_candidate_id", "unknown")
        source_id = row.get("source_candidate_id", "")
        if context in seen_ids:
            errors.append(f"duplicate Gate 2 candidate ID: {context}")
        seen_ids.add(context)
        if row.get("source_candidate_file") != EXPECTED_SOURCE_FILE:
            errors.append(f"{context}: source file must be the Perek 2 token-split standards TSV")
        if source_id not in verified_ids:
            errors.append(f"{context}: source candidate must be verified token-split clean noun standards")
        if source_id in follow_up_ids:
            errors.append(f"{context}: follow-up raw candidate must not be included")
        source = source_by_id.get(source_id)
        if not source:
            errors.append(f"{context}: source candidate ID not found in token-split source TSV")
        else:
            if source.get("enrichment_review_status") != "yossi_enrichment_verified":
                errors.append(f"{context}: source enrichment status must be yossi_enrichment_verified")
            if source.get("yossi_decision") != "verified":
                errors.append(f"{context}: source Yossi decision must be verified")
            if source.get("canonical_skill_id") != row.get("canonical_skill_id"):
                errors.append(f"{context}: canonical skill ID must match source row")
            if row.get("source_ref") != source.get("ref"):
                errors.append(f"{context}: source ref must match source row")
        if row.get("approved_family") != "basic_noun_recognition":
            errors.append(f"{context}: approved_family must stay basic_noun_recognition")
        if row.get("canonical_skill_id") != "phrase_translation":
            errors.append(f"{context}: canonical skill must remain phrase_translation token-split standards mapping")
        if row.get("enrichment_review_status") != "yossi_enrichment_verified":
            errors.append(f"{context}: proposal enrichment status must be yossi_enrichment_verified")
        for field in REVIEW_STATUS_FIELDS:
            if row.get(field) != "needs_review":
                errors.append(f"{context}: {field} must be needs_review")
        decision = row.get("yossi_gate_2_decision", "")
        expected_status = EXPECTED_STATUS_BY_DECISION.get(decision)
        if expected_status is None:
            errors.append(f"{context}: unexpected Yossi Gate 2 decision: {decision}")
        elif row.get("gate_2_candidate_status") != expected_status:
            errors.append(f"{context}: gate_2_candidate_status must be {expected_status}")
        for field, expected in GATE_FIELDS.items():
            if row.get(field) != expected:
                errors.append(f"{context}: {field} must be {expected}")
        if not row.get("yossi_gate_2_notes"):
            errors.append(f"{context}: Yossi notes must be populated after decision application")
        if decision == "approve_with_revision":
            for phrase in REVISION_NOTE_PHRASES.get(context, ()):
                if phrase not in row.get("yossi_gate_2_notes", ""):
                    errors.append(f"{context}: revision note missing phrase: {phrase}")
        elif context in REVISION_NOTE_PHRASES:
            errors.append(f"{context}: expected approve_with_revision decision")
        if decision == "needs_follow_up":
            for phrase in FOLLOW_UP_NOTE_PHRASES.get(context, ()):
                if phrase not in row.get("yossi_gate_2_notes", ""):
                    errors.append(f"{context}: follow-up note missing phrase: {phrase}")
        elif context in FOLLOW_UP_NOTE_PHRASES:
            errors.append(f"{context}: expected needs_follow_up decision")
        if row.get("hebrew_token") == "את" or row.get("hebrew_token") == "אֶת":
            errors.append(f"{context}: direct-object marker row must not be included")
        if row.get("approved_family") in {"shoresh_identification", "basic_verb_form_recognition", "direct_object_marker_recognition"}:
            errors.append(f"{context}: unsafe family included")
        for field in ("hebrew_token", "hebrew_phrase"):
            value = row.get(field, "")
            if not HEBREW_RE.search(value):
                errors.append(f"{context}: {field} must contain real Hebrew")
            if "???" in value or "×" in value or "Ö" in value:
                errors.append(f"{context}: {field} contains placeholder/mojibake corruption")

    if not YOSSI_REVIEW_CSV.read_bytes().startswith(b"\xef\xbb\xbf"):
        errors.append("Gate 2 Yossi review CSV must be UTF-8-BOM")
    with YOSSI_REVIEW_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    if review_rows and list(review_rows[0].keys()) != REVIEW_COLUMNS:
        errors.append("Gate 2 Yossi review CSV columns do not match expected schema")
    if len(review_rows) != len(rows):
        errors.append("Gate 2 Yossi review CSV row count must match proposal TSV")
    review_decision_counts = Counter(row.get("yossi_gate_2_decision", "") for row in review_rows)
    for decision, expected_count in EXPECTED_DECISION_COUNTS.items():
        if review_decision_counts.get(decision, 0) != expected_count:
            errors.append(f"Gate 2 Yossi review CSV expected {expected_count} {decision} rows")
    if any(not row.get("yossi_notes") for row in review_rows):
        errors.append("Gate 2 Yossi review CSV notes must be populated after decision application")

    decision_counts = Counter(row.get("yossi_gate_2_decision", "") for row in rows)
    for decision, expected_count in EXPECTED_DECISION_COUNTS.items():
        if decision_counts.get(decision, 0) != expected_count:
            errors.append(f"Gate 2 proposal expected {expected_count} {decision} rows")

    artifact_text = "\n".join(
        path.read_text(encoding="utf-8-sig" if path.suffix == ".csv" else "utf-8")
        for path in (
            README,
            PROPOSAL_TSV,
            BALANCE_REPORT,
            YOSSI_REVIEW_MD,
            YOSSI_REVIEW_CSV,
            PROPOSAL_REPORT,
            REVIEW_APPLIED_REPORT,
            TEMPLATE_PLANNING_READINESS_REPORT,
        )
    )
    for phrase in (
        "no questions",
        "No questions",
        "No answer choices",
        "No answer keys",
        "No distractors",
        "No controlled drafts",
        "No protected-preview content",
        "No reviewed-bank entries",
        "No runtime",
        "student-facing",
        "all gates remain closed",
    ):
        if phrase not in artifact_text:
            errors.append(f"Gate 2 artifacts missing safety phrase: {phrase}")
    for forbidden in ("???", "×", "Ö"):
        if forbidden in artifact_text:
            errors.append(f"Gate 2 artifacts contain forbidden/corrupt phrase: {forbidden}")

    readme_text = README.read_text(encoding="utf-8")
    for path in (
        PROPOSAL_TSV,
        BALANCE_REPORT,
        YOSSI_REVIEW_MD,
        YOSSI_REVIEW_CSV,
        PROPOSAL_REPORT,
        REVIEW_APPLIED_REPORT,
        TEMPLATE_PLANNING_READINESS_REPORT,
    ):
        if rel(path).replace("data/gate_2_input_planning/", "") not in readme_text:
            errors.append(f"Gate 2 README missing artifact link: {rel(path)}")

    return {
        "valid": not errors,
        "errors": errors,
        "proposal_path": rel(PROPOSAL_TSV),
        "row_count": len(rows),
        "unique_token_count": len({row.get("hebrew_token", "") for row in rows}),
        "ref_count": len({row.get("source_ref", "") for row in rows}),
        "review_csv_path": rel(YOSSI_REVIEW_CSV),
        "decision_counts": dict(decision_counts),
    }


def main() -> int:
    summary = validate_gate_2_input_planning()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
