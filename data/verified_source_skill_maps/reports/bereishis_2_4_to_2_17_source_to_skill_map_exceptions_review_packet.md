# Bereishis 2:4-Bereishis 2:17 Source-to-Skill Map Exceptions Review Packet

This is extraction-accuracy and mapping confirmation for trusted source-derived content. It is not generated-question review, not question approval, not protected-preview approval, not reviewed-bank approval, and not runtime approval.

## A. Scope

- Map file: `data/verified_source_skill_maps/bereishis_2_4_to_2_17_source_to_skill_map.tsv`
- Scope: Bereishis 2:4 through Bereishis 2:17
- Row count: 54 phrase-level rows
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
| Bereishis 2:4 | אֵלֶּה | these (mentioned previously are) | phrase_translation | pending, non-runtime |
| Bereishis 2:8 | גַּן בְּעֵדֶן מִקֶּדֶם | a garden in Eiden from East (on the East side of Eiden) | phrase_translation | pending, non-runtime |
| Bereishis 2:10 | וְנָהָר יֹצֵא מֵעֵדֶן | and a river goes out from Eiden | phrase_translation | pending, non-runtime |
| Bereishis 2:12 | שָׁם הַבְּדֹלַח וְאֶבֶן הַשֹּׁהַם | there is the crystal and the Shoham stone | phrase_translation | pending, non-runtime |
| Bereishis 2:17 | מוֹת תָּמוּת | you will die | phrase_translation | pending, non-runtime |

## F. Rows With Uncertainty

All rows currently carry an uncertainty reason because morphology, Zekelman Standard mapping, difficulty, and question-type eligibility are not safely consolidated at row level yet.

| Ref | Hebrew phrase | Uncertainty reason |
|---|---|---|
| Bereishis 2:4 | אֵלֶּה | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:4 | תוֹלְדוֹת | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:4 | הַשָּׁמַיִם וְהָאָרֶץ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:4 | בְּהִבָּרְאָם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:4 | בְּיוֹם עֲשׂוֹת יְהוָה אֱלֹהִים | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:4 | אֶרֶץ וְשָׁמָיִם | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | וְכֹל שִׂיחַ הַשָּׂדֶה | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | טֶרֶם יִהְיֶה בָאָרֶץ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | וְכׇל עֵשֶׂב הַשָּׂדֶה טֶרֶם יִצְמָח | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | כִּי לֹא הִמְטִיר יְהוָה אֱלֹהִים עַל הָאָרֶץ | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## F1. High-Risk Rows Needing Yossi Review

These rows were selected because they have long English explanations, parenthetical wording, or long Hebrew phrase boundaries. They are not unsafe; they are the rows most worth checking before any future extraction verification.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 2:4 | תוֹלְדוֹת | the ones that were born from (made out of or as part of) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | וְאָדָם אַיִן לַעֲבֹד אֶת הָאֲדָמָה | and a person isn't (available) to work the ground | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | וְכׇל עֵשֶׂב הַשָּׂדֶה טֶרֶם יִצְמָח | and all the grass of the field has not yet sprouted | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | כִּי לֹא הִמְטִיר יְהוָה אֱלֹהִים עַל הָאָרֶץ | because Hashem did not cause rain (to come down) on the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:6 | וְהִשְׁקָה אֶת כׇּל פְּנֵי הָאֲדָמָה | and it will water the whole face of the ground | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:7 | וַיִּיצֶר יְהוָה אֱלֹהִים אֶת הָאָדָם | and Hashem formed the person | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:7 | וַיִּפַּח בְּאַפָּיו נִשְׁמַת חַיִּים | and He blew in his nostrils a soul of life | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:8 | גַּן בְּעֵדֶן מִקֶּדֶם | a garden in Eiden from East (on the East side of Eiden) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:9 | וְעֵץ הַדַּעַת טוֹב וָרָע | and the tree of knowledge of (when one eats of it he gets to know the difference between) good and bad | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:9 | וַיַּצְמַח יְהוָה אֱלֹהִים מִן הָאֲדָמָה | and Hashem caused to sprout from the ground | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:9 | נֶחְמָד לְמַרְאֶה וְטוֹב לְמַאֲכָל | geshmak for sight and good for food | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:14 | וְשֵׁם הַנָּהָר הַשְּׁלִישִׁי חִדֶּקֶל | and the name of the third river is Chidekel | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:15 | וַיִּקַּח יְהוָה אֱלֹהִים אֶת הָאָדָם | and Hashem took the person | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:15 | וַיַּנִּחֵהוּ בְגַן עֵדֶן | and He caused him to rest (He placed him) in the garden of Eiden | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## G. Missing Translations

