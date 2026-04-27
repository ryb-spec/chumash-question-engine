# Yossi Source-to-Skill Review Sheet

## Review Summary

- Scope: Bereishis 2:1-2:3
- Source map: `data/verified_source_skill_maps/bereishis_2_1_to_2_3_source_to_skill_map.tsv`
- Source map row count: 9
- Rows needing review in this sheet: 9
- Clean sample rows in this sheet: 0
- Allowed decisions: `verified`, `fix_translation`, `fix_hebrew_phrase`, `fix_phrase_boundary`, `fix_skill_classification`, `source_only`, `block_for_questions`, `needs_follow_up`

Mark each row with one of the allowed decisions. If everything is accurate, use `verified`.

Your job is not to approve questions. Your job is only to confirm whether the source-to-skill extraction is accurate enough to mark this slice extraction-verified. All question, preview, reviewed-bank, runtime, and student-facing gates remain closed.

## What Yossi Is Confirming

- Hebrew phrase text is correct.
- English/source translation is aligned to the correct Hebrew phrase.
- Phrase boundaries and joins are reasonable.
- Parentheticals are attached to the correct phrase.
- Skill/classification is reasonable for source-to-skill planning.
- Any row that should remain source-only is identified.
- Any correction needed before extraction verification is clear.

## What Yossi Is Not Approving

- Not question approval.
- Not protected-preview approval.
- Not reviewed-bank approval.
- Not runtime approval.
- Not student-facing release.
- Not answer-key approval.
- Not generated-question approval.

## Review Rows

| Row ID | Ref | Hebrew phrase | Linear translation | Issue type | What to check | Default | Yossi decision | Notes |
|---|---|---|---|---|---|---|---|---|
| bereishis_2_1_to_2_3_source_to_skill_map_row_002 | Bereishis 2:1 | וְכׇל צְבָאָם | and all their multitudes (all they contained) | long_parenthetical;phrase_boundary_check;source_only_recommended | Confirm the parenthetical belongs to this Hebrew phrase. Confirm Hebrew-English phrase alignment against the trusted source. Keep source-only unless a separate future question/protected-preview gate approves use. | verified |  |  |
| bereishis_2_1_to_2_3_source_to_skill_map_row_009 | Bereishis 2:3 | אֲשֶׁר בָּרָא אֱלֹהִים לַעֲשׂוֹת | that Hashem created (and was supposed) to make (on the seventh day, namely, the person, and instead He made double on the sixth day and ceased on the seventh) | long_parenthetical;awkward_source_wording;phrase_boundary_check;source_only_recommended | Confirm the parenthetical belongs to this Hebrew phrase. Confirm awkward English is source-derived and should remain unchanged. Confirm Hebrew-English phrase alignment against the trusted source. Keep source-only unless a separate future question/protected-preview gate approves use. | verified |  |  |
| bereishis_2_1_to_2_3_source_to_skill_map_row_003 | Bereishis 2:2 | וַיְכַל אֱלֹהִים בַּיּוֹם הַשְּׁבִיעִי מְלַאכְתּוֹ אֲשֶׁר עָשָׂה | and Hashem finished in the seventh day His constructive work that He made | long_hebrew_boundary;phrase_boundary_check;source_only_recommended | Confirm the Hebrew phrase boundary and segment join are reasonable. Confirm Hebrew-English phrase alignment against the trusted source. Keep source-only unless a separate future question/protected-preview gate approves use. | verified |  |  |
| bereishis_2_1_to_2_3_source_to_skill_map_row_006 | Bereishis 2:3 | וַיְבָרֶךְ אֱלֹהִים אֶת יוֹם הַשְּׁבִיעִי וַיְקַדֵּשׁ אֹתוֹ | and Hashem blessed the seventh day and He caused it to be holy | long_hebrew_boundary;phrase_boundary_check;source_only_recommended | Confirm the Hebrew phrase boundary and segment join are reasonable. Confirm Hebrew-English phrase alignment against the trusted source. Keep source-only unless a separate future question/protected-preview gate approves use. | verified |  |  |
| bereishis_2_1_to_2_3_source_to_skill_map_row_001 | Bereishis 2:1 | וַיְכֻלּוּ הַשָּׁמַיִם וְהָאָרֶץ | and the sky and land were completed | phrase_boundary_check;source_only_recommended | Confirm Hebrew-English phrase alignment against the trusted source. Keep source-only unless a separate future question/protected-preview gate approves use. | verified |  |  |
| bereishis_2_1_to_2_3_source_to_skill_map_row_004 | Bereishis 2:2 | וַיִּשְׁבֹּת בַּיּוֹם הַשְּׁבִיעִי | and He ceased in the seventh day | phrase_boundary_check;source_only_recommended | Confirm Hebrew-English phrase alignment against the trusted source. Keep source-only unless a separate future question/protected-preview gate approves use. | verified |  |  |
| bereishis_2_1_to_2_3_source_to_skill_map_row_005 | Bereishis 2:2 | מִכָּל מְלַאכְתּוֹ אֲשֶׁר עָשָׂה | from all His constructive work that He made | phrase_boundary_check;source_only_recommended | Confirm Hebrew-English phrase alignment against the trusted source. Keep source-only unless a separate future question/protected-preview gate approves use. | verified |  |  |
| bereishis_2_1_to_2_3_source_to_skill_map_row_007 | Bereishis 2:3 | כִּי בוֹ שָׁבַת | because in it He ceased | phrase_boundary_check;source_only_recommended | Confirm Hebrew-English phrase alignment against the trusted source. Keep source-only unless a separate future question/protected-preview gate approves use. | verified |  |  |
| bereishis_2_1_to_2_3_source_to_skill_map_row_008 | Bereishis 2:3 | מִכָּל מְלַאכְתּוֹ | from all His constructive work | phrase_boundary_check;source_only_recommended | Confirm Hebrew-English phrase alignment against the trusted source. Keep source-only unless a separate future question/protected-preview gate approves use. | verified |  |  |
