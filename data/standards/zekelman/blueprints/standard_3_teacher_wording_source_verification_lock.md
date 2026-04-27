# Zekelman Standard 3 Teacher Wording and Source Verification Lock File

## 1. Purpose

This document defines the missing locks required before any protected preview generation for Zekelman Standard 3. It follows the protected preview readiness gate, which found that all Standard 3 lanes remain blocked for protected preview generation.

This is review-only. This is not runtime-ready. This is not question-ready. This does not generate questions. This does not authorize preview generation by itself. This records what must be locked before a future prompt may generate a tiny protected preview packet.

## 2. Hard Boundaries

- Runtime status: `not_runtime_ready`
- Question-generation status: `not_question_ready`
- Reviewed-bank status: `not_approved_for_reviewed_bank`
- Student-facing status: `not_student_facing`
- Promotion status: `blocked_pending_future_gate`
- Preview generation status: `blocked_until_locks_completed_and_future_prompt_authorizes`

This lock file does not authorize:

- generated questions
- sample questions
- answer choices
- answer keys
- active templates
- runtime activation
- UI changes
- reviewed-bank promotion
- production-data changes
- student-facing use

## 3. Teacher Review Findings Recorded

Reviewer: Yossi Bassman

Reviewed file: `data/standards/zekelman/blueprints/standard_3_mvp_candidate_input_lists.md`

Recorded for lock-file purposes:

- These findings are for future protected-preview planning only.
- These findings do not authorize runtime activation, reviewed-bank promotion, student-facing use, or general question generation.
- Teacher/project lead visually reviewed and approved the listed candidate input rows in `data/standards/zekelman/blueprints/standard_3_mvp_candidate_input_source_verification_sheet.md`.
- Approved item-level decisions were recorded as `approve_input` for `STD3-01-NOUN-001`, `STD3-01-NOUN-002`, `STD3-01-NOUN-003`, `STD3-02-SHORESH-001`, `STD3-05-SUFFIX-001`, `STD3-05-SUFFIX-002`, `STD3-06-PREFIX-001`, `STD3-06-PREFIX-002`, `STD3-06-PREFIX-003`, `STD3-06-PREFIX-004`, `STD3-07-VERB-001`, `STD3-07-VERB-002`, `STD3-07-VERB-003`, and `STD3-07-VERB-004`.
- 3.05 pronoun referent tracking remains `not_approved_yet` for protected preview and needs teacher-selected local, clear referent examples.
- The expanded 3.02 shoresh list beyond the one source-backed `שמר` candidate remains not approved.
- Any item that depends on excluded content remains not approved.
- Any unlisted input item or future input without explicit teacher approval remains not approved.
- 3.06 visible prefixes/articles must be confirmed as visible/simple forms only before approval.
- 3.07 foundational verb clues must be confirmed as basic tense/person/form clues only, not advanced parsing.

The lock status below is updated only for lanes whose approved inputs, boundaries, excluded content, question-type map, answer-key review rules, packet format, and preview-size limit are complete. A locked lane only authorizes eligibility for a future separate protected-preview prompt. It does not authorize question generation in this task.

## 4. Lock Criteria

Every lane must satisfy all of these lock criteria before it can be included in a future protected preview:

1. Teacher wording boundary is explicit.
2. Source/PDF verification is complete for the exact vocabulary or examples.
3. Approved vocabulary/example list exists.
4. Protected/deferred content is explicitly excluded.
5. Allowed question-type family is already mapped.
6. Answer-key review rules are defined.
7. Teacher-review packet format is defined.
8. Preview-size limit is defined.
9. Runtime and reviewed-bank promotion remain blocked.

If any criterion is missing, the lane remains blocked.

## 5. Lane-by-Lane Lock Table

