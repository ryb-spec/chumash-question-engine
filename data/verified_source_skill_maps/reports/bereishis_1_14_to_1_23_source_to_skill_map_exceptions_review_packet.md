# Bereishis 1:14-Bereishis 1:23 Source-to-Skill Map Exceptions Review Packet

This is extraction-accuracy and mapping confirmation for trusted source-derived content. It is not generated-question review, not question approval, not protected-preview approval, not reviewed-bank approval, and not runtime approval.

## A. Scope

- Map file: `data/verified_source_skill_maps/bereishis_1_14_to_1_23_source_to_skill_map.tsv`
- Scope: Bereishis 1:14 through Bereishis 1:23
- Row count: 39 phrase-level rows
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
| Bereishis 1:14 | וַיֹּאמֶר אֱלֹקִים | and Hashem said | phrase_translation | pending, non-runtime |
| Bereishis 1:16 | וְאֵת הַכּוֹכָבִים | and the stars | phrase_translation | pending, non-runtime |
| Bereishis 1:18 | וַיַּרְא אֱלֹקִים כִּי טוֹב | and Hashem saw that it was good (to continue as such) | phrase_translation | pending, non-runtime |
| Bereishis 1:20 | עַל פְּנֵי רְקִיעַ הַשָּׁמָיִם | on the face of (in front of) the spread of the sky | phrase_translation | pending, non-runtime |
| Bereishis 1:23 | יוֹם חֲמִישִׁי | fifth day | phrase_translation | pending, non-runtime |

## F. Rows With Uncertainty

All rows currently carry an uncertainty reason because morphology, Zekelman Standard mapping, difficulty, and question-type eligibility are not safely consolidated at row level yet.

| Ref | Hebrew phrase | Uncertainty reason |
|---|---|---|
| Bereishis 1:14 | וַיֹּאמֶר אֱלֹקִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | יְהִי מְאֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | לְהַבְדִּיל בֵּין הַיּוֹם וּבֵין הַלָּיְלָה | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | וְהָיוּ לְאֹתֹת | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | וּלְמוֹעֲדִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | וּלְיָמִים וְשָׁנִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:15 | וְהָיוּ לִמְאוֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:15 | לְהָאִיר עַל הָאָרֶץ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:15 | וַיְהִי כֵן | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:16 | וַיַּעַשׂ אֱלֹקִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## F1. High-Risk Rows Needing Yossi Review

These rows were selected because they have long English explanations, parenthetical wording, or long Hebrew phrase boundaries. They are not unsafe; they are the rows most worth checking before any future extraction verification.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:14 | וְהָיוּ לְאֹתֹת | and they (the luminaries) will be for signs (e.g. an eclipse is a bad sign) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | וּלְיָמִים וְשָׁנִים | and for days and years (a sun year is a year and a moon year is a month) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | יְהִי מְאֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | there should be luminaries in the spread of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | לְהַבְדִּיל בֵּין הַיּוֹם וּבֵין הַלָּיְלָה | to separate between the day and between the night | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:15 | וְהָיוּ לִמְאוֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | and they will be for luminaries in the spread of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:16 | אֶת הַמָּאוֹר הַגָּדֹל לְמֶמְשֶׁלֶת הַיּוֹם | the big luminary for the rulership of the day | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:16 | אֶת שְׁנֵי הַמְּאֹרֹת הַגְּדֹלִים | the two big luminaries | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:16 | וְאֶת הַמָּאוֹר הַקָּטֹן לְמֶמְשֶׁלֶת הַלָּיְלָה | and the small(er) luminary for the rulership of the night | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:18 | וּלְהַבְדִּיל בֵּין הָאוֹר וּבֵין הַחֹשֶׁךְ | and to separate between the light and between the darkness | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:20 | וְעוֹף יְעוֹפֵף עַל הָאָרֶץ | and (the water should also make) a bird (which) will fly on the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:20 | שֶׁרֶץ נֶפֶשׁ חַיָּה | (things which move without legs or that the leg movements are unnoticeable) a live soul | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:21 | אֲשֶׁר שָׁרְצוּ הַמַּיִם לְמִינֵהֶם | that the water made for (the continuation of) their types (each one was able to have children of its own species) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:21 | וְאֵת כָּל נֶפֶשׁ הַחַיָּה הָרֹמֶשֶׂת | and all the (creatures containing) live souls which creep | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:21 | וְאֵת כָּל עוֹף כָּנָף לְמִינֵהוּ | and all winged birds for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:22 | וּמִלְאוּ אֶת הַמַּיִם בַּיַּמִּים | and fill up the water in the oceans | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:22 | פְּרוּ וּרְבוּ | be fruitful (have children) and multiply (have multiple children) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## G. Missing Translations

No rows are missing Linear phrase translation, Metsudah verse context, or Koren secondary verse context.

## H. Ambiguous Phrase Joins

Rows were generated from existing phrase-level Linear Chumash extraction. Yossi should confirm that each phrase join is faithful to the trusted source before verification.

