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

## 3. Lock Criteria

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

## 4. Lane-by-Lane Lock Table

| Skill Lane | Standard ID | Current Preview Status | Teacher Wording Boundary Needed | Source/PDF Verification Needed | Approved Inputs Needed | Explicit Exclusions | Lock Status | What Would Unlock This Lane | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.01 Nouns / שמות עצם | `3.01` | `blocked` | Boundary must limit preview work to taught nouns from an approved vocabulary list, controlled translation, and approved multiple-meaning cases only. | Verify approved noun-list source, exact Hebrew spelling, accepted English meanings, and any multiple-meaning notes. | Approved noun vocabulary list with source references. | Untaught vocabulary, broad contextual inference, uncontrolled multiple meanings, non-source-verified vocabulary. | `partially_locked_but_missing_required_inputs` | Teacher approves the wording boundary, noun list, source/PDF verification, excluded content, answer-key rules, packet format, and preview-size limit. | The lane concept is approved for planning, but inputs are not locked. |
| 3.02 Simple Shorashim / שורשים | `3.02` | `blocked` | Boundary must limit preview work to simple shoresh identification and basic meaning only. | Verify approved simple shoresh list source, exact root spelling, accepted basic meaning, and exclusion of weak/altered roots. | Approved simple shoresh list. | Weak-letter roots, altered-root recognition, advanced contextual shoresh translation, full verb parsing, level-advanced root transformations. | `partially_locked_but_missing_required_inputs` | Teacher approves simple-root boundary, root list, source/PDF verification, excluded weak/altered roots, answer-key rules, packet format, and preview-size limit. | Simple shoresh work may move forward for planning only; preview generation remains blocked. |
| 3.05 Pronoun Referent Tracking | `3.05` | `blocked` | Boundary must limit preview work to local, clear referents only. | Verify exact pronoun examples, local referent clarity, and exclusion of cross-pasuk referents. | Approved local pronoun/referent examples. | Cross-pasuk referents, ambiguous referents, context-heavy interpretation, broad pronoun interpretation without teacher wording boundaries. | `partially_locked_but_missing_required_inputs` | Teacher approves local-referent boundary, examples, source/PDF verification, ambiguity exclusions, answer-key rules, packet format, and preview-size limit. | This must remain separate from pronominal suffix decoding. |
| 3.05 Pronominal Suffix Decoding | `3.05` | `blocked` | Boundary must limit preview work to teacher-approved suffix examples and basic person/gender/number decoding. | Verify exact suffix examples, local word forms, and person/gender/number forms. | Approved pronominal suffix examples. | Ambiguous suffixes, context-heavy interpretation, verb-linked clue systems unless separately approved, bundling with referent tracking. | `partially_locked_but_missing_required_inputs` | Teacher approves suffix-decoding boundary, examples, source/PDF verification, excluded cases, answer-key rules, packet format, and preview-size limit. | This lane is mapped but not locked. |
| 3.06 Visible Prefixes / Articles | `3.06` | `blocked` | Boundary must limit preview work to visible prefixes and ה הידיעה where nikud-sensitive interpretation is not required. | Verify exact prefix/article examples and confirm forms do not depend on unverified nikud-sensitive interpretation. | Approved prefix/article examples. | Two functions of את, ו ההיפוך unless separately approved, ה השאלה unless separately approved, ה המגמה unless separately approved, context-heavy interpretation, nikud-sensitive distinctions not yet verified. | `partially_locked_but_missing_required_inputs` | Teacher approves visible-form boundary, examples, source/PDF verification, excluded content, answer-key rules, packet format, and preview-size limit. | The visible-form concept may move forward for planning only. |
| 3.07 Foundational Verb Clues | `3.07` | `blocked` | Boundary must limit preview work to foundational tense/person/form clues and not full parsing or advanced translation. | Verify exact verb examples, basic tense/person/form clues, and exclusion of advanced parsing and weak-root analysis. | Approved foundational verb examples. | בנינים, passive forms, ציווי, מקור, שם הפועל, weak-root verb analysis, full parsing of complex verb forms, advanced translation precision. | `partially_locked_but_missing_required_inputs` | Teacher approves foundational verb-clue boundary, examples, source/PDF verification, excluded advanced forms, answer-key rules, packet format, and preview-size limit. | Foundational verb clues remain planning-only until inputs are locked. |
| 3.04 Noun/Adjective Features | `3.04` | `blocked` | Later/cautious boundary must be separately approved before preview use. | Verify Hebrew examples, nekudos, level placement, and source/PDF examples. | Approved noun/adjective feature examples. | Over-bundling with סמיכות, irregular forms unless teacher-approved, adjective agreement unless approved, context-heavy phrase interpretation. | `blocked_missing_required_locks` | A future teacher review approves a narrow boundary, examples, source verification, and preview eligibility. | Not part of the first MVP preview scope. |
| 3.04 סמיכות | `3.04` | `blocked` | Protected boundary must be separately approved before preview use. | Verify סמיכות examples, forms, nekudos, and level placement against source PDFs. | Approved סמיכות examples. | Context-heavy phrase translation, compact questions that remove needed phrase context, unverified examples, broad grouping support. | `blocked_missing_required_locks` | A future teacher review approves a narrow סמיכות boundary and source-verified examples. | Compact סמיכות remains protected. |
| 3.08 Grouping and Word Order | `3.08` | `blocked` | Protected/context-sensitive boundary must be separately approved before preview use. | Verify Loshon page references and examples visually in the PDFs and confirm full-context boundaries. | Approved full-context grouping or word-order examples. | Compact isolated questions, context-stripped word-order questions, broad independent full-pasuk grouping, overclaiming source support. | `blocked_missing_required_locks` | Future source/PDF verification and teacher approval create a narrow full-context preview boundary. | Not suitable for compact preview yet. |
| 3.10 Nikud | `3.10` | `blocked` | Deferred; no MVP preview wording boundary should be created now. | Direct source review would be required in a later phase. | None for MVP. | All MVP diagnostic use, question generation, nikud-sensitive distinctions, OCR-sensitive charts. | `deferred_not_eligible_for_mvp_preview` | A later phase explicitly reopens 3.10 with direct source review and teacher decision. | Not eligible for MVP preview. |

