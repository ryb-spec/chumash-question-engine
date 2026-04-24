# Master Prompt: Curriculum Resource Extraction Batch

You are working in the chumash-question-engine repo.

Your job is to run one controlled curriculum extraction batch.

This project already has an inactive curriculum extraction factory under:

data/curriculum_extraction/

The goal is to turn selected Chumash curriculum resources into structured, validated, source-traced, engine-ready data WITHOUT touching runtime.

This is NOT runtime integration.
This is NOT UI work.
This is NOT scoring/mastery work.
This is NOT corpus promotion.
This is NOT reviewed-question-bank work.

Everything extracted remains inactive unless a future explicit runtime-integration branch says otherwise.

---

# BATCH VARIABLES

Before doing any work, identify and confirm these variables from the user’s instruction.

If any are missing, STOP and report exactly what is missing.

Required variables:

- BATCH_ID:
  Example: batch_002_linear_bereishis

- BRANCH:
  Example: feature/curriculum-batch-002-linear-bereishis

- SOURCE_PACKAGE_ID:
  Example: linear_chumash_translation

- SOURCE_NAME:
  Example: Linear Chumash Translation for Most Parshiyos in Torah

- SOURCE_FILE_OR_LOCAL_SOURCE:
  Example:
  local_curriculum_sources/7984C_b_01409_pshat_of_torah.pdf
  OR
  local_curriculum_sources/source_key_excerpt_batch_001.md

- SOURCE_RANGE:
  Example: Bereishis 1:6 through Bereishis 2:3

- RECORD_TYPES_TO_EXTRACT:
  Examples:
  pasuk_segment
  translation_rule
  vocab_entry
  word_parse
  word_parse_task
  comprehension_question

- TARGET_RECORD_COUNTS:
  Example:
  pasuk_segment: 75–125
  translation_rule: 0–10

- PREVIEW_QUESTION_TYPES:
  Examples:
  phrase_translation
  hebrew_to_english_match
  english_to_hebrew_match

---

# HARD RULES

Do not modify:

- streamlit_app.py
- runtime/
- engine/
- assessment_scope.py
- data/corpus_manifest.json
- active reviewed question bank files
- UI files
- scoring/mastery files
- unrelated tests
- unrelated scripts

Do not:

- connect anything to runtime
- promote any corpus slice
- write to reviewed question bank
- mark extracted records reviewed
- set anything runtime_active
- guess translations
- invent Hebrew
- infer missing answers without source-backed evidence
- generate live questions
- broaden the batch scope
- start the next batch
- merge branches
- create a PR unless explicitly instructed by the user and allowed by repo instructions

If any forbidden action seems necessary, STOP and report instead of proceeding.

---

# REQUIRED STATUS VALUES

Every extracted record must remain:

review_status = needs_review
runtime_status = not_runtime_active
confidence = low or medium

Never use:

review_status = reviewed
runtime_status = runtime_active
confidence = high

unless the user gives a future explicit human-review/promotion instruction.

---

# LOCAL SOURCE POLICY

Source PDFs and source excerpts may be stored locally under:

local_curriculum_sources/

This folder is gitignored and must not be committed.

Do not copy full PDFs into the repo.

You may create cleaned markdown excerpts under:

data/curriculum_extraction/raw_sources/<BATCH_ID>/

Only copy the relevant cleaned excerpt, not the full source PDF.

If required source material is missing, create a source gap report and STOP.

Create:

data/curriculum_extraction/reports/<BATCH_ID>_source_gap_request.md

The report must list:

- exact missing file
- exact pages or range needed
- exact content needed
- which record types are blocked
- what the user must provide next

Do not guess from memory.

---

# PREFLIGHT

Before starting extraction, run:

git branch --show-current
git status --short
python scripts/validate_curriculum_extraction.py
python scripts/load_curriculum_extraction.py --summary
python -m pytest tests/test_curriculum_extraction_validation.py tests/test_curriculum_question_preview.py

Then confirm:

1. Current branch matches the expected branch.
2. Worktree is clean.
3. data/curriculum_extraction/ exists.
4. scripts/validate_curriculum_extraction.py exists.
5. scripts/load_curriculum_extraction.py exists.
6. Source file or local source excerpt exists.
7. Validation passes.
8. Loader summary passes.
9. Targeted tests pass.

If any condition fails, STOP and report.

Do not create files before preflight passes.

---

# ALLOWED PATHS

Unless the user explicitly says otherwise, you may modify only:

