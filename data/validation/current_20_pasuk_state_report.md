# Current 20-Pasuk Validation Report

Date: 2026-04-16

Scope: current local 20-pasuk parsed assessment state, without expanding the dataset.

## Summary

- Parsed pesukim count: 20
- Flow success count: 20 / 20
- Flow failure count: 0
- Token occurrences: 243
- Unique parsed surface forms: 116
- Translation review records: 204
- Parser/UI/scoring changes in this pass: none

Question type counts across successful flows:

| Question type | Count |
|---|---:|
| word_meaning | 20 |
| prefix_suffix | 20 |
| verb_tense | 20 |
| subject_identification | 17 |
| shoresh | 3 |

## Reproducibility Risk

The parsed dataset is not fully reproducible from the current local source file alone.

`data/source/bereishis_1_1_to_4_20.json` currently has corrupted literal `?` text for Bereishis 1:11-1:20, while `data/pesukim_100.json` contains repaired Hebrew text with nekudos for those same pesukim.

If the parser dataset is regenerated from the current source file as-is, Bereishis 1:11-1:20 will regress to corrupted `?` tokens and the 20/20 flow-success state will not be preserved.

## Parsed-Only Repairs

The following parsed pesukim/tokens are repaired only in parsed data at this time. They are not reproducible from the current source file until the source text is repaired upstream.

- Bereishis 1:11: וַיֹּאמֶר, אֱלֹקִים, תַּדְשֵׁא, הָאָרֶץ, דֶּשֶׁא, עֵשֶׂב, מַזְרִיעַ, זֶרַע, עֵץ, פְּרִי, עֹשֶׂה, פְּרִי, לְמִינוֹ, אֲשֶׁר, זַרְעוֹ, בוֹ, עַל, הָאָרֶץ, וַיְהִי, כֵן
- Bereishis 1:12: וַתּוֹצֵא, הָאָרֶץ, דֶּשֶׁא, עֵשֶׂב, מַזְרִיעַ, זֶרַע, לְמִינֵהוּ, וְעֵץ, עֹשֶׂה, פְּרִי, אֲשֶׁר, זַרְעוֹ, בוֹ, לְמִינֵהוּ, וַיַּרְא, אֱלֹקִים, כִּי, טוֹב
- Bereishis 1:13: וַיְהִי, עֶרֶב, וַיְהִי, בֹקֶר, יוֹם, שְׁלִישִׁי
- Bereishis 1:14: וַיֹּאמֶר, אֱלֹקִים, יְהִי, מְאֹרֹת, בִּרְקִיעַ, הַשָּׁמַיִם, לְהַבְדִּיל, בֵּין, הַיּוֹם, וּבֵין, הַלָּיְלָה, וְהָיוּ, לְאֹתֹת, וּלְמוֹעֲדִים, וּלְיָמִים, וְשָׁנִים
- Bereishis 1:15: וְהָיוּ, לִמְאוֹרֹת, בִּרְקִיעַ, הַשָּׁמַיִם, לְהָאִיר, עַל, הָאָרֶץ, וַיְהִי, כֵן
- Bereishis 1:16: וַיַּעַשׂ, אֱלֹקִים, אֶת, שְׁנֵי, הַמְּאֹרֹת, הַגְּדֹלִים, אֶת, הַמָּאוֹר, הַגָּדֹל, לְמֶמְשֶׁלֶת, הַיּוֹם, וְאֶת, הַמָּאוֹר, הַקָּטֹן, לְמֶמְשֶׁלֶת, הַלָּיְלָה, וְאֵת, הַכּוֹכָבִים
- Bereishis 1:17: וַיִּתֵּן, אֹתָם, אֱלֹקִים, בִּרְקִיעַ, הַשָּׁמָיִם, לְהָאִיר, עַל, הָאָרֶץ
- Bereishis 1:18: וְלִמְשֹׁל, בַּיּוֹם, וּבַלַּיְלָה, וּלְהַבְדִּיל, בֵּין, הָאוֹר, וּבֵין, הַחֹשֶׁךְ, וַיַּרְא, אֱלֹקִים, כִּי, טוֹב
- Bereishis 1:19: וַיְהִי, עֶרֶב, וַיְהִי, בֹקֶר, יוֹם, רְבִיעִי
- Bereishis 1:20: וַיֹּאמֶר, אֱלֹקִים, יִשְׁרְצוּ, הַמַּיִם, שֶׁרֶץ, נֶפֶשׁ, חַיָּה, וְעוֹף, יְעוֹפֵף, עַל, הָאָרֶץ, עַל, פְּנֵי, רְקִיעַ, הַשָּׁמָיִם

## Enrichment Status

Bereishis 1:11-1:20 also include parsed-only enrichment in `data/word_bank.json`, including obvious/high-confidence lemma, shoresh, verb morphology, context translation, semantic group, role hint, and entity type fields.

Examples of parsed-only enrichment:

| Surface | Enrichment |
|---|---|
| תַּדְשֵׁא | shoresh דשא, verb, hifil, future_jussive, "let sprout" |
| וַתּוֹצֵא | shoresh יצא, verb, hifil, vav_consecutive_past, "brought forth" |
| מְאֹרֹת | noun, cosmic_entity, object_candidate, "lights" |
| לְהַבְדִּיל | shoresh בדל, verb, hifil infinitive, "to separate" |
| וְהָיוּ | shoresh היה, verb, future, "and they shall be" |
| וַיִּתֵּן | shoresh נתן, verb, vav_consecutive_past, "placed" |
| וְלִמְשֹׁל | shoresh משל, verb infinitive, "to rule" |
| יִשְׁרְצוּ | shoresh שרץ, verb, future_jussive, "let swarm" |
| יְעוֹפֵף | shoresh עוף, verb, future_jussive, "let fly" |
| הַכּוֹכָבִים | noun, cosmic_entity, object_candidate, "the stars" |

## Authority Recommendation

Recommended model:

1. Source text authority: `data/source/bereishis_1_1_to_4_20.json` should be the upstream authority for exact Torah text and should be repaired to UTF-8 Hebrew for Bereishis 1:11-1:20 before any future full regeneration.
2. Parsed authority: `data/word_bank.json`, `data/word_occurrences.json`, and `data/translation_reviews.json` should hold parsed analysis, morphology, semantic tags, and review workflow metadata.
3. Review discipline: parsed-only enrichment should remain usable for the current assessment state, but human-review-sensitive context translations should stay `needs_review` until approved.

## Known Caveats

- Current 20/20 flow success depends on repaired parsed data, not on the current corrupted source file.
- Some non-selected or low-value tokens may still have generated placeholder-like analyses; current quiz-quality filters avoid using them as weak question sources.
- A future regeneration from source should first repair the source text, then preserve or reapply reviewed parsed authority metadata.
