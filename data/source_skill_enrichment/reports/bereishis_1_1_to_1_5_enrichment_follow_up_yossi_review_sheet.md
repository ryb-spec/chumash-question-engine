# Bereishis 1:1-1:5 Enrichment Follow-Up Yossi Review Sheet

## Scope Summary

- Scope: Bereishis 1:1-1:5 enrichment follow-up candidates only.
- Unresolved candidates included: 10.
- Already verified candidates are intentionally excluded from this follow-up sheet.
- Every proposed skill and standard reference below is anchored through `data/standards/canonical_skill_contract.json`.
- Mark each row with one allowed decision: `verified`, `needs_follow_up`, `source_only`, `block_for_questions`, `fix_morphology`, `fix_standard`, or `fix_vocabulary`.
- Recommended decisions below are intentionally conservative; none of these unresolved rows are pre-cleared for verification.
- This is enrichment follow-up review only. It is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

## Vocabulary/Shoresh Follow-Up

### `vocab_b1_1_r002_t001` | Bereishis 1:1 | ברא

- Current decision/status: `fix_vocabulary` / `needs_follow_up`.
- What changed since last review: Evidence strengthened but First 150 remains unconfirmed: vocab_entry.bara supports ברא=create/created as a high-frequency Bereishis verb sample, and word_parse.bereishis_1_1.bara supports shoresh ברא=create. Searches did not find an exact repo-local First 150 record for ברא; therefore first_150_match remains false and this stays unresolved for Yossi follow-up.
- Contract anchor: `ROOT.IDENTIFY`.
- Contract standards: `3.02` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The unresolved `shoresh` proposal maps directly through `ROOT.IDENTIFY` in the canonical contract, which carries Standard 3.02 without treating vocabulary sampling as approval.
- Missing evidence: Exact First 150 Shorashim and Keywords source record for ???.
- What Yossi needs to decide: Can ???=create/created stay a review-only shoresh candidate from the linked sample evidence, or does Yossi want a local First 150 source row before any enrichment verification?
- Recommended decision: `fix_vocabulary`.

### `vocab_b1_3_r013_t002` | Bereishis 1:3 | אור

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened: vocab_entry.or is an exact First 150 Shorashim and Keywords in Bereishis sample for אור=light. The sample itself has review_status=needs_review/manual_sample_only, so this remains a follow-up candidate and does not become automatically verified.
- Contract anchor: `WORD.MEANING_BASIC`.
- Contract standards: `3.01` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The unresolved `noun_keyword` proposal maps through `WORD.MEANING_BASIC`, the contract lane tied to Standard 3.01 noun-vocabulary work.
- Missing evidence: Reviewed or normalized First 150 row; the current support is sample-only and still needs Yossi confirmation.
- What Yossi needs to decide: Is sample `vocab_entry.or` enough to keep ???=light as a review-only vocabulary candidate, or should it wait for a reviewed First 150 source row?
- Recommended decision: `needs_follow_up`.

### `vocab_b1_2_r007_t001` | Bereishis 1:2 | וחשך

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence clarified, not fully strengthened: verified phrase/source extraction supports וחשך=and darkness in context, but no exact First 150, vocabulary seed, or trusted standalone keyword record for base חשך was located. Prefix/conjunction morphology remains separate from vocabulary evidence.
- Contract anchor: `WORD.MEANING_BASIC`.
- Contract standards: `3.01` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The lexical target is base ???, so the unresolved noun-keyword proposal anchors through `WORD.MEANING_BASIC`; the prefixed ? remains outside this vocabulary claim.
- Missing evidence: Standalone trusted vocabulary or shoresh record for ???=darkness.
- What Yossi needs to decide: Should ??? stay source-only or follow-up until a standalone vocabulary record exists, instead of leaning on contextual phrase evidence alone?
- Recommended decision: `source_only`.

## Morphology Follow-Up

### `morph_b1_2_r004_t001` | Bereishis 1:2 | והארץ

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Component evidence strengthened: DK-CONJ-001 models prefixed ? as a conjunction before a noun; DK-ARTICLE-001 models prefixed ? as the definite article before a noun; the base ארץ=land vocabulary candidate is already Yossi enrichment-verified. This supports the proposed והארץ component analysis (והארץ -> ? + ? + ארץ) for follow-up review, but it does not by itself verify the exact token split.
- Contract anchor: `PREFIX.FORM_IDENTIFY; WORD.PARTS.SEGMENT`.
- Contract standards: `3.06` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The unresolved `prefix/article split needs evidence` note maps through `PREFIX.FORM_IDENTIFY`; `WORD.PARTS.SEGMENT` keeps the token-splitting lane explicit without claiming more than the evidence supports.
- Missing evidence: No reviewed token-level source explicitly parses ????? as ? + ? + ??? in this enrichment layer.
- What Yossi needs to decide: Can Yossi keep ????? in a review-only prefix/article split lane from the linked component evidence, or should the token stay unresolved until an explicit token parse is cited?
- Recommended decision: `fix_morphology`.

### `morph_b1_3_r013_t001` | Bereishis 1:3 | יהי

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened but remains unresolved: local word_bank entries for יהי/???? record future_jussive-style hints, and Zekelman 3.07 supports verb/future-prefix work using ???? markers. No trusted reviewed source in this pilot directly parses יהי as shoresh היה with jussive/imperfect function, so this remains follow-up evidence rather than verification.
- Contract anchor: `WORD.PART_OF_SPEECH_BASIC; VERB.TENSE.FUTURE; PREFIX.OTIYOT_EITAN`.
- Contract standards: `3.04; 3.07` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The unresolved `verb` and `jussive/verb-form candidate needs evidence` labels map through `WORD.PART_OF_SPEECH_BASIC`, `VERB.TENSE.FUTURE`, and `PREFIX.OTIYOT_EITAN` in the contract, while staying review-only.
- Missing evidence: A reviewed token-level morphology source directly connecting ??? to its shoresh and jussive or imperfect function in Bereishis 1:3.
- What Yossi needs to decide: Is the linked 3.07 and local-word-bank evidence enough to keep ??? in a review-only verb-form lane, or should it remain unresolved until a direct morphology source is cited?
- Recommended decision: `needs_follow_up`.

