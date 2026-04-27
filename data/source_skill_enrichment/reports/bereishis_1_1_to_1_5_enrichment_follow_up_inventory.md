# Bereishis 1:1-1:5 Enrichment Follow-Up Inventory

## Summary

- This inventory lists exactly the unresolved candidates from the Bereishis 1:1-1:5 enrichment pilot.
- Already verified candidates are not repeated below except in this summary.
- Verified summary after this evidence pass:
- morphology: 5 total; 3 verified; 2 unresolved.
- vocabulary_shoresh: 6 total; 3 verified; 3 unresolved.
- standards: 6 total; 1 verified; 5 unresolved.
- Data hygiene audit: candidate TSV columns match validator schemas; row counts are stable; required confidence/review status fields are present; review CSV files remain UTF-8-BOM; `reviewed_bank_allowed=false` is present on all candidate rows; the vocabulary Markdown display concern was checked against TSV/CSV data and no column shift was found in the underlying candidate TSV.

## Evidence Searches Performed

- `data/curriculum_extraction/normalized/vocabulary_priority_pack.seed.jsonl` searched for exact `???`, `???`, and `???` records.
- `data/curriculum_extraction/samples/vocab_entries.sample.jsonl` searched for exact sample vocabulary records.
- `data/curriculum_extraction/samples/word_parse.sample.jsonl` searched for exact word-parse records.
- `data/dikduk_rules/rules_loshon_foundation.jsonl` searched for prefix/article/conjunction rules.
- `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json` searched for token-level standards lanes.
- `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_supplemental_crosswalk.json` searched for support/caution by Standard 3 strand.
- `data/word_bank.json` searched for project-derived exact `???` parse hints; used as reference only, not approval.

## Unresolved Candidates

### `morph_b1_2_r004_t001`

- Candidate type: `morphology`.
- Ref: Bereishis 1:2.
- Hebrew token/phrase: והארץ.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `medium`.
- Current evidence_source_id: `data/dikduk_rules/rules_loshon_foundation.jsonl:DK-CONJ-001; data/dikduk_rules/rules_loshon_foundation.jsonl:DK-ARTICLE-001; data/source_skill_enrichment/vocabulary_shoresh_candidates/bereishis_1_1_to_1_5_vocabulary_shoresh_candidates.tsv:vocab_b1_2_r004_t001`.
- Current evidence_note: Component evidence strengthened: DK-CONJ-001 models prefixed ? as a conjunction before a noun; DK-ARTICLE-001 models prefixed ? as the definite article before a noun; the base ארץ=land vocabulary candidate is already Yossi enrichment-verified. This supports the proposed והארץ component analysis (והארץ -> ? + ? + ארץ) for follow-up review, but it does not by itself verify the exact token split.
- Reason it needs follow-up: Yossi asked for trusted evidence for likely ? + ? + ארץ; component evidence is now linked, but exact token-level morphology still needs Yossi follow-up.
- Missing evidence: No reviewed token-level source explicitly parses the exact token ????? as ? + ? + ??? in this enrichment layer.
- Recommended next evidence source: Yossi review against DK-CONJ-001, DK-ARTICLE-001, and the verified base ??? vocabulary candidate.
- Evidence strengthening possible in this task: Yes - component rules and base-vocabulary evidence linked.
- Should appear in Yossi follow-up sheet: yes.

### `morph_b1_3_r013_t001`

- Candidate type: `morphology`.
- Ref: Bereishis 1:3.
- Hebrew token/phrase: יהי.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `low`.
- Current evidence_source_id: `data/word_bank.json:???; data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.07; data/standards/zekelman/crosswalks/zekelman_2025_standard_3_supplemental_crosswalk.json:3.07`.
- Current evidence_note: Evidence strengthened but remains unresolved: local word_bank entries for יהי/???? record future_jussive-style hints, and Zekelman 3.07 supports verb/future-prefix work using ???? markers. No trusted reviewed source in this pilot directly parses יהי as shoresh היה with jussive/imperfect function, so this remains follow-up evidence rather than verification.
- Reason it needs follow-up: Yossi requested trusted rule evidence for ??? / jussive or imperfect ?let there be.? Existing evidence is suggestive but not direct enough.
- Missing evidence: A reviewed token-level morphology source directly connecting ??? to ??? and its jussive/imperfect function in Bereishis 1:3.
- Recommended next evidence source: Yossi or trusted dikduk source review of ??? against 3.07/future-prefix materials and local word-bank reference hints.
- Evidence strengthening possible in this task: Partial - supporting references linked, but exact parse evidence still missing.
- Should appear in Yossi follow-up sheet: yes.

### `vocab_b1_1_r002_t001`

