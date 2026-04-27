# Zekelman Standard 3 MVP Candidate Input Lists

## 1. Purpose

This document proposes exact candidate input lists for teacher approval before any protected preview generation for the approved Zekelman Standard 3 MVP diagnostic lanes.

These candidates are traced to existing source-backed artifacts, structured standards records, Loshon HaTorah / Loshon Hakodesh rule candidates, or extracted source references already in the repository. They are not student-facing items, not generated questions, and not approved preview inputs yet.

The purpose is to help a teacher/project lead verify:

- the exact Hebrew item or example
- the English meaning or feature being considered
- the source path and source note
- whether the item should be approved, revised, rejected, or deferred

## 2. Hard Boundaries

- Runtime status: `not_runtime_ready`
- Question-generation status: `not_question_ready`
- Reviewed-bank status: `not_approved_for_reviewed_bank`
- Student-facing status: `not_student_facing`
- Input approval status: `selected_inputs_approved_for_future_protected_preview_planning_only`
- Preview generation status: `blocked`

This document does not authorize:

- generated questions
- sample questions
- answer choices
- answer keys
- active question templates
- runtime activation
- UI changes
- reviewed-bank promotion
- production-data changes
- student-facing use

## 3. Teacher Review Findings Recorded

Reviewer: Yossi Bassman

Reviewed file: `data/standards/zekelman/blueprints/standard_3_mvp_candidate_input_lists.md`

Overall decision recorded:

- These decisions are for future protected-preview planning only.
- These decisions do not authorize runtime activation, reviewed-bank promotion, student-facing use, or general question generation.

Explicit decisions and notes recorded from the teacher review:

| Lane | Recorded decision or note | Impact on this file |
|---|---|---|
| 3.01 Nouns / שמות עצם | Item-level approvals recorded for `STD3-01-NOUN-001`, `STD3-01-NOUN-002`, and `STD3-01-NOUN-003`. | Approved only for future protected-preview planning. Do not expand beyond approved noun inputs without explicit teacher approval. |
| 3.02 Simple Shorashim / שורשים | Item-level approval recorded for `STD3-02-SHORESH-001`; current approved candidate remains limited to `שמר`. Expanded 3.02 shoresh list beyond the one source-backed candidate remains not approved. | Keep `שמר` as the only approved source-backed candidate; do not add additional roots. |
| 3.05 Pronoun Referent Tracking | `not_approved_yet`. Needs teacher-selected local, clear referent examples. Do not include in preview yet. | Mark this lane as `not_approved_yet` for candidate input use. |
| 3.05 Pronominal Suffix Decoding | Item-level approvals recorded for `STD3-05-SUFFIX-001` and `STD3-05-SUFFIX-002`. | Approved only for suffix decoding using approved examples and basic possessive suffix meaning. |
| 3.06 Visible Prefixes / Articles | Item-level approvals recorded for `STD3-06-PREFIX-001`, `STD3-06-PREFIX-002`, `STD3-06-PREFIX-003`, and `STD3-06-PREFIX-004`. | Approved only for visible/simple prefix or article recognition in the approved examples. |
| 3.07 Foundational Verb Clues | Item-level approvals recorded for `STD3-07-VERB-001`, `STD3-07-VERB-002`, `STD3-07-VERB-003`, and `STD3-07-VERB-004`. | Approved only for foundational tense/person/form clues in the approved examples, not advanced parsing. |

Explicit non-approval recorded:

- 3.05 pronoun referent tracking is not approved for protected preview.
- Expanded 3.02 shoresh list beyond the one source-backed candidate is not approved.
- Any item that depends on excluded content is not approved.
- Any unlisted input item or future input without explicit teacher approval is not approved.

No specific item-removal correction was provided in the review findings.

## 4. Candidate Input Lists

Source/PDF verification status terms used below:

- `teacher_project_lead_visually_reviewed`: the teacher/project lead visually reviewed the item and approved it for future protected-preview planning only.
- `source_backed_candidate_needs_visual_pdf_confirmation`: the item is present in an existing structured/source-backed artifact and has a source note, but a human still needs to verify the exact source/PDF location visually before preview use.
- `needs_teacher_selected_source_example`: no safe exact candidate example is available in the current artifacts for this lane; a teacher/project lead must select and verify examples.
- `approve_input`: the item is approved for future protected-preview planning only. This does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation.
- `pending_teacher_review`: the item has not been approved for preview use.

