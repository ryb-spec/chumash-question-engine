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

- generated questions
- protected preview questions
- answer choices
- answer keys for generated questions
- reviewed-bank promotion
- runtime activation
- student-facing use
- production data changes

## Review Path Selector

| Content Type | Correct Review Path | What Yossi Reviews | Still Requires Separate Gate? |
|---|---|---|---|
| Trusted teacher-source extraction | Extraction accuracy confirmation | Source matching, Hebrew fidelity, extracted translations/explanations, classification, and mapping | Yes, before question generation or runtime use |
| AI-generated questions | Full generated-question review | Accuracy, educational fit, wording, distractors, answer key, source support, and student readiness | Yes |
| Protected preview packet | Protected preview review | Whether preview items are accurate, bounded, clear, and still non-runtime | Yes |
| Reviewed-bank promotion | Reviewed-bank promotion gate | Candidate schema, review evidence, source support, statuses, and blocked-content checks | Yes |
| Runtime activation | Runtime activation gate | Loader behavior, active scope, rollback, monitoring, and student-facing approval | Yes |
| Unclear source | Targeted confirmation item | The exact unclear issue and the recommended status after confirmation | Yes, if the source remains unclear |

## Reviewer Instructions For Trusted Sources

For each extracted source item, Yossi should confirm:

- Was the source copied or OCRed accurately?
- Is the Hebrew faithful to the source?
- Are translations, explanations, examples, or answer keys extracted accurately?
- Is the classification correct?
- Is the standards or skill mapping reasonable?
- Is anything unclear enough to require a specific confirmation item?

Do not ask:

- "Do you approve this educational source?"
- "Should this source content be taught?"
- "Is the pedagogy approved from scratch?"
- "May this become runtime-ready?"
- "May this become question-ready?"

Those are the wrong questions for trusted source extraction packets.

## Item Review Table Template

| Item ID | Source Name | Source Path | Source Page/Reference | Extracted Text Or Data | Classification/Mapping | What Yossi Must Check | Recommended Status | Yossi Decision | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `example_item_id` | `source_name` | `path/to/source` | `page/ref` | `extracted content` | `classification or mapping` | Confirm source match, Hebrew fidelity, extraction accuracy, and mapping reasonableness. | `pending_yossi_extraction_accuracy_pass` |  |  |

## Allowed Decisions

- `yossi_extraction_verified`: Extraction, classification, and mapping accurately represent the trusted source.
- `needs_specific_confirmation`: A targeted issue needs Yossi or project-lead clarification.
- `blocked_unclear_source`: The source authority, provenance, or extraction is too unclear to use.

## Targeted Confirmation Item Template

Use this when the system cannot decide a specific point.

| Field | Required Content |
|---|---|
| Source name | Name of the source or artifact |
| File path | Exact repo path |
| Unclear issue | One specific issue, not a broad blocker |
| Exact question for Yossi | The smallest question needed to unblock classification |
| Recommended status after confirmation | The status to use if Yossi confirms the issue |

## Generated Questions Remain Separate

AI-generated and system-generated questions still require full review. A trusted source extraction pass does not approve prompts, distractors, answer choices, answer keys, student-facing wording, reviewed-bank promotion, or runtime activation.

## Runtime Promotion Remains Separate

Verified source-derived content may support future planning, protected preview work, or standards mapping. It does not become runtime-active unless a separate runtime activation gate explicitly authorizes that change.
