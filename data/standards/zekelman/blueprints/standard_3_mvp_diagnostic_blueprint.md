# Zekelman Standard 3 MVP Diagnostic Blueprint

## 1. Purpose

This document converts teacher-reviewed Zekelman Standard 3 decisions into a planning-only diagnostic blueprint. It defines the first MVP diagnostic planning structure before any skill-to-question-type mapping or preview generation.

This blueprint is based on the completed teacher-reviewed diagnostic planning grid and the recorded Standard 3 review decisions. It answers which Standard 3 skills may move forward for planning, what each lane may cover, what must remain protected or deferred, and what must happen before any question generation.

This is planning only. This is not runtime behavior. This is not question generation. This is not student-facing content.

## 2. Hard Boundaries

- Runtime status: `not_runtime_ready`
- Question-generation status: `not_question_ready`
- Reviewed-bank status: `not_approved_for_reviewed_bank`
- Student-facing status: `not_student_facing`
- Promotion status: `blocked_pending_future_gate`

This blueprint does not authorize:

- runtime activation
- UI changes
- student-facing diagnostics
- generated questions
- sample questions
- reviewed-bank promotion
- answer keys
- production data changes

## 3. MVP Diagnostic Skill Lanes

### A. 3.01 Nouns / שמות עצם

- Standard ID: `3.01`
- Lane name: Nouns / שמות עצם
- MVP inclusion status: Included for planning only.
- Teacher wording boundary needed: Yes. The lane requires source-verified wording and teacher-approved vocabulary scope.
- Source/PDF verification needed: Yes. The canonical Zekelman wording and vocabulary-list boundaries require verification.
- Question generation status: Not allowed yet.

Allowed diagnostic focus:

- taught noun recognition
- Hebrew-to-English translation of approved nouns
- controlled English-to-Hebrew recall
- controlled multiple-meaning work only from approved vocabulary lists
- transfer into unfamiliar pesukim only when vocabulary scope is source-approved and teacher-approved

Protected/deferred areas:

- untaught vocabulary
- broad contextual inference without an approved word list
- non-source-verified wording
- uncontrolled multiple-meaning inference

### B. 3.02 Shorashim / שורשים

- Standard ID: `3.02`
- Lane name: Simple shorashim / שורשים
- MVP inclusion status: Included for planning only, limited to simple shoresh work.
- Teacher wording boundary needed: Yes. The lane requires a clear boundary between simple root recognition and advanced root analysis.
- Source/PDF verification needed: Yes. Level mapping and weak-letter boundaries require verification.
- Question generation status: Not allowed yet.

Allowed diagnostic focus:

- simple shoresh identification
- connecting common taught shorashim to basic meaning
- recognizing simple repeated root families
- separating simple root recognition from full verb parsing

Protected/deferred areas:

- weak-letter roots
- altered-root recognition
- advanced contextual shoresh translation
- full verb parsing
- level-advanced root transformations

### C. 3.05 Pronouns

- Standard ID: `3.05`
- Lane name: Pronouns
- MVP inclusion status: Included for planning only, but split into separate lanes.
- Required split: Pronoun referent tracking; pronominal suffix decoding.
- Teacher wording boundary needed: Yes. Referent tracking and suffix decoding must not be bundled into one broad skill.
- Source/PDF verification needed: Yes. Hebrew forms, level fit, and referent-distance boundaries require verification.
- Question generation status: Not allowed yet.

Allowed diagnostic focus:

- local referent identification
- basic person/gender/number awareness
- suffix recognition on teacher-approved examples
- simple pronoun/referent matching where the referent is local and clear

Protected/deferred areas:

- cross-pasuk referent tracking
- context-heavy ambiguity
- unclear referents
- verb-linked clue systems unless separately approved
- broad pronoun interpretation without teacher wording boundaries

### D. 3.06 Prefixes / Articles

- Standard ID: `3.06`
- Lane name: Visible prefixes / articles
- MVP inclusion status: Included for planning only, limited to visible forms.
- Teacher wording boundary needed: Yes. Visible-form recognition must stay separate from context-heavy interpretation.
- Source/PDF verification needed: Yes. Source wording and nikud-sensitive distinctions require verification before expansion.
- Question generation status: Not allowed yet.

Allowed diagnostic focus:

- visible prefix identification
- basic function of ו
- ה הידיעה
- common inseparable prefixes such as ב / כ / ל / מ
- article/prefix recognition where nikud-sensitive interpretation is not required

Protected/deferred areas:

- two functions of את
- ו ההיפוך unless separately mapped and teacher-approved
- ה השאלה unless source-verified and teacher-approved
- ה המגמה unless source-verified and teacher-approved
- context-heavy interpretation
- nikud-sensitive distinctions not yet verified

### E. 3.07 Verbs

- Standard ID: `3.07`
- Lane name: Foundational verb clues
- MVP inclusion status: Included for planning only, limited to foundational verb clues.
- Teacher wording boundary needed: Yes. Foundational form recognition must stay separate from advanced parsing and translation precision.
- Source/PDF verification needed: Yes. Level placement and approved form clues require verification.
- Question generation status: Not allowed yet.

Allowed diagnostic focus:

- foundational tense clues
- basic person clues
- basic form clues
- simple tense/person recognition where teacher-approved
- separating form recognition from full translation precision

Protected/deferred areas:

- בנינים
- passive forms
- ציווי
- מקור
- שם הפועל
- advanced translation precision
- weak-root verb analysis
- full parsing of complex verb forms

## 4. Cautious / Later Lanes

### 3.04 Nouns and Adjectives

Recorded decision: `approve_with_wording_revision`

Planning treatment: May support later diagnostic planning with wording revision.

Required split:

- noun/adjective feature work
- סמיכות recognition

Protection: Keep סמיכות context-protected unless future teacher review approves a narrower diagnostic boundary.

MVP status: Not part of the first MVP diagnostic blueprint except as a later/cautious lane.

Question generation status: Not allowed yet.

### 3.08 Grouping and Word Order

Recorded decision: `approve_with_wording_revision`

Planning treatment: Important for translation quality, but context-sensitive.

Protection: Do not use for compact diagnostic questions yet. Use later only with full-context review and careful wording boundaries.

MVP status: Later/cautious lane.

Question generation status: Not allowed yet.

### 3.10 Nikud

Recorded decision: `defer_to_later_phase`

Planning treatment: Keep out of the MVP diagnostic blueprint except as a caution note.

Protection: Do not use for MVP diagnostic planning beyond recording the deferral.

MVP status: Deferred.

Question generation status: Not allowed.

## 5. Diagnostic Design Principles

1. Test one skill at a time wherever possible.
2. Separate recognition from translation.
3. Separate vocabulary knowledge from grammar analysis.
4. Separate local form recognition from context-heavy interpretation.
5. Use only source-verified Hebrew wording.
6. Avoid OCR-sensitive material unless manually verified.
7. Do not use weak-letter or altered-root examples in the MVP unless separately approved.
8. Do not use context-heavy pronoun, את, or word-order questions in the MVP.
9. Require teacher-approved wording boundaries before preview generation.
10. Require a separate skill-to-question-type map before any question generation.
11. Require a separate protected preview-generation gate before sample questions are created.
12. Require teacher review before promotion.

## 6. MVP Readiness Table

| Skill Lane | Standard ID | MVP Included? | Diagnostic Readiness | Requires Teacher Wording Boundary? | Requires Source/PDF Verification? | Protected/Deferred Content | Question Generation Allowed Now? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3.01 Nouns | `3.01` | Yes, planning only | Foundational planning may move forward. | Yes | Yes | Untaught vocabulary, uncontrolled multiple-meaning inference, broad contextual inference | No |
| 3.02 Simple Shorashim | `3.02` | Yes, planning only | Simple shoresh identification may move forward with level protection. | Yes | Yes | Weak-letter roots, altered-root recognition, advanced contextual shoresh translation, full verb parsing | No |
| 3.05 Pronoun Referent Tracking | `3.05` | Yes, planning only | May move forward as a separate local referent lane. | Yes | Yes | Cross-pasuk referents, unclear referents, context-heavy ambiguity | No |
| 3.05 Pronominal Suffix Decoding | `3.05` | Yes, planning only | May move forward as a separate suffix-decoding lane. | Yes | Yes | Bundled pronoun interpretation, unclear suffix examples, verb-linked clue systems unless separately approved | No |
| 3.06 Visible Prefixes / Articles | `3.06` | Yes, planning only | Visible-form identification may move forward. | Yes | Yes | Two functions of את, ו ההיפוך, ה השאלה, ה המגמה, nikud-sensitive distinctions | No |
| 3.07 Foundational Verb Clues | `3.07` | Yes, planning only | Foundational tense/person/form clues may move forward with level adjustment. | Yes | Yes | בנינים, passive forms, ציווי, מקור, שם הפועל, weak-root verb analysis, advanced translation precision | No |
| 3.04 Noun/Adjective Features | `3.04` | No, later/cautious | May support later planning after wording revision. | Yes | Yes | Irregular forms, adjective agreement, broad phrase-structure use | No |
| 3.04 סמיכות | `3.04` | No, later/cautious | May support later planning as a separate protected lane. | Yes | Yes | Context-heavy סמיכות use and broad grouping support without further review | No |
| 3.08 Grouping and Word Order | `3.08` | No, later/cautious | Important but context-sensitive; not compact question-ready. | Yes | Yes | Broad full-pasuk grouping, compact diagnostic use, unsourced page/example claims | No |
| 3.10 Nikud | `3.10` | No, deferred | Deferred to later phase. | Yes | Yes | Full ניקוד systems, תנועות, שבאים, דגשים, syllables, טעמי המקרא | No |

## 7. What This Blueprint Allows

This blueprint allows only:

- planning future diagnostic lanes
- preparing a future skill-to-question-type map
- identifying protected/deferred areas
- aligning future work with teacher-reviewed decisions

## 8. What This Blueprint Does Not Allow

This blueprint does not allow:

- question generation
- sample question creation
- answer-key creation
- runtime activation
- UI changes
- reviewed-bank promotion
- student-facing use
- production data changes

## 9. Remaining Blockers Before Question Generation

- source/PDF verification still required
- teacher-approved wording boundaries still required
- explicit skill-to-question-type map still required
- protected preview generation prompt still required
- generated preview packet still requires teacher review
- promotion gate still required
- runtime activation still requires a separate future decision
- reviewed-bank promotion still requires a separate future decision

## 10. Recommended Next Step

Create a Standard 3 skill-to-question-type map as a review-only planning artifact.

This next step should still not generate questions.
