# Bereishis 2:18-Bereishis 2:25 Source-to-Skill Map Exceptions Review Packet

This is extraction-accuracy and mapping confirmation for trusted source-derived content. It is not generated-question review, not question approval, not protected-preview approval, not reviewed-bank approval, and not runtime approval.

## A. Scope

- Map file: `data/verified_source_skill_maps/bereishis_2_18_to_2_25_source_to_skill_map.tsv`
- Scope: Bereishis 2:18 through Bereishis 2:25
- Row count: 36 phrase-level rows
- Current status: deterministic pending source-to-skill slice only
- Extraction review status: `pending_yossi_extraction_accuracy_pass`

## B. Source Files Used

- `7984C_b_01409_pshat_of_torah.pdf`
- `data/curriculum_extraction/normalized/batch_003_linear_chumash_bereishis_2_4_to_2_25_pasuk_segments.jsonl`
- `data/curriculum_extraction/raw_sources/batch_003/linear_chumash_bereishis_2_4_to_2_25_cleaned.md`
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
| Bereishis 2:18 | וַיֹּאמֶר יְהוָה אֱלֹהִים | and Hashem said | phrase_translation | pending, non-runtime |
| Bereishis 2:20 | לְכָל הַבְּהֵמָה וּלְעוֹף הַשָּׁמַיִם | to all the domestic animals and to the birds of the sky | phrase_translation | pending, non-runtime |
| Bereishis 2:21 | וַיִּקַּח אַחַת מִצַּלְעֹתָיו | and He took one of his sides | phrase_translation | pending, non-runtime |
| Bereishis 2:23 | וַיֹּאמֶר הָאָדָם | and the person said | phrase_translation | pending, non-runtime |
| Bereishis 2:25 | וְלֹא יִתְבֹּשָׁשׁוּ | and they would not become embarrassed | phrase_translation | pending, non-runtime |

## F. Rows With Uncertainty

All rows currently carry an uncertainty reason because morphology, Zekelman Standard mapping, difficulty, and question-type eligibility are not safely consolidated at row level yet.

| Ref | Hebrew phrase | Uncertainty reason |
|---|---|---|
| Bereishis 2:18 | וַיֹּאמֶר יְהוָה אֱלֹהִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:18 | לֹא טוֹב | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:18 | הֱיוֹת הָאָדָם לְבַדּוֹ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:18 | אֶעֱשֶׂה לּוֹ עֵזֶר כְּנֶגְדּוֹ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | וַיִּצֶר יְהוָה אֱלֹהִים מִן הָאֲדָמָה | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | כָּל חַיַּת הַשָּׂדֶה | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | וְאֵת כָּל עוֹף הַשָּׁמַיִם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | וַיָּבֵא אֶל הָאָדָם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | לִרְאוֹת מַה יִּקְרָא לוֹ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | וְכֹל אֲשֶׁר יִקְרָא לוֹ הָאָדָם נֶפֶשׁ חַיָּה | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## F1. High-Risk Rows Needing Yossi Review

These rows were selected because they have long English explanations, parenthetical wording, or long Hebrew phrase boundaries. They are not unsafe; they are the rows most worth checking before any future extraction verification.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 2:18 | אֶעֱשֶׂה לּוֹ עֵזֶר כְּנֶגְדּוֹ | I will make for him a helper opposite him | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | וְכֹל אֲשֶׁר יִקְרָא לוֹ הָאָדָם נֶפֶשׁ חַיָּה | and any live soul that the person will call to him (a name) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | וַיִּצֶר יְהוָה אֱלֹהִים מִן הָאֲדָמָה | and Hashem formed from the ground | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:20 | לְכָל הַבְּהֵמָה וּלְעוֹף הַשָּׁמַיִם | to all the domestic animals and to the birds of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:21 | וַיִּסְגֹּר בָּשָׂר תַּחְתֶּנָּה | and He closed flesh under (in place of) her (the missing side) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:21 | וַיִּקַּח אַחַת מִצַּלְעֹתָיו | and He took one of his sides | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:21 | וַיַּפֵּל יְהוָה אֱלֹהִים תַּרְדֵּמָה עַל הָאָדָם | and Hashem caused a deep sleep to fall on the person | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:22 | אֶת הַצֵּלָע אֲשֶׁר לָקַח מִן הָאָדָם | the side that He took from the person | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:23 | עֶצֶם מֵעֲצָמַי וּבָשָׂר מִבְּשָׂרִי | bone from my bones and flesh from my flesh | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:25 | וַיִּהְיוּ שְׁנֵיהֶם עֲרוּמִּים | and they were both unclothed | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## G. Missing Translations

No rows are missing Linear phrase translation, Metsudah verse context, or Koren secondary verse context.

## H. Ambiguous Phrase Joins

Rows were generated from existing phrase-level Linear Chumash extraction. Yossi should confirm that each phrase join is faithful to the trusted source before verification.

## H1. Long Parentheticals Needing Review

Yossi should confirm that each parenthetical explanation belongs to the Hebrew phrase shown here, not to a neighboring phrase.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 2:19 | וְכֹל אֲשֶׁר יִקְרָא לוֹ הָאָדָם נֶפֶשׁ חַיָּה | and any live soul that the person will call to him (a name) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:21 | וַיִּסְגֹּר בָּשָׂר תַּחְתֶּנָּה | and He closed flesh under (in place of) her (the missing side) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## H2. Long Hebrew Phrase Boundaries Needing Review

Yossi should confirm that these longer Hebrew phrase boundaries match the source phrase breaks and segment order.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 2:21 | וַיַּפֵּל יְהוָה אֱלֹהִים תַּרְדֵּמָה עַל הָאָדָם | and Hashem caused a deep sleep to fall on the person | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | וְכֹל אֲשֶׁר יִקְרָא לוֹ הָאָדָם נֶפֶשׁ חַיָּה | and any live soul that the person will call to him (a name) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:19 | וַיִּצֶר יְהוָה אֱלֹהִים מִן הָאֲדָמָה | and Hashem formed from the ground | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:20 | לְכָל הַבְּהֵמָה וּלְעוֹף הַשָּׁמַיִם | to all the domestic animals and to the birds of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:22 | אֶת הַצֵּלָע אֲשֶׁר לָקַח מִן הָאָדָם | the side that He took from the person | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:23 | עֶצֶם מֵעֲצָמַי וּבָשָׂר מִבְּשָׂרִי | bone from my bones and flesh from my flesh | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:21 | וַיִּסְגֹּר בָּשָׂר תַּחְתֶּנָּה | and He closed flesh under (in place of) her (the missing side) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:18 | אֶעֱשֶׂה לּוֹ עֵזֶר כְּנֶגְדּוֹ | I will make for him a helper opposite him | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:25 | וַיִּהְיוּ שְׁנֵיהֶם עֲרוּמִּים | and they were both unclothed | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:21 | וַיִּקַּח אַחַת מִצַּלְעֹתָיו | and He took one of his sides | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

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
| Bereishis 2:18 | וַיֹּאמֶר יְהוָה אֱלֹהִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:18 | לֹא טוֹב | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:18 | הֱיוֹת הָאָדָם לְבַדּוֹ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:18 | אֶעֱשֶׂה לּוֹ עֵזֶר כְּנֶגְדּוֹ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:19 | וַיִּצֶר יְהוָה אֱלֹהִים מִן הָאֲדָמָה | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:19 | כָּל חַיַּת הַשָּׂדֶה | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:19 | וְאֵת כָּל עוֹף הַשָּׁמַיִם | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:19 | וַיָּבֵא אֶל הָאָדָם | Keep source-only until separate question/protected-preview gate. |

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
