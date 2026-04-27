# Trusted Teacher Source Extraction Accuracy Review Packet

## Purpose

This future-facing packet is generated from the trusted teacher-source extraction review template.
It asks Yossi for one extraction-accuracy confirmation pass, not broad educational re-approval.

## Template Source

- Policy: `docs/sources/trusted_teacher_source_policy.md`
- Template: `docs/sources/trusted_teacher_source_extraction_review_packet_template.md`

## Hard Boundaries

- Runtime status: `not_runtime_ready`
- Question-generation status: `not_question_ready`
- Student-facing status: `not_student_facing`
- Reviewed-bank status: `not_approved_for_reviewed_bank`
- Current review path: `trusted_source_extraction_accuracy_pass`

This packet does not authorize generated questions, answer choices, answer keys, protected previews, reviewed-bank promotion, runtime activation, or student-facing use.

## Source Package

- Source package ID: `linear_chumash_translation_most_parshiyos_in_torah`
- Display name: Linear Chumash Translation for Most Parshiyos in Torah
- Source authority: `trusted_teacher_source`
- Teacher source status: `trusted_teacher_source`
- Extraction review status: `pending_yossi_extraction_accuracy_pass`
- Requires Yossi accuracy pass: `True`
- Runtime status: `not_runtime_ready`
- Question-ready status: `not_question_ready`

Expected future record types:
- `pasuk_segment`
- `translation_rule`

## Extraction Batch

- Batch ID: `batch_005_linear_bereishis_4_1_to_4_16`
- Label: Batch 005 Linear Chumash Translation excerpt
- Status: `reviewed_for_planning_non_runtime`
- Extraction review status: `yossi_extraction_verified`
- Integration status: `not_runtime_active`
- Runtime active: `False`

Raw source files:
- `data/curriculum_extraction/raw_sources/batch_005/linear_chumash_bereishis_4_1_to_4_16_cleaned.md`

Normalized data files:
- `data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl`

## Yossi Extraction-Accuracy Checklist

- Confirm that the copied or OCRed source text matches the source.
- Confirm that Hebrew spelling, nikud, and table layout are faithful where relevant.
- Confirm that translations, explanations, answer keys, or examples were extracted accurately.
- Confirm that classification and standards/skill mapping are reasonable.
- Flag any unclear item for specific confirmation.

Do not re-approve the educational value of this trusted source from scratch. That is not the review task here.

## Item Review Table

| Item ID | Source Path | Source Page/Reference | Extracted Text Or Data | Classification/Mapping | What Yossi Must Check | Yossi Decision | Notes |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  | Confirm source match, Hebrew fidelity, extraction accuracy, and mapping reasonableness. |  |  |

## Targeted Confirmation Items

| Confirmation Item ID | Source Name | File Path | Unclear Issue | Exact Question For Yossi | Current Status | Recommended Status |
|---|---|---|---|---|---|---|
| `confirm_loshon_foundation_rules_jsonl_source_alignment` | Loshon HaTorah / Loshon Hakodesh foundation rules, source-modeled JSONL | `data/dikduk_rules/rules_loshon_foundation.jsonl` | The JSONL is a source-derived internal artifact. It cites Loshon source pages/lessons, but exact record-to-page alignment is not fully confirmed. | Confirm whether this source-modeled JSONL may be treated as trusted source-derived content after checking representative records against the Loshon PDFs. | `needs_specific_confirmation` | yossi_extraction_verified if the representative source alignment is accurate; otherwise needs_specific_confirmation for the affected records. |

## Review Paths That Remain Strict

- AI-generated questions still require full generated-question review.
- Protected preview packets still require protected preview review.
- Answer choices and answer keys still require their own review before use.
- Reviewed-bank promotion still requires a reviewed-bank promotion gate.
- Runtime activation still requires a runtime activation gate.

## Template Excerpt Used

```markdown
# Trusted Teacher Source Extraction Accuracy Packet Template

## Purpose

Use this template for future packets that review extracted content from trusted teacher or standards source material.

This is not a broad educational approval packet. Yossi is not being asked to re-approve the educational value of trusted source content from scratch. Yossi is being asked to confirm that the system copied, OCRed, classified, and mapped the source accurately.

## Source Categories Covered

This template may be used for:

- Zekelman Chumash Standards resources
- Zekelman sample assessment questions
- Dikduk resources and workbooks
- Loshon Hakodesh / Loshon HaTorah resources
- Other clearly teacher-created Chumash, dikduk, or assessment resources used as source references

## Hard Boundaries

- Runtime status: `not_runtime_ready`
- Question-generation status: `not_question_ready`
- Student-facing status: `not_student_facing`
- Reviewed-bank status: `not_approved_for_reviewed_bank`
- Current review path: `trusted_source_extraction_accuracy_pass`

This packet does not authorize:
```

## Final Status

- Trusted-source extraction packet: ready for Yossi extraction-accuracy pass
- Runtime: blocked
- Question generation: blocked
- Reviewed bank: blocked
- Student-facing use: blocked