- data/curriculum_extraction/raw_sources/<BATCH_ID>/
- data/curriculum_extraction/normalized/
- data/curriculum_extraction/generated_questions_preview/
- data/curriculum_extraction/reports/
- data/curriculum_extraction/curriculum_extraction_manifest.json
- scripts/generate_curriculum_question_preview.py
- scripts/validate_curriculum_extraction.py
- scripts/load_curriculum_extraction.py only if needed
- tests/test_curriculum_extraction_validation.py
- tests/test_curriculum_question_preview.py
- docs/curriculum_extraction_factory.md

Do not modify any runtime, engine, UI, scoring, mastery, corpus, or reviewed-bank files.

---

# EXTRACTION REQUIREMENTS

Create a cleaned source file when appropriate:

data/curriculum_extraction/raw_sources/<BATCH_ID>/<cleaned_source_name>.md

Create normalized JSONL files according to record type:

data/curriculum_extraction/normalized/<BATCH_ID>_<record_type>.jsonl

Examples:

data/curriculum_extraction/normalized/batch_002_linear_bereishis_pasuk_segments.jsonl
data/curriculum_extraction/normalized/batch_002_linear_bereishis_translation_rules.jsonl

Every normalized record must include:

- id
- schema_version
- record_type
- extraction_batch_id
- source_package_id
- source_trace
- review_status
- runtime_status
- confidence
- extraction_quality_flags

Every source_trace must include:

- source_name
- source_file
- source_page_start
- source_page_end
- source_section
- source_ref
- source_snippet_raw
- source_snippet_normalized
- extraction_method
- extraction_note
- source_has_answer_key
- review_status

Preserve raw source text.

Do not replace raw Hebrew or raw English with normalized text.

Normalized fields may be empty if normalization is uncertain.

---

# RECORD TYPE RULES

## pasuk_segment

Use for phrase/word/full-pasuk translation records.

Required fields:

- canonical_ref
- sefer
- parsha
- perek
- pasuk
- pasuk_range
- segment_order
- segment_level
- hebrew_raw
- hebrew_normalized
- english_raw
- english_normalized
- missing_hebrew_flag
- missing_translation_flag
- translation_type
- parenthetical_clarification
- translation_rule_tags
- source_footnote_refs
- skill_tags
- linked_vocab_ids
- linked_word_parse_ids

Rules:

- Preserve source order.
- Use phrase-level segmentation unless instructed otherwise.
- Do not invent missing translations.
- If Hebrew is noisy but source-backed, preserve it and add an extraction_quality_flag.
- If a segment is unreliable, skip it and report it.

---

## translation_rule

Use only when the source explicitly provides a rule, note, or repeated translation principle.

Required fields:

- rule_key
- rule_label
- student_facing_explanation
- example_refs
- skill_tags

Rules:

- Do not invent rules.
- Do not generalize beyond the source.
- If a rule is reused from an already extracted rule, reference the existing rule key.

---

## vocab_entry

Use for vocabulary, words, shorashim, names, concepts, and frequency lists.

Required fields:

- hebrew
- normalized_hebrew
- entry_type
- english_glosses
- needs_gloss_review
- sefer_scope
- frequency_source
- frequency_band
- global_frequency_band
- priority_level
- skill_tags

Rules:

- If the source does not provide an English gloss, leave english_glosses empty.
- If english_glosses is empty, set needs_gloss_review = true.
- Do not guess glosses.
- Use source-backed glosses only.

---

## word_parse

Use for completed word breakdowns where the source provides enough answer-bearing data.

Required fields:

- canonical_ref
- sefer
- parsha
- perek
- pasuk
- word_in_pasuk_raw
- word_in_pasuk_normalized
- base_word
- target_shoresh_raw
- target_shoresh_normalized
- shoresh_meaning
- prefixes
- suffixes
- grammar_features
- literal_translation
- contextual_translation
- answer_status
- skill_tags

Rules:

- Prefixes and suffixes must be arrays of objects.
- Do not force shoresh/suffix/prefix fields if not source-backed.
- If incomplete, add clear extraction_quality_flags.
- If answer_status = source_provided, an answer/translation/parse payload must exist.

---

## word_parse_task

Use for worksheet task rows where students are asked to locate or fill answers.

Required fields:

- task_type
- sefer
- parsha
- perek
- pasuk
- pasuk_range
- target_shoresh_raw
- target_shoresh_normalized
- expected_word_in_pasuk
- prefixes
- suffixes
- answer_status
- skill_tags

Rules:

