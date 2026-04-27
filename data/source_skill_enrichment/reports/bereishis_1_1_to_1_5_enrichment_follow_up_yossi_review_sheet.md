# Bereishis 1:1-1:5 Enrichment Follow-Up Yossi Review Sheet

## Scope Summary

- Scope: Bereishis 1:1-1:5 enrichment follow-up candidates only.
- Unresolved candidates included: 10.
- Already verified candidates are intentionally excluded from this follow-up sheet.
- Mark each row with one allowed decision: `verified`, `needs_follow_up`, `source_only`, `block_for_questions`, `fix_morphology`, `fix_standard`, or `fix_vocabulary`.
- This is enrichment follow-up review only. It is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing approval.

## Vocabulary/Shoresh Follow-Up

### `vocab_b1_1_r002_t001` | Bereishis 1:1 | ברא

- Current decision/status: `fix_vocabulary` / `needs_follow_up`.
- What changed since last review: Evidence strengthened but First 150 remains unconfirmed: vocab_entry.bara supports ברא=create/created as a high-frequency Bereishis verb sample, and word_parse.bereishis_1_1.bara supports shoresh ברא=create. Searches did not find an exact repo-local First 150 record for ברא; therefore first_150_match remains false and this stays unresolved for Yossi follow-up.
- Missing evidence: Exact First 150 Shorashim and Keywords source record for ???.
- What Yossi needs to decide: Can ברא=create/created be enrichment-verified from the linked vocab/word-parse samples despite no exact local First 150 row?
- Recommended decision: `needs_follow_up`.

### `vocab_b1_3_r013_t002` | Bereishis 1:3 | אור

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened: vocab_entry.or is an exact First 150 Shorashim and Keywords in Bereishis sample for אור=light. The sample itself has review_status=needs_review/manual_sample_only, so this remains a follow-up candidate and does not become automatically verified.
- Missing evidence: Reviewed/normalized First 150 row; current evidence is sample-only and needs Yossi confirmation.
- What Yossi needs to decide: Is sample `vocab_entry.or` sufficient to verify אור=light as vocabulary enrichment?
- Recommended decision: `verified`.

### `vocab_b1_2_r007_t001` | Bereishis 1:2 | וחשך

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence clarified, not fully strengthened: verified phrase/source extraction supports וחשך=and darkness in context, but no exact First 150, vocabulary seed, or trusted standalone keyword record for base חשך was located. Prefix/conjunction morphology remains separate from vocabulary evidence.
- Missing evidence: Standalone trusted vocabulary/shoresh record for ???/darkness.
- What Yossi needs to decide: Should חשך=darkness stay follow-up/source-only until a standalone vocabulary record is found?
- Recommended decision: `needs_follow_up`.

## Morphology Follow-Up

### `morph_b1_2_r004_t001` | Bereishis 1:2 | והארץ

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Component evidence strengthened: DK-CONJ-001 models prefixed ? as a conjunction before a noun; DK-ARTICLE-001 models prefixed ? as the definite article before a noun; the base ארץ=land vocabulary candidate is already Yossi enrichment-verified. This supports the proposed והארץ component analysis (והארץ -> ? + ? + ארץ) for follow-up review, but it does not by itself verify the exact token split.
- Missing evidence: No reviewed token-level source explicitly parses the exact token ????? as ? + ? + ??? in this enrichment layer.
- What Yossi needs to decide: Can Yossi approve והארץ as ? conjunction + ? definite article + base noun ארץ for enrichment only?
- Recommended decision: `verified`.

### `morph_b1_3_r013_t001` | Bereishis 1:3 | יהי

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened but remains unresolved: local word_bank entries for יהי/???? record future_jussive-style hints, and Zekelman 3.07 supports verb/future-prefix work using ???? markers. No trusted reviewed source in this pilot directly parses יהי as shoresh היה with jussive/imperfect function, so this remains follow-up evidence rather than verification.
- Missing evidence: A reviewed token-level morphology source directly connecting ??? to ??? and its jussive/imperfect function in Bereishis 1:3.
- What Yossi needs to decide: Is the linked 3.07/future-prefix evidence enough to approve יהי as a היה-root jussive/imperfect candidate, or should it stay follow-up?
- Recommended decision: `needs_follow_up`.

## Standards Follow-Up

### `std_b1_1_r002` | Bereishis 1:1 | ברא אלקים

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened for a token-level split: Zekelman 3.02 covers cumulative shoresh vocabulary and root identification; word_parse.bereishis_1_1.bara supports token ברא as shoresh ברא. The current candidate is phrase-level (ברא ?????), so it remains needs_follow_up until split to token ברא.
- Missing evidence: Token-level standards candidate for ??? only.
- What Yossi needs to decide: Should this phrase-level row be replaced by or split into a token-level ??? -> 3.02 standards candidate?
- Recommended decision: `fix_standard`.

### `std_b1_1_r003` | Bereishis 1:1 | את השמים ואת הארץ

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence clarified for token-level split: 3.01 applies to noun vocabulary such as שמים/ארץ; 3.03 covers function-word vocabulary; 3.06 and the raw Standard 3 appendix discuss את as direct-object marker/with and definite nouns/articles. The phrase is too broad for one standards candidate.
- Missing evidence: Separate token-level candidates for ??, ????, ???, and article/prefix features.
- What Yossi needs to decide: Should Yossi approve splitting this broad phrase into function-word and noun-vocabulary standards candidates?
- Recommended decision: `fix_standard`.

### `std_b1_3_r013` | Bereishis 1:3 | יהי אור

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened for a token-level split: 3.01 can apply to noun vocabulary token אור, and vocab_entry.or supports אור=light as a First 150 sample. יהי belongs to a separate morphology/verb-form review lane, likely related to 3.07, so the phrase-level standards row remains unresolved.
- Missing evidence: Token-level standards candidate for ??? only, plus separate morphology/verb-form candidate for ???.
- What Yossi needs to decide: Should אור be split into a token-level 3.01 standards candidate while יהי stays morphology follow-up?
- Recommended decision: `fix_standard`.

### `std_b1_5_r020` | Bereishis 1:5 | לאור יום

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence strengthened for a token-level split: אור has First 150 sample support and יום=day is Yossi enrichment-verified vocabulary; 3.01 applies to noun vocabulary while 3.06/prefix evidence may be needed for the ? prefix in ????. The phrase-level standards row remains too bundled.
- Missing evidence: Separate token-level standards candidates for ???, ???, and ? prefix if standards mapping is desired.
- What Yossi needs to decide: Should this be split into אור/יום noun-vocabulary standards candidates and a separate ? prefix standards candidate?
- Recommended decision: `fix_standard`.

### `std_b1_2_r010` | Bereishis 1:2 | מרחפת

- Current decision/status: `needs_follow_up` / `needs_follow_up`.
- What changed since last review: Evidence gap remains: the verified source-to-skill row supports מרחפת as source-derived text, and 3.07 is the broad verb standard, but no trusted local token-level parse or standards mapping was located for מרחפת. Keep as needs_mapping_review.
- Missing evidence: Trusted parse and standards mapping for ?????.
- What Yossi needs to decide: Should מרחפת remain standards follow-up until morphology evidence exists?
- Recommended decision: `needs_follow_up`.
