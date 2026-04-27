# Zekelman Standard 3 Reviewed-Bank Planning Gate

## 1. Purpose

This gate evaluates whether the 10 teacher-reviewed Zekelman Standard 3 protected preview items are ready to be transformed into future reviewed-bank candidate records.

This gate does not promote anything. It does not create reviewed-bank records. It does not activate runtime behavior. It does not create student-facing content.

The purpose is limited to planning the next protected step: whether a future task may create reviewed-bank candidate records in a separate protected candidate area.

## 2. Hard Boundaries

- Runtime: blocked
- Reviewed bank: blocked
- Student-facing use: blocked
- Question-ready status: blocked
- Current artifact: reviewed-bank planning gate only

This report does not authorize runtime activation, reviewed-bank promotion, production use, student-facing use, general question generation, or any change to question-ready/runtime-ready status.

## 3. Source Artifacts Reviewed

The current branch is `feature/standard-3-reviewed-bank-planning-gate`. The Standard 3 blueprint and protected-preview artifacts referenced by this gate are not present in this branch worktree. They were reviewed from the local git ref `feature/standard-3-diagnostic-blueprint-v0` at commit `a49c885`.

Artifacts reviewed from `feature/standard-3-diagnostic-blueprint-v0`:

- `data/standards/zekelman/preview/standard_3_mvp_protected_preview_packet.md`
- `data/standards/zekelman/reports/standard_3_mvp_protected_preview_review_completion_report.md`
- `data/standards/zekelman/blueprints/standard_3_teacher_wording_source_verification_lock.md`
- `data/standards/zekelman/blueprints/standard_3_mvp_candidate_input_lists.md`
- `data/standards/zekelman/blueprints/standard_3_skill_to_question_type_map.md`
- `data/standards/zekelman/blueprints/standard_3_mvp_teacher_input_approval_packet.md`
- `data/standards/zekelman/blueprints/standard_3_mvp_diagnostic_blueprint.md`

Current-branch planning context reviewed:

- `PLANS.md`

This source note is important: this report is a planning gate based on the protected-preview evidence from the diagnostic-blueprint branch. It should not be read as proof that the current branch already contains those blueprint or preview source files.

## 4. Candidate Preview Items Evaluated

The protected preview review completion report records 8 items approved as originally acceptable for later preview iteration, 2 items approved with revision, 0 rejected items, and 0 items needing more review after revisions.

| Preview Item ID | Standard ID | Skill lane | Approved input used | Teacher review status | Revision status | Eligible for reviewed-bank candidate planning? | Required reviewed-bank fields still needed | Notes |
|---|---|---|---|---|---|---|---|---|
| `STD3-MVP-PREVIEW-001` | `3.01` | Nouns / שמות עצם | בן | `approve_for_later_preview_iteration` | `not_revised` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Clear noun translation item: בן -> son / a son. |
| `STD3-MVP-PREVIEW-002` | `3.01` | Nouns / שמות עצם | מלך | `approve_for_later_preview_iteration` | `not_revised` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Clear English-to-Hebrew noun recall item: king / a king -> מלך. |
| `STD3-MVP-PREVIEW-003` | `3.02` | Simple Shorashim / שורשים | שמר | `approve_with_revision` | `revision_applied` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Revised prompt now asks: "Which shoresh means guard / keep?" Expected answer: שמר. |
| `STD3-MVP-PREVIEW-004` | `3.02` | Simple Shorashim / שורשים | שמר | `approve_for_later_preview_iteration` | `not_revised` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Clear shoresh-to-basic-meaning item: שמר -> guard / keep. |
| `STD3-MVP-PREVIEW-005` | `3.05` | Pronominal Suffix Decoding | ספרי | `approve_for_later_preview_iteration` | `not_revised` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Clear pronominal suffix decoding item: ספרי -> my book. |
| `STD3-MVP-PREVIEW-006` | `3.05` | Pronominal Suffix Decoding | ספרו | `approve_for_later_preview_iteration` | `not_revised` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Clear pronominal suffix decoding item: ספרו -> his book. |
| `STD3-MVP-PREVIEW-007` | `3.06` | Visible Prefixes / Articles | הבן | `approve_for_later_preview_iteration` | `not_revised` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Clear visible article item: הבן contains ה / ה הידיעה. |
| `STD3-MVP-PREVIEW-008` | `3.06` | Visible Prefixes / Articles | בבית | `approve_for_later_preview_iteration` | `not_revised` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Clear visible prefix item: בבית begins with ב. |
| `STD3-MVP-PREVIEW-009` | `3.07` | Foundational Verb Clues | שמרתי | `approve_with_revision` | `revision_applied` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Revised prompt now asks: "In שמרתי, what does the ending תי help show?" Expected answer: "It shows 'I' and past tense." |
| `STD3-MVP-PREVIEW-010` | `3.07` | Foundational Verb Clues | אשמור | `approve_for_later_preview_iteration` | `not_revised` | Yes, for a future candidate-creation task only | Reviewed candidate ID; protected candidate record schema; final promotion status; runtime status; source/PDF verification reference; reviewer notes field | Acceptable foundational future-tense clue item using אשמור. |

## 5. Reviewed-Bank Candidate Requirements

Before any future reviewed-bank candidate record can be created, each candidate must include:

- reviewed candidate ID
- source preview item ID
- standard ID
- skill lane
- question-type family
- approved Hebrew input
- approved input reference
- final prompt
- expected answer
- teacher-review status
- source/PDF verification reference
- protected/deferred-content check
- answer-key rationale
- reviewer notes
- promotion status
- runtime status

Any future candidate schema should also preserve the protected-review boundary: candidate records are not reviewed-bank approved, not runtime-ready, not question-ready, and not student-facing.

## 6. Promotion Readiness Finding

The 10 teacher-reviewed protected preview items are eligible for a future reviewed-bank candidate creation task, but they are not yet reviewed-bank records and are not runtime-ready.

A separate future prompt must create reviewed-bank candidate records in a protected candidate area only.

## 7. Continued Blocks

The following remain blocked:

- runtime activation
- student-facing use
- direct reviewed-bank promotion
- general question generation
- expanding beyond the 10 teacher-reviewed preview items
- expanding beyond locked lanes and approved inputs
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
- OCR-sensitive Hebrew not already approved

## 8. Recommended Next Step

Create a protected reviewed-bank candidate records file for only the 10 teacher-reviewed preview items.

That future task must:

- create candidate records only
- not mark them reviewed-bank approved
- not activate runtime
- not create student-facing content
- not modify production reviewed-bank files

Before that task starts, confirm whether the future work branch contains the required Standard 3 blueprint and protected-preview source artifacts or explicitly reads them from the diagnostic-blueprint branch. The candidate-creation task should not proceed from missing source artifacts.
