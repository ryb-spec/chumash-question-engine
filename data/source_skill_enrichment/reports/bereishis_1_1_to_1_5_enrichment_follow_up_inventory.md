# Bereishis 1:1-1:5 Enrichment Follow-Up Inventory

## Summary

- This inventory lists exactly the unresolved candidates from the Bereishis 1:1-1:5 enrichment pilot.
- Already verified candidates are not repeated below except in this summary.
- Verified summary after this evidence pass:
- morphology: 5 total; 3 verified; 2 unresolved.
- vocabulary_shoresh: 6 total; 3 verified; 3 unresolved.
- standards: 6 total; 1 verified; 5 unresolved.
- All proposed skill and standard references below are anchored through `data/standards/canonical_skill_contract.json`.
- Data hygiene audit: candidate TSV columns match validator schemas; row counts are stable; required confidence/review status fields are present; review CSV files remain UTF-8-BOM; `reviewed_bank_allowed=false` is present on all candidate rows; unresolved follow-up recommendations remain conservative and do not pre-clear verification.

## Evidence Searches Performed

- `data/curriculum_extraction/normalized/vocabulary_priority_pack.seed.jsonl` searched for exact ???, ???, and ??? records.
- `data/curriculum_extraction/samples/vocab_entries.sample.jsonl` searched for exact sample vocabulary records.
- `data/curriculum_extraction/samples/word_parse.sample.jsonl` searched for exact word-parse records.
- `data/dikduk_rules/rules_loshon_foundation.jsonl` searched for prefix/article/conjunction rules.
- `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json` searched for token-level standards lanes.
- `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_supplemental_crosswalk.json` searched for support/caution by Standard 3 strand.
- `data/word_bank.json` searched for project-derived exact parse hints; used as reference only, not approval.
- `data/standards/canonical_skill_contract.json` used to reconcile every unresolved follow-up row to canonical skill IDs and conservative standards anchors.

## Unresolved Candidates

### `vocab_b1_1_r002_t001`

- Candidate type: `vocabulary_shoresh`.
- Ref: Bereishis 1:1.
- Hebrew token/phrase: ברא.
- Current Yossi decision: `fix_vocabulary`.
- Current review status: `needs_follow_up`.
- Current confidence: `low`.
- Current evidence_source_id: `data/curriculum_extraction/samples/vocab_entries.sample.jsonl:vocab_entry.bara; data/curriculum_extraction/samples/word_parse.sample.jsonl:word_parse.bereishis_1_1.bara`.
- Current evidence_note: Evidence strengthened but First 150 remains unconfirmed: vocab_entry.bara supports ברא=create/created as a high-frequency Bereishis verb sample, and word_parse.bereishis_1_1.bara supports shoresh ברא=create. Searches did not find an exact repo-local First 150 record for ברא; therefore first_150_match remains false and this stays unresolved for Yossi follow-up.
- Canonical contract mapping: `ROOT.IDENTIFY` with standards `3.02`.
- Contract mapping rationale: The unresolved `shoresh` proposal maps directly through `ROOT.IDENTIFY` in the canonical contract, which carries Standard 3.02 without treating vocabulary sampling as approval.
- Reason it needs follow-up: Yossi flagged ??? as core, but the repo still lacks an exact local First 150 row.
- Missing evidence: Exact First 150 Shorashim and Keywords source record for ???.
- Recommended next evidence source: Yossi can decide whether the linked vocab/word-parse samples are enough for enrichment-only evidence or require the missing First 150 row first.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
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
- Canonical contract mapping: `WORD.MEANING_BASIC` with standards `3.01`.
- Contract mapping rationale: The unresolved `noun_keyword` proposal maps through `WORD.MEANING_BASIC`, the contract lane tied to Standard 3.01 noun-vocabulary work.
- Reason it needs follow-up: The exact sample exists, but it is still manual-sample evidence rather than a reviewed source row.
- Missing evidence: Reviewed or normalized First 150 row; the current support is sample-only and still needs Yossi confirmation.
- Recommended next evidence source: Yossi review of `vocab_entry.or` against the reviewed-source threshold for enrichment only.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
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
- Canonical contract mapping: `WORD.MEANING_BASIC` with standards `3.01`.
- Contract mapping rationale: The lexical target is base ???, so the unresolved noun-keyword proposal anchors through `WORD.MEANING_BASIC`; the prefixed ? remains outside this vocabulary claim.
- Reason it needs follow-up: The current evidence is contextual phrase support only, not a standalone vocabulary witness.
- Missing evidence: Standalone trusted vocabulary or shoresh record for ???=darkness.
- Recommended next evidence source: Find a trusted vocabulary source for ??? or keep the row explicitly source-only.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
- Should appear in Yossi follow-up sheet: yes.

