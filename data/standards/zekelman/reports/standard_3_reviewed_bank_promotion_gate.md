# Zekelman Standard 3 Reviewed-Bank Promotion Gate

## 1. Purpose

This gate evaluates whether the 10 Zekelman Standard 3 protected reviewed-bank candidate records are ready for a future reviewed-bank promotion task.

This gate does not promote anything. It does not create reviewed-bank records. It does not activate runtime behavior. It does not create student-facing content.

The purpose is limited to deciding whether a future, separate promotion task may create or update reviewed-bank files from these protected candidate records while preserving the runtime and student-facing blocks.

## 2. Hard Boundaries

- Runtime: blocked
- Reviewed-bank promotion: blocked until separate future promotion prompt
- Student-facing use: blocked
- Question-ready status: blocked
- Current artifact: reviewed-bank promotion gate only

This report does not authorize runtime activation, production use, student-facing use, reviewed-bank promotion, broader question generation, or any change to runtime-ready/question-ready status.

## 3. Candidate Records Evaluated

| Candidate Record ID | Source Preview Item ID | Standard ID | Skill Lane | Approved Input | Teacher Review Status | Reviewed-Bank Candidate Status | Runtime Status | Student-Facing Status | Promotion Eligibility | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `STD3-MVP-RBC-001` | `STD3-MVP-PREVIEW-001` | `3.01` | Nouns / שמות עצם | בן | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Clear noun translation item. בן -> son / a son. |
| `STD3-MVP-RBC-002` | `STD3-MVP-PREVIEW-002` | `3.01` | Nouns / שמות עצם | מלך | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Clear English-to-Hebrew noun recall item. king / a king -> מלך. |
| `STD3-MVP-RBC-003` | `STD3-MVP-PREVIEW-003` | `3.02` | Simple Shorashim / שורשים | שמר | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Revised per teacher review. Final prompt asks which shoresh means guard / keep. |
| `STD3-MVP-RBC-004` | `STD3-MVP-PREVIEW-004` | `3.02` | Simple Shorashim / שורשים | שמר | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Clear shoresh-to-basic-meaning item. שמר -> guard / keep. |
| `STD3-MVP-RBC-005` | `STD3-MVP-PREVIEW-005` | `3.05` | Pronominal Suffix Decoding | ספרי | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Clear pronominal suffix decoding item. ספרי -> my book. |
| `STD3-MVP-RBC-006` | `STD3-MVP-PREVIEW-006` | `3.05` | Pronominal Suffix Decoding | ספרו | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Clear pronominal suffix decoding item. ספרו -> his book. |
| `STD3-MVP-RBC-007` | `STD3-MVP-PREVIEW-007` | `3.06` | Visible Prefixes / Articles | הבן | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Clear visible article item. הבן contains ה / ה הידיעה. |
| `STD3-MVP-RBC-008` | `STD3-MVP-PREVIEW-008` | `3.06` | Visible Prefixes / Articles | בבית | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Clear visible prefix item. בבית begins with ב. |
| `STD3-MVP-RBC-009` | `STD3-MVP-PREVIEW-009` | `3.07` | Foundational Verb Clues | שמרתי | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Revised per teacher review. Final prompt asks what the ending תי helps show. |
| `STD3-MVP-RBC-010` | `STD3-MVP-PREVIEW-010` | `3.07` | Foundational Verb Clues | אשמור | `teacher_reviewed_for_protected_preview` | `candidate_only_not_promoted` | `not_runtime_ready` | `not_student_facing` | Eligible for a future promotion task only | Acceptable foundational future-tense clue item. אשמור reviews a future-tense clue. |

## 4. Promotion Criteria

Before any future promotion into the reviewed-bank structure, each item must satisfy all of the following:

- candidate record exists
- source preview item exists
- teacher review completed
- final prompt and expected answer are present
- answer-key rationale is present
- approved input reference is present
- protected/deferred-content check is present
- source verification status is present
- no blocked content is used
- reviewed-bank schema/target location is identified
- promotion remains non-runtime unless separately authorized

The current candidate records satisfy the planning evidence requirements for a future promotion task. They do not identify or update the final production reviewed-bank target location in this task, and they do not become runtime-active.

## 5. Gate Finding

The 10 Standard 3 protected candidate records are eligible for a future reviewed-bank promotion task, but they are not promoted by this gate. A separate future promotion prompt must create or update reviewed-bank files, and runtime activation must remain blocked unless separately authorized.

## 6. Still Blocked

The following remain blocked:

- runtime activation
- student-facing use
- broader question generation
- expansion beyond the 10 candidates
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

## 7. Recommended Next Step

Create a separate reviewed-bank promotion prompt that promotes only these 10 protected candidate records into the reviewed-bank structure, while keeping runtime and student-facing use blocked.

That future promotion task must:

- use only `STD3-MVP-RBC-001` through `STD3-MVP-RBC-010`
- identify the exact reviewed-bank target schema and target path before writing
- preserve non-runtime and non-student-facing status unless a separate future runtime authorization exists
- avoid expanding beyond the locked lanes, approved inputs, and teacher-reviewed prompts
- keep all excluded content blocked