| Skill Lane | Standard ID | Current Preview Status | Teacher Wording Boundary Needed | Source/PDF Verification Needed | Approved Inputs Needed | Explicit Exclusions | Lock Status | What Would Unlock This Lane | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.01 Nouns / שמות עצם | `3.01` | `blocked_until_explicit_future_prompt` | Boundary limits preview work to taught nouns from approved input rows, controlled translation, and no uncontrolled multiple-meaning work. | Complete for approved rows `STD3-01-NOUN-001`, `STD3-01-NOUN-002`, and `STD3-01-NOUN-003` based on teacher/project-lead visual review. | Approved noun inputs: בן, מלך, איש. | Untaught vocabulary, broad contextual inference, uncontrolled multiple meanings, non-source-verified vocabulary, unlisted noun inputs. | `locked_for_future_protected_preview` | A future separate protected-preview prompt may use only the approved noun inputs and preserved boundaries. | Locked only for future protected-preview planning. This does not authorize question generation now. |
| 3.02 Simple Shorashim / שורשים | `3.02` | `blocked_until_explicit_future_prompt` | Boundary limits preview work to simple shoresh identification and basic meaning only. | Complete for approved row `STD3-02-SHORESH-001` based on teacher/project-lead visual review. | Approved simple shoresh input: שמר only. | Expanded shoresh list beyond שמר, weak-letter roots, altered-root recognition, advanced contextual shoresh translation, full verb parsing, level-advanced root transformations. | `locked_for_future_protected_preview` | A future separate protected-preview prompt may use only `שמר` for simple shoresh recognition and basic meaning. | Locked only for the one approved source-backed root. Expanded 3.02 shoresh list remains blocked. |
| 3.05 Pronoun Referent Tracking | `3.05` | `blocked` | Boundary must limit preview work to local, clear referents only. | Verify exact pronoun examples, local referent clarity, and exclusion of cross-pasuk referents. | Teacher-selected and approved local pronoun/referent examples. | Cross-pasuk referents, ambiguous referents, context-heavy interpretation, broad pronoun interpretation without teacher wording boundaries. | `blocked_missing_required_locks` | Teacher selects local, clear referent examples and explicitly approves them after source/PDF verification. | Teacher review decision: `not_approved_yet`. Needs teacher-selected local, clear referent examples. Do not include in preview yet. |
| 3.05 Pronominal Suffix Decoding | `3.05` | `blocked_until_explicit_future_prompt` | Boundary limits preview work to approved suffix examples and basic possessive suffix meaning. | Complete for approved rows `STD3-05-SUFFIX-001` and `STD3-05-SUFFIX-002` based on teacher/project-lead visual review. | Approved suffix inputs: ספרי, ספרו. | Pronoun referent tracking, ambiguous suffix interpretation, context-heavy interpretation, verb-linked clue systems unless separately approved, bundling with referent tracking. | `locked_for_future_protected_preview` | A future separate protected-preview prompt may use only the approved suffix inputs and preserved boundaries. | Locked only for suffix decoding using approved examples. Pronoun referent tracking remains blocked. |
| 3.06 Visible Prefixes / Articles | `3.06` | `blocked_until_explicit_future_prompt` | Boundary limits preview work to visible/simple prefix or article recognition in approved examples. | Complete for approved rows `STD3-06-PREFIX-001`, `STD3-06-PREFIX-002`, `STD3-06-PREFIX-003`, and `STD3-06-PREFIX-004` based on teacher/project-lead visual review. | Approved prefix/article inputs: הבן, ואיש, למלך, בבית. | Two functions of את, ו ההיפוך unless separately approved, ה השאלה unless separately approved, ה המגמה unless separately approved, context-heavy interpretation, unverified nikud-sensitive interpretation, unlisted prefix/article inputs. | `locked_for_future_protected_preview` | A future separate protected-preview prompt may use only the approved visible/simple prefix and article inputs. | Locked only for the approved visible/simple forms. This does not support ו ההיפוך, את, ה השאלה, or ה המגמה. |
| 3.07 Foundational Verb Clues | `3.07` | `blocked_until_explicit_future_prompt` | Boundary limits preview work to foundational tense/person/form clues in approved examples. | Complete for approved rows `STD3-07-VERB-001`, `STD3-07-VERB-002`, `STD3-07-VERB-003`, and `STD3-07-VERB-004` based on teacher/project-lead visual review. | Approved foundational verb inputs: שמרתי, שמרו, אשמור, תשמרי. | Full parsing, בנינים, passive forms, ציווי, מקור, שם הפועל, weak-root verb analysis, advanced translation precision, unlisted verb inputs. | `locked_for_future_protected_preview` | A future separate protected-preview prompt may use only the approved foundational verb-clue inputs and preserved boundaries. | Locked only for basic tense/person/form clue recognition, not advanced parsing. |
| 3.04 Noun/Adjective Features | `3.04` | `blocked` | Later/cautious boundary must be separately approved before preview use. | Verify Hebrew examples, nekudos, level placement, and source/PDF examples. | Approved noun/adjective feature examples. | Over-bundling with סמיכות, irregular forms unless teacher-approved, adjective agreement unless approved, context-heavy phrase interpretation. | `blocked_missing_required_locks` | A future teacher review approves a narrow boundary, examples, source verification, and preview eligibility. | Not part of the first MVP preview scope. |
| 3.04 סמיכות | `3.04` | `blocked` | Protected boundary must be separately approved before preview use. | Verify סמיכות examples, forms, nekudos, and level placement against source PDFs. | Approved סמיכות examples. | Context-heavy phrase translation, compact questions that remove needed phrase context, unverified examples, broad grouping support. | `blocked_missing_required_locks` | A future teacher review approves a narrow סמיכות boundary and source-verified examples. | Compact סמיכות remains protected. |
| 3.08 Grouping and Word Order | `3.08` | `blocked` | Protected/context-sensitive boundary must be separately approved before preview use. | Verify Loshon page references and examples visually in the PDFs and confirm full-context boundaries. | Approved full-context grouping or word-order examples. | Compact isolated questions, context-stripped word-order questions, broad independent full-pasuk grouping, overclaiming source support. | `blocked_missing_required_locks` | Future source/PDF verification and teacher approval create a narrow full-context preview boundary. | Not suitable for compact preview yet. |
| 3.10 Nikud | `3.10` | `blocked` | Deferred; no MVP preview wording boundary should be created now. | Direct source review would be required in a later phase. | None for MVP. | All MVP diagnostic use, question generation, nikud-sensitive distinctions, OCR-sensitive charts. | `deferred_not_eligible_for_mvp_preview` | A later phase explicitly reopens 3.10 with direct source review and teacher decision. | Not eligible for MVP preview. |

