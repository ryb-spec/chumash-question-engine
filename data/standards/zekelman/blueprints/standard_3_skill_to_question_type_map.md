# Zekelman Standard 3 Skill-to-Question-Type Map

## 1. Purpose

This document maps teacher-reviewed Zekelman Standard 3 MVP diagnostic lanes to possible future question-type families. It translates the non-runtime MVP diagnostic blueprint into a clearer structure for later question design discussions.

This is planning only. This does not generate questions. This does not authorize question generation. This does not activate runtime behavior. This does not create reviewed-bank content.

The map is intended to help:

- teachers understand what each future question-type family would measure
- developers understand what future templates may need
- reviewers identify what remains blocked before preview generation

## 2. Hard Boundaries

- Runtime status: `not_runtime_ready`
- Question-generation status: `not_question_ready`
- Reviewed-bank status: `not_approved_for_reviewed_bank`
- Student-facing status: `not_student_facing`
- Promotion status: `blocked_pending_future_gate`

This map does not authorize:

- generated questions
- sample questions
- answer keys
- active templates
- runtime activation
- UI changes
- reviewed-bank promotion
- production-data changes

## 3. Question-Type Design Rules

1. Test one skill at a time wherever possible.
2. Separate recognition from translation.
3. Separate vocabulary recall from grammar analysis.
4. Avoid context-heavy interpretation in the MVP.
5. Use only source-verified Hebrew wording.
6. Use only teacher-approved vocabulary and examples.
7. Do not use OCR-sensitive Hebrew unless manually verified.
8. Do not use weak-letter roots unless separately approved.
9. Do not use ambiguous pronoun referents in the MVP.
10. Do not use the two functions of את until separately approved.
11. Do not use ו ההיפוך unless separately mapped and approved.
12. Do not include 3.10 ניקוד in MVP question types.
13. Every future generated preview must require separate teacher review.

## 4. MVP Skill-to-Question-Type Map

| Skill Lane | Standard ID | MVP Status | Future Question-Type Family | What the Question Type May Assess | What the Question Type Must Avoid | Required Inputs Before Generation | Teacher Approval Needed? | Question Generation Allowed Now? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.01 Nouns / שמות עצם | `3.01` | Included for planning only | taught noun recognition; Hebrew-to-English noun translation; English-to-Hebrew noun recall; controlled multiple-meaning noun check | approved taught noun vocabulary; source-verified vocabulary lists; controlled multiple-meaning examples from approved lists only | untaught vocabulary; broad contextual inference; uncontrolled multiple meanings; non-source-verified wording | teacher-approved vocabulary lists; source/PDF-verified noun wording; approved multiple-meaning boundaries | Yes | No |
| 3.02 Simple Shorashim / שורשים | `3.02` | Included for planning only, limited to simple shoresh work | simple shoresh identification; shoresh-to-basic-meaning match; simple repeated-root recognition | simple roots only; taught/common shorashim; root family recognition where forms are simple | weak-letter roots; altered roots; advanced contextual root translation; full verb parsing | teacher-approved simple root list; verified level boundary; excluded weak/altered-root list | Yes | No |
| 3.05 Pronoun Referent Tracking | `3.05` | Included for planning only as a separate lane | local pronoun referent identification; simple pronoun-to-referent match | local referents; clear nearby antecedents; teacher-approved examples only | cross-pasuk referents; ambiguous referents; context-heavy interpretation | teacher-approved referent-distance boundary; source/PDF-verified examples; ambiguity exclusion rules | Yes | No |
| 3.05 Pronominal Suffix Decoding | `3.05` | Included for planning only as a separate lane | suffix recognition; suffix person/gender/number identification; simple suffix meaning match | teacher-approved suffix examples; clear local word forms; basic person/gender/number awareness | ambiguous suffixes; context-heavy interpretation; verb-linked clue systems unless separately approved | teacher-approved suffix examples; verified Hebrew forms; approved person/gender/number wording | Yes | No |
| 3.06 Visible Prefixes / Articles | `3.06` | Included for planning only, limited to visible forms | visible prefix identification; prefix-function recognition; ה הידיעה recognition; common inseparable-prefix recognition | visible ו; ה הידיעה; ב / כ / ל / מ; non-nikud-sensitive prefix/article forms | two functions of את; ו ההיפוך unless separately approved; ה השאלה unless source-verified and teacher-approved; ה המגמה unless source-verified and teacher-approved; context-heavy interpretation | teacher-approved visible-form list; verified source wording; exclusion rules for context-heavy and nikud-sensitive forms | Yes | No |
| 3.07 Foundational Verb Clues | `3.07` | Included for planning only, limited to foundational verb clues | tense clue recognition; person clue recognition; simple form-clue identification; form-to-basic-meaning support | foundational tense/person/form clues; simple teacher-approved examples; recognition before full translation precision | בנינים; passive forms; ציווי; מקור; שם הפועל; weak-root verbs; advanced parsing; advanced translation precision | teacher-approved form-clue list; verified level placement; excluded advanced verb-form list | Yes | No |

