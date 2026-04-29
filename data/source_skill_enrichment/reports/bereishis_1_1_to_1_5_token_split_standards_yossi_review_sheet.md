# Bereishis 1:1-1:5 Token-Split Standards Yossi Review Sheet

## Scope Summary

- Scope: token-split standards follow-up candidates replacing bundled phrase-level review rows for Bereishis 1:1-1:5.
- Source TSV: `data/source_skill_enrichment/standards_candidates/bereishis_1_1_to_1_5_token_split_standards_candidates.tsv`.
- Canonical contract anchor: `data/standards/canonical_skill_contract.json`.
- Candidate count: 10 review-only token-split rows.
- Allowed Yossi decisions: `verified`, `needs_follow_up`, `source_only`, `block_for_questions`, `fix_standard`.
- This is standards enrichment follow-up only. It is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

### `stdtok_b1_1_r002_t001` | parent `std_b1_1_r002` | Bereishis 1:1 | ברא

- Parent phrase: `ברא אלקים`.
- Proposed Zekelman standard: `3.02`.
- Canonical skill ID: `ROOT.IDENTIFY`.
- Canonical standard anchor: `3.02`.
- Confidence: `medium`.
- Current status: `yossi_enrichment_verified`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `verified`.
- Yossi note: Yossi approved token-level 3.02 / ROOT.IDENTIFY for ברא only; the parent phrase remains unresolved.
- Evidence note: Token-level evidence supports ברא as a shoresh-identification standards candidate under Standard 3.02, mapped through ROOT.IDENTIFY in the canonical contract. This approval applies to token ברא only, not to the parent phrase ברא אלקים.

### `stdtok_b1_1_r003_t001` | parent `std_b1_1_r003` | Bereishis 1:1 | את

- Parent phrase: `את השמים ואת הארץ`.
- Proposed Zekelman standard: `3.03`.
- Canonical skill ID: `PARTICLE.DIRECT_OBJECT_MARKER`.
- Canonical standard anchor: `3.03`.
- Confidence: `medium`.
- Current status: `yossi_enrichment_verified`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `verified`.
- Yossi note: Yossi approved token-level direct-object-marker mapping for את under 3.03 / PARTICLE.DIRECT_OBJECT_MARKER.
- Evidence note: The first את is a clean token-level direct-object-marker follow-up candidate anchored to PARTICLE.DIRECT_OBJECT_MARKER and Standard 3.03. This approval is only for token את, not for the whole phrase.

### `stdtok_b1_1_r003_t002` | parent `std_b1_1_r003` | Bereishis 1:1 | שמים

- Parent phrase: `את השמים ואת הארץ`.
- Proposed Zekelman standard: `3.01`.
- Canonical skill ID: `WORD.MEANING_BASIC`.
- Canonical standard anchor: `3.01`.
- Confidence: `low`.
- Current status: `needs_follow_up`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `needs_follow_up`.
- Yossi note: Yossi kept שמים as follow-up until stronger noun-vocabulary evidence is linked.
- Evidence note: Base noun שמים is a plausible 3.01 noun-vocabulary follow-up candidate, but the current local evidence is still low-confidence because no separate vocabulary seed was linked. The row remains useful for Yossi follow-up only.

### `stdtok_b1_1_r003_t003` | parent `std_b1_1_r003` | Bereishis 1:1 | את

- Parent phrase: `את השמים ואת הארץ`.
- Proposed Zekelman standard: `3.03`.
- Canonical skill ID: `PARTICLE.DIRECT_OBJECT_MARKER`.
- Canonical standard anchor: `3.03`.
- Confidence: `medium`.
- Current status: `yossi_enrichment_verified`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `verified`.
- Yossi note: Yossi approved token-level direct-object-marker mapping for את from surface ואת; conjunction handling remains separate.
- Evidence note: This row isolates base את from surface ואת so the conjunction stays out of the standards claim. The direct-object-marker mapping to 3.03 / PARTICLE.DIRECT_OBJECT_MARKER is approved for the token-level candidate only.

### `stdtok_b1_1_r003_t004` | parent `std_b1_1_r003` | Bereishis 1:1 | ארץ