## 6. Required Teacher Wording Boundaries

### 3.01 Nouns / שמות עצם

Teacher wording boundary required:
“Future diagnostic preview may assess only taught nouns from an approved vocabulary list. Questions may ask recognition or controlled translation of those nouns. Multiple-meaning work is allowed only when the approved list explicitly includes the alternate meanings.”

Still not allowed:

- untaught vocabulary
- broad contextual inference
- uncontrolled multiple meanings
- non-source-verified vocabulary

### 3.02 Simple Shorashim / שורשים

Teacher wording boundary required:
“Future diagnostic preview may assess only simple shoresh identification and basic meaning for teacher-approved roots. It may not require weak-letter recognition, altered-root reconstruction, advanced contextual root translation, or full verb parsing.”

Still not allowed:

- weak-letter roots
- altered-root recognition
- advanced contextual shoresh translation
- full verb parsing
- level-advanced root transformations

### 3.05 Pronoun Referent Tracking

Teacher wording boundary required:
“Future diagnostic preview may assess only local, clear pronoun referents where the antecedent is nearby and teacher-approved. It may not require cross-pasuk tracking or interpretation of ambiguous referents.”

Still not allowed:

- cross-pasuk referent tracking
- ambiguous referents
- context-heavy interpretation
- broad pronoun interpretation without teacher wording boundaries

### 3.05 Pronominal Suffix Decoding

