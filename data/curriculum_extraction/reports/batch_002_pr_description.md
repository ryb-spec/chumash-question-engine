Title: Add Batch 002 Linear Chumash Bereishis extraction

## What changed

This branch adds Batch 002 curriculum extraction artifacts for `Bereishis 1:6` through `Bereishis 2:3` using the inactive curriculum extraction factory.

Included in this batch:
- cleaned source excerpt for the Batch 002 range
- normalized `pasuk_segment` extraction records
- Batch 002 preview question file
- Batch 002 summary, preview summary, and manual review packet
- merge-readiness reporting for inactive infrastructure

Batch 002 output is limited to translation/context support:
- `pasuk_segment`: `123`
- `translation_rule`: `0`
- preview questions: `100`

Supported preview lanes:
- `phrase_translation`
- `hebrew_to_english_match`
- `english_to_hebrew_match`

## What did not change

This PR does not:
- integrate anything into runtime
- modify Streamlit
- modify `runtime/`
- modify `engine/`
- modify `assessment_scope.py`
- modify `data/corpus_manifest.json`
- modify the reviewed question bank
- modify scoring or mastery behavior
- promote any corpus slice

Preview questions remain inactive and are not live runtime content.
The loader continues to ignore preview files safely.

## Validation / Testing

Pre-merge checks passed:
- `python scripts/validate_curriculum_extraction.py`
- `python scripts/load_curriculum_extraction.py --summary`
- `python -m pytest`

Result summary:
- validator: `valid: true`
- loader: `integration_status = not_runtime_active`
- full test suite: `467 passed`

## Manual Review

- Batch 002 manual review packet was created and replaced with the reviewer-edited version.
- Manual review covered sampled extraction records and sampled preview questions.
- Manual review did not alter extraction JSONL records, preview generation logic, or runtime behavior.

## Why this is safe to merge

- All extracted records remain inactive:
  - `review_status = needs_review`
  - `runtime_status = not_runtime_active`
- No runtime or engine wiring was added.
- No reviewed-question-bank changes were made.
- No corpus scope or live serving scope changed.
- Preview generation remains isolated under `data/curriculum_extraction/generated_questions_preview/`.

## What remains blocked

Blocked or deferred lanes for this batch:
- `mi_amar_el_mi`
- `al_mi_neemar`
- `word_parse_task` answer checking
- `translation_rule_recognition`

These lanes were intentionally excluded because Batch 002 is a translation-only extraction and does not include answer-key-backed comprehension or parse-task records.

## What comes next

Recommended next batch:
- the next contiguous inactive Linear Chumash extraction batch after `Bereishis 2:3`

That future work should stay in a separate explicit branch and remain isolated until reviewed and explicitly approved for any broader use.
