# Bereishis Perek 2 Enrichment Compressed Review Summary

## Totals

- raw candidate total: 1083
- compressed group total: 167
- crosswalk rows: 1083

## Raw Candidate Counts

- morphology: 328
- vocabulary/shoresh: 328
- phrase-level standards: 99
- token-split standards: 328

## Count by Category

| category | count |
| --- | --- |
| ambiguous_context_heavy_vocabulary | 38 |
| clean_shoresh_group | 7 |
| clean_vocabulary_noun_group | 31 |
| direct_object_or_function_word_follow_up | 1 |
| morphology_function_word_source_only | 7 |
| morphology_general_deferred | 1 |
| morphology_prefix_article_or_stem_follow_up | 1 |
| morphology_suffix_construct_follow_up | 1 |
| morphology_verb_form_sensitive | 2 |
| phrase_level_standards_source_only | 1 |
| prefix_preposition_or_function_word_follow_up | 9 |
| token_split_clean_noun_standards | 31 |
| token_split_function_word_follow_up | 1 |
| token_split_general_context_follow_up | 26 |
| token_split_prefix_preposition_follow_up | 9 |
| token_split_verb_form_follow_up | 1 |

## Count by Recommended Decision

| recommended_decision | group_count | raw_candidate_count |
| --- | --- | --- |
| needs_follow_up | 159 | 945 |
| source_only | 8 | 138 |

## Risk Counts

| risk_level | group_count |
| --- | --- |
| high | 64 |
| medium | 103 |

## High-Confidence Groups

The original compressed packet recommended no automatic verification before Yossi review; later clean-group review verified only token-split clean noun standards for enrichment mapping.

## Deferred Groups

Morphology, verb-form-sensitive rows, prefix/preposition/function-word rows, and broad phrase-level standards are recommended as `needs_follow_up` or `source_only`.

## Blocked / Source-Only Groups

Phrase-level standards are recommended source-only parent rows where token-split standards are preferred. Function-word morphology may also remain source-only.

## Next Action

Yossi should review the compressed packet and CSV, fill group-level decisions, and then run a later decision-application task that uses the raw-to-compressed crosswalk to update raw rows conservatively.

## Safety Statement

This is enrichment review only. Yossi clean-group decisions have been applied separately for enrichment mapping only. No question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval exists. All gates remain closed.
This is enrichment review only: not question approval, not protected-preview approval, not reviewed-bank approval, not runtime approval, and not student-facing approval.

## Clean-Group Decision Application Note

Yossi clean-group decisions were later applied through the clean-group crosswalk: 31 token-split clean noun standards groups / 91 raw candidates were verified for enrichment mapping only, and 38 clean vocabulary/shoresh groups / 100 raw candidates remain needs_follow_up. This does not approve questions, protected-preview use, reviewed-bank use, runtime use, or student-facing use.
