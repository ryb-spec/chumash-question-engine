# Bereishis 1:24-Bereishis 1:31 Source-to-Skill Map Exceptions Review Packet

This is extraction-accuracy and mapping confirmation for trusted source-derived content. It is not generated-question review, not question approval, not protected-preview approval, not reviewed-bank approval, not runtime approval, and not student-facing approval.

## A. Scope

- Map file: `data/verified_source_skill_maps/bereishis_1_24_to_1_31_source_to_skill_map.tsv`
- Scope: Bereishis 1:24 through Bereishis 1:31
- Row count: 38 phrase-level rows
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
| Bereishis 1:24 | וַיֹּאמֶר אֱלֹקִים | and Hashem said | phrase_translation | pending, non-runtime |
| Bereishis 1:26 | בְּצַלְמֵנוּ כִּדְמוּתֵנוּ | with our form like our likeness | phrase_translation | pending, non-runtime |
| Bereishis 1:28 | פְּרוּ וּרְבוּ וּמִלְאוּ אֶת הָאָרֶץ | be fruitful and multiply and fill up the land | phrase_translation | pending, non-runtime |
| Bereishis 1:29 | אֶת כָּל עֵשֶׂב זֹרֵעַ זֶרַע | all grass which makes seed | phrase_translation | pending, non-runtime |
| Bereishis 1:31 | יוֹם הַשִּׁשִּׁי | the sixth day | phrase_translation | pending, non-runtime |

## F. Rows With Uncertainty

All rows currently carry an uncertainty reason because morphology, Zekelman Standard mapping, difficulty, and question-type eligibility are not safely consolidated at row level yet.

| Ref | Hebrew phrase | Uncertainty reason |
|---|---|---|
| Bereishis 1:24 | וַיֹּאמֶר אֱלֹקִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:24 | תּוֹצֵא הָאָרֶץ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:24 | נֶפֶשׁ חַיָּה לְמִינָהּ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:24 | בְּהֵמָה וָרֶמֶשׂ וְחַיְתוֹ אֶרֶץ לְמִינָהּ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:24 | וַיְהִי כֵן | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | וַיַּעַשׂ אֱלֹקִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | אֶת חַיַּת הָאָרֶץ לְמִינָהּ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | וְאֶת הַבְּהֵמָה לְמִינָהּ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | וְאֵת כָּל רֶמֶשׂ הָאֲדָמָה לְמִינֵהוּ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | וַיַּרְא אֱלֹקִים כִּי טוֹב | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## F1. High-Risk Rows Needing Yossi Review

These rows were selected because they have long English explanations, parenthetical wording, or long Hebrew phrase boundaries. They are not unsafe; they are the rows most worth checking before any future extraction verification.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:24 | בְּהֵמָה וָרֶמֶשׂ וְחַיְתוֹ אֶרֶץ לְמִינָהּ | domestic animals and creepers and wild animals of the land for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | אֶת חַיַּת הָאָרֶץ לְמִינָהּ | the wild animals of the land for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | וְאֵת כָּל רֶמֶשׂ הָאֲדָמָה לְמִינֵהוּ | and all the creepers of the ground for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | וְאֶת הַבְּהֵמָה לְמִינָהּ | and the domestic animals for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:26 | וְיִרְדּוּ בִדְגַת הַיָּם וּבְעוֹף הַשָּׁמַיִם | and they (the people) will rule in the fish of the ocean and the birds of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:26 | וּבַבְּהֵמָה וּבְכָל הָאָרֶץ וּבְכָל הָרֶמֶשׂ הָרֹמֵשׂ עַל הָאָרֶץ | and in the animals and in all the land (the ground itself-to dig etc.) and in all the creepers which creep on the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:27 | וַיִּבְרָא אֱלֹקִים אֶת הָאָדָם בְּצַלְמוֹ | and Hashem created the person with His form | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:28 | וַיְבָרֶךְ אֹתָם אֱלֹקִים וַיֹּאמֶר לָהֶם אֱלֹקִים | and Hashem blessed them and Hashem said to them | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:28 | וּרְדוּ בִּדְגַת הַיָּם וּבְעוֹף הַשָּׁמַיִם | and rule in the fish of the ocean and in the birds of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:29 | וְאֶת כָּל הָעֵץ אֲשֶׁר בּוֹ פְרִי עֵץ זֹרֵעַ זָרַע | and all the trees that in it (is) fruit of a tree (which those fruit) makes seed | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:30 | וּלְכֹל רוֹמֵשׂ עַל הָאָרֶץ אֲשֶׁר בּוֹ נֶפֶשׁ חַיָּה | and for all which creep on the land (including domestic animals), that is in it a live soul | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:31 | וַיַּרְא אֱלֹהִים אֶת כׇּל אֲשֶׁר עָשָׂה | and Hashem saw all that He made | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## G. Missing Translations

No rows are missing Linear phrase translation, Metsudah verse context, or Koren secondary verse context.

## H. Ambiguous Phrase Joins

Rows were generated from existing phrase-level Linear Chumash extraction. Yossi should confirm that each phrase join is faithful to the trusted source before verification.

## H1. Long Parentheticals Needing Review

Yossi should confirm that each parenthetical explanation belongs to the Hebrew phrase shown here, not to a neighboring phrase.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:24 | בְּהֵמָה וָרֶמֶשׂ וְחַיְתוֹ אֶרֶץ לְמִינָהּ | domestic animals and creepers and wild animals of the land for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | אֶת חַיַּת הָאָרֶץ לְמִינָהּ | the wild animals of the land for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | וְאֶת הַבְּהֵמָה לְמִינָהּ | and the domestic animals for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | וְאֵת כָּל רֶמֶשׂ הָאֲדָמָה לְמִינֵהוּ | and all the creepers of the ground for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:26 | וְיִרְדּוּ בִדְגַת הַיָּם וּבְעוֹף הַשָּׁמַיִם | and they (the people) will rule in the fish of the ocean and the birds of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:26 | וּבַבְּהֵמָה וּבְכָל הָאָרֶץ וּבְכָל הָרֶמֶשׂ הָרֹמֵשׂ עַל הָאָרֶץ | and in the animals and in all the land (the ground itself-to dig etc.) and in all the creepers which creep on the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:29 | וְאֶת כָּל הָעֵץ אֲשֶׁר בּוֹ פְרִי עֵץ זֹרֵעַ זָרַע | and all the trees that in it (is) fruit of a tree (which those fruit) makes seed | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:30 | וּלְכֹל רוֹמֵשׂ עַל הָאָרֶץ אֲשֶׁר בּוֹ נֶפֶשׁ חַיָּה | and for all which creep on the land (including domestic animals), that is in it a live soul | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## H2. Long Hebrew Phrase Boundaries Needing Review

Yossi should confirm that these longer Hebrew phrase boundaries match the source phrase breaks and segment order.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:26 | וּבַבְּהֵמָה וּבְכָל הָאָרֶץ וּבְכָל הָרֶמֶשׂ הָרֹמֵשׂ עַל הָאָרֶץ | and in the animals and in all the land (the ground itself-to dig etc.) and in all the creepers which creep on the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:30 | וּלְכֹל רוֹמֵשׂ עַל הָאָרֶץ אֲשֶׁר בּוֹ נֶפֶשׁ חַיָּה | and for all which creep on the land (including domestic animals), that is in it a live soul | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:29 | וְאֶת כָּל הָעֵץ אֲשֶׁר בּוֹ פְרִי עֵץ זֹרֵעַ זָרַע | and all the trees that in it (is) fruit of a tree (which those fruit) makes seed | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:28 | וַיְבָרֶךְ אֹתָם אֱלֹקִים וַיֹּאמֶר לָהֶם אֱלֹקִים | and Hashem blessed them and Hashem said to them | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:26 | וְיִרְדּוּ בִדְגַת הַיָּם וּבְעוֹף הַשָּׁמַיִם | and they (the people) will rule in the fish of the ocean and the birds of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:28 | וּרְדוּ בִּדְגַת הַיָּם וּבְעוֹף הַשָּׁמַיִם | and rule in the fish of the ocean and in the birds of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:24 | בְּהֵמָה וָרֶמֶשׂ וְחַיְתוֹ אֶרֶץ לְמִינָהּ | domestic animals and creepers and wild animals of the land for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:27 | וַיִּבְרָא אֱלֹקִים אֶת הָאָדָם בְּצַלְמוֹ | and Hashem created the person with His form | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:31 | וַיַּרְא אֱלֹהִים אֶת כׇּל אֲשֶׁר עָשָׂה | and Hashem saw all that He made | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:25 | וְאֵת כָּל רֶמֶשׂ הָאֲדָמָה לְמִינֵהוּ | and all the creepers of the ground for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## H3. Awkward But Source-Derived Wording

These rows contain wording that may feel awkward in English but appears to be source-derived from the Linear Chumash extraction. Yossi should confirm the wording is copied/extracted accurately rather than normalized into smoother generated language.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:29 | אֲשֶׁר עַל פְּנֵי כָל הָאָרֶץ | that is on the face of all the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

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
| Bereishis 1:24 | וַיֹּאמֶר אֱלֹקִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:24 | תּוֹצֵא הָאָרֶץ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:24 | נֶפֶשׁ חַיָּה לְמִינָהּ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:24 | בְּהֵמָה וָרֶמֶשׂ וְחַיְתוֹ אֶרֶץ לְמִינָהּ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:24 | וַיְהִי כֵן | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:25 | וַיַּעַשׂ אֱלֹקִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:25 | אֶת חַיַּת הָאָרֶץ לְמִינָהּ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:25 | וְאֶת הַבְּהֵמָה לְמִינָהּ | Keep source-only until separate question/protected-preview gate. |

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