- If answer key is not present, answer_status = not_extracted.
- Do not infer expected_word_in_pasuk from your own knowledge.
- If answer key is missing, add extraction_quality_flags:
  answer_key_required_not_present_in_repo

---

## comprehension_question

Use for question prompts such as מי אמר אל מי and על מי נאמר.

Required fields:

- question_type
- sefer
- parsha
- perek
- pasuk
- quoted_phrase_raw
- question_text
- expected_answer
- answer_status
- skill_tags

Rules:

- If there is no source-backed answer key, expected_answer = null.
- If expected_answer is null, answer_status = not_provided.
- Add extraction_quality_flags:
  missing_expected_answer

Do not guess the answer.

---

# MANIFEST UPDATE

Update:

data/curriculum_extraction/curriculum_extraction_manifest.json

Add a new batch entry:

- batch_id
- status
- review_status = needs_review
- runtime_active = false
- source package
- raw_source_files
- normalized_data_files
- generated_question_preview_files if preview was generated

Keep:

integration_status = not_runtime_active
runtime_active = false

---

# PREVIEW GENERATION

Generate preview questions only from answer-bearing data.

Preview files go here:

data/curriculum_extraction/generated_questions_preview/<BATCH_ID>_preview.jsonl

Allowed supported question types depend on the source.

For Linear Chumash / phrase translation batches, supported types are usually:

- phrase_translation
- hebrew_to_english_match
- english_to_hebrew_match

For word_parse batches, supported types may include:

- shoresh_identification
- prefix_identification
- suffix_identification
- full_word_translation

For vocab batches, supported types may include:

- vocab_translation
- hebrew_to_english_match
- english_to_hebrew_match

Do not generate:

- mi_amar_el_mi
- al_mi_neemar
- word_parse_task answer checking

unless the records have source-backed expected answers.

Each preview question must include:

- id
- schema_version
- record_type = generated_question_preview
- source_record_id
- source_package_id
- question_type
- prompt
- answer
- distractors
- skill_tags
- source_trace
- review_status = needs_review
- runtime_status = not_runtime_active
- confidence = low

Rules:

- Do not generate from missing answers.
- Do not invent distractors if safe distractors are unavailable.
- Output must be deterministic.
- Loader must continue to ignore preview files safely.

---

# VALIDATION REQUIREMENTS

Extend validation only if needed.

Validation must enforce:

- every normalized record has source_trace
- every source_package_id exists in registry
- every record has review_status
- no record is reviewed
- no record is runtime_active
- no record has confidence = high
- every JSONL file is valid
- every id is unique
- every skill_tag reference exists
- every preview question references a valid source_record_id
- loader ignores preview data safely
- source_provided records have answer payloads
- missing-answer records have explicit extraction_quality_flags

---

# REQUIRED REPORTS

Create a batch summary:

data/curriculum_extraction/reports/<BATCH_ID>_summary.md

Include:

- source used
- source range
- files created
- normalized record counts
- skipped records
- extraction risks
- validation result
- recommendation

Create a preview summary if preview was generated:

data/curriculum_extraction/reports/<BATCH_ID>_preview_summary.md

Include:

- preview question counts by type
- supported lanes
- blocked lanes
- skipped source records
- weak data areas
- recommendation:
  READY_FOR_MANUAL_REVIEW
  or BLOCKED

If the batch is blocked, create a blocker report:

data/curriculum_extraction/reports/<BATCH_ID>_blocker_report.md

or source-specific gap report:

data/curriculum_extraction/reports/<BATCH_ID>_source_gap_request.md

---

# FINAL RUN

At the end, run:

python scripts/validate_curriculum_extraction.py
python scripts/load_curriculum_extraction.py --summary
python -m pytest
git diff --name-only
git status --short

---

# FINAL REPORT TO USER

Report:

1. Current branch
2. Files created/changed
3. Record counts by type
4. Preview question counts by type, if generated
5. Validation result
6. Loader summary
7. Full test result
8. Git diff
9. Git status
10. Confirmation no runtime/UI/mastery/corpus files touched
11. Blockers, if any
12. Recommendation:
    READY_FOR_MANUAL_REVIEW
    BLOCKED_NEEDS_SOURCE
    MERGE_INACTIVE_INFRASTRUCTURE
    or HOLD

---

# STOP RULE

Stop after the requested batch.

Do not:

- start another batch
- merge branches
- create a PR
- connect to runtime
- write to reviewed question bank
- promote corpus scope
- broaden source range

One batch. One report. One clean stopping point.
