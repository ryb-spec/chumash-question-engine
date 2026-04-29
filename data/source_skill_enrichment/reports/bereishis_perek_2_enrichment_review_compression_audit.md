# Bereishis Perek 2 Enrichment Review Compression Audit

## Raw Candidate Totals

- morphology: 328
- vocabulary/shoresh: 328
- phrase-level standards: 99
- token-split standards: 328
- total raw candidates: 1083

## Compression Totals

- compressed review groups: 167
- crosswalk rows: 1083

## Duplicate Token Groups

Repeated token grouping was done by normalized token or conservative pattern. The largest compressed groups are:

| review_group_id | category | hebrew_token_or_pattern | refs_or_count | recommended_decision |
| --- | --- | --- | --- | --- |
| p2_comp_013 | phrase_level_standards_source_only | phrase-level standards parent rows | 99 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+17 more refs) | source_only |
| p2_comp_008 | morphology_general_deferred | general morphology deferred | 95 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+17 more refs) | needs_follow_up |
| p2_comp_010 | morphology_suffix_construct_follow_up | suffix / construct / number-sensitive form | 84 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+17 more refs) | needs_follow_up |
| p2_comp_009 | morphology_prefix_article_or_stem_follow_up | heh/article or stem-sensitive form | 55 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+15 more refs) | needs_follow_up |
| p2_comp_081 | token_split_verb_form_follow_up | verb-form-sensitive token-split rows | 55 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8 (+13 more refs) | needs_follow_up |
| p2_comp_162 | prefix_preposition_or_function_word_follow_up | ו | 42 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9 (+12 more refs) | needs_follow_up |
| p2_comp_011 | morphology_verb_form_sensitive | future / jussive / imperfect-looking form | 29 candidates; Bereishis 2:3, Bereishis 2:4, Bereishis 2:5, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9, Bereishis 2:10 (+10 more refs) | needs_follow_up |
| p2_comp_012 | morphology_verb_form_sensitive | vav narrative / vav hahipuch | 26 candidates; Bereishis 2:1, Bereishis 2:2, Bereishis 2:3, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9, Bereishis 2:15, Bereishis 2:16 (+7 more refs) | needs_follow_up |
| p2_comp_077 | token_split_prefix_preposition_follow_up | ל | 24 candidates; Bereishis 2:3, Bereishis 2:5, Bereishis 2:7, Bereishis 2:9, Bereishis 2:10, Bereishis 2:15, Bereishis 2:16, Bereishis 2:17 (+6 more refs) | needs_follow_up |
| p2_comp_164 | prefix_preposition_or_function_word_follow_up | ל | 23 candidates; Bereishis 2:3, Bereishis 2:5, Bereishis 2:7, Bereishis 2:9, Bereishis 2:10, Bereishis 2:15, Bereishis 2:16, Bereishis 2:17 (+6 more refs) | needs_follow_up |
| p2_comp_074 | token_split_prefix_preposition_follow_up | ה | 21 candidates; Bereishis 2:5, Bereishis 2:9, Bereishis 2:11, Bereishis 2:12, Bereishis 2:13, Bereishis 2:14, Bereishis 2:17, Bereishis 2:18 (+3 more refs) | needs_follow_up |
| p2_comp_161 | prefix_preposition_or_function_word_follow_up | ה | 20 candidates; Bereishis 2:5, Bereishis 2:9, Bereishis 2:11, Bereishis 2:12, Bereishis 2:13, Bereishis 2:14, Bereishis 2:17, Bereishis 2:18 (+3 more refs) | needs_follow_up |
| p2_comp_078 | token_split_prefix_preposition_follow_up | מ | 18 candidates; Bereishis 2:2, Bereishis 2:3, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9, Bereishis 2:10, Bereishis 2:16 (+6 more refs) | needs_follow_up |
| p2_comp_165 | prefix_preposition_or_function_word_follow_up | מ | 18 candidates; Bereishis 2:2, Bereishis 2:3, Bereishis 2:6, Bereishis 2:7, Bereishis 2:8, Bereishis 2:9, Bereishis 2:10, Bereishis 2:16 (+6 more refs) | needs_follow_up |
| p2_comp_075 | token_split_prefix_preposition_follow_up | ו | 17 candidates; Bereishis 2:1, Bereishis 2:5, Bereishis 2:6, Bereishis 2:10, Bereishis 2:15, Bereishis 2:17, Bereishis 2:19, Bereishis 2:20 (+2 more refs) | needs_follow_up |

## High-Confidence Vocabulary Groups

No Perek 2 vocabulary/shoresh raw candidate is marked high confidence yet. Clean vocabulary/noun groups are therefore recommended for first-pass review as `needs_follow_up`, not as automatic verification.

## Clean Noun Groups

Clean noun-looking groups are compressed under `clean_vocabulary_noun_group` and `token_split_clean_noun_standards`. These are practical first-pass review targets, but they still need Yossi decisions before any raw row changes.

## Clean Shoresh Groups

Shoresh-looking groups are compressed under `clean_shoresh_group`. They remain `needs_follow_up` because the current raw rows do not supply reviewed root evidence.

## Direct-Object / Function-Word Candidates

Function-word candidates, including any `את` rows, are isolated into follow-up groups. They must not be treated as simple vocabulary translation rows.

## Token-Split Standards Groups

Token-split rows are grouped separately from phrase-level parent standards. Clean noun/vocabulary token-split groups are first-pass review targets; prefix, preposition, function-word, and verb-form-sensitive rows are follow-up.

## Phrase-Level Standards Superseded by Token-Split Rows

All 99 phrase-level standards rows are compressed into source-only parent review groups because token-split standards are the preferred later review path.

## Morphology / Verb-Form-Sensitive Clusters to Defer

Morphology rows are grouped into conservative defer/follow-up patterns: vav narrative/vav hahipuch, future/jussive, imperative, person/gender/number, suffix/construct, uncertain stem/binyan, function-word source-only, and general morphology deferred.

## Ambiguous / Context-Heavy Rows

Rows with low evidence, broad phrase context, prefixes/prepositions, or uncertain token role remain `needs_follow_up` or `source_only` recommendations.

## High-Risk or Blocked Groups

No group is recommended as `verified` in this compressed packet. High-risk groups are not blocked automatically; they are routed to `needs_follow_up`, `source_only`, or later `block_for_questions` if Yossi chooses.

## Safety Statement

This is enrichment review only. It is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.
This is enrichment review only: not question approval, not protected-preview approval, not reviewed-bank approval, not runtime approval, and not student-facing approval.
