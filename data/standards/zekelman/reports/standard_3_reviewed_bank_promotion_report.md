# Zekelman Standard 3 Reviewed-Bank Promotion Report

## 1. Files Created

- `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json`
- `data/standards/zekelman/reports/standard_3_reviewed_bank_promotion_report.md`

## 2. Files Modified

- None.

The existing runtime reviewed-bank file `data/active_scope_reviewed_questions.json` was intentionally not modified. Existing staged reviewed-support files under `data/staged/*/reviewed_questions.json` were intentionally not modified.

## 3. Records Promoted

The following 10 protected candidate records were promoted into a protected, non-runtime Zekelman standards reviewed-bank artifact:

- `STD3-MVP-RBC-001` -> `STD3-MVP-RB-001`
- `STD3-MVP-RBC-002` -> `STD3-MVP-RB-002`
- `STD3-MVP-RBC-003` -> `STD3-MVP-RB-003`
- `STD3-MVP-RBC-004` -> `STD3-MVP-RB-004`
- `STD3-MVP-RBC-005` -> `STD3-MVP-RB-005`
- `STD3-MVP-RBC-006` -> `STD3-MVP-RB-006`
- `STD3-MVP-RBC-007` -> `STD3-MVP-RB-007`
- `STD3-MVP-RBC-008` -> `STD3-MVP-RB-008`
- `STD3-MVP-RBC-009` -> `STD3-MVP-RB-009`
- `STD3-MVP-RBC-010` -> `STD3-MVP-RB-010`

No additional records were added.

## 4. Exact Status Values Used

Every promoted protected record uses:

- `review_status`: `reviewed_for_protected_bank`
- `runtime_status`: `not_runtime_active`
- `student_facing_status`: `not_student_facing`
- `promotion_source`: `standard_3_mvp_reviewed_bank_candidate_records`
- `standard`: `3`
- `source_scope`: `zekelman_standard_3_mvp`

## 5. Runtime Remains Blocked

Runtime remains blocked.

This task did not modify runtime files, runtime routing, app code, Streamlit code, quiz runtime behavior, active templates, or production app files. The promoted records live only in:

- `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json`

That file is a protected standards reviewed-bank artifact and is marked `not_runtime_active`.

## 6. Student-Facing Use Remains Blocked

Student-facing use remains blocked.

Every promoted protected record uses `student_facing_status`: `not_student_facing`.

## 7. No Extra Records Added

Only the 10 records listed in the promotion scope were included. The protected reviewed-bank JSON has `record_count`: `10`.

## 8. Excluded Content Confirmation

No excluded content was included.

The promoted protected reviewed-bank records do not include:

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

## 9. Validation Results

JSON integrity check for `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json` passed:

- valid JSON: yes
- record count: 10
- runtime statuses: `not_runtime_active`
- review statuses: `reviewed_for_protected_bank`
- student-facing statuses: `not_student_facing`
- promotion sources: `standard_3_mvp_reviewed_bank_candidate_records`
- standards: `3`
- source scopes: `zekelman_standard_3_mvp`

Required validation commands:

- `python scripts/validate_source_texts.py`: passed
- `python scripts/validate_curriculum_extraction.py`: passed
- `python scripts/validate_standards_data.py`: passed
- `python -m pytest tests/test_standards_data_validation.py`: passed, 9 tests passed

## 10. Remaining Blockers Before Runtime Activation

Runtime activation remains blocked until a separate future task explicitly authorizes it.

Remaining blockers:

- active runtime reviewed-bank integration is not authorized
- student-facing use is not authorized
- app routing is not authorized to consume this protected standards bank
- question-ready status is not authorized
- production question generation is not authorized
- broader Standard 3 expansion is not authorized
- excluded lanes and content remain blocked
- any future runtime integration needs its own safety gate, validator coverage, and explicit approval
