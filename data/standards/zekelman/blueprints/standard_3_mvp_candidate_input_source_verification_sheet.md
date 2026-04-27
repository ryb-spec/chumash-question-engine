# Standard 3 MVP Candidate Input Source Verification and Approval Sheet

## 1. Purpose

This sheet is for teacher/project-lead visual verification and item-by-item approval of exact candidate inputs before any protected preview can be unlocked.

It is based on the Standard 3 MVP candidate input lists, the teacher wording/source verification lock file, the teacher input approval packet, the skill-to-question-type map, and the MVP diagnostic blueprint.

Teacher/project lead has visually reviewed the listed candidate rows and the item-level decisions are recorded below. These approvals are for future protected-preview planning only and do not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation.

## 2. Hard Boundaries

- Runtime: blocked
- Question generation: blocked
- Reviewed bank: blocked
- Student-facing use: blocked
- Current artifact: teacher source-verification and input-approval sheet only

This sheet does not authorize generated questions, sample questions, answer choices, answer keys, active templates, runtime activation, UI changes, reviewed-bank promotion, production-data changes, or student-facing use.

## 3. Review Decision Options

Use only these decision options when filling in the Teacher decision column:

- `approve_input`
- `approve_with_revision`
- `reject_input`
- `needs_more_source_review`

The Teacher decision column records the actual item-level decision supplied by the teacher/project lead. Approval on this sheet can support a later lock-file update only; it still does not generate questions or unlock runtime use.

## 4. Candidate Input Verification Tables

### 3.01 Nouns / שמות עצם

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source page/reference if available | What the teacher must visually check | Excluded-content risk? | Recommended default decision | Teacher decision | Teacher notes |
|---|---|---|---|---|---|---|---|---|---|---|
| STD3-01-NOUN-001 | בן | son / a son | 3.01 noun recognition and controlled noun translation | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md` | Rule `DK-NOUN-001`; candidate `lht_cand_noun_implied_indefinite`; Lesson 1; main extracted page 81 / printed p. 160 summary citing pg. 2 | Confirm the Hebrew spelling appears in the cited source, confirm the English meaning matches the source, confirm this is a simple taught noun, and confirm no alternate meaning is being used. | Low if verified; reject or revise if it becomes contextual, untaught, or alternate-meaning work. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |
| STD3-01-NOUN-002 | מלך | king / a king | 3.01 noun recognition and controlled noun translation | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md` | Rule `DK-NOUN-001`; candidate `lht_cand_noun_implied_indefinite`; Lesson 1; main extracted page 81 / printed p. 160 summary citing pg. 2 | Confirm the Hebrew spelling appears in the cited source, confirm the English meaning matches the source, confirm this is a simple taught noun, and confirm it does not require phrase context. | Low if verified; reject or revise if it depends on broad contextual inference. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |
| STD3-01-NOUN-003 | איש | man / a man | 3.01 noun recognition and controlled noun translation | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md` | Rule `DK-CONJ-001`; candidate `lht_cand_prefixed_vav_conjunction`; Lesson 1; main extracted page 81 / printed p. 160 summary citing pg. 3 | Confirm the base noun appears in the cited source, confirm the English meaning, and decide whether this base noun belongs in the approved 3.01 noun list rather than only in the prefix lane. | Medium until teacher confirms it belongs in the 3.01 noun list. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |

### 3.02 Simple Shorashim / שורשים

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source page/reference if available | What the teacher must visually check | Excluded-content risk? | Recommended default decision | Teacher decision | Teacher notes |
|---|---|---|---|---|---|---|---|---|---|---|
| STD3-02-SHORESH-001 | שמר | basic root meaning: guard / keep | 3.02 simple shoresh identification | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`; `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md` | Rules `DK-PARSE-002`, `DK-VERB-PAST-001`, `DK-VERB-FUTURE-001`; candidates `lht_cand_shoresh_added_letters`, `lht_cand_past_tense_markers`, `lht_cand_future_tense_markers`; Lesson 5; main extracted page 81 / printed p. 160 summary citing pgs. 35-36; answer extracted pages 11-12 / Lessons 5-6 | Confirm the root spelling, confirm the basic meaning, confirm that this is suitable as simple shoresh recognition only, and confirm that weak-letter roots, altered roots, and full verb parsing are not being introduced. | Medium. The example is tied to verb forms, so teacher must keep it limited to simple root recognition and not full parsing. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |

Note: the teacher review finding says the current safe candidate appears limited to `שמר`; more simple shorashim are needed before this lane is useful. Expanded 3.02 roots are not included here.

