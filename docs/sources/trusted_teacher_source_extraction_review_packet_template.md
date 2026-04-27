# Trusted Source Extraction Accuracy Review Packet

## Purpose

Use this template for future packets that review extracted content from trusted teacher or standards source material.

This is not a broad educational approval packet. Yossi is not being asked to re-approve the educational value of trusted source content from scratch. Yossi is being asked to confirm that the system copied, OCRed, classified, and mapped the source accurately.

The packet should be print-friendly and practical: it should show actual extracted records, source references, source/extracted evidence fields, checkboxes, issue areas, and a final decision page. Yossi should not need to hunt through raw Markdown and JSONL files just to know what to review.

## Source Categories Covered

This template may be used for:

- Zekelman Chumash Standards resources
- Zekelman sample assessment questions
- Dikduk resources and workbooks
- Loshon Hakodesh / Loshon HaTorah resources
- Linear Chumash Translation source materials
- Other clearly teacher-created Chumash, dikduk, or assessment resources used as source references

## Required Packet Structure

### 1. One-Page Review Summary

Include:

- batch ID
- source package
- source authority
- pasuk range or content range
- raw source file path
- normalized data file path
- number of extracted records
- record types included
- extraction review status
- runtime/question/student-facing status
- recommended current Yossi decision
- Yossi decision box

Decision box:

- [ ] Approved extraction accuracy
- [ ] Approved with corrections needed
- [ ] Not approved yet

Signature / reviewer:
Date:
Notes:

### 2. What Yossi Is Checking

Use plain English:

- I am checking extraction accuracy only.
- I am not re-approving the educational value of this trusted source.
- I am not approving runtime use.
- I am not approving generated questions.

### 3. Safety Boundaries

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

### 4. Review Instructions

Give Yossi a simple process:

1. Review the expanded source/evidence cards.
2. Check Hebrew-English phrase matching.
3. Check parenthetical/explanatory alignment.
4. Check long phrase boundaries and segment order.
5. Mark any row needing correction before verification.
6. Leave the batch pending unless all sampled evidence supports full extraction accuracy.

### 5. Expanded Source Evidence Review Samples

For each sample item, show clearly separated fields instead of a cramped table:

- Reference
- Source reference
- Source excerpt
- Cleaned source Hebrew side
- Extracted Hebrew
- Source English / Translation side
- Extracted English / Translation
- Parenthetical / explanatory text
- Segment order
- Classification
- Mapping / skill
- Warning flags
- Source extraction method
- Source extraction note
- Why this match is believed correct
- Human review question

Then include:

- [ ] Source match
- [ ] Hebrew phrase alignment
- [ ] English / translation alignment
- [ ] Parenthetical explanation alignment
- [ ] Segment order matches pasuk flow
- [ ] Classification and mapping reasonable
- [ ] Needs correction

Notes:
____________________________________________________

### 6. Sample Selection Logic

Generated packets should include an expanded deterministic evidence set when records carry warning flags:

- first 5 extracted records
- last 5 extracted records
- 10 deterministic random records selected by stable hash
- 10 longest English or explanatory records
- all records with substantial parenthetical explanations
- 10 longest Hebrew phrase segments
- any record with missing or suspicious display fields
- any record with unusual classification or unclear mapping
- any record connected to a targeted confirmation item

Keep the packet readable, but do not under-sample noisy PDF batches. If every record carries warning flags, include the expanded deterministic sample set in the main packet, a short appendix count summary, and the path to the full normalized file.

### 7. Extraction Summary Table

Include counts:

- total records
- records by type
- records with Hebrew
- records with English/translation
- records missing source reference
- records missing Hebrew
- records missing translation
- records with classification/mapping
- records with warnings

### 8. Targeted Confirmation Items

Only include confirmation items relevant to the selected source package or batch.

For noisy PDF / canonical-Hebrew-alignment batches, always include targeted confirmation items for:

- Hebrew-English phrase matching
- parenthetical explanation alignment
- long phrase boundary accuracy
- copied/extracted source wording versus generated wording
- acceptable cleanup/normalization
- segment order matching pasuk flow

Do not include unrelated global confirmation items in a batch-specific packet. Move them to a separate global source-confirmation packet or state that they were intentionally omitted.

### 9. Corrections Log

| Item ID | Issue Type | Correction Needed | Yossi Notes | Resolved? |
|---|---|---|---|---|
|  | Hebrew/OCR, Translation/explanation, Missing record, Wrong reference, Wrong classification, Wrong mapping, Unclear source, or Other |  |  |  |

### 10. Final Decision Page

End with a clean final decision page suitable for printing:

Batch:
Reviewer:
Date:

Decision:

- [ ] Approved extraction accuracy
- [ ] Approved with corrections needed
- [ ] Not approved yet

Required corrections:

1.
2.
3.

Final notes:

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

## Generator Usage

Future scripts that need a trusted teacher-source extraction packet should call:

- `scripts/generate_trusted_source_extraction_review_packet.py`

Use this generator only for trusted source extraction accuracy review. Do not use it for generated-question packets, protected preview packets, answer-key review, reviewed-bank promotion, runtime activation, or student-facing release decisions.

## Validator Requirement Before `yossi_extraction_verified`

The curriculum extraction validator requires trusted-source extraction batches to link a generated extraction accuracy packet before they can be treated as verified. Batches marked `yossi_extraction_verified` must also record the verifier, verification date, packet path, and confirmation artifact path.

This validator rule protects source-derived review only. It does not approve generated questions, answer keys, reviewed-bank promotion, runtime activation, or student-facing release.
