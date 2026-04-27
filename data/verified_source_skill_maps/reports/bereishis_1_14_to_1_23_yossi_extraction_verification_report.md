# Bereishis 1:14-1:23 Yossi Extraction Verification Report

## Verification Summary

Yossi reviewed and verified all 39 rows in the Bereishis 1:14-1:23 source-to-skill map for extraction accuracy.

This is extraction-accuracy verification for trusted source-derived planning rows only.

## Scope

- Scope: Bereishis 1:14-1:23
- Map file: `data/verified_source_skill_maps/bereishis_1_14_to_1_23_source_to_skill_map.tsv`
- Rows verified: 39 phrase-level rows
- Review packet: `data/verified_source_skill_maps/reports/bereishis_1_14_to_1_23_source_to_skill_map_exceptions_review_packet.md`

## What Was Verified

- Hebrew phrase boundaries are acceptable for source-to-skill planning.
- Linear Chumash phrase extraction is acceptable.
- Linear translation alignment is acceptable.
- Metsudah verse context is joined to the correct pesukim.
- Koren secondary context is joined to the correct pesukim.
- Parenthetical explanations are acceptable as source-derived wording.
- Awkward English wording should be preserved as source-derived wording, not normalized during this step.
- `phrase_translation` / `translation_context` is an acceptable planning classification for this slice.

## High-Risk Rows Specifically Accepted

- Bereishis 1:14 | `וְהָיוּ לְאֹתֹת`
- Bereishis 1:14 | `וּלְיָמִים וְשָׁנִים`
- Bereishis 1:14 | `יְהִי מְאֹרֹת בִּרְקִיעַ הַשָּׁמַיִם`
- Bereishis 1:14 | `לְהַבְדִּיל בֵּין הַיּוֹם וּבֵין הַלָּיְלָה`
- Bereishis 1:15 | `וְהָיוּ לִמְאוֹרֹת בִּרְקִיעַ הַשָּׁמַיִם`
- Bereishis 1:16 | `אֶת שְׁנֵי הַמְּאֹרֹת הַגְּדֹלִים`
- Bereishis 1:16 | `אֶת הַמָּאוֹר הַגָּדֹל לְמֶמְשֶׁלֶת הַיּוֹם`
- Bereishis 1:16 | `וְאֶת הַמָּאוֹר הַקָּטֹן לְמֶמְשֶׁלֶת הַלָּיְלָה`
- Bereishis 1:18 | `וּלְהַבְדִּיל בֵּין הָאוֹר וּבֵין הַחֹשֶׁךְ`
- Bereishis 1:20 | `וְעוֹף יְעוֹפֵף עַל הָאָרֶץ`
- Bereishis 1:20 | `שֶׁרֶץ נֶפֶשׁ חַיָּה`
- Bereishis 1:21 | `אֲשֶׁר שָׁרְצוּ הַמַּיִם לְמִינֵהֶם`
- Bereishis 1:21 | `וְאֵת כָּל נֶפֶשׁ הַחַיָּה הָרֹמֶשֶׂת`
- Bereishis 1:21 | `וְאֵת כָּל עוֹף כָּנָף לְמִינֵהוּ`
- Bereishis 1:22 | `וּמִלְאוּ אֶת הַמַּיִם בַּיַּמִּים`
- Bereishis 1:22 | `פְּרוּ וּרְבוּ`

## What Was Not Approved

- Not question approval.
- Not protected-preview approval.
- Not reviewed-bank approval.
- Not runtime approval.
- Not student-facing release.
- Not generated-question approval.
- Not answer-choice approval.
- Not answer-key approval.
- Not Zekelman standards-specific question use.

## Safety Statuses

- `question_allowed` remains `needs_review`.
- `runtime_allowed` remains `false`.
- `protected_preview_allowed` remains `false`.
- `reviewed_bank_allowed` remains `false`.

No row is marked ready for questions, protected preview, reviewed bank, runtime, or student-facing use.

## Still Requiring Future Passes

- Morphology still requires a separate future pass.
- Zekelman standards mapping still requires a separate future pass.
- Difficulty still requires a separate future pass.
- Question eligibility still requires a separate future gate.

## Next Recommended Step

Generate the next safe contiguous source-to-skill slice after Bereishis 1:23 using the deterministic builder script, with conservative statuses and a fresh exceptions review packet for Yossi.
