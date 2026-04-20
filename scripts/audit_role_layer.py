from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from contextlib import ExitStack
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import engine.flow_builder as flow_builder
from assessment_scope import (
    active_scope_gold_annotation_for_text,
    active_parsed_pesukim_records,
    active_pesukim_records,
    question_matches_gold_skill_record,
    repo_path,
)
from pasuk_flow_generator import generate_question


SKILLS = (
    "subject_identification",
    "object_identification",
    "phrase_translation",
)


def _coverage_snapshot(*, use_parsed_artifact, use_overrides):
    support = {}
    examples = {}
    for skill in SKILLS:
        supported = 0
        skipped = 0
        reasons = Counter()
        supported_examples = []
        skipped_examples = []

        parsed_patcher = (
            patch.object(flow_builder, "active_scope_parsed_analysis", return_value=None)
            if not use_parsed_artifact
            else patch.object(flow_builder, "active_scope_parsed_analysis", wraps=flow_builder.active_scope_parsed_analysis)
        )
        override_patcher = (
            patch.object(flow_builder, "active_scope_skill_override", return_value=None)
            if not use_overrides
            else patch.object(flow_builder, "active_scope_skill_override", wraps=flow_builder.active_scope_skill_override)
        )
        with ExitStack() as stack:
            stack.enter_context(parsed_patcher)
            stack.enter_context(override_patcher)
            for record in active_pesukim_records():
                ref = record.get("ref", {})
                question = generate_question(skill, record.get("text", ""))
                item = {
                    "ref": f"{ref.get('perek')}:{ref.get('pasuk')}",
                    "question": question.get("question"),
                    "correct_answer": question.get("correct_answer"),
                    "reason": question.get("reason"),
                    "source": question.get("source"),
                    "analysis_source": question.get("analysis_source"),
                }
                if question.get("status") == "skipped":
                    skipped += 1
                    reasons[question.get("reason") or "skipped"] += 1
                    if len(skipped_examples) < 5:
                        skipped_examples.append(item)
                else:
                    supported += 1
                    if len(supported_examples) < 5:
                        supported_examples.append(item)

        support[skill] = {
            "supported": supported,
            "skipped": skipped,
            "skip_reasons": dict(reasons),
            "supported_refs": [
                item["ref"] for item in supported_examples
            ],
        }
        examples[skill] = {
            "supported_examples": supported_examples,
            "skipped_examples": skipped_examples,
        }

    return support, examples


def _gold_truth_snapshot():
    truth = {}
    for skill in SKILLS:
        approved_refs = []
        suppressed_refs = []
        for record in active_pesukim_records():
            ref = record.get("ref", {})
            ref_key = f"{ref.get('perek')}:{ref.get('pasuk')}"
            gold_skill = (active_scope_gold_annotation_for_text(record.get("text", "")) or {}).get("skills", {}).get(skill)
            if not gold_skill:
                continue
            if gold_skill.get("status") == "approved":
                approved_refs.append(ref_key)
            else:
                suppressed_refs.append(ref_key)
        truth[skill] = {
            "approved": len(approved_refs),
            "suppressed": len(suppressed_refs),
            "approved_refs": approved_refs,
            "suppressed_refs": suppressed_refs,
        }
    return truth


def _gold_alignment_snapshot(*, use_parsed_artifact, use_overrides):
    alignment = {}
    parsed_patcher = (
        patch.object(flow_builder, "active_scope_parsed_analysis", return_value=None)
        if not use_parsed_artifact
        else patch.object(flow_builder, "active_scope_parsed_analysis", wraps=flow_builder.active_scope_parsed_analysis)
    )
    override_patcher = (
        patch.object(flow_builder, "active_scope_skill_override", return_value=None)
        if not use_overrides
        else patch.object(flow_builder, "active_scope_skill_override", wraps=flow_builder.active_scope_skill_override)
    )

    with ExitStack() as stack:
        stack.enter_context(parsed_patcher)
        stack.enter_context(override_patcher)
        for skill in SKILLS:
            matched_approved = []
            matched_suppressed = []
            missed_gold = []
            unsupported_in_gold = []
            for record in active_pesukim_records():
                ref = record.get("ref", {})
                ref_key = f"{ref.get('perek')}:{ref.get('pasuk')}"
                question = generate_question(skill, record.get("text", ""))
                gold_skill = (active_scope_gold_annotation_for_text(record.get("text", "")) or {}).get("skills", {}).get(skill)
                if not gold_skill:
                    continue

                if gold_skill.get("status") == "suppressed":
                    unsupported_in_gold.append(ref_key)
                    if question.get("status") == "skipped":
                        matched_suppressed.append(ref_key)
                    continue

                if question_matches_gold_skill_record(question, gold_skill):
                    matched_approved.append(ref_key)
                else:
                    missed_gold.append(ref_key)

            alignment[skill] = {
                "matched_approved_refs": matched_approved,
                "matched_approved_count": len(matched_approved),
                "missed_gold_refs": missed_gold,
                "missed_gold_count": len(missed_gold),
                "matched_suppressed_refs": matched_suppressed,
                "matched_suppressed_count": len(matched_suppressed),
                "unsupported_in_gold_refs": unsupported_in_gold,
                "unsupported_in_gold_count": len(unsupported_in_gold),
            }
    return alignment


