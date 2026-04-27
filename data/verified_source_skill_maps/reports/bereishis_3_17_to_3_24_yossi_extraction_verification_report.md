# Bereishis 3:17-3:24 Yossi Extraction Verification Report

## A. Verification Summary

Yossi reviewed the Bereishis 3:17-3:24 Yossi review sheet and exceptions review packet and verified all 38 phrase-level rows for extraction accuracy.

This verification confirms source-to-skill extraction only. It does not approve generated questions, question approval, protected-preview approval, reviewed-bank approval, runtime approval, student-facing use, answer choices, answer keys, or Zekelman standards-specific question use.

## B. Scope

- Scope: Bereishis 3:17-3:24
- Rows verified: 38
- Source-to-skill map: `data/verified_source_skill_maps/bereishis_3_17_to_3_24_source_to_skill_map.tsv`
- Build report: `data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_source_to_skill_map_build_report.md`
- Exceptions packet: `data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_source_to_skill_map_exceptions_review_packet.md`
- Markdown review sheet: `data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_review_sheet.md`
- CSV review sheet: `data/verified_source_skill_maps/reports/bereishis_3_17_to_3_24_yossi_review_sheet.csv`

## C. What Was Verified

- Hebrew phrase boundaries are acceptable for source-to-skill planning.
- Linear Chumash phrase extraction is acceptable.
- Linear translation alignment is acceptable.
- Metsudah verse context is joined to the correct pesukim.
- Koren secondary context is joined to the correct pesukim where present.
- Parenthetical explanations are acceptable as source-derived wording.
- Awkward English wording is source-derived and should not be normalized during this step.
- Consequence/exile/Gan Eden closure language is correctly preserved as source-derived planning content.
- `phrase_translation` / `translation_context` is an acceptable planning classification for this slice.

## D. High-Risk Rows Accepted

Yossi specifically accepted the following rows as extraction-accurate despite high-risk flags:

| Ref | Hebrew phrase |
| --- | --- |
| Bereishis 3:17 | כִּי שָׁמַעְתָּ לְקוֹל אִשְׁתֶּךָ |
| Bereishis 3:17 | אֲרוּרָה הָאֲדָמָה בַּעֲבוּרֶךָ |
| Bereishis 3:18 | וְקוֹץ וְדַרְדַּר תַּצְמִיחַ לָךְ |
| Bereishis 3:19 | עַד שׁוּבְךָ אֶל הָאֲדָמָה |
| Bereishis 3:19 | וְאֶל עָפָר תָּשׁוּב |
| Bereishis 3:20 | וַיִּקְרָא הָאָדָם שֵׁם אִשְׁתּוֹ |
| Bereishis 3:22 | הֵן הָאָדָם הָיָה כְּאַחַד מִמֶּנּוּ |
| Bereishis 3:23 | וַיְשַׁלְּחֵהוּ יְהוָה אֱלֹהִים מִגַּן עֵדֶן |
| Bereishis 3:24 | וַיַּשְׁכֵּן מִקֶּדֶם לְגַן עֵדֶן |
| Bereishis 3:24 | וְאֵת לַהַט הַחֶרֶב הַמִּתְהַפֶּכֶת |
| Bereishis 3:24 | לִשְׁמֹר אֶת דֶּרֶךְ עֵץ הַחַיִּים |

## E. Yossi Source-Only Note

Yossi marked all 38 rows source-only for future question/protected-preview planning. This slice must not be used for generated questions until a separate question eligibility gate.

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

Create a Bereishis Perek 3 source-to-skill completion report after confirming all Perek 3 slices are extraction-verified and safety-closed.