## H1. Long Parentheticals Needing Review

Yossi should confirm that each parenthetical explanation belongs to the Hebrew phrase shown here, not to a neighboring phrase.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:14 | וְהָיוּ לְאֹתֹת | and they (the luminaries) will be for signs (e.g. an eclipse is a bad sign) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | וּלְיָמִים וְשָׁנִים | and for days and years (a sun year is a year and a moon year is a month) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:16 | וְאֶת הַמָּאוֹר הַקָּטֹן לְמֶמְשֶׁלֶת הַלָּיְלָה | and the small(er) luminary for the rulership of the night | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:20 | שֶׁרֶץ נֶפֶשׁ חַיָּה | (things which move without legs or that the leg movements are unnoticeable) a live soul | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:20 | וְעוֹף יְעוֹפֵף עַל הָאָרֶץ | and (the water should also make) a bird (which) will fly on the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:21 | וְאֵת כָּל נֶפֶשׁ הַחַיָּה הָרֹמֶשֶׂת | and all the (creatures containing) live souls which creep | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:21 | אֲשֶׁר שָׁרְצוּ הַמַּיִם לְמִינֵהֶם | that the water made for (the continuation of) their types (each one was able to have children of its own species) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:21 | וְאֵת כָּל עוֹף כָּנָף לְמִינֵהוּ | and all winged birds for (the continuation of) its type | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:22 | פְּרוּ וּרְבוּ | be fruitful (have children) and multiply (have multiple children) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## H2. Long Hebrew Phrase Boundaries Needing Review

Yossi should confirm that these longer Hebrew phrase boundaries match the source phrase breaks and segment order.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:16 | וְאֶת הַמָּאוֹר הַקָּטֹן לְמֶמְשֶׁלֶת הַלָּיְלָה | and the small(er) luminary for the rulership of the night | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | לְהַבְדִּיל בֵּין הַיּוֹם וּבֵין הַלָּיְלָה | to separate between the day and between the night | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:16 | אֶת הַמָּאוֹר הַגָּדֹל לְמֶמְשֶׁלֶת הַיּוֹם | the big luminary for the rulership of the day | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:18 | וּלְהַבְדִּיל בֵּין הָאוֹר וּבֵין הַחֹשֶׁךְ | and to separate between the light and between the darkness | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:15 | וְהָיוּ לִמְאוֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | and they will be for luminaries in the spread of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:21 | וְאֵת כָּל נֶפֶשׁ הַחַיָּה הָרֹמֶשֶׂת | and all the (creatures containing) live souls which creep | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:14 | יְהִי מְאֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | there should be luminaries in the spread of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:21 | אֲשֶׁר שָׁרְצוּ הַמַּיִם לְמִינֵהֶם | that the water made for (the continuation of) their types (each one was able to have children of its own species) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:22 | וּמִלְאוּ אֶת הַמַּיִם בַּיַּמִּים | and fill up the water in the oceans | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:16 | אֶת שְׁנֵי הַמְּאֹרֹת הַגְּדֹלִים | the two big luminaries | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## H3. Awkward But Source-Derived Wording

These rows contain wording that may feel awkward in English but appears to be source-derived from the Linear Chumash extraction. Yossi should confirm the wording is copied/extracted accurately rather than normalized into smoother generated language.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 1:14 | יְהִי מְאֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | there should be luminaries in the spread of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:15 | וְהָיוּ לִמְאוֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | and they will be for luminaries in the spread of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:16 | אֶת הַמָּאוֹר הַגָּדֹל לְמֶמְשֶׁלֶת הַיּוֹם | the big luminary for the rulership of the day | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:16 | וְאֶת הַמָּאוֹר הַקָּטֹן לְמֶמְשֶׁלֶת הַלָּיְלָה | and the small(er) luminary for the rulership of the night | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:17 | בִּרְקִיעַ הַשָּׁמָיִם | in the spread of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:20 | עַל פְּנֵי רְקִיעַ הַשָּׁמָיִם | on the face of (in front of) the spread of the sky | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 1:21 | אֲשֶׁר שָׁרְצוּ הַמַּיִם לְמִינֵהֶם | that the water made for (the continuation of) their types (each one was able to have children of its own species) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

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
| Bereishis 1:14 | וַיֹּאמֶר אֱלֹקִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:14 | יְהִי מְאֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:14 | לְהַבְדִּיל בֵּין הַיּוֹם וּבֵין הַלָּיְלָה | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:14 | וְהָיוּ לְאֹתֹת | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:14 | וּלְמוֹעֲדִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:14 | וּלְיָמִים וְשָׁנִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:15 | וְהָיוּ לִמְאוֹרֹת בִּרְקִיעַ הַשָּׁמַיִם | Keep source-only until separate question/protected-preview gate. |
| Bereishis 1:15 | לְהָאִיר עַל הָאָרֶץ | Keep source-only until separate question/protected-preview gate. |

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
