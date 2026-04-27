# Morphology and Standards Enrichment Audit

## A. Phrase-Level Translation and Alignment Data

Existing phrase-level source truth is strongest in:

- `data/verified_source_skill_maps/`: extraction-verified source-to-skill maps through Bereishis 3:24.
- `data/curriculum_extraction/normalized/linear_chumash_bereishis_1_1_to_1_5_pasuk_segments.seed.jsonl`: Linear Chumash / Pshat of Torah phrase-level extraction for the pilot slice.
- `data/curriculum_extraction/normalized/batch_002_linear_chumash_bereishis_1_6_to_2_3_pasuk_segments.jsonl`
- `data/curriculum_extraction/normalized/batch_003_linear_chumash_bereishis_2_4_to_2_25_pasuk_segments.jsonl`
- `data/curriculum_extraction/normalized/batch_004_linear_chumash_bereishis_3_1_to_3_24_pasuk_segments.jsonl`
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`: canonical Hebrew source coverage.
- `data/source_texts/translations/sefaria/bereishis_english_metsudah.jsonl`: Metsudah primary verse context.
- `data/source_texts/translations/sefaria/bereishis_english_koren.jsonl`: Koren secondary noncommercial verse context.
- `data/source_texts/translations/translation_sources_registry.json`: version-level translation provenance.

The phrase-level source-to-skill maps are already reviewed for extraction accuracy. They are not question-ready and should remain safety-closed.

## B. Morphology Data

Existing morphology support is partial and uneven:

- `data/curriculum_extraction/samples/word_parse.sample.jsonl` contains low-confidence manual sample records for `ברא`, `אלקים`, and `היתה`.
- `data/active_scope_gold_annotations.json` and `data/active_scope_reviewed_questions.json` contain runtime/reviewed examples, but those are reference-only for this enrichment layer.
- `skill_catalog.py` and `docs/runtime_skill_canonical_alignment.md` describe current engine morphology lanes such as shoresh, prefix, suffix, tense, and part of speech.
- `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json` and related Loshon HaTorah reports contain supplemental rule candidates, but OCR/source matching still needs careful review.

Safe auto-proposals are limited. Candidate rows may cite existing word-parse samples, but the review status must remain pending or follow-up.

## C. Vocabulary and Shoresh Data

Vocabulary and shoresh support exists in:

- `data/curriculum_extraction/normalized/vocabulary_priority_pack.seed.jsonl`: cleaned seed vocabulary and shoresh entries, including First 150 Shorashim and Keywords in Bereishis support for several words.
- `data/curriculum_extraction/samples/vocab_entries.sample.jsonl`: schema/sample vocabulary records.
- `data/standards/zekelman/reviewed_bank/standard_3_mvp_reviewed_bank.json`: reviewed-bank examples; reference only, not automatic approval.
- `data/active_scope_reviewed_questions.json`: runtime reviewed examples; reference only, not automatic approval.

First 150 matches may support a candidate, but they do not approve questions or protected-preview use.

## D. Standards Data

Standards support exists in:

- `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json`: structured Standard 3 extraction.
- `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_skill_mapping_draft.json`: draft Standard 3 skill mappings.
- `data/standards/zekelman/crosswalks/loshon_hatorah_to_zekelman_standard_3_crosswalk.json`: supplemental Loshon HaTorah crosswalk.
- `data/standards/crosswalks/canonical_skill_crosswalk.seed.v1.json`: broader canonical skill crosswalk.
- `skill_catalog.py`: current internal skill catalog.
- `docs/runtime_skill_canonical_alignment.md`: runtime skill alignment notes.

These files support candidate mapping only. Zekelman mappings still need separate careful review before any question eligibility decision.

## E. Ingredient Locations and Contributions

| File or Directory | Contribution | Safe Use Now |
|---|---|---|
| `data/verified_source_skill_maps/` | Phrase-level extraction-verified source rows | Link candidates to verified rows |
| `data/curriculum_extraction/normalized/` | Linear Chumash phrase extraction and seed vocab/parse samples | Candidate evidence only |
| `data/source_texts/` | Canonical Hebrew and translation metadata | Source/provenance validation |
| `data/standards/zekelman/` | Zekelman Standard 3 extraction, crosswalks, review artifacts | Standards candidate evidence only |
| `data/sources/loshon_hatorah/` | Supplemental morphology/language rule candidates | Candidate evidence only |
| `skill_catalog.py` | Internal skill identifiers and micro-standards | Candidate skill IDs only |
| `data/active_scope_reviewed_questions.json` | Reviewed runtime examples | Reference only, no auto-approval |

## F. What Can Be Safely Auto-Proposed

- High confidence candidate: links from a verified source-to-skill row to a clearly existing evidence record, with no runtime/question approval.
- Medium confidence candidate: vocabulary or standards candidate with matching source evidence but still pending Yossi enrichment review.
- Needs Yossi review: any morphology, Zekelman mapping, or token-level split that depends on interpretation.
- Blocked/unclear: weak roots, compound phrases, ambiguous function words, OCR-sensitive Loshon HaTorah evidence, or any candidate without clear evidence.

## G. What Should Not Be Auto-Filled

- Do not backfill all morphology fields into phrase-level source-to-skill rows.
- Do not infer shoresh for every word in a phrase.
- Do not treat reviewed-bank examples as automatic enrichment approval.
- Do not treat Koren as primary or commercially cleared.
- Do not turn Standard 3 draft mappings into final Zekelman mappings.
- Do not mark enrichment candidates question-ready, protected-preview-ready, runtime-ready, reviewed-bank-ready, or student-facing.
- Do not use this enrichment pilot to generate questions.
