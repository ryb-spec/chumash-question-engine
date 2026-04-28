# Bereishis 1:1-1:5 Token-Split Standards Audit

This audit explains why the bundled phrase-level standards follow-up rows are too broad and how the replacement token-split review-only candidates were prepared.

- Canonical contract used for every skill and standard anchor: `data/standards/canonical_skill_contract.json`.
- Replacement TSV: `data/source_skill_enrichment/standards_candidates/bereishis_1_1_to_1_5_token_split_standards_candidates.tsv`.
- No token-level standards candidate in this audit is verified until Yossi reviews it; the later applied-review report records which rows were approved.
- no question, protected-preview, reviewed-bank, runtime, or student-facing gate was opened.

## `std_b1_1_r002` | ברא אלקים

- Why the phrase-level candidate is too broad: Standard 3.02 evidence clearly supports token ברא as shoresh work, but the full phrase includes אלקים, which is not covered by the same root-identification claim.
- Tokens needing separate review: ברא as root-identification; אלקים could only become a separate noun-vocabulary follow-up if stronger local evidence is gathered later.
- Canonical skill IDs used: `ROOT.IDENTIFY`.
- Zekelman standards that may apply: `3.02`.
- What remains uncertain: whether anything beyond ברא should be proposed from this phrase in the current pilot.
- Why no token-level candidate is verified yet: the token split was precise, but final approval was reserved for Yossi review rather than inferred automatically.

## `std_b1_1_r003` | את השמים ואת הארץ

- Why the phrase-level candidate is too broad: it mixes two direct-object-marker uses with two noun-vocabulary targets, so one standards row hides multiple review decisions.
- Tokens needing separate review: first את, base שמים, second את from surface ואת, and base ארץ.
- Canonical skill IDs used: `PARTICLE.DIRECT_OBJECT_MARKER`, `WORD.MEANING_BASIC`.
- Zekelman standards that may apply: `3.03` for direct-object-marker/function-word review and `3.01` for noun vocabulary.
- What remains uncertain: whether article-level 3.06 follow-up should be added later for שמים/ארץ once separate article evidence is stronger.
- Why no token-level candidate is verified yet: the contract lanes are clearer now, but each token still required Yossi review and none of the rows were auto-approved.

## `std_b1_3_r013` | יהי אור

- Why the phrase-level candidate is too broad: אור fits a noun-vocabulary lane, while יהי belongs in a separate verb-form or morphology-oriented lane.
- Tokens needing separate review: יהי and אור.
- Canonical skill IDs used: `VERB.TENSE.FUTURE`, `WORD.MEANING_BASIC`.
- Zekelman standards that may apply: `3.07` for the verb-form side and `3.01` for noun vocabulary.
- What remains uncertain: whether יהי should remain only a standards follow-up row or wait for stronger morphology evidence before Yossi narrows it further.
- Why no token-level candidate is verified yet: even the stronger אור evidence was still review-only sample support and the יהי parse remained indirect before Yossi review.

## `std_b1_5_r020` | לאור יום

- Why the phrase-level candidate is too broad: the phrase mixes a prefixed preposition candidate with two noun-vocabulary targets.
- Tokens needing separate review: prefixed ל from לאור, base אור, and יום.
- Canonical skill IDs used: `PREFIX.BASIC_PREPOSITIONS`, `WORD.MEANING_BASIC`.
- Zekelman standards that may apply: `3.06` for the prefixed ? lane and `3.01` for noun vocabulary.
- What remains uncertain: whether the prefixed ל row is strong enough for verification or should remain follow-up until Yossi confirms the standards framing.
- Why no token-level candidate is verified yet: even with clearer token boundaries, the standards mappings stayed review-only until Yossi made an explicit decision.