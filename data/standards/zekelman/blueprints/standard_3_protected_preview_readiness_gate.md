# Zekelman Standard 3 Protected Preview Readiness Gate

## 1. Purpose

This document is a strict readiness gate before any protected preview generation for Zekelman Standard 3. It follows the teacher-reviewed diagnostic planning grid, the MVP diagnostic blueprint, and the skill-to-question-type map.

This gate answers:

- which Standard 3 skill lanes are ready for a future tiny preview packet
- which lanes remain blocked
- what evidence or teacher approval is missing
- what may not be generated yet

This document does not generate questions and does not authorize runtime use. It is a review-only planning artifact.

## 2. Hard Boundaries

- Runtime status: `not_runtime_ready`
- Question-generation status: `not_question_ready`
- Reviewed-bank status: `not_approved_for_reviewed_bank`
- Student-facing status: `not_student_facing`
- Promotion status: `blocked_pending_future_gate`
- Preview generation status: `blocked_until_explicit_future_prompt`

This readiness gate does not authorize:

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

## 3. Readiness Criteria for Future Protected Preview Generation

Every lane must satisfy all of these criteria before it can be included in a future protected preview:

1. Teacher-reviewed diagnostic lane exists.
2. Skill-to-question-type family is defined.
3. Teacher-approved wording boundary exists.
4. Source/PDF verification is complete for the exact examples or vocabulary to be used.
5. Approved vocabulary/example list exists.
6. Protected/deferred content is explicitly excluded.
7. Preview size limit is defined.
8. Answer-key review rules are defined.
9. Teacher-review packet format is defined.
10. Runtime and reviewed-bank promotion remain blocked.

Failure of any required criterion means the lane remains blocked from preview generation.

## 4. Lane-by-Lane Preview Readiness Table

| Skill Lane | Standard ID | Existing Review Decision | Question-Type Family Defined? | Teacher Wording Boundary Complete? | Source/PDF Verification Complete? | Approved Examples/Vocabulary Available? | Protected Content Excluded? | Preview Readiness Status | Allowed Future Action | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.01 Nouns / שמות עצם | `3.01` | `approve_as_foundational_skill` | Yes | No | No | No | Planning exclusions listed; lock file still needed | `blocked` | Create a teacher wording/source verification lock file and approved vocabulary list before any preview prompt. | This lane is not ready for protected preview generation. The blocker is not the skill concept; the blocker is missing approved inputs. |
| 3.02 Simple Shorashim / שורשים | `3.02` | `approve_with_level_adjustment` | Yes | No | No | No | Planning exclusions listed; lock file still needed | `blocked` | Define a teacher-approved simple-root list and excluded weak/altered-root list. | This lane remains planning-only until the simple-root boundary and examples are verified. |
| 3.05 Pronoun Referent Tracking | `3.05` | `approve_with_wording_revision` | Yes | No | No | No | Planning exclusions listed; lock file still needed | `blocked` | Finalize local-referent wording boundaries and source-verified examples. | This lane is not ready because local referent distance and ambiguity rules are not locked. |
| 3.05 Pronominal Suffix Decoding | `3.05` | `approve_with_wording_revision` | Yes | No | No | No | Planning exclusions listed; lock file still needed | `blocked` | Finalize suffix examples, person/gender/number wording, and exclusion rules. | This lane must remain separate from pronoun referent tracking and verb-linked clue systems. |
| 3.06 Visible Prefixes / Articles | `3.06` | `approve_with_wording_revision` | Yes | No | No | No | Planning exclusions listed; lock file still needed | `blocked` | Create a verified visible-form list and explicit exclusions for את, ו ההיפוך, and nikud-sensitive forms. | This lane is not ready for protected preview generation until visible-form scope is locked. |
| 3.07 Foundational Verb Clues | `3.07` | `approve_with_level_adjustment` | Yes | No | No | No | Planning exclusions listed; lock file still needed | `blocked` | Define teacher-approved foundational tense/person/form examples and excluded advanced verb forms. | This lane remains planning-only until advanced parsing is explicitly excluded in a lock file. |
| 3.04 Noun/Adjective Features | `3.04` | `approve_with_wording_revision` | Yes | No | No | No | Planning exclusions listed; lock file still needed | `blocked` | Complete wording revision and verify examples before any later preview consideration. | This is a cautious/later lane, not part of the first MVP preview scope. |
| 3.04 סמיכות | `3.04` | `approve_with_wording_revision` | Yes | No | No | No | Planning exclusions listed; lock file still needed | `blocked` | Define a narrow teacher-approved סמיכות boundary before any preview consideration. | Compact סמיכות questions remain blocked without a teacher-approved boundary. |
| 3.08 Grouping and Word Order | `3.08` | `approve_with_wording_revision` | Yes | No | No | No | Planning exclusions listed; lock file still needed | `blocked` | Verify Loshon page references/examples and define full-context wording boundaries. | This lane is not ready for protected preview generation; compact word-order questions remain blocked. |
| 3.10 Nikud | `3.10` | `defer_to_later_phase` | No for MVP | No | No | No | Blocked by deferral | `blocked` | Keep deferred; do not include in MVP preview planning. | This lane is not ready and remains out of MVP preview generation. |

## 5. Expected Conservative Outcome

No Standard 3 lane is currently ready for protected preview generation.

This result is intentionally conservative. Several lanes may move forward for planning, but the current files do not prove that teacher-approved wording boundaries, source/PDF-verified examples, approved vocabulary/example lists, answer-key review rules, and teacher-review packet format are complete.

The blocker is not the skill concept; the blocker is missing approved inputs.

This remains planning-only.

## 6. If Any Lane Is Conditionally Ready

No lane is conditionally ready in this gate.

Because no lane satisfies all readiness criteria, no future protected preview scope is authorized by this document. If a future gate marks one or more lanes as `conditionally_ready_for_future_protected_preview`, the preview scope must remain tiny and protected:

- no more than 3 questions per approved lane
- no more than 10 total questions
- non-runtime only
- clearly labeled as teacher-review preview
- answer key included only for teacher review
- no reviewed-bank promotion
- no student-facing use

Do not generate those questions now.

## 7. If No Lane Is Ready

Minimum work needed before preview generation:

- finalize teacher wording boundaries
- identify exact source-verified Hebrew examples
- approve vocabulary lists
- define answer-key review rules
- define teacher-review packet format
- create an explicit excluded-content lock file
- define a preview-size limit
- create a separate protected preview-generation prompt

## 8. Blocked Content List

The following content remains blocked:

- 3.10 ניקוד
- weak-letter roots
- altered-root recognition
- advanced contextual shoresh translation
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

## 9. Recommendation

No lane is ready for protected preview generation.

The next development step should be a teacher wording/source verification lock file before preview generation. That lock file should name the exact approved examples, vocabulary lists, wording boundaries, and excluded content for each lane that may later be considered for a tiny protected preview.

## 10. Final Status Summary

- Runtime: blocked
- Question generation: blocked unless future explicit prompt authorizes protected preview
- Reviewed bank: blocked
- Student-facing use: blocked
- Current artifact status: review-only readiness gate