- Candidate type: `vocabulary_shoresh`.
- Ref: Bereishis 1:1.
- Hebrew token/phrase: ברא.
- Current Yossi decision: `fix_vocabulary`.
- Current review status: `needs_follow_up`.
- Current confidence: `low`.
- Current evidence_source_id: `data/curriculum_extraction/samples/vocab_entries.sample.jsonl:vocab_entry.bara; data/curriculum_extraction/samples/word_parse.sample.jsonl:word_parse.bereishis_1_1.bara`.
- Current evidence_note: Evidence strengthened but First 150 remains unconfirmed: vocab_entry.bara supports ברא=create/created as a high-frequency Bereishis verb sample, and word_parse.bereishis_1_1.bara supports shoresh ברא=create. Searches did not find an exact repo-local First 150 record for ברא; therefore first_150_match remains false and this stays unresolved for Yossi follow-up.
- Reason it needs follow-up: Yossi flagged ברא as core, but exact First 150 evidence is still absent locally.
- Missing evidence: Exact First 150 Shorashim and Keywords source record for ???.
- Recommended next evidence source: Yossi may accept the vocab/word-parse samples as sufficient candidate evidence or request the missing First 150 source row.
- Evidence strengthening possible in this task: Yes - exact sample and word-parse evidence linked; First 150 gap documented.
- Should appear in Yossi follow-up sheet: yes.

### `vocab_b1_3_r013_t002`

- Candidate type: `vocabulary_shoresh`.
- Ref: Bereishis 1:3.
- Hebrew token/phrase: אור.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `low`.
- Current evidence_source_id: `data/curriculum_extraction/samples/vocab_entries.sample.jsonl:vocab_entry.or`.
- Current evidence_note: Evidence strengthened: vocab_entry.or is an exact First 150 Shorashim and Keywords in Bereishis sample for אור=light. The sample itself has review_status=needs_review/manual_sample_only, so this remains a follow-up candidate and does not become automatically verified.
- Reason it needs follow-up: Yossi asked for First 150 evidence and entry ID confirmation. Exact sample exists, but source status still needs review.
- Missing evidence: Reviewed/normalized First 150 row; current evidence is sample-only and needs Yossi confirmation.
- Recommended next evidence source: Yossi review of vocab_entry.or as exact First 150 sample support.
- Evidence strengthening possible in this task: Yes - exact First 150 sample evidence isolated and caveated.
- Should appear in Yossi follow-up sheet: yes.

### `vocab_b1_2_r007_t001`

- Candidate type: `vocabulary_shoresh`.
- Ref: Bereishis 1:2.
- Hebrew token/phrase: וחשך.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `low`.
- Current evidence_source_id: `source_to_skill_map_row_007; data/curriculum_extraction/normalized/linear_chumash_bereishis_1_1_to_1_5_pasuk_segments.seed.jsonl:pasuk_segment_bereishis_1_2_004`.
- Current evidence_note: Evidence clarified, not fully strengthened: verified phrase/source extraction supports וחשך=and darkness in context, but no exact First 150, vocabulary seed, or trusted standalone keyword record for base חשך was located. Prefix/conjunction morphology remains separate from vocabulary evidence.
- Reason it needs follow-up: Yossi noted darkness is reasonable but evidence weak; local search found contextual phrase evidence only.
- Missing evidence: Standalone trusted vocabulary/shoresh record for ???/darkness.
- Recommended next evidence source: Locate First 150/vocabulary source for ??? or keep source-only/follow-up.
- Evidence strengthening possible in this task: Partial - contextual phrase evidence documented; standalone vocabulary gap remains.
- Should appear in Yossi follow-up sheet: yes.

### `std_b1_1_r002`

- Candidate type: `standards`.
- Ref: Bereishis 1:1.
- Hebrew token/phrase: ברא אלקים.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `medium`.
- Current evidence_source_id: `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.02; data/standards/zekelman/crosswalks/zekelman_2025_standard_3_supplemental_crosswalk.json:3.02; data/curriculum_extraction/samples/word_parse.sample.jsonl:word_parse.bereishis_1_1.bara`.
- Current evidence_note: Evidence strengthened for a token-level split: Zekelman 3.02 covers cumulative shoresh vocabulary and root identification; word_parse.bereishis_1_1.bara supports token ברא as shoresh ברא. The current candidate is phrase-level (ברא ?????), so it remains needs_follow_up until split to token ברא.
- Reason it needs follow-up: 3.02 applies to token ???, not the whole phrase.
- Missing evidence: Token-level standards candidate for ??? only.
- Recommended next evidence source: Create/review a token-level 3.02 candidate for ???, leaving ????? separate.
- Evidence strengthening possible in this task: Yes - exact token evidence and 3.02 support linked.
- Should appear in Yossi follow-up sheet: yes.

### `std_b1_1_r003`

- Candidate type: `standards`.
- Ref: Bereishis 1:1.
- Hebrew token/phrase: את השמים ואת הארץ.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `low`.
- Current evidence_source_id: `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.01; data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.03; data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.06; docs/standards/zekelman/extracted/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8_raw_text.md:2107-2113`.
- Current evidence_note: Evidence clarified for token-level split: 3.01 applies to noun vocabulary such as שמים/ארץ; 3.03 covers function-word vocabulary; 3.06 and the raw Standard 3 appendix discuss את as direct-object marker/with and definite nouns/articles. The phrase is too broad for one standards candidate.
- Reason it needs follow-up: Phrase contains ?? markers plus nouns; multiple standards lanes are mixed.
- Missing evidence: Separate token-level candidates for ??, ????, ???, and article/prefix features.
- Recommended next evidence source: Token-level standards split: ?? -> function/direct-object marker review; ????/??? -> 3.01 noun vocabulary; article morphology -> 3.06 if needed.
- Evidence strengthening possible in this task: Yes - standards lanes identified, but no candidate verified.
- Should appear in Yossi follow-up sheet: yes.

### `std_b1_3_r013`

- Candidate type: `standards`.
- Ref: Bereishis 1:3.
- Hebrew token/phrase: יהי אור.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `medium`.
- Current evidence_source_id: `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.01; data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.07; data/curriculum_extraction/samples/vocab_entries.sample.jsonl:vocab_entry.or`.
- Current evidence_note: Evidence strengthened for a token-level split: 3.01 can apply to noun vocabulary token אור, and vocab_entry.or supports אור=light as a First 150 sample. יהי belongs to a separate morphology/verb-form review lane, likely related to 3.07, so the phrase-level standards row remains unresolved.
- Reason it needs follow-up: 3.01 may apply to ??? but the phrase also includes ???.
- Missing evidence: Token-level standards candidate for ??? only, plus separate morphology/verb-form candidate for ???.
- Recommended next evidence source: Yossi review of ??? -> 3.01 from vocab_entry.or; keep ??? separate under morphology/3.07.
- Evidence strengthening possible in this task: Yes - exact ??? evidence and 3.01/3.07 split documented.
- Should appear in Yossi follow-up sheet: yes.

### `std_b1_5_r020`

- Candidate type: `standards`.
- Ref: Bereishis 1:5.
- Hebrew token/phrase: לאור יום.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `medium`.
- Current evidence_source_id: `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.01; data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.06; data/curriculum_extraction/samples/vocab_entries.sample.jsonl:vocab_entry.or; data/source_skill_enrichment/vocabulary_shoresh_candidates/bereishis_1_1_to_1_5_vocabulary_shoresh_candidates.tsv:vocab_b1_5_r020_t002`.
- Current evidence_note: Evidence strengthened for a token-level split: אור has First 150 sample support and יום=day is Yossi enrichment-verified vocabulary; 3.01 applies to noun vocabulary while 3.06/prefix evidence may be needed for the ? prefix in ????. The phrase-level standards row remains too bundled.
- Reason it needs follow-up: Phrase includes prefix + ??? + ??? and needs token-level mapping.
- Missing evidence: Separate token-level standards candidates for ???, ???, and ? prefix if standards mapping is desired.
- Recommended next evidence source: Split to ??? -> 3.01, ??? -> 3.01, and ? prefix -> 3.06 only if Yossi wants prefix standards enrichment.
- Evidence strengthening possible in this task: Yes - exact token evidence and standards lanes documented.
- Should appear in Yossi follow-up sheet: yes.

### `std_b1_2_r010`

- Candidate type: `standards`.
- Ref: Bereishis 1:2.
- Hebrew token/phrase: מרחפת.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `low`.
- Current evidence_source_id: `source_to_skill_map_row_010; data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json:3.07`.
- Current evidence_note: Evidence gap remains: the verified source-to-skill row supports מרחפת as source-derived text, and 3.07 is the broad verb standard, but no trusted local token-level parse or standards mapping was located for מרחפת. Keep as needs_mapping_review.
- Reason it needs follow-up: No strong standards evidence exists for this token in the pilot.
- Missing evidence: Trusted parse and standards mapping for ?????.
- Recommended next evidence source: Future morphology/verb enrichment source before any standards mapping.
- Evidence strengthening possible in this task: Partial - relevant broad standard identified; exact evidence gap documented.
- Should appear in Yossi follow-up sheet: yes.
