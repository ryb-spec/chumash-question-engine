# Bereishis 3:8-Bereishis 3:16 Source-to-Skill Map Exceptions Review Packet

This is extraction-accuracy and mapping confirmation for trusted source-derived content. It is not generated-question review, not question approval, not protected-preview approval, not reviewed-bank approval, and not runtime approval.

## A. Scope

- Map file: `data/verified_source_skill_maps/bereishis_3_8_to_3_16_source_to_skill_map.tsv`
- Scope: Bereishis 3:8 through Bereishis 3:16
- Row count: 48 phrase-level rows
- Current status: deterministic pending source-to-skill slice only
- Extraction review status: `pending_yossi_extraction_accuracy_pass`

## B. Source Files Used

- `7984C_b_01409_pshat_of_torah.pdf`
- `data/curriculum_extraction/normalized/batch_004_linear_chumash_bereishis_3_1_to_3_24_pasuk_segments.jsonl`
- `data/curriculum_extraction/raw_sources/batch_004/linear_chumash_bereishis_3_1_to_3_24_cleaned.md`
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
| Bereishis 3:8 | וַיִּשְׁמְעוּ אֶת קוֹל יְהוָה אֱלֹהִים | and they heard the voice of Hashem | phrase_translation | pending, non-runtime |
| Bereishis 3:11 | מִי הִגִּיד לְךָ | who told you | phrase_translation | pending, non-runtime |
| Bereishis 3:12 | מִן הָעֵץ | from the tree | phrase_translation | pending, non-runtime |
| Bereishis 3:14 | כִּי עָשִׂיתָ זֹּאת | because you did this | phrase_translation | pending, non-runtime |
| Bereishis 3:16 | וְהוּא יִמְשָׁל בָּךְ | and he will rule over you | phrase_translation | pending, non-runtime |

## F. Rows With Uncertainty

All rows currently carry an uncertainty reason because morphology, Zekelman Standard mapping, difficulty, and question-type eligibility are not safely consolidated at row level yet.

| Ref | Hebrew phrase | Uncertainty reason |
|---|---|---|
| Bereishis 3:8 | וַיִּשְׁמְעוּ אֶת קוֹל יְהוָה אֱלֹהִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:8 | מִתְהַלֵּךְ בַּגָּן | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:8 | לְרוּחַ הַיּוֹם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:8 | וַיִּתְחַבֵּא הָאָדָם וְאִשְׁתּוֹ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:8 | מִפְּנֵי יְהוָה אֱלֹהִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:8 | בְּתוֹךְ עֵץ הַגָּן | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:9 | וַיִּקְרָא יְהוָה אֱלֹהִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:9 | אֶל הָאָדָם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:9 | וַיֹּאמֶר לוֹ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:9 | אַיֶּכָּה | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## F1. High-Risk Rows Needing Yossi Review

These rows were selected because they have long English explanations, parenthetical wording, or long Hebrew phrase boundaries. They are not unsafe; they are the rows most worth checking before any future extraction verification.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 3:8 | וַיִּשְׁמְעוּ אֶת קוֹל יְהוָה אֱלֹהִים | and they heard the voice of Hashem | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:8 | וַיִּתְחַבֵּא הָאָדָם וְאִשְׁתּוֹ | and the person and his wife hid themselves | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:10 | אֶת קֹלְךָ שָׁמַעְתִּי בַּגָּן | I heard Your voice in the garden | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:11 | לְבִלְתִּי אֲכָל מִמֶּנּוּ אָכָלְתָּ | not to eat from it | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:12 | הָאִשָּׁה אֲשֶׁר נָתַתָּה עִמָּדִי | the woman that You gave to be with me | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:13 | וַיֹּאמֶר יְהוָה אֱלֹהִים לָאִשָּׁה | and Hashem said to the woman | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:14 | וַיֹּאמֶר יְהוָה אֱלֹהִים אֶל הַנָּחָשׁ | and Hashem said to the snake | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:14 | מִכָּל הַבְּהֵמָה וּמִכֹּל חַיַּת הַשָּׂדֶה | from more than all the domestic animals and from more than all the wild animals of the field | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:15 | וּבֵין זַרְעֲךָ וּבֵין זַרְעָהּ | and between your children and her children | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:16 | הַרְבָּה אַרְבֶּה עִצְּבוֹנֵךְ וְהֵרֹנֵךְ | a lot I will make a lot your pain and your pregnancy | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

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
| Bereishis 3:14 | מִכָּל הַבְּהֵמָה וּמִכֹּל חַיַּת הַשָּׂדֶה | from more than all the domestic animals and from more than all the wild animals of the field | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:16 | הַרְבָּה אַרְבֶּה עִצְּבוֹנֵךְ וְהֵרֹנֵךְ | a lot I will make a lot your pain and your pregnancy | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:14 | וַיֹּאמֶר יְהוָה אֱלֹהִים אֶל הַנָּחָשׁ | and Hashem said to the snake | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:8 | וַיִּשְׁמְעוּ אֶת קוֹל יְהוָה אֱלֹהִים | and they heard the voice of Hashem | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:11 | לְבִלְתִּי אֲכָל מִמֶּנּוּ אָכָלְתָּ | not to eat from it | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:13 | וַיֹּאמֶר יְהוָה אֱלֹהִים לָאִשָּׁה | and Hashem said to the woman | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:12 | הָאִשָּׁה אֲשֶׁר נָתַתָּה עִמָּדִי | the woman that You gave to be with me | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:8 | וַיִּתְחַבֵּא הָאָדָם וְאִשְׁתּוֹ | and the person and his wife hid themselves | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:15 | וּבֵין זַרְעֲךָ וּבֵין זַרְעָהּ | and between your children and her children | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 3:10 | אֶת קֹלְךָ שָׁמַעְתִּי בַּגָּן | I heard Your voice in the garden | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## H3. Awkward But Source-Derived Wording

These rows contain wording that may feel awkward in English but appears to be source-derived from the Linear Chumash extraction. Yossi should confirm the wording is copied/extracted accurately rather than normalized into smoother generated language.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
No awkward source-derived wording rows were detected.

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
| Bereishis 3:8 | וַיִּשְׁמְעוּ אֶת קוֹל יְהוָה אֱלֹהִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 3:8 | מִתְהַלֵּךְ בַּגָּן | Keep source-only until separate question/protected-preview gate. |
| Bereishis 3:8 | לְרוּחַ הַיּוֹם | Keep source-only until separate question/protected-preview gate. |
| Bereishis 3:8 | וַיִּתְחַבֵּא הָאָדָם וְאִשְׁתּוֹ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 3:8 | מִפְּנֵי יְהוָה אֱלֹהִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 3:8 | בְּתוֹךְ עֵץ הַגָּן | Keep source-only until separate question/protected-preview gate. |
| Bereishis 3:9 | וַיִּקְרָא יְהוָה אֱלֹהִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 3:9 | אֶל הָאָדָם | Keep source-only until separate question/protected-preview gate. |

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