def build_role_layer_audit():
    parsed_records = list(active_parsed_pesukim_records())
    role_status_counts = Counter(
        (record.get("role_layer") or {}).get("status", "missing")
        for record in parsed_records
    )

    without_overrides_support, without_overrides_examples = _coverage_snapshot(
        use_parsed_artifact=True,
        use_overrides=False,
    )
    with_overrides_support, with_overrides_examples = _coverage_snapshot(
        use_parsed_artifact=True,
        use_overrides=True,
    )
    gold_truth = _gold_truth_snapshot()
    parser_vs_gold = _gold_alignment_snapshot(
        use_parsed_artifact=True,
        use_overrides=False,
    )
    override_vs_gold = _gold_alignment_snapshot(
        use_parsed_artifact=True,
        use_overrides=True,
    )

    improvements = {}
    still_skipped = {}
    for skill in SKILLS:
        without_supported = set()
        with_supported = set()
        for record in active_pesukim_records():
            ref = record.get("ref", {})
            ref_key = f"{ref.get('perek')}:{ref.get('pasuk')}"

            with patch.object(flow_builder, "active_scope_skill_override", return_value=None):
                baseline_question = generate_question(skill, record.get("text", ""))
            current_question = generate_question(skill, record.get("text", ""))

            if baseline_question.get("status") != "skipped":
                without_supported.add(ref_key)
            if current_question.get("status") != "skipped":
                with_supported.add(ref_key)

        improvements[skill] = sorted(with_supported - without_supported)
        still_skipped[skill] = sorted(
            ref_key
            for ref_key in (
                f"{record.get('ref', {}).get('perek')}:{record.get('ref', {}).get('pasuk')}"
                for record in active_pesukim_records()
            )
            if ref_key not in with_supported
        )

    return {
        "active_scope": {
            "pesukim_count": len(list(active_pesukim_records())),
            "parsed_pesukim_count": len(parsed_records),
            "parsed_role_status_counts": dict(role_status_counts),
        },
        "parsed_artifact_without_overrides": {
            "support": without_overrides_support,
            "examples": without_overrides_examples,
        },
        "parsed_artifact_with_overrides": {
            "support": with_overrides_support,
            "examples": with_overrides_examples,
        },
        "gold_truth": gold_truth,
        "parser_vs_gold": parser_vs_gold,
        "override_vs_gold": override_vs_gold,
        "override_delta_supported": {
            skill: with_overrides_support[skill]["supported"] - without_overrides_support[skill]["supported"]
            for skill in SKILLS
        },
        "override_improvements": improvements,
        "still_skipped_after_overrides": still_skipped,
    }


def write_role_layer_audit(output_dir=None):
    audit = build_role_layer_audit()
    base = Path(output_dir) if output_dir else repo_path("data", "validation")
    base.mkdir(parents=True, exist_ok=True)
    json_path = base / "role_layer_audit.json"
    md_path = base / "role_layer_audit.md"

    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Role Layer Audit",
        "",
        f"- Active pesukim: {audit['active_scope']['pesukim_count']}",
        f"- Parsed pesukim with role data: {audit['active_scope']['parsed_pesukim_count']}",
        f"- Role status counts: {audit['active_scope']['parsed_role_status_counts']}",
        "",
    ]
    for skill in SKILLS:
        baseline = audit["parsed_artifact_without_overrides"]["support"][skill]
        current = audit["parsed_artifact_with_overrides"]["support"][skill]
        gold = audit["gold_truth"][skill]
        parser_gold = audit["parser_vs_gold"][skill]
        override_gold = audit["override_vs_gold"][skill]
        lines.extend(
            [
                f"## {skill}",
                "",
                f"- Gold-approved refs: {gold['approved']}",
                f"- Gold-suppressed refs: {gold['suppressed']}",
                f"- Supported without overrides: {baseline['supported']}",
                f"- Skipped without overrides: {baseline['skipped']}",
                f"- Supported with overrides: {current['supported']}",
                f"- Skipped with overrides: {current['skipped']}",
                f"- Parser matches gold-approved refs: {parser_gold['matched_approved_count']}",
                f"- Parser misses gold-approved refs: {parser_gold['missed_gold_count']}",
                f"- Override matches gold-approved refs: {override_gold['matched_approved_count']}",
                f"- Override misses gold-approved refs: {override_gold['missed_gold_count']}",
                f"- Support not approved even in gold: {override_gold['unsupported_in_gold_count']}",
                f"- Override delta supported: {audit['override_delta_supported'][skill]}",
                f"- Improved refs: {audit['override_improvements'][skill]}",
                f"- Still skipped refs: {audit['still_skipped_after_overrides'][skill]}",
                "",
            ]
        )

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return audit


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(write_role_layer_audit(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
