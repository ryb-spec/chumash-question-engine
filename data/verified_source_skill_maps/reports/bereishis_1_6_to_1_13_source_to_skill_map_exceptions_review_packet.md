# Bereishis 1:6-Bereishis 1:13 Source-to-Skill Map Exceptions Review Packet

This is extraction-accuracy and mapping confirmation for trusted source-derived content. It is not generated-question review, not question approval, not protected-preview approval, not reviewed-bank approval, and not runtime approval.

## A. Scope

- Map file: `data/verified_source_skill_maps/bereishis_1_6_to_1_13_source_to_skill_map.tsv`
- Scope: Bereishis 1:6 through Bereishis 1:13
- Row count: 37 phrase-level rows
- Current status: deterministic pending source-to-skill slice only
- Extraction review status: `pending_yossi_extraction_accuracy_pass`

## B. Source Files Used

- `7984C_b_01409_pshat_of_torah.pdf`
- `data/curriculum_extraction/normalized/batch_002_linear_chumash_bereishis_1_6_to_2_3_pasuk_segments.jsonl`
- `data/curriculum_extraction/raw_sources/batch_002/linear_chumash_bereishis_1_6_to_2_3_cleaned.md`
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
| Bereishis 1:6 | וַיֹּאמֶר אֱלֹקִים | and Hashem said | phrase_translation | pending, non-runtime |
| Bereishis 1:8 | יוֹם שֵׁנִי | second day | phrase_translation | pending, non-runtime |
| Bereishis 1:10 | וַיִּקְרָא אֱלֹקִים לַיַּבָּשָׁה אֶרֶץ | and Hashem called the dry land Eretz | phrase_translation | pending, non-runtime |
| Bereishis 1:11 | עֵץ פְּרִי עֹשֶׂה פְּרִי | fruit tree which makes a fruit | phrase_translation | pending, non-runtime |
| Bereishis 1:13 | יוֹם שְׁלִישִׁי | third day | phrase_translation | pending, non-runtime |

## F. Rows With Uncertainty

All rows currently carry an uncertainty reason because morphology, Zekelman Standard mapping, difficulty, and question-type eligibility are not safely consolidated at row level yet.

| Ref | Hebrew phrase | Uncertainty reason |
|---|---|---|
| Bereishis 1:6 | וַיֹּאמֶר אֱלֹקִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:6 | יְהִי רָקִיעַ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:6 | בְּתוֹךְ הַמָּיִם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:6 | וִיהִי מַבְדִּיל | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:6 | בֵּין מַיִם לָמָיִם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:7 | וַיַּעַשׂ אֱלֹקִים אֶת הָרָקִיעַ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:7 | וַיַּבְדֵּל | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:7 | בֵּין הַמַּיִם אֲשֶׁר מִתַּחַת לָרָקִיעַ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:7 | וּבֵין הַמַּיִם אֲשֶׁר מֵעַל לָרָקִיעַ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:7 | וַיְהִי כֵן | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## G. Missing Translations

No rows are missing Linear phrase translation, Metsudah verse context, or Koren secondary verse context.

## H. Ambiguous Phrase Joins

Rows were generated from existing phrase-level Linear Chumash extraction. Yossi should confirm that each phrase join is faithful to the trusted source before verification.

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
| Bereishis 1:6 | וַיֹּאמֶר אֱלֹקִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:6 | יְהִי רָקִיעַ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:6 | בְּתוֹךְ הַמָּיִם | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:6 | וִיהִי מַבְדִּיל | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:6 | בֵּין מַיִם לָמָיִם | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:7 | וַיַּעַשׂ אֱלֹקִים אֶת הָרָקִיעַ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:7 | וַיַּבְדֵּל | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:7 | בֵּין הַמַּיִם אֲשֶׁר מִתַּחַת לָרָקִיעַ | Keep source-only until separate question/protected-preview gate. |

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