Teacher wording boundary required:
“Future diagnostic preview may assess only teacher-approved suffix examples and basic person/gender/number decoding. It may not bundle suffix decoding with pronoun referent tracking or verb-linked clue systems unless separately approved.”

Still not allowed:

- ambiguous suffixes
- context-heavy interpretation
- verb-linked clue systems unless separately approved
- bundling suffix decoding with referent tracking

### 3.06 Visible Prefixes / Articles

Teacher wording boundary required:
“Future diagnostic preview may assess only visible prefixes and ה הידיעה where nikud-sensitive interpretation is not required. It may not assess את, ו ההיפוך, ה השאלה, ה המגמה, or context-heavy prefix/article interpretation unless those subareas are separately approved.”

Still not allowed:

- two functions of את
- ו ההיפוך unless separately approved
- ה השאלה unless separately approved
- ה המגמה unless separately approved
- context-heavy interpretation
- nikud-sensitive distinctions not yet verified

### 3.07 Foundational Verb Clues

Teacher wording boundary required:
“Future diagnostic preview may assess only foundational tense/person/form clues on teacher-approved examples. It may not require full verb parsing, advanced translation precision, weak-root analysis, בנינים, passive forms, ציווי, מקור, or שם הפועל.”

Still not allowed:

- בנינים
- passive forms
- ציווי
- מקור
- שם הפועל
- weak-root verb analysis
- full parsing of complex verb forms
- advanced translation precision

### 3.04 Noun/Adjective Features

Teacher wording boundary required:
Later/cautious unless a separate teacher boundary is approved.

Still not allowed:

- irregular forms unless teacher-approved
- adjective agreement unless teacher-approved
- context-heavy phrase interpretation
- over-bundling with סמיכות

### 3.04 סמיכות

Teacher wording boundary required:
Protected unless a narrow teacher-approved boundary is added.

Still not allowed:

- compact סמיכות questions without teacher-approved boundary
- context-heavy phrase translation
- unverified examples
- broad grouping support

### 3.08 Grouping and Word Order

Teacher wording boundary required:
Protected/context-sensitive and not suitable for compact preview yet.

Still not allowed:

- compact isolated questions
- context-stripped word-order questions
- broad independent full-pasuk grouping
- questions that depend on broad interpretation

### 3.10 Nikud

Teacher wording boundary required:
Deferred and not eligible for MVP preview.

Still not allowed:

- all MVP diagnostic use
- question generation
- nikud-sensitive distinctions
- OCR-sensitive charts

## 7. Source/PDF Verification Requirements

Before future preview generation, source verification must prove the following:

For `3.01`:

- approved noun list source
- exact Hebrew spelling
- accepted English meanings
- multiple-meaning notes, if used

For `3.02`:

- approved simple shoresh list source
- exact Hebrew root spelling
- accepted basic meaning
- confirmation that weak/altered roots are excluded

For `3.05`:

- exact pronoun/suffix examples
- local referent clarity
- person/gender/number form verification
- confirmation that cross-pasuk referents are excluded

For `3.06`:

- exact prefix/article examples
- confirmation that forms are visible and not dependent on unverified nikud-sensitive interpretation
- confirmation that את and ו ההיפוך are excluded unless separately approved

For `3.07`:

- exact verb examples
- basic tense/person/form clue verification
- confirmation that advanced parsing and weak-root analysis are excluded

## 8. Approved Inputs Needed Before Preview

Required future inputs:

- approved vocabulary list for 3.01 nouns: complete for approved inputs בן, מלך, איש only
- approved simple shoresh list for 3.02: complete for approved input שמר only; expanded list beyond `שמר` remains not approved
- approved pronoun examples for 3.05 referent tracking: missing; lane is `not_approved_yet` for protected preview
- approved suffix examples for 3.05 suffix decoding: complete for approved inputs ספרי, ספרו only
- approved prefix/article examples for 3.06: complete for approved inputs הבן, ואיש, למלך, בבית only
- approved foundational verb examples for 3.07: complete for approved inputs שמרתי, שמרו, אשמור, תשמרי only
- excluded-content list: approved as protection boundary in the teacher input approval packet
- answer-key review rules: approved for future protected preview only in the teacher input approval packet
- teacher-review packet format: approved for future protected preview only in the teacher input approval packet
- preview-size limit: approved for future protected preview only in the teacher input approval packet