## 5. Required Teacher Wording Boundaries

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

## 6. Source/PDF Verification Requirements

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

## 7. Approved Inputs Needed Before Preview

Required future inputs:

- approved vocabulary list for 3.01 nouns: missing
- approved simple shoresh list for 3.02: missing
- approved pronoun examples for 3.05 referent tracking: missing
- approved suffix examples for 3.05 suffix decoding: missing
- approved prefix/article examples for 3.06: missing
- approved foundational verb examples for 3.07: missing
- excluded-content list: drafted here, not yet teacher-locked
- answer-key review rules: drafted here, not yet teacher-locked
- teacher-review packet format: drafted here, not yet teacher-locked
- preview-size limit: drafted here, not yet teacher-locked

Do not create the actual vocabulary or example lists from this lock file. They do not currently exist as clearly approved input lists in the reviewed source files.

## 8. Explicit Excluded Content Lock

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

## 9. Answer-Key Review Rules Needed

Before preview generation, answer-key rules must state:

- every answer must be traceable to the approved input list or verified source example
- every distractor must be plausible but not misleading
- no answer may depend on deferred content
- answer key must explain the specific skill being assessed
- answer key must flag if teacher review is required
- answer key may not be treated as reviewed-bank approval

These rules are required for a future protected preview packet only. They do not authorize answer-key creation now.

## 10. Teacher-Review Packet Format Needed

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

## 11. Preview Size Limit

Maximum future protected preview size:

- no more than 3 questions per unlocked MVP lane
- no more than 10 questions total
- only lanes marked `locked_for_future_protected_preview` may be included
- preview must remain non-runtime and teacher-review only

No lane is currently marked `locked_for_future_protected_preview`.

## 12. Final Lock Status Summary

No Standard 3 lane is currently locked for protected preview generation.

Locked lanes:

- None

Blocked lanes:

- `3.01` Nouns / שמות עצם
- `3.02` Simple Shorashim / שורשים
- `3.05` Pronoun Referent Tracking
- `3.05` Pronominal Suffix Decoding
- `3.06` Visible Prefixes / Articles
- `3.07` Foundational Verb Clues
- `3.04` Noun/Adjective Features
- `3.04` סמיכות
- `3.08` Grouping and Word Order

Deferred lanes:

- `3.10` Nikud

Exact inputs missing before future protected preview generation:

- teacher-approved wording boundaries
- source/PDF-verified vocabulary and examples
- approved noun list
- approved simple shoresh list
- approved pronoun examples
- approved suffix examples
- approved prefix/article examples
- approved foundational verb examples
- teacher-locked excluded-content list
- teacher-locked answer-key review rules
- teacher-locked review packet format
- teacher-locked preview-size limit

## 13. Recommended Next Step

No lanes are locked.

The next step is to create or approve the exact input lists and teacher wording boundaries first. Do not proceed to question generation until at least one lane is marked `locked_for_future_protected_preview` by a later, explicit review artifact.