### 3.05 Pronominal Suffix Decoding

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source page/reference if available | What the teacher must visually check | Excluded-content risk? | Recommended default decision | Teacher decision | Teacher notes |
|---|---|---|---|---|---|---|---|---|---|---|
| STD3-05-SUFFIX-001 | ספרי | my book; singular noun with first-person singular possessive suffix | 3.05 pronominal suffix decoding | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`; `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md` | Rule `DK-POSSESSIVE-001`; candidate `lht_cand_possessive_suffix_singular`; Lesson 4; main extracted page 81 / printed p. 161 summary citing pgs. 26-30; answer extracted pages 9-10 / Lesson 4 | Confirm the Hebrew spelling and nekudos if used, confirm the owner meaning, confirm this is a singular noun suffix example, and confirm it does not require context-heavy interpretation. | Low to medium. Keep as suffix decoding only; do not turn it into referent tracking or verb-linked clue work. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |
| STD3-05-SUFFIX-002 | ספרו | his book; singular noun with third-person masculine singular possessive suffix | 3.05 pronominal suffix decoding | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`; `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md` | Rule `DK-POSSESSIVE-001`; candidate `lht_cand_possessive_suffix_singular`; Lesson 4; main extracted page 81 / printed p. 161 summary citing pgs. 26-30; answer extracted pages 9-10 / Lesson 4 | Confirm the Hebrew spelling and nekudos if used, confirm the owner meaning, confirm this is a singular noun suffix example, and confirm it does not depend on ambiguous context. | Low to medium. Keep as suffix decoding only; do not use as verb-linked clue work. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |

### 3.06 Visible Prefixes / Articles

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source page/reference if available | What the teacher must visually check | Excluded-content risk? | Recommended default decision | Teacher decision | Teacher notes |
|---|---|---|---|---|---|---|---|---|---|---|
| STD3-06-PREFIX-001 | הבן | definite article ה; the son | 3.06 visible prefixes/articles | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md` | Rule `DK-ARTICLE-001`; candidate `lht_cand_article_heh`; Lesson 1; main extracted page 81 / printed p. 160 summary citing pg. 2 | Confirm the Hebrew spelling appears in the cited source, confirm ה functions as ה הידיעה here, confirm the English meaning, and confirm no nikud-sensitive distinction is required. | Low if visually verified. Keep limited to visible article recognition. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |
| STD3-06-PREFIX-002 | ואיש | prefixed ו; and a man | 3.06 visible prefixes/articles | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md` | Rule `DK-CONJ-001`; candidate `lht_cand_prefixed_vav_conjunction`; Lesson 1; main extracted page 81 / printed p. 160 summary citing pg. 3 | Confirm the Hebrew spelling appears in the cited source, confirm ו is simple conjunction ו, and confirm this is not ו ההיפוך. | Medium until teacher confirms it is simple ו only. Reject if it requires ו ההיפוך or tense reversal. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |
| STD3-06-PREFIX-003 | למלך | prefixed ל; to the king | 3.06 visible prefixes/articles | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md` | Rule family `DK-PREP-002` through `DK-PREP-007`; candidate `lht_cand_prefix_prepositions`; Lesson 3; main extracted page 8 / Lesson 3 and page 63 / Lesson 14 | Confirm the Hebrew spelling appears in the cited source, confirm ל is a visible/simple prefix, confirm the English meaning, and confirm no context-heavy interpretation is required. | Medium. Keep to visible ל only; reject or revise if it depends on source ambiguity or non-MVP prefix rules. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |
| STD3-06-PREFIX-004 | בבית | prefixed ב; in the house | 3.06 visible prefixes/articles | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md` | Rule family `DK-PREP-002` through `DK-PREP-007`; candidate `lht_cand_prefix_prepositions`; Lesson 3; main extracted page 8 / Lesson 3 and page 63 / Lesson 14 | Confirm the Hebrew spelling appears in the cited source, confirm ב is a visible/simple prefix, confirm the English meaning, and confirm no unverified nikud-sensitive distinction is required. | Medium. Keep to visible ב only; reject or revise if it requires nikud-sensitive interpretation. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |

### 3.07 Foundational Verb Clues

