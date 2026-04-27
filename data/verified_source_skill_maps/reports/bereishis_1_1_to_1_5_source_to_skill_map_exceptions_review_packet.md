# Bereishis 1:1-Bereishis 1:5 Source-to-Skill Map Exceptions Review Packet

This is extraction-accuracy and mapping confirmation for trusted source-derived content. It is not generated-question review, not question approval, not protected-preview approval, not reviewed-bank approval, and not runtime approval.

## A. Scope

- Map file: `data/verified_source_skill_maps/bereishis_1_1_to_1_5_source_to_skill_map.tsv`
- Scope: Bereishis 1:1 through Bereishis 1:5
- Row count: 23 phrase-level rows
- Current status: deterministic pending source-to-skill slice only
- Extraction review status: `pending_yossi_extraction_accuracy_pass`

## B. Source Files Used

- `7984C_b_01409_pshat_of_torah.pdf`
- `data/curriculum_extraction/normalized/linear_chumash_bereishis_1_1_to_1_5_pasuk_segments.seed.jsonl`
- `data/curriculum_extraction/raw_sources/batch_001/bacharach_shemos_prefix_suffix_perek_1_1_to_7_cleaned.md`
- `data/curriculum_extraction/raw_sources/batch_001/bacharach_vaeira_textual_skills_perek_6_cleaned.md`
- `data/curriculum_extraction/raw_sources/batch_001/linear_chumash_bereishis_1_1_to_1_5_cleaned.md`
- `data/curriculum_extraction/raw_sources/batch_001/pasuk_coming_to_teach_sample_answer_key_cleaned.md`
- `data/curriculum_extraction/raw_sources/batch_001/vocabulary_priority_pack_cleaned.md`
- `data/source_texts/translations/sefaria/bereishis_english_koren.jsonl`
- `data/source_texts/translations/sefaria/bereishis_english_metsudah.jsonl`

## C. What Yossi Is Confirming

Yossi is confirming:

- the Linear Chumash phrase extraction matches the trusted source
- Hebrew phrase text is faithful enough for source-derived planning
- Metsudah verse translation context was joined to the correct pasuk
- Koren secondary noncommercial context was joined to the correct pasuk
- `phrase_translation` / `translation_context` classification is reasonable
- uncertainty fields correctly identify what is not yet safe to use

## D. What Yossi Is Not Approving

This packet does not approve:

- generated questions
- answer choices
- answer keys
- protected preview generation
- reviewed-bank promotion
- runtime activation
- student-facing use
- commercial use of Koren

## E. Representative Clean Rows

| Ref | Hebrew phrase | Linear translation | Skill | Safety |
|---|---|---|---|---|
| Bereishis 1:1 | בראשית | in the beginning | phrase_translation | pending, non-runtime |
| Bereishis 1:2 | על פני תהום | on the face of the deep waters | phrase_translation | pending, non-runtime |
| Bereishis 1:3 | ויאמר אלקים | and Hashem said | phrase_translation | pending, non-runtime |
| Bereishis 1:4 | כי טוב | that it was good | phrase_translation | pending, non-runtime |
| Bereishis 1:5 | יום אחד | one day | phrase_translation | pending, non-runtime |

## F. Rows With Uncertainty

All rows currently carry an uncertainty reason because morphology, Zekelman Standard mapping, difficulty, and question-type eligibility are not safely consolidated at row level yet.

| Ref | Hebrew phrase | Uncertainty reason |
|---|---|---|
| Bereishis 1:1 | בראשית | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:1 | ברא אלקים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:1 | את השמים ואת הארץ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | והארץ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | היתה | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | תהו ובהו | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | וחשך | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | על פני תהום | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | ורוח אלקים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | מרחפת | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |

## F1. High-Risk Rows Needing Yossi Review