### `morph_b1_2_r004_t001`

- Candidate type: `morphology`.
- Ref: Bereishis 1:2.
- Hebrew token/phrase: והארץ.
- Current Yossi decision: `needs_follow_up`.
- Current review status: `needs_follow_up`.
- Current confidence: `medium`.
- Current evidence_source_id: `data/dikduk_rules/rules_loshon_foundation.jsonl:DK-CONJ-001; data/dikduk_rules/rules_loshon_foundation.jsonl:DK-ARTICLE-001; data/source_skill_enrichment/vocabulary_shoresh_candidates/bereishis_1_1_to_1_5_vocabulary_shoresh_candidates.tsv:vocab_b1_2_r004_t001`.
- Current evidence_note: Component evidence strengthened: DK-CONJ-001 models prefixed ? as a conjunction before a noun; DK-ARTICLE-001 models prefixed ? as the definite article before a noun; the base ארץ=land vocabulary candidate is already Yossi enrichment-verified. This supports the proposed והארץ component analysis (והארץ -> ? + ? + ארץ) for follow-up review, but it does not by itself verify the exact token split.
- Canonical contract mapping: `PREFIX.FORM_IDENTIFY; WORD.PARTS.SEGMENT` with standards `3.06`.
- Contract mapping rationale: The unresolved `prefix/article split needs evidence` note maps through `PREFIX.FORM_IDENTIFY`; `WORD.PARTS.SEGMENT` keeps the token-splitting lane explicit without claiming more than the evidence supports.
- Reason it needs follow-up: The component rules are stronger now, but they still do not amount to a reviewed token-level parse of the exact form.
- Missing evidence: No reviewed token-level source explicitly parses ????? as ? + ? + ??? in this enrichment layer.
- Recommended next evidence source: Yossi review against DK-CONJ-001, DK-ARTICLE-001, and the verified base ??? vocabulary candidate.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
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
- Canonical contract mapping: `WORD.PART_OF_SPEECH_BASIC; VERB.TENSE.FUTURE; PREFIX.OTIYOT_EITAN` with standards `3.04; 3.07`.
- Contract mapping rationale: The unresolved `verb` and `jussive/verb-form candidate needs evidence` labels map through `WORD.PART_OF_SPEECH_BASIC`, `VERB.TENSE.FUTURE`, and `PREFIX.OTIYOT_EITAN` in the contract, while staying review-only.
- Reason it needs follow-up: The current evidence is suggestive, but it still stops short of a trusted parse for the exact token.
- Missing evidence: A reviewed token-level morphology source directly connecting ??? to its shoresh and jussive or imperfect function in Bereishis 1:3.
- Recommended next evidence source: Yossi or a trusted dikduk source review of ??? against the 3.07 verb-form lane.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
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
- Canonical contract mapping: `ROOT.IDENTIFY` with standards `3.02`.
- Contract mapping rationale: The proposed `std3_02_shoresh_identification` reference maps directly through `ROOT.IDENTIFY`; the unresolved issue is phrase scope, not contract identity.
- Reason it needs follow-up: The standard lane is clear, but the current row is still too broad because only ??? has token-level shoresh evidence.
- Missing evidence: A token-level standards candidate for ??? alone rather than the full phrase ??? ?????.
- Recommended next evidence source: Create or review a token-only ??? -> 3.02 standards candidate and leave phrase-level residue out of scope.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
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
- Canonical contract mapping: `PARTICLE.DIRECT_OBJECT_MARKER; WORD.MEANING_BASIC; PREFIX.FORM_IDENTIFY` with standards `3.01; 3.03; 3.06`.
- Contract mapping rationale: The current phrase mixes noun vocabulary with direct-object-marker and article-prefix material; those references map through `WORD.MEANING_BASIC`, `PARTICLE.DIRECT_OBJECT_MARKER`, and `PREFIX.FORM_IDENTIFY` in the contract.
- Reason it needs follow-up: The standards references are legitimate, but they point to multiple contract lanes that should not stay bundled in one phrase row.
- Missing evidence: Separate token-level candidates for ??, ?????, ????, and any article or prefix features instead of one bundled phrase row.
- Recommended next evidence source: Token-level split: ?? into the particle lane, ????/??? into noun-vocabulary, and article material only if Yossi wants that extra lane.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
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
- Canonical contract mapping: `WORD.MEANING_BASIC; VERB.TENSE.FUTURE; PREFIX.OTIYOT_EITAN` with standards `3.01; 3.07`.
- Contract mapping rationale: The 3.01 noun-vocabulary reference maps through `WORD.MEANING_BASIC`, while the unresolved ??? verb-form evidence belongs in the 3.07-aligned `VERB.TENSE.FUTURE` and `PREFIX.OTIYOT_EITAN` lanes.
- Reason it needs follow-up: The phrase mixes a good ??? vocabulary anchor with a separate ??? verb-form problem, so one phrase-level standards row is still misleading.
- Missing evidence: A token-level standards candidate for ??? plus a separate disposition for ??? under morphology or verb-form review.
- Recommended next evidence source: Yossi review of ??? as the token-level standards anchor; keep ??? on the morphology track until better evidence exists.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
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
- Canonical contract mapping: `WORD.MEANING_BASIC; PREFIX.BASIC_PREPOSITIONS` with standards `3.01; 3.03; 3.06`.
- Contract mapping rationale: The noun-vocabulary references map through `WORD.MEANING_BASIC`, while the prefixed ? aligns to `PREFIX.BASIC_PREPOSITIONS`; the contract keeps those lanes separate.
- Reason it needs follow-up: The current row still bundles prefix and noun-vocabulary work that the contract now separates cleanly.
- Missing evidence: Separate token-level candidates for ???, ???, and prefixed ? if Yossi wants standards treatment for all parts of the phrase.
- Recommended next evidence source: Split ??? and ??? into noun-vocabulary review, and only add the ? prefix lane if Yossi explicitly wants that standards treatment.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
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
- Canonical contract mapping: `VERB.TENSE.PAST; VERB.TENSE.PRESENT; VERB.TENSE.FUTURE; VERB.COMMAND` with standards `3.07`.
- Contract mapping rationale: The broad 3.07 reference does map into the contract, but only as a set of unresolved verb-form lanes; this row should not claim a narrower canonical skill until a trusted parse exists.
- Reason it needs follow-up: There is still no token-level parse strong enough to choose one 3.07 verb-form sub-lane with confidence.
- Missing evidence: A trusted token-level parse for ????? plus a narrower contract lane within Standard 3.07.
- Recommended next evidence source: Future morphology or dikduk evidence before narrowing ????? to a specific canonical verb-form lane.
- Evidence strengthening possible in this task: Yes - mapping and evidence framing were tightened without verifying the candidate automatically.
- Should appear in Yossi follow-up sheet: yes.