| Item ID | Hebrew item/example | English meaning or feature | Skill lane | Source path | Source page/reference if available | What the teacher must visually check | Excluded-content risk? | Recommended default decision | Teacher decision | Teacher notes |
|---|---|---|---|---|---|---|---|---|---|---|
| STD3-07-VERB-001 | שמרתי | past-tense ending clue; first-person singular meaning in the source artifact | 3.07 foundational verb clues | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md` | Rules `DK-PARSE-002` and `DK-VERB-PAST-001`; candidates `lht_cand_shoresh_added_letters` and `lht_cand_past_tense_markers`; Lesson 5; answer extracted page 11 / Lesson 5 | Confirm the Hebrew spelling appears in the cited source, confirm this is a basic past/person clue, confirm the meaning, and confirm it is not being used for full parsing or advanced translation precision. | Medium. It is safe only if limited to foundational tense/person/form clues. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |
| STD3-07-VERB-002 | שמרו | past-tense plural ending clue | 3.07 foundational verb clues | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md` | Rule `DK-VERB-PAST-001`; candidate `lht_cand_past_tense_markers`; Lesson 5; answer extracted page 11 / Lesson 5 | Confirm the Hebrew spelling appears in the cited source, confirm this is a basic past/plural clue, confirm the meaning or feature, and confirm it does not require full parsing. | Medium. Keep as a basic clue only. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |
| STD3-07-VERB-003 | אשמור | future-tense prefix clue; first-person singular meaning in the source artifact | 3.07 foundational verb clues | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md` | Rules `DK-PARSE-002` and `DK-VERB-FUTURE-001`; candidates `lht_cand_shoresh_added_letters` and `lht_cand_future_tense_markers`; Lesson 5; answer extracted pages 11-12 / Lessons 5-6 | Confirm the Hebrew spelling appears in the cited source, confirm this is a basic future/person clue, confirm the meaning, and confirm it does not generalize to weak-root forms. | Medium. Keep as foundational future clue only; do not use for weak-root or full parsing work. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |
| STD3-07-VERB-004 | תשמרי | future-tense prefix/suffix clue; second-person feminine singular meaning in the source artifact | 3.07 foundational verb clues | `data/dikduk_rules/rules_loshon_foundation.jsonl`; `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`; `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md` | Rule `DK-VERB-FUTURE-001`; candidate `lht_cand_future_tense_markers`; Lesson 5; answer extracted pages 11-12 / Lessons 5-6 | Confirm the Hebrew spelling appears in the cited source, confirm the basic future/person/gender/number clue, confirm the meaning or feature, and confirm this is not advanced parsing. | Medium to high. Include only if teacher confirms this person/gender/number clue is simple enough for MVP preview planning. | `needs_more_source_review` | `approve_input` | Teacher/project lead visually reviewed this item and approves it for future protected-preview planning only. This approval does not authorize runtime activation, student-facing use, reviewed-bank promotion, or general question generation. |

## 5. What the Teacher Must Visually Check

For each row, the teacher/project lead should check:

- Confirm the Hebrew spelling appears in the cited source.
- Confirm the English meaning or grammar feature matches the cited source.
- Confirm the item does not depend on excluded content.
- Confirm the item is simple enough for MVP preview planning.
- Confirm the item belongs in the listed lane and is not being bundled with a different skill.
- Confirm the source/PDF reference is specific enough to support later protected-preview use.

## 6. Blocked / Not Included Lanes

These lanes and areas are not included in the verification tables:

- 3.05 Pronoun Referent Tracking: not approved yet; no safe local referent examples are selected.
- Expanded 3.02 list beyond source-backed candidates: not approved yet; only `שמר` is listed.
- 3.04 Noun/Adjective Features: deferred to later phase.
- 3.04 סמיכות: protected later lane.
- 3.08 Grouping and Word Order: context-sensitive later lane.
- 3.10 Nikud: deferred and not eligible for MVP protected preview.

## 7. Final Approval Summary

Teacher/project-lead summary to complete after visual verification:

- Inputs approved: `STD3-01-NOUN-001`, `STD3-01-NOUN-002`, `STD3-01-NOUN-003`, `STD3-02-SHORESH-001`, `STD3-05-SUFFIX-001`, `STD3-05-SUFFIX-002`, `STD3-06-PREFIX-001`, `STD3-06-PREFIX-002`, `STD3-06-PREFIX-003`, `STD3-06-PREFIX-004`, `STD3-07-VERB-001`, `STD3-07-VERB-002`, `STD3-07-VERB-003`, `STD3-07-VERB-004`
- Inputs approved with revision: none recorded
- Inputs rejected: none recorded
- Inputs needing more source review: none recorded for listed candidate rows
- Lanes still blocked: 3.05 Pronoun Referent Tracking; expanded 3.02 list beyond `שמר`; 3.04 Noun/Adjective Features; 3.04 סמיכות; 3.08 Grouping and Word Order; 3.10 Nikud; any unlisted input item; any future input without explicit teacher approval

Final reminder: approving an input on this sheet can support a later lock-file update, but it still does not authorize question generation, answer-key creation, runtime activation, reviewed-bank promotion, or student-facing use.