### A. 3.01 Nouns / שמות עצם

Boundary: use only taught nouns from an approved vocabulary list. Do not include untaught vocabulary, broad contextual inference, uncontrolled multiple meanings, or non-source-verified vocabulary.

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source note/page/reference if available | Source/PDF verification status | Teacher approval status | Notes |
|---|---|---|---|---|---|---|---|---|
| STD3-01-NOUN-001 | בן | son / a son | 3.01 noun recognition and controlled noun translation | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule `DK-NOUN-001`; candidate `lht_cand_noun_implied_indefinite`; Lesson 1; raw evidence points to `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`, main extracted page 81 / printed p. 160 summary citing pg. 2 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only as a simple noun candidate. No alternate meaning is approved here. |
| STD3-01-NOUN-002 | מלך | king / a king | 3.01 noun recognition and controlled noun translation | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule `DK-NOUN-001`; candidate `lht_cand_noun_implied_indefinite`; Lesson 1; raw evidence points to main extracted page 81 / printed p. 160 summary citing pg. 2 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only as a simple noun candidate. Do not use for broader phrase inference. |
| STD3-01-NOUN-003 | איש | man / a man | 3.01 noun recognition and controlled noun translation | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule `DK-CONJ-001`; candidate `lht_cand_prefixed_vav_conjunction`; Lesson 1; raw evidence points to main extracted page 81 / printed p. 160 summary citing pg. 3 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only as an approved noun input. |

### B. 3.02 Simple Shorashim / שורשים

Boundary: use only simple shoresh identification and basic meaning from an approved root list. Exclude weak-letter roots, altered-root recognition, advanced contextual root translation, and full verb parsing.

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source note/page/reference if available | Source/PDF verification status | Teacher approval status | Notes |
|---|---|---|---|---|---|---|---|---|
| STD3-02-SHORESH-001 | שמר | basic root meaning: guard / keep | 3.02 simple shoresh identification | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rules `DK-PARSE-002`, `DK-VERB-PAST-001`, and `DK-VERB-FUTURE-001`; candidates `lht_cand_shoresh_added_letters`, `lht_cand_past_tense_markers`, and `lht_cand_future_tense_markers`; Lesson 5; raw evidence points to `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`, main extracted page 81 / printed p. 160 summary citing pgs. 35-36, and `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md`, answer extracted pages 11-12 / Lessons 5-6 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Current approved candidate is limited to `שמר`. Use only for simple root recognition. Do not use to require full parsing of שמרתי, שמרו, אשמור, or תשמרי. |

Additional simple roots are not selected in this file because the current artifacts do not provide a clearly approved simple-root list for MVP preview use. The teacher review explicitly did not approve an expanded 3.02 shoresh list beyond the one source-backed candidate. A teacher/project lead should approve an exact expanded simple shoresh list before this lane can be useful for protected-preview planning.

### C. 3.05 Pronoun Referent Tracking

Boundary: use only local, clear pronoun referents where the referent is nearby and unambiguous. Exclude cross-pasuk referents, ambiguous referents, and context-heavy interpretation.

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source note/page/reference if available | Source/PDF verification status | Teacher approval status | Notes |
|---|---|---|---|---|---|---|---|---|
| STD3-05-REFERENT-NEEDED | No exact candidate selected from current artifacts | Local pronoun referent tracking | 3.05 pronoun referent tracking | `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json`; `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_supplemental_crosswalk.json`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Zekelman 3.05 and supplemental sources support pronoun work, and Loshon candidate `lht_cand_person_gender_number_labels` supports person/gender/number labels, but the current artifacts do not provide a safe local antecedent example for referent tracking | `needs_teacher_selected_source_example` | `not_approved_yet` | Teacher review decision: `not_approved_yet`. Needs teacher-selected local, clear referent examples. Do not include in preview yet. Do not convert standalone pronouns such as אתם or היא into referent-tracking examples unless a local, source-backed antecedent is selected and verified. |

### D. 3.05 Pronominal Suffix Decoding

