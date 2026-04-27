# Zekelman Standard 3 Runtime Loader Discovery Report

## 1. Purpose

This report documents runtime-loader discovery for possible future controlled test-mode exposure of the 10 protected Zekelman Standard 3 MVP reviewed-bank records.

This report does not activate runtime. It does not modify app routing. It does not modify active scope. It does not expose anything to students.

The goal is to identify how reviewed questions are currently loaded, whether the protected Standard 3 bank is currently ignored by runtime, and what would be required before any future controlled test-mode activation.

## 2. Hard Boundaries

- Runtime activation: blocked
- App routing changes: blocked
- Active-scope update: blocked
- Staged reviewed-bank update: blocked
- Student-facing use: blocked
- UI changes: blocked
- Current artifact: runtime-loader discovery report only

No runtime, UI, active-scope, staged reviewed-bank, production app, student-facing, quiz runtime, or active-template files were modified.

## 3. Protected Standard 3 Bank in Scope

- Source file: `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json`
- Record count: 10
- `runtime_status`: `not_runtime_active`
- `student_facing_status`: `not_student_facing`
- Scope: Standard 3 MVP only

The protected bank includes only these lanes:

- `3.01` Nouns / שמות עצם
- `3.02` Simple Shorashim / שורשים
- `3.05` Pronominal Suffix Decoding
- `3.06` Visible Prefixes / Articles
- `3.07` Foundational Verb Clues

## 4. Runtime Loading Map

| Area | File path | Role | Used by runtime now? | Safe to modify in future activation task? | Notes |
|---|---|---|---|---|---|
| Active reviewed-question source | `data/active_scope_reviewed_questions.json` | Current app-facing reviewed question bank. | Yes | No, not for first test-mode pass | This is the live reviewed bank for the active scope. It should stay untouched until a separate explicit activation decision. |
| Active reviewed-question loader | `assessment_scope.py` | Defines `ACTIVE_SCOPE_REVIEWED_QUESTIONS_PATH`, loads and canonicalizes active reviewed questions, and exposes `active_scope_reviewed_questions_for_text(...)`. | Yes | Candidate for future test-mode loader design | Current path is hardwired to `data/active_scope_reviewed_questions.json`. |
| Active reviewed-question selector | `engine/flow_builder.py` | Imports `active_scope_reviewed_questions_for_text(...)`, selects reviewed questions via `reviewed_question_for_pasuk_skill(...)`, clones them, and validates payloads. | Yes | Candidate for future test-mode adapter design | Existing runtime expects active-scope question records, not standards-side compact records. |
| Runtime payload validation | `engine/flow_builder.py` | `validate_question_payload(...)` requires valid choices, correct answer in choices, and other runtime question fields. | Yes | Candidate for future compatibility tests | Protected Standard 3 records do not currently include answer choices or active-scope pasuk binding. |
| Runtime serve validation | `runtime/question_flow.py` | Used by reviewed-bank build tooling to validate questions before serve. | Yes | Candidate for future test-mode validation | Future adapter should pass serve validation before any runtime exposure. |
| Staged reviewed-question sources | `data/staged/*/reviewed_questions.json` | Staged reviewed support for corpus promotion/build workflows. | Not directly default runtime; used by build/promotion tooling | No, unless explicitly targeted later | These files should stay untouched for Standard 3 test-mode discovery. |
| Corpus manifest staged paths | `data/corpus_manifest.json` | Lists staged reviewed question files under parsed corpora. | Indirectly used by build scripts | No, not for first test-mode pass | Manifest points to staged `reviewed_questions.json`, not the protected Standard 3 bank. |
| Reviewed-bank builder | `scripts/build_reviewed_question_bank.py` | Builds `data/active_scope_reviewed_questions.json` and imports staged reviewed support. | Build-time, not live app route | Candidate for future offline transformation design only | Future Standard 3 adapter may borrow validation patterns, but should not rebuild active bank by default. |
| Streamlit UI | `streamlit_app.py` | Supported live quiz UI/runtime entry point. | Yes | Blocked unless separately authorized | No UI change is needed for discovery. A future controlled mode may avoid UI first. |
| Runtime reviewed-bank tests | `tests/test_active_scope_reviewed_questions.py` | Tests active reviewed bank validity, scope membership, and runtime preference. | Yes | Add separate tests in future task | Current tests validate active-scope bank behavior, not protected Standard 3 records. |
| Runtime quality tests | `tests/test_runtime_quality_scope.py`, `tests/test_question_types_contract.py`, `tests/test_runtime_question_flow.py` | Cover generation and runtime quality paths. | Yes | Add targeted test-mode regressions in future task | Future activation should prove default runtime is unchanged when test mode is off. |