## 5. Cautious / Later Skill-to-Question-Type Map

### 3.04 Noun/Adjective Features

Recorded decision: `approve_with_wording_revision`

Future status: Later/cautious planning only.

Possible future question-type families:

- noun/adjective feature recognition
- gender/number awareness
- adjective matching

Must avoid:

- over-bundling with סמיכות
- irregular forms unless teacher-approved
- context-heavy phrase interpretation

Question Generation Allowed Now? No

### 3.04 סמיכות

Recorded decision: `approve_with_wording_revision`

Future status: Protected later lane.

Possible future question-type families:

- simple סמיכות recognition only after teacher-approved boundary

Must avoid:

- context-heavy phrase translation
- compact questions that remove needed phrase context
- unverified examples

Question Generation Allowed Now? No

### 3.08 Grouping and Word Order

Recorded decision: `approve_with_wording_revision`

Future status: Later/cautious lane.

Possible future question-type families:

- full-context phrase grouping
- word-order adjustment for translation

Must avoid:

- compact isolated questions
- context-stripped word-order questions
- overclaiming source support
- questions that depend on broad interpretation

Question Generation Allowed Now? No

### 3.10 Nikud

Recorded decision: `defer_to_later_phase`

Future status: Deferred.

Possible future question-type families: None for MVP.

Must avoid:

- all MVP diagnostic use
- question generation
- nikud-sensitive distinctions
- OCR-sensitive charts

Question Generation Allowed Now? No

## 6. Required Inputs Before Future Preview Generation

Before any protected preview generation prompt, the project must have:

- teacher-approved vocabulary lists
- source/PDF-verified Hebrew examples
- approved wording boundaries for each lane
- approved question-type families
- explicit excluded-content list
- preview-size limit
- teacher-review packet format
- answer-key review rules
- separate protected preview-generation prompt

## 7. Map Readiness Table

| Standard ID | Skill Lane | Map Status | Future Question-Type Family Defined? | Teacher Boundary Still Needed? | Source/PDF Verification Still Needed? | Allowed in Protected Preview Yet? | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `3.01` | Nouns / שמות עצם | MVP planning lane | Yes | Yes | Yes | No | Requires approved vocabulary lists and source-verified wording. |
| `3.02` | Simple Shorashim / שורשים | MVP planning lane | Yes | Yes | Yes | No | Limited to simple roots; weak-letter and altered-root work remains blocked. |
| `3.05` | Pronoun Referent Tracking | MVP planning lane | Yes | Yes | Yes | No | Local, clear referents only after teacher boundary approval. |
| `3.05` | Pronominal Suffix Decoding | MVP planning lane | Yes | Yes | Yes | No | Must remain separate from referent tracking and verb-linked clue systems. |
| `3.06` | Visible Prefixes / Articles | MVP planning lane | Yes | Yes | Yes | No | Visible forms only; את, ו ההיפוך, and nikud-sensitive distinctions remain blocked. |
| `3.07` | Foundational Verb Clues | MVP planning lane | Yes | Yes | Yes | No | Recognition-focused only; advanced parsing remains blocked. |
| `3.04` | Noun/Adjective Features | Later/cautious lane | Yes | Yes | Yes | No | Requires wording revision and source-verified examples before preview use. |
| `3.04` | סמיכות | Protected later lane | Yes | Yes | Yes | No | Keep context-protected unless a narrower boundary is approved. |
| `3.08` | Grouping and Word Order | Later/cautious lane | Yes | Yes | Yes | No | Full-context only in later planning; no compact isolated use. |
| `3.10` | Nikud | Deferred | No for MVP | Yes | Yes | No | Keep out of MVP question types. |

## 8. What This Map Allows

This map allows only:

- future planning
- question-type discussion
- teacher review of diagnostic boundaries
- preparation for a later protected preview-generation prompt

## 9. What This Map Does Not Allow

This map does not allow:

- generating questions
- writing sample questions
- creating answer choices
- creating answer keys
- activating runtime behavior
- changing UI
- modifying reviewed-bank data
- using the content with students

## 10. Remaining Blockers Before Question Generation

- teacher-approved wording boundaries
- source/PDF verification
- approved question-type map review
- protected preview-generation prompt
- teacher review of generated preview packet
- promotion gate
- runtime activation decision
- reviewed-bank promotion decision

## 11. Recommended Next Step

Review the skill-to-question-type map, then create a protected preview-generation prompt that generates only a very small, clearly labeled, non-runtime preview packet.

Even the next step should remain non-runtime and teacher-review only.