Boundary: use only teacher-approved pronominal suffix examples where the suffix form and basic person/gender/number meaning are clear. Exclude ambiguous suffixes, context-heavy interpretation, and verb-linked clue systems unless separately approved.

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source note/page/reference if available | Source/PDF verification status | Teacher approval status | Notes |
|---|---|---|---|---|---|---|---|---|
| STD3-05-SUFFIX-001 | ספרי | my book; singular noun with first-person singular possessive suffix | 3.05 pronominal suffix decoding | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule `DK-POSSESSIVE-001`; candidate `lht_cand_possessive_suffix_singular`; Lesson 4; raw evidence points to `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`, main extracted page 81 / printed p. 161 summary citing pgs. 26-30, and `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md`, answer extracted pages 9-10 / Lesson 4 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only as a basic suffix decoding example. |
| STD3-05-SUFFIX-002 | ספרו | his book; singular noun with third-person masculine singular possessive suffix | 3.05 pronominal suffix decoding | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule `DK-POSSESSIVE-001`; candidate `lht_cand_possessive_suffix_singular`; Lesson 4; raw evidence points to main extracted page 81 / printed p. 161 summary citing pgs. 26-30 and answer extracted pages 9-10 / Lesson 4 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only as a basic suffix decoding example. Do not use as a verb-linked clue or context-heavy interpretation item. |

Plural possessive examples such as דבריהם, דברו, and דבריו are source-backed in the Loshon artifacts, but they are not selected for the first MVP candidate list because they introduce singular/plural possessive caution and could overcomplicate the protected preview boundary.

### E. 3.06 Visible Prefixes / Articles

Boundary: use only visible prefixes and article forms where the function is clear and does not depend on unverified nikud-sensitive interpretation. Exclude את, ו ההיפוך, ה השאלה, ה המגמה, context-heavy interpretation, and nikud-sensitive distinctions that have not been manually verified.

Teacher review note: confirm examples are visible/simple forms only before any protected-preview use.

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source note/page/reference if available | Source/PDF verification status | Teacher approval status | Notes |
|---|---|---|---|---|---|---|---|---|
| STD3-06-PREFIX-001 | הבן | definite article ה; the son | 3.06 visible prefixes/articles | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule `DK-ARTICLE-001`; candidate `lht_cand_article_heh`; Lesson 1; raw evidence points to `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`, main extracted page 81 / printed p. 160 summary citing pg. 2 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only for visible ה הידיעה recognition. |
| STD3-06-PREFIX-002 | ואיש | prefixed ו; and a man | 3.06 visible prefixes/articles | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule `DK-CONJ-001`; candidate `lht_cand_prefixed_vav_conjunction`; Lesson 1; raw evidence points to main extracted page 81 / printed p. 160 summary citing pg. 3 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only as simple conjunction ו. This does not support ו ההיפוך. |
| STD3-06-PREFIX-003 | למלך | prefixed ל; to the king | 3.06 visible prefixes/articles | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule family `DK-PREP-002` through `DK-PREP-007`; candidate `lht_cand_prefix_prepositions`; Lesson 3; raw evidence points to main extracted page 8 / Lesson 3 and page 63 / Lesson 14 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only for visible ל prefix recognition. |
| STD3-06-PREFIX-004 | בבית | prefixed ב; in the house | 3.06 visible prefixes/articles | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule family `DK-PREP-002` through `DK-PREP-007`; candidate `lht_cand_prefix_prepositions`; Lesson 3; raw evidence points to main extracted page 8 / Lesson 3 and page 63 / Lesson 14 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only for visible ב prefix recognition where no unverified nikud-sensitive distinction is required. |

The source-backed examples מהארץ, כאב, and שאמר are not selected for this first candidate list because they may introduce additional context, spelling, ambiguity, or non-MVP prefix boundaries that need separate teacher review.

### F. 3.07 Foundational Verb Clues

Boundary: use only foundational tense/person/form clues from teacher-approved examples. Exclude full parsing, advanced translation precision, weak-root analysis, בנינים, passive forms, ציווי, מקור, and שם הפועל.