Discovery finding: no Python runtime loader reference to `standard_3_mvp_reviewed_bank`, `data/standards/zekelman/reviewed_bank`, or the protected Standard 3 reviewed-bank path was found. The standards-side protected bank is currently ignored by runtime.

## 5. Schema Comparison

Protected Standard 3 reviewed-bank record fields include:

- `reviewed_bank_record_id`
- `source_candidate_record_id`
- `source_preview_item_id`
- `standard`
- `standard_id`
- `source_scope`
- `skill_lane`
- `question_type_family`
- `approved_hebrew_input`
- `approved_input_reference`
- `final_prompt`
- `expected_answer`
- `answer_key_rationale`
- `protected_deferred_content_check`
- `review_status`
- `runtime_status`
- `student_facing_status`
- `promotion_source`
- `reviewer_notes`

Active runtime reviewed-question records currently include fields such as:

- `reviewed_id`
- `question_text`
- `question`
- `choices`
- `correct_answer`
- `skill`
- `question_type`
- `mode`
- `standard`
- `micro_standard`
- `difficulty`
- `word`
- `selected_word`
- `source`
- `pasuk`
- `pasuk_id`
- `pasuk_ref`
- `review_family`
- `analysis_source`
- `alias_skills`

Compatibility finding:

- The protected Standard 3 bank is not runtime-compatible as-is.
- The protected bank is standards/review oriented, not app-question oriented.
- It lacks `choices`, `correct_answer`, `skill`, runtime `question_type`, `mode`, `micro_standard`, `difficulty`, `word`, `selected_word`, `pasuk`, `pasuk_id`, `pasuk_ref`, `reviewed_id`, `review_family`, and `alias_skills`.
- It uses `final_prompt` and `expected_answer`, while runtime expects `question`/`question_text` and `correct_answer`.
- It includes conservative safety/status fields that runtime does not currently use as gating fields for active reviewed questions.

Transformation needed before any activation:

- Map `final_prompt` to `question` and `question_text`.
- Map `expected_answer` to `correct_answer`.
- Map `approved_hebrew_input` to `word` and `selected_word`.
- Create a stable `reviewed_id`.
- Map each Standard 3 lane to runtime `skill`, `question_type`, `review_family`, `standard`, `micro_standard`, and `difficulty`.
- Add four valid answer choices for every item, with the correct answer included exactly once.
- Decide whether a test-mode record needs `pasuk`, `pasuk_id`, and `pasuk_ref`; if so, choose a safe test-mode source rather than silently binding to active Chumash scope.
- Preserve `runtime_status: not_runtime_active` unless a future activation task defines a separate test-mode eligibility flag.

## 6. Controlled Test-Mode Options

### Option A: Adapter / Transformation Layer

What it would change:

- Add a separate adapter that reads the protected Standard 3 bank and transforms records into runtime-compatible question objects only when a test-mode flag is enabled.

Benefits:

- Keeps `data/active_scope_reviewed_questions.json` untouched.
- Keeps standards-side provenance intact.
- Makes schema conversion explicit and testable.

Risks:

- Requires careful skill/question-type mapping.
- Requires safe distractor/choice policy before runtime payload validation can pass.
- May need a non-standard pasuk/source binding strategy because these are standards drills, not active-scope pasuk records.

Rollback method:

- Disable the test-mode flag or remove the adapter registration.

Tests needed:

- Adapter parses exactly 10 records.
- Adapter rejects extra records.
- Adapter produces runtime-compatible records.
- Default runtime remains unchanged when test mode is off.

### Option B: Separate Staged Reviewed-Question File

What it would change:

- Create a separate Standard 3 staged reviewed-question file in runtime-compatible schema, still disconnected from default runtime.