These rows were selected because they have long English explanations, parenthetical wording, or long Hebrew phrase boundaries. They are not unsafe; they are the rows most worth checking before any future extraction verification.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:1 | את השמים ואת הארץ | the sky and the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | על פני המים | on the face of the waters | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | על פני תהום | on the face of the deep waters | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:3 | ויאמר אלקים | and Hashem said | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:4 | בין האור ובין החשך | between the light and between the darkness | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:4 | ויבדל אלקים | and Hashem separated | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:4 | וירא אלקים את האור | and Hashem saw the light | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:5 | ויהי ערב ויהי בקר | and it was evening and it was morning | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:5 | ויקרא אלקים | and Hashem called | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:5 | ולחשך קרא לילה | and to the darkness He called night | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |

## G. Missing Translations

No rows are missing Linear phrase translation, Metsudah verse context, or Koren secondary verse context.

## H. Ambiguous Phrase Joins

Rows were generated from existing phrase-level Linear Chumash extraction. Yossi should confirm that each phrase join is faithful to the trusted source before verification.

## H1. Long Parentheticals Needing Review

Yossi should confirm that each parenthetical explanation belongs to the Hebrew phrase shown here, not to a neighboring phrase.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
No long parenthetical rows were detected.

## H2. Long Hebrew Phrase Boundaries Needing Review

Yossi should confirm that these longer Hebrew phrase boundaries match the source phrase breaks and segment order.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:4 | וירא אלקים את האור | and Hashem saw the light | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:4 | בין האור ובין החשך | between the light and between the darkness | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:1 | את השמים ואת הארץ | the sky and the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:5 | ויהי ערב ויהי בקר | and it was evening and it was morning | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:5 | ולחשך קרא לילה | and to the darkness He called night | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | על פני תהום | on the face of the deep waters | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | על פני המים | on the face of the waters | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:3 | ויאמר אלקים | and Hashem said | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:4 | ויבדל אלקים | and Hashem separated | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:5 | ויקרא אלקים | and Hashem called | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |

## H3. Awkward But Source-Derived Wording

These rows contain wording that may feel awkward in English but appears to be source-derived from the Linear Chumash extraction. Yossi should confirm the wording is copied/extracted accurately rather than normalized into smoother generated language.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:2 | על פני תהום | on the face of the deep waters | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |
| Bereishis 1:2 | על פני המים | on the face of the waters | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. |

## I. Missing Or Uncertain Morphology

Shoresh, prefixes, suffixes, tense, part of speech, and dikduk-feature fields are intentionally blank. The builder does not invent morphology.

## J. Skill Mapping Questions

Current mapping:

- `skill_primary`: `phrase_translation`
- `skill_secondary`: `translation_context`
- `skill_id`: `phrase_translation`

Question for Yossi/project lead: Is this the correct planning classification for these phrase-level Linear Chumash rows before any future protected preview work?

## K. Standards Mapping Questions

Zekelman Standard mapping is intentionally blank. A separate standards-mapping pass is needed before these rows can support standards-specific protected-preview planning.

## L. Rows Recommended As Source-Only

| Ref | Hebrew phrase | Recommendation |
|---|---|---|
| Bereishis 1:1 | בראשית | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:1 | ברא אלקים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:1 | את השמים ואת הארץ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:2 | והארץ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:2 | היתה | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:2 | תהו ובהו | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:2 | וחשך | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:2 | על פני תהום | Keep source-only until separate question/protected-preview gate. |

All rows should remain source-only until Yossi extraction verification and a later explicit question/protected-preview gate.

## M. Safety Status Summary

- Runtime: blocked
- Question generation: blocked
- Question-ready status: blocked
- Protected preview: blocked
- Reviewed bank: blocked
- Student-facing use: blocked

## N. Recommended Next Action

Yossi should review this packet for extraction accuracy and mapping reasonableness. If all rows are accurate, run a separate verification-recording task that marks only this slice `yossi_extraction_verified` while keeping all question/runtime/student-facing gates closed.