- Parent phrase: `את השמים ואת הארץ`.
- Proposed Zekelman standard: `3.01`.
- Canonical skill ID: `WORD.MEANING_BASIC`.
- Canonical standard anchor: `3.01`.
- Confidence: `medium`.
- Current status: `yossi_enrichment_verified`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `verified`.
- Yossi note: Yossi approved token-level 3.01 / WORD.MEANING_BASIC for base noun ארץ.
- Evidence note: Base noun ארץ already has vocabulary support elsewhere in the pilot, so it is an acceptable token-level Standard 3.01 standards candidate under WORD.MEANING_BASIC. The approval applies to token ארץ only.

### `stdtok_b1_3_r013_t001` | parent `std_b1_3_r013` | Bereishis 1:3 | יהי

- Parent phrase: `יהי אור`.
- Proposed Zekelman standard: `3.07`.
- Canonical skill ID: `VERB.TENSE.FUTURE`.
- Canonical standard anchor: `3.07`.
- Confidence: `low`.
- Current status: `needs_follow_up`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `needs_follow_up`.
- Yossi note: Yossi kept יהי follow-up pending stronger morphology / verb-form evidence.
- Evidence note: יהי belongs in a 3.07 verb-form review lane if Yossi wants a standards candidate, but the current evidence is still indirect and no trusted token-level morphology parse has been approved. The row remains follow-up only.

### `stdtok_b1_3_r013_t002` | parent `std_b1_3_r013` | Bereishis 1:3 | אור

- Parent phrase: `יהי אור`.
- Proposed Zekelman standard: `3.01`.
- Canonical skill ID: `WORD.MEANING_BASIC`.
- Canonical standard anchor: `3.01`.
- Confidence: `medium`.
- Current status: `yossi_enrichment_verified`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `verified`.
- Yossi note: Yossi approved token-level 3.01 / WORD.MEANING_BASIC for אור.
- Evidence note: אור is a clean token-level noun-vocabulary standards candidate under Standard 3.01 and maps through WORD.MEANING_BASIC in the canonical contract. The row is approved for enrichment only and does not change any safety gate.

### `stdtok_b1_5_r020_t001` | parent `std_b1_5_r020` | Bereishis 1:5 | אור

- Parent phrase: `לאור יום`.
- Proposed Zekelman standard: `3.01`.
- Canonical skill ID: `WORD.MEANING_BASIC`.
- Canonical standard anchor: `3.01`.
- Confidence: `medium`.
- Current status: `yossi_enrichment_verified`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `verified`.
- Yossi note: Yossi approved base אור from לאור as 3.01 / WORD.MEANING_BASIC only; prefixed ל remains separate.
- Evidence note: Base noun אור can be reviewed separately from surface לאור as a Standard 3.01 token-level candidate under WORD.MEANING_BASIC. Yossi approved the base noun only; the prefixed ל analysis remains separate.

### `stdtok_b1_5_r020_t002` | parent `std_b1_5_r020` | Bereishis 1:5 | יום

- Parent phrase: `לאור יום`.
- Proposed Zekelman standard: `3.01`.
- Canonical skill ID: `WORD.MEANING_BASIC`.
- Canonical standard anchor: `3.01`.
- Confidence: `medium`.
- Current status: `yossi_enrichment_verified`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `verified`.
- Yossi note: Yossi approved token-level 3.01 / WORD.MEANING_BASIC for יום.
- Evidence note: יום is a clean token-level noun-vocabulary standards candidate under Standard 3.01 and maps through WORD.MEANING_BASIC in the canonical contract. The row is approved for enrichment only and does not change any safety gate.

### `stdtok_b1_5_r020_t003` | parent `std_b1_5_r020` | Bereishis 1:5 | ל

- Parent phrase: `לאור יום`.
- Proposed Zekelman standard: `3.06`.
- Canonical skill ID: `PREFIX.BASIC_PREPOSITIONS`.
- Canonical standard anchor: `3.06`.
- Confidence: `low`.
- Current status: `needs_follow_up`.
- Recommended decision before review: `needs_follow_up`.
- Applied Yossi decision: `needs_follow_up`.
- Yossi note: Yossi kept prefixed ל follow-up pending stronger 3.06 prefix/preposition evidence.
- Evidence note: The prefixed ל on surface לאור is a plausible 3.06 token-level candidate mapped through PREFIX.BASIC_PREPOSITIONS, but the current evidence is still low-confidence. The row remains follow-up only until stronger prefix/preposition standards evidence is linked.