Benefits:

- Matches existing staged reviewed-support pattern more closely.
- Could reuse some reviewed-bank build/validation tooling.

Risks:

- Easier to confuse with corpus staged files under `data/staged/*/reviewed_questions.json`.
- Could accidentally look like corpus promotion content rather than standards test-mode content.
- Still requires choices, runtime skill IDs, and source binding.

Rollback method:

- Leave the staged file unreferenced, or remove the future test-mode reference.

Tests needed:

- Staged Standard 3 file is not referenced by default runtime.
- Active reviewed bank remains unchanged.
- Future loader reads only the staged Standard 3 file when test mode is explicit.

### Option C: Feature-Flag Loader for Standards-Side Protected Bank

What it would change:

- Add a feature-flagged loader that reads `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json` directly only when an explicit test flag is enabled.

Benefits:

- Keeps the reviewed bank in the standards folder.
- Strong provenance and minimal data duplication.
- Makes it clear this is not active Chumash corpus content.

Risks:

- Runtime still needs an adapter because the schema differs from active reviewed questions.
- Direct loading from standards paths may blur boundaries unless naming and tests are strict.

Rollback method:

- Disable the feature flag.

Tests needed:

- Feature flag off: no Standard 3 protected records are reachable.
- Feature flag on: exactly 10 protected records are reachable.
- Records remain `not_runtime_active` unless a separate test-mode eligibility mechanism is approved.

## 7. Recommended Future Path

Recommended path: Option A, an adapter/transformation layer behind an explicit teacher/admin-only test-mode flag.

This is the safest next implementation direction because it avoids touching `data/active_scope_reviewed_questions.json`, avoids changing staged reviewed-question files, keeps default runtime unchanged, and forces the schema mismatch to be solved openly.

Use conservative rules:

- Do not activate default runtime.
- Prefer teacher/admin-only test mode.
- Keep `data/active_scope_reviewed_questions.json` untouched until a later explicit activation decision.
- Keep student-facing use blocked.
- Keep the protected Standard 3 bank as the source of truth for the 10 records.

## 8. Required Tests Before Any Future Activation

Before any future activation task, add tests covering:

- protected bank parses successfully
- transformation produces runtime-compatible records
- only the 10 Standard 3 records are loaded
- excluded content remains absent
- default runtime remains unchanged when test mode is off
- active scope is untouched
- staged reviewed questions are untouched unless explicitly targeted
- UI remains unchanged unless separately authorized
- feature/test flag is required
- no test-mode records enter student progress/mastery tracking unless separately authorized
- generated records pass `validate_question_payload(...)` or a future equivalent test-mode validator

## 9. Still Blocked

The following remain blocked:

- runtime activation
- student-facing use
- app routing changes
- active-scope update
- staged reviewed-bank update
- broader question generation
- expansion beyond the 10 records
- expansion beyond locked lanes and approved inputs
- 3.05 Pronoun Referent Tracking
- expanded 3.02 shoresh list beyond שמר
- 3.04
- 3.08
- 3.10
- weak-letter roots
- altered-root recognition
- advanced contextual shoresh translation
- full verb parsing
- two functions of את
- ו ההיפוך
- ה השאלה
- ה המגמה
- בנינים
- passive forms
- ציווי
- מקור
- שם הפועל
- weak-root verb analysis
- cross-pasuk pronoun referents
- ambiguous pronoun referents
- context-stripped word-order questions
- compact סמיכות questions

## 10. Final Status Summary

- Runtime activation: blocked
- Active scope: untouched
- Staged reviewed questions: untouched
- Student-facing use: blocked
- Current artifact: discovery report only
- Recommended next step: controlled test-mode implementation plan, not activation

## 11. Validation Results

Required validation commands:

- `python scripts/validate_source_texts.py`: passed
- `python scripts/validate_curriculum_extraction.py`: passed
- `python scripts/validate_standards_data.py`: passed
- `python -m pytest tests/test_standards_data_validation.py`: passed, 9 tests passed

Protected reviewed-bank parse check:

- `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json`: parsed successfully
- record count: 10
- runtime statuses: `not_runtime_active`
- student-facing statuses: `not_student_facing`