Do not create questions from these approved inputs in this task. These locks only make the listed rows eligible for a future separate protected-preview prompt.

## 9. Explicit Excluded Content Lock

The following content is excluded from any future protected preview unless a later review explicitly changes the boundary:

- 3.10 ניקוד
- weak-letter roots
- altered-root recognition
- advanced contextual shoresh translation
- full verb parsing
- two functions of את
- ו ההיפוך unless separately approved
- ה השאלה unless separately approved
- ה המגמה unless separately approved
- בנינים
- passive forms
- ציווי
- מקור
- שם הפועל
- weak-root verb analysis
- cross-pasuk pronoun referents
- ambiguous pronoun referents
- context-stripped word-order questions
- compact סמיכות questions without teacher-approved boundary
- any OCR-sensitive Hebrew not manually verified

## 10. Answer-Key Review Rules Needed

Before preview generation, answer-key rules must state:

- every answer must be traceable to the approved input list or verified source example
- every distractor must be plausible but not misleading
- no answer may depend on deferred content
- answer key must explain the specific skill being assessed
- answer key must flag if teacher review is required
- answer key may not be treated as reviewed-bank approval

These rules are required for a future protected preview packet only. They do not authorize answer-key creation now.

## 11. Teacher-Review Packet Format Needed

Each future preview item must include:

- Standard ID
- skill lane
- question-type family
- exact Hebrew source/example
- source/PDF reference or approved-list reference
- expected answer
- why this tests the stated skill
- protected/deferred content check
- teacher reviewer notes field
- reviewer decision field

Do not create preview items now.

## 12. Preview Size Limit

Maximum future protected preview size:

- no more than 3 questions per unlocked MVP lane
- no more than 10 questions total
- only lanes marked `locked_for_future_protected_preview` may be included
- preview must remain non-runtime and teacher-review only

Only lanes marked `locked_for_future_protected_preview` in this file may be considered by a future separate protected-preview prompt.

## 13. Final Lock Status Summary

The following Standard 3 lanes are locked only for future protected-preview planning, pending a separate explicit protected-preview prompt.

Locked lanes:

- `3.01` Nouns / שמות עצם: locked for approved inputs בן, מלך, איש only
- `3.02` Simple Shorashim / שורשים: locked for approved input שמר only
- `3.05` Pronominal Suffix Decoding: locked for approved inputs ספרי, ספרו only
- `3.06` Visible Prefixes / Articles: locked for approved inputs הבן, ואיש, למלך, בבית only
- `3.07` Foundational Verb Clues: locked for approved inputs שמרתי, שמרו, אשמור, תשמרי only

Blocked lanes:

- `3.05` Pronoun Referent Tracking
- `3.04` Noun/Adjective Features
- `3.04` סמיכות
- `3.08` Grouping and Word Order
- expanded `3.02` shoresh list beyond שמר
- any item depending on excluded content
- any unlisted input item
- any future input without explicit teacher approval

Deferred lanes:

- `3.10` Nikud

Remaining blockers before protected preview generation:

- approved pronoun examples
- protected-preview generation is still blocked until a separate future prompt explicitly authorizes it
- no answer choices, answer keys, generated questions, or sample questions may be created from this lock file
- runtime activation, reviewed-bank promotion, and student-facing use remain blocked
- all unlisted inputs remain blocked until explicitly reviewed and approved

## 14. Recommended Next Step

The next step is a separate protected-preview generation prompt limited only to lanes marked `locked_for_future_protected_preview` and only to the approved input rows listed in this lock file.

Do not proceed to general question generation, runtime activation, reviewed-bank promotion, or student-facing use.