Teacher review note: confirm examples test basic tense/person/form clues only, not advanced parsing, before any protected-preview use.

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source note/page/reference if available | Source/PDF verification status | Teacher approval status | Notes |
|---|---|---|---|---|---|---|---|---|
| STD3-07-VERB-001 | שמרתי | past-tense ending clue; first-person singular meaning in the source artifact | 3.07 foundational verb clues | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rules `DK-PARSE-002` and `DK-VERB-PAST-001`; candidates `lht_cand_shoresh_added_letters` and `lht_cand_past_tense_markers`; Lesson 5; raw evidence points to `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md`, answer extracted page 11 / Lesson 5 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only for foundational clue awareness. Do not require full parsing or broad translation precision. |
| STD3-07-VERB-002 | שמרו | past-tense plural ending clue | 3.07 foundational verb clues | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule `DK-VERB-PAST-001`; candidate `lht_cand_past_tense_markers`; Lesson 5; raw evidence points to answer extracted page 11 / Lesson 5 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only for foundational past/plural clue awareness. |
| STD3-07-VERB-003 | אשמור | future-tense prefix clue; first-person singular meaning in the source artifact | 3.07 foundational verb clues | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rules `DK-PARSE-002` and `DK-VERB-FUTURE-001`; candidates `lht_cand_shoresh_added_letters` and `lht_cand_future_tense_markers`; Lesson 5; raw evidence points to `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md`, answer extracted pages 11-12 / Lessons 5-6 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only as a future prefix clue candidate. Do not generalize to weak-root forms. |
| STD3-07-VERB-004 | תשמרי | future-tense prefix/suffix clue; second-person feminine singular meaning in the source artifact | 3.07 foundational verb clues | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` | Rule `DK-VERB-FUTURE-001`; candidate `lht_cand_future_tense_markers`; Lesson 5; raw evidence points to answer extracted pages 11-12 / Lessons 5-6 | `teacher_project_lead_visually_reviewed` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. Use only for foundational future/person/gender/number clue awareness, not advanced parsing. |

## 5. Lanes Not Ready for Candidate Inputs

These lanes are deferred and no candidate input lists are prepared for them in this file.

| Deferred lane | Reason not prepared |
|---|---|
| 3.04 Noun/Adjective Features | Deferred to later phase. It requires a separate narrow teacher-approved boundary and should not be included in the first protected preview. |
| 3.04 סמיכות | Protected later lane. Compact סמיכות questions are blocked unless a separate narrow teacher-approved boundary is created. |
| 3.08 Grouping and Word Order | Context-sensitive later lane. Do not include compact or context-stripped word-order questions in the first protected preview. |
| 3.10 Nikud | Deferred. Not eligible for MVP protected preview. OCR-sensitive and source/PDF-sensitive material requires direct review before any diagnostic planning. |

## 6. Excluded Content Confirmation

The following excluded content is not included in the candidate input lists above:

- 3.10 ניקוד
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
- compact סמיכות questions without teacher-approved boundary
- OCR-sensitive Hebrew not manually verified

## 7. Teacher Approval Needed

Teacher/project-lead checklist for each candidate item:

- Approve the exact Hebrew item or example.
- Approve the English meaning or grammar feature.
- Confirm the source/PDF reference visually.
- Reject or revise any item whose wording, level, spelling, nekudos, or source match is not safe.
- Add teacher notes for any item that needs a narrower boundary.
- Confirm that no excluded content has slipped into the lane.

Lane-level approval still needed:

- 3.01: approve exact noun list, English meanings, and source/PDF references.
- 3.02: approve an expanded exact simple shoresh list and confirm weak/altered roots are excluded. The expanded list beyond `שמר` is not approved yet.
- 3.05 pronoun referent tracking: select exact local referent examples because no safe examples were found in current artifacts. This lane is `not_approved_yet` for protected preview.
- 3.05 pronominal suffix decoding: approve exact suffix examples and person/gender/number meanings.
- 3.06: approve exact visible prefix/article examples and confirm they are visible/simple forms only. Confirm את, ו ההיפוך, ה השאלה, and ה המגמה remain excluded.
- 3.07: approve exact verb examples and confirm that they test basic tense/person/form clues only, not advanced parsing.

## 8. Final Status Summary

- Runtime: blocked
- Question generation: blocked
- Reviewed bank: blocked
- Student-facing use: blocked
- Candidate inputs: listed rows approved for future protected-preview planning only
- Source/PDF verification: teacher/project lead visually reviewed the listed candidate rows
- 3.05 pronoun referent tracking: not approved yet
- Expanded 3.02 shoresh list: not approved yet
- Protected preview generation: still blocked until a separate future protected-preview prompt explicitly authorizes it