No rows are missing Linear phrase translation, Metsudah verse context, or Koren secondary verse context.

## H. Ambiguous Phrase Joins

Rows were generated from existing phrase-level Linear Chumash extraction. Yossi should confirm that each phrase join is faithful to the trusted source before verification.

## H1. Long Parentheticals Needing Review

Yossi should confirm that each parenthetical explanation belongs to the Hebrew phrase shown here, not to a neighboring phrase.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 2:4 | תוֹלְדוֹת | the ones that were born from (made out of or as part of) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | כִּי לֹא הִמְטִיר יְהוָה אֱלֹהִים עַל הָאָרֶץ | because Hashem did not cause rain (to come down) on the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:8 | גַּן בְּעֵדֶן מִקֶּדֶם | a garden in Eiden from East (on the East side of Eiden) | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:9 | וְעֵץ הַדַּעַת טוֹב וָרָע | and the tree of knowledge of (when one eats of it he gets to know the difference between) good and bad | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:15 | וַיַּנִּחֵהוּ בְגַן עֵדֶן | and He caused him to rest (He placed him) in the garden of Eiden | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## H2. Long Hebrew Phrase Boundaries Needing Review

Yossi should confirm that these longer Hebrew phrase boundaries match the source phrase breaks and segment order.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 2:5 | כִּי לֹא הִמְטִיר יְהוָה אֱלֹהִים עַל הָאָרֶץ | because Hashem did not cause rain (to come down) on the land | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:9 | וַיַּצְמַח יְהוָה אֱלֹהִים מִן הָאֲדָמָה | and Hashem caused to sprout from the ground | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:14 | וְשֵׁם הַנָּהָר הַשְּׁלִישִׁי חִדֶּקֶל | and the name of the third river is Chidekel | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:7 | וַיִּיצֶר יְהוָה אֱלֹהִים אֶת הָאָדָם | and Hashem formed the person | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:7 | וַיִּפַּח בְּאַפָּיו נִשְׁמַת חַיִּים | and He blew in his nostrils a soul of life | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:15 | וַיִּקַּח יְהוָה אֱלֹהִים אֶת הָאָדָם | and Hashem took the person | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | וְכׇל עֵשֶׂב הַשָּׂדֶה טֶרֶם יִצְמָח | and all the grass of the field has not yet sprouted | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:6 | וְהִשְׁקָה אֶת כׇּל פְּנֵי הָאֲדָמָה | and it will water the whole face of the ground | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:5 | וְאָדָם אַיִן לַעֲבֹד אֶת הָאֲדָמָה | and a person isn't (available) to work the ground | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |
| Bereishis 2:9 | נֶחְמָד לְמַרְאֶה וְטוֹב לְמַאֲכָל | geshmak for sight and good for food | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

## H3. Awkward But Source-Derived Wording

These rows contain wording that may feel awkward in English but appears to be source-derived from the Linear Chumash extraction. Yossi should confirm the wording is copied/extracted accurately rather than normalized into smoother generated language.

| Ref | Hebrew phrase | Linear translation | Review reason |
|---|---|---|---|
| Bereishis 2:6 | וְהִשְׁקָה אֶת כׇּל פְּנֵי הָאֲדָמָה | and it will water the whole face of the ground | Yossi extraction-accuracy review pending; morphology fields, Zekelman standard mapping, difficulty, and question-type eligibility are not safely row-level consolidated yet. Source PDF text layer was noisy; phrase alignment needs Yossi extraction review. |

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
| Bereishis 2:4 | אֵלֶּה | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:4 | תוֹלְדוֹת | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:4 | הַשָּׁמַיִם וְהָאָרֶץ | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:4 | בְּהִבָּרְאָם | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:4 | בְּיוֹם עֲשׂוֹת יְהוָה אֱלֹהִים | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:4 | אֶרֶץ וְשָׁמָיִם | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:5 | וְכֹל שִׂיחַ הַשָּׂדֶה | Keep source-only until separate question/protected-preview gate. |
| Bereishis 2:5 | טֶרֶם יִהְיֶה בָאָרֶץ | Keep source-only until separate question/protected-preview gate. |

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
