# Bereishis 3:1-3:7 Yossi Extraction Verification Report

## A. Verification Summary

Yossi reviewed the Bereishis 3:1-3:7 Yossi review sheet and exceptions review packet and verified all 33 phrase-level rows for extraction accuracy.

This verification confirms the source-to-skill extraction only. It does not approve generated questions, question approval, protected-preview status, reviewed-bank status, runtime status, student-facing use, answer choices, or answer keys.

## B. Scope

- Scope: Bereishis 3:1-3:7
- Rows verified: 33
- Source-to-skill map: `data/verified_source_skill_maps/bereishis_3_1_to_3_7_source_to_skill_map.tsv`
- Build report: `data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_source_to_skill_map_build_report.md`
- Exceptions packet: `data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_source_to_skill_map_exceptions_review_packet.md`
- Markdown review sheet: `data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_review_sheet.md`
- CSV review sheet: `data/verified_source_skill_maps/reports/bereishis_3_1_to_3_7_yossi_review_sheet.csv`

## C. What Was Verified

- Hebrew phrase boundaries are acceptable for source-to-skill planning.
- Linear Chumash phrase extraction is acceptable.
- Linear translation alignment is acceptable.
- Metsudah verse context is joined to the correct pesukim.
- Koren secondary context is joined to the correct pesukim where present.
- Parenthetical explanations are acceptable as source-derived wording.
- Dialogue structure and narrative flow are correctly preserved.
- Awkward wording is acceptable as source-derived wording and should not be normalized during this step.
- `phrase_translation` / `translation_context` is an acceptable planning classification for this slice.

## D. High-Risk Rows Accepted

Yossi specifically accepted the following rows as extraction-accurate despite high-risk flags:

| Ref | Hebrew phrase |
| --- | --- |
| Bereishis 3:1 | אַף כִּי אָמַר אֱלֹהִים |
| Bereishis 3:1 | לֹא תֹאכְלוּ מִכֹּל עֵץ הַגָּן |
| Bereishis 3:4 | לֹא מוֹת תְּמֻתוּן |
| Bereishis 3:5 | כִּי בְּיוֹם אֲכָלְכֶם מִמֶּנּוּ |
| Bereishis 3:5 | וִהְיִיתֶם כֵּאלֹהִים |
| Bereishis 3:6 | וְנֶחְמָד הָעֵץ לְהַשְׂכִּיל |
| Bereishis 3:6 | וַתִּתֵּן גַּם לְאִישָׁהּ עִמָּהּ |
| Bereishis 3:7 | וַתִּפָּקַחְנָה עֵינֵי שְׁנֵיהֶם |
| Bereishis 3:7 | וַיֵּדְעוּ כִּי עֵירֻמִּם הֵם |

## E. Yossi Source-Only Note

Yossi marked all 33 rows source-only for future question/protected-preview planning. Dialogue and persuasion language in this slice should not be used for question generation until a later gate.

## F. What Was Not Approved

- Not question approval.
- Not protected-preview approval.
- Not reviewed-bank promotion.
- Not runtime approval.
- Not student-facing release.
- Not generated-question approval.
- Not answer-key approval.

## G. Safety Statuses

- `question_allowed` remains `needs_review`.
- `runtime_allowed` remains `false`.
- `protected_preview_allowed` remains `false`.
- `reviewed_bank_allowed` remains `false`.

## H. Remaining Future Gates

Morphology, Zekelman standards mapping, difficulty, question eligibility, protected-preview eligibility, generated-question review, reviewed-bank promotion, and runtime activation all require separate future passes.

## I. Next Recommended Step

Generate the next safe Bereishis Perek 3 source-to-skill slice using the deterministic builder and Yossi-friendly review workflow.