## Standards Follow-Up

### `std_b1_1_r002` | Bereishis 1:1 | ברא אלקים

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened for a token-level split: Zekelman 3.02 covers cumulative shoresh vocabulary and root identification; word_parse.bereishis_1_1.bara supports token ברא as shoresh ברא. The current candidate is phrase-level (ברא ?????), so it remains needs_follow_up until split to token ברא.
- Contract anchor: `ROOT.IDENTIFY`.
- Contract standards: `3.02` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The proposed `std3_02_shoresh_identification` reference maps directly through `ROOT.IDENTIFY`; the unresolved issue is phrase scope, not contract identity.
- Missing evidence: A token-level standards candidate for ??? alone rather than the full phrase ??? ?????.
- What Yossi needs to decide: Should this broad phrase row be split so only ??? anchors to Standard 3.02 and the rest of the phrase stays outside this standards candidate?
- Recommended decision: `fix_standard`.

### `std_b1_1_r003` | Bereishis 1:1 | את השמים ואת הארץ

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence clarified for token-level split: 3.01 applies to noun vocabulary such as שמים/ארץ; 3.03 covers function-word vocabulary; 3.06 and the raw Standard 3 appendix discuss את as direct-object marker/with and definite nouns/articles. The phrase is too broad for one standards candidate.
- Contract anchor: `PARTICLE.DIRECT_OBJECT_MARKER; WORD.MEANING_BASIC; PREFIX.FORM_IDENTIFY`.
- Contract standards: `3.01; 3.03; 3.06` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The current phrase mixes noun vocabulary with direct-object-marker and article-prefix material; those references map through `WORD.MEANING_BASIC`, `PARTICLE.DIRECT_OBJECT_MARKER`, and `PREFIX.FORM_IDENTIFY` in the contract.
- Missing evidence: Separate token-level candidates for ??, ?????, ????, and any article or prefix features instead of one bundled phrase row.
- What Yossi needs to decide: Should Yossi split this phrase into direct-object-marker and noun-vocabulary contract lanes instead of treating it as one standards candidate?
- Recommended decision: `fix_standard`.

### `std_b1_3_r013` | Bereishis 1:3 | יהי אור

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened for a token-level split: 3.01 can apply to noun vocabulary token אור, and vocab_entry.or supports אור=light as a First 150 sample. יהי belongs to a separate morphology/verb-form review lane, likely related to 3.07, so the phrase-level standards row remains unresolved.
- Contract anchor: `WORD.MEANING_BASIC; VERB.TENSE.FUTURE; PREFIX.OTIYOT_EITAN`.
- Contract standards: `3.01; 3.07` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The 3.01 noun-vocabulary reference maps through `WORD.MEANING_BASIC`, while the unresolved ??? verb-form evidence belongs in the 3.07-aligned `VERB.TENSE.FUTURE` and `PREFIX.OTIYOT_EITAN` lanes.
- Missing evidence: A token-level standards candidate for ??? plus a separate disposition for ??? under morphology or verb-form review.
- What Yossi needs to decide: Should Yossi split ??? ??? so ??? anchors to the noun-vocabulary lane while ??? stays in morphology follow-up?
- Recommended decision: `fix_standard`.

### `std_b1_5_r020` | Bereishis 1:5 | לאור יום

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened for a token-level split: אור has First 150 sample support and יום=day is Yossi enrichment-verified vocabulary; 3.01 applies to noun vocabulary while 3.06/prefix evidence may be needed for the ? prefix in ????. The phrase-level standards row remains too bundled.
- Contract anchor: `WORD.MEANING_BASIC; PREFIX.BASIC_PREPOSITIONS`.
- Contract standards: `3.01; 3.03; 3.06` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The noun-vocabulary references map through `WORD.MEANING_BASIC`, while the prefixed ? aligns to `PREFIX.BASIC_PREPOSITIONS`; the contract keeps those lanes separate.
- Missing evidence: Separate token-level candidates for ???, ???, and prefixed ? if Yossi wants standards treatment for all parts of the phrase.
- What Yossi needs to decide: Should ???? ??? be split into noun-vocabulary and prefix lanes instead of staying one phrase-level standards row?
- Recommended decision: `fix_standard`.

### `std_b1_2_r010` | Bereishis 1:2 | מרחפת

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence gap remains: the verified source-to-skill row supports מרחפת as source-derived text, and 3.07 is the broad verb standard, but no trusted local token-level parse or standards mapping was located for מרחפת. Keep as needs_mapping_review.
- Contract anchor: `VERB.TENSE.PAST; VERB.TENSE.PRESENT; VERB.TENSE.FUTURE; VERB.COMMAND`.
- Contract standards: `3.07` via `data/standards/canonical_skill_contract.json`.
- Why this maps through contract: The broad 3.07 reference does map into the contract, but only as a set of unresolved verb-form lanes; this row should not claim a narrower canonical skill until a trusted parse exists.
- Missing evidence: A trusted token-level parse for ????? plus a narrower contract lane within Standard 3.07.
- What Yossi needs to decide: Should ????? remain unresolved inside the broad 3.07 verb lane until a trusted parse clarifies which contract sub-lane actually fits?
- Recommended decision: `needs_follow_up`.
