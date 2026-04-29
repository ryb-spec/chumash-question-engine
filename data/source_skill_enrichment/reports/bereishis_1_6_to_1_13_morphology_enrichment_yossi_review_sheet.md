# Bereishis 1:6-1:13 Morphology Enrichment Yossi Review Sheet

Yossi is reviewing enrichment candidates only.

This is enrichment review only. It is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

Allowed Yossi decisions:

- `verified`
- `needs_follow_up`
- `source_only`
- `block_for_questions`
- `fix_morphology`
- `fix_standard`
- `fix_vocabulary`

## `morph_b1_6_r002_t001`

- Ref: `Bereishis 1:6`
- Hebrew phrase: יְהִי רָקִיעַ
- Hebrew token: יהי
- Proposed values: `part_of_speech=verb; dikduk_feature=jussive/verb-form candidate needs evidence`
- Evidence source id: `data/word_bank.json:יהי; data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.07; data/standards/zekelman/crosswalks/zekelman_2025_standard_3_supplemental_crosswalk.json:3.07`
- Evidence note: Local word_bank references and Standard 3.07 materials suggest a future/jussive-style verb-form lane for יהי, but this slice still lacks a trusted token-level parse for the exact form. Keep as review-only morphology follow-up.
- Confidence: `low`
- Current status: `needs_follow_up`
- What to check: confirm the cited local evidence is enough for enrichment review and does not open any later gate.
- Recommended default decision: `needs_follow_up`

## `morph_b1_6_r004_t002`

- Ref: `Bereishis 1:6`
- Hebrew phrase: וִיהִי מַבְדִּיל
- Hebrew token: מבדיל
- Proposed values: `shoresh=בדל; tense=present; part_of_speech=verb; dikduk_feature=participle/present verb candidate`
- Evidence source id: `data/word_bank.json:מבדיל`
- Evidence note: Local word_bank entries for מבדיל support a verb analysis with a present/participle-style reading, but the slice still needs Yossi review before any morphology details are treated as settled.
- Confidence: `medium`
- Current status: `pending_yossi_enrichment_review`
- What to check: confirm the cited local evidence is enough for enrichment review and does not open any later gate.
- Recommended default decision: `verified`

## `morph_b1_7_r007_t001`

- Ref: `Bereishis 1:7`
- Hebrew phrase: וַיַּבְדֵּל
- Hebrew token: ויבדל
- Proposed values: `shoresh=בדל; tense=past; person=3; gender=masculine; number=singular; part_of_speech=verb; dikduk_feature=vav-hahipuch / past-style verb candidate`
- Evidence source id: `data/word_bank.json:ויבדל; data/curriculum_extraction/generated_questions_preview/batch_001_preview.jsonl:pasuk_segment_bereishis_1_4_003`
- Evidence note: Local word_bank entries and earlier curriculum preview references support a separated/separating verb reading for ויבדל, but the exact vav-hahipuch analysis still needs Yossi review before enrichment details are treated as stable.
- Confidence: `low`
- Current status: `needs_follow_up`
- What to check: confirm the cited local evidence is enough for enrichment review and does not open any later gate.
- Recommended default decision: `needs_follow_up`

## `morph_b1_9_r014_t003`

- Ref: `Bereishis 1:9`
- Hebrew phrase: וַיֹּאמֶר אֱלֹקִים יִקָּווּ הַמַּיִם
- Hebrew token: יקוו
- Proposed values: `tense=future; number=plural; part_of_speech=verb; dikduk_feature=plural future/jussive candidate`
- Evidence source id: `data/word_bank.json:יקוו; data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.07`
- Evidence note: Local word_bank entries suggest a plural future-style verb reading for יקוו, and Standard 3.07 is the conservative standards lane for later review. The exact form still needs Yossi morphology review.
- Confidence: `low`
- Current status: `needs_follow_up`
- What to check: confirm the cited local evidence is enough for enrichment review and does not open any later gate.
- Recommended default decision: `needs_follow_up`

## `morph_b1_9_r017_t001`

- Ref: `Bereishis 1:9`
- Hebrew phrase: וְתֵרָאֶה הַיַּבָּשָׁה
- Hebrew token: ותראה
- Proposed values: `part_of_speech=verb; dikduk_feature=nifal/future-style verb candidate needs evidence`
- Evidence source id: `data/word_bank.json:ותראה; data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.07`
- Evidence note: Local word_bank references make ותראה a useful morphology follow-up candidate, but the exact stem and tense/function still need stronger token-level evidence before this row can move beyond review-only follow-up.
- Confidence: `low`
- Current status: `needs_follow_up`
- What to check: confirm the cited local evidence is enough for enrichment review and does not open any later gate.
- Recommended default decision: `needs_follow_up`

## `morph_b1_11_r023_t001`

- Ref: `Bereishis 1:11`
- Hebrew phrase: תַּדְשֵׁא הָאָרֶץ דֶּשֶׁא
- Hebrew token: תדשא
- Proposed values: `shoresh=דשא; tense=future; part_of_speech=verb; dikduk_feature=future verb candidate`
- Evidence source id: `data/word_bank.json:תדשא; data/word_bank.json:דשא`
- Evidence note: Local word_bank entries connect תדשא to the דשא lexical family and support a verb-form review lane. This is a controlled review-only morphology candidate and still needs Yossi confirmation before any enrichment detail is treated as settled.
- Confidence: `medium`
- Current status: `pending_yossi_enrichment_review`
- What to check: confirm the cited local evidence is enough for enrichment review and does not open any later gate.
- Recommended default decision: `verified`

## `morph_b1_11_r024_t002`

- Ref: `Bereishis 1:11`
- Hebrew phrase: עֵשֶׂב מַזְרִיעַ זֶרַע
- Hebrew token: מזריע
- Proposed values: `shoresh=זרע; tense=present; part_of_speech=verb; dikduk_feature=participle/present verb candidate`
- Evidence source id: `data/word_bank.json:מזריע; data/word_bank.json:זרע`
- Evidence note: Local word_bank entries support treating מזריע as part of the זרע lexical family with a present/participle-style morphology lane. Keep this as review-only pending Yossi confirmation.
- Confidence: `medium`
- Current status: `pending_yossi_enrichment_review`
- What to check: confirm the cited local evidence is enough for enrichment review and does not open any later gate.
- Recommended default decision: `verified`
