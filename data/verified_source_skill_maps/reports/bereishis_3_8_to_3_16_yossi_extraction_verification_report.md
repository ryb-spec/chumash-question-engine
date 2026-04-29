# Bereishis 3:8-3:16 Yossi Extraction Verification Report

## A. Verification Summary

Yossi reviewed the Bereishis 3:8-3:16 Yossi review sheet and exceptions review packet and verified all 48 phrase-level rows for extraction accuracy.

This verification confirms source-to-skill extraction only. It does not approve generated questions, question approval, protected-preview approval, reviewed-bank approval, runtime approval, student-facing use, answer choices, answer keys, or Zekelman standards-specific question use.

## B. Scope

- Scope: Bereishis 3:8-3:16
- Rows verified: 48
- Source-to-skill map: `data/verified_source_skill_maps/bereishis_3_8_to_3_16_source_to_skill_map.tsv`
- Build report: `data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_source_to_skill_map_build_report.md`
- Exceptions packet: `data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_source_to_skill_map_exceptions_review_packet.md`
- Markdown review sheet: `data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_review_sheet.md`
- CSV review sheet: `data/verified_source_skill_maps/reports/bereishis_3_8_to_3_16_yossi_review_sheet.csv`

## C. What Was Verified

- Hebrew phrase boundaries are acceptable for source-to-skill planning.
- Linear Chumash phrase extraction is acceptable.
- Linear translation alignment is acceptable.
- Metsudah verse context is joined to the correct pesukim.
- Koren secondary context is joined to the correct pesukim where present.
- Parenthetical explanations are acceptable as source-derived wording.
- Awkward English wording is source-derived and should not be normalized during this step.
- Dialogue, accountability, curse/consequence language, and narrative flow are correctly preserved as source-derived planning content.
- `phrase_translation` / `translation_context` is an acceptable planning classification for this slice.

## D. High-Risk Rows Accepted

Yossi specifically accepted the following rows as extraction-accurate despite high-risk flags:

| Ref | Hebrew phrase |
| --- | --- |
| Bereishis 3:8 | וַיִּשְׁמְעוּ אֶת קוֹל יְהוָה אֱלֹהִים |
| Bereishis 3:8 | וַיִּתְחַבֵּא הָאָדָם וְאִשְׁתּוֹ |
| Bereishis 3:10 | אֶת קֹלְךָ שָׁמַעְתִּי בַּגָּן |
| Bereishis 3:11 | לְבִלְתִּי אֲכָל מִמֶּנּוּ אָכָלְתָּ |
| Bereishis 3:12 | הָאִשָּׁה אֲשֶׁר נָתַתָּה עִמָּדִי |
| Bereishis 3:13 | וַיֹּאמֶר יְהוָה אֱלֹהִים לָאִשָּׁה |
| Bereishis 3:14 | וַיֹּאמֶר יְהוָה אֱלֹהִים אֶל הַנָּחָשׁ |
| Bereishis 3:14 | מִכָּל הַבְּהֵמָה וּמִכֹּל חַיַּת הַשָּׂדֶה |
| Bereishis 3:15 | וּבֵין זַרְעֲךָ וּבֵין זַרְעָהּ |
| Bereishis 3:15 | הוּא יְשׁוּפְךָ רֹאשׁ |
| Bereishis 3:15 | וְאַתָּה תְּשׁוּפֶנּוּ עָקֵב |
| Bereishis 3:16 | הַרְבָּה אַרְבֶּה עִצְּבוֹנֵךְ וְהֵרֹנֵךְ |

## E. Yossi Source-Only Note

Yossi marked all 48 rows source-only for future question/protected-preview planning. This slice must not be used for generated questions until a separate question eligibility gate.

## F. What Was Not Approved

- Not question approval.
- Not protected-preview approval.
- Not reviewed-bank promotion.
- Not runtime approval.
- Not student-facing release.
- Not generated-question approval.
- Not answer-key approval.
- Not Zekelman standards-specific question approval.

## G. Safety Statuses

- `question_allowed` remains `needs_review`.
- `runtime_allowed` remains `false`.
- `protected_preview_allowed` remains `false`.
- `reviewed_bank_allowed` remains `false`.

## H. Remaining Future Gates

Morphology, Zekelman mapping, difficulty, question eligibility, protected-preview eligibility, generated-question review, reviewed-bank promotion, and runtime activation all require separate future passes.

## I. Next Recommended Step

Generate the next safe Bereishis Perek 3 source-to-skill slice using the deterministic builder and Yossi-friendly review workflow.
