# Bereishis 1:1-1:5 Enrichment Pilot Completion Report

## A. Executive Summary

Bereishis 1:1-1:5 now has a reviewed enrichment pilot pattern across morphology, vocabulary/shoresh, and standards. This milestone locks the pilot as a reusable review-only pattern; it does not mark the slice fully resolved, and it does not open any later approval gate.

## B. Scope

- Bereishis 1:1-1:5 only.

## C. Architecture

- source-to-skill maps remain phrase-level extraction truth
- enrichment lives in separate candidate layers
- token-level morphology and standards are handled outside the source-to-skill maps
- canonical skill contract anchors standards and skill IDs through `data/standards/canonical_skill_contract.json`
- question eligibility remains a later gate

## D. Candidate Summary

- morphology: total=5; verified=3; needs_follow_up=2; source_only=0; blocked=0; safety_gates=question_allowed:needs_review/protected_preview_allowed:false/reviewed_bank_allowed:false/runtime_allowed:false
- vocabulary_shoresh: total=6; verified=3; needs_follow_up=3; source_only=0; blocked=0; safety_gates=question_allowed:needs_review/protected_preview_allowed:false/reviewed_bank_allowed:false/runtime_allowed:false
- phrase_level_standards: total=6; verified=1; needs_follow_up=5; superseded_unresolved=4; safety_gates=question_allowed:needs_review/protected_preview_allowed:false/reviewed_bank_allowed:false/runtime_allowed:false
- token_split_standards: total=10; verified=7; needs_follow_up=3; source_only=0; blocked=0; safety_gates=question_allowed:needs_review/protected_preview_allowed:false/reviewed_bank_allowed:false/runtime_allowed:false

Canonical contract validation remains required for every enrichment artifact and continues to pass through `data/standards/canonical_skill_contract.json`.

## E. Verified Enrichment

### Morphology

- `morph_b1_1_r002_t001` | ברא | shoresh ברא; past 3ms verb parse candidate
- `morph_b1_1_r002_t002` | אלקים | noun; plural form / singular meaning feature candidate
- `morph_b1_2_r005_t001` | היתה | shoresh היה; past 3fs verb parse candidate

### Vocabulary/Shoresh

- `vocab_b1_2_r004_t001` | והארץ -> base ארץ | noun-keyword `land`
- `vocab_b1_5_r020_t002` | יום | noun-keyword `day`
- `vocab_b1_2_r011_t003` | המים -> base מים | noun-keyword `water`

### Phrase-Level Standards

- `std_b1_2_r004` | והארץ | verified phrase-level standards candidate retained from the original pilot while all safety gates stay closed

### Token-Split Standards

- `stdtok_b1_1_r002_t001` | ברא | `3.02` / `ROOT.IDENTIFY`
- `stdtok_b1_1_r003_t001` | את | `3.03` / `PARTICLE.DIRECT_OBJECT_MARKER`
- `stdtok_b1_1_r003_t003` | את` from surface `ואת` | `3.03` / `PARTICLE.DIRECT_OBJECT_MARKER`
- `stdtok_b1_1_r003_t004` | ארץ | `3.01` / `WORD.MEANING_BASIC`
- `stdtok_b1_3_r013_t002` | אור | `3.01` / `WORD.MEANING_BASIC`
- `stdtok_b1_5_r020_t001` | אור` from `לאור` | `3.01` / `WORD.MEANING_BASIC`
- `stdtok_b1_5_r020_t002` | יום | `3.01` / `WORD.MEANING_BASIC`

## F. Remaining Follow-Up

- `וחשך` remains vocabulary/shoresh follow-up only; current support is contextual phrase evidence, not a stronger standalone vocabulary witness.
- `יהי` remains morphology and standards follow-up only; the pilot still lacks stronger token-level verb-form evidence.
- `שמים` remains token-split standards follow-up only; the standards row is plausible but still low-confidence without a stronger local vocabulary link.
- prefixed `ל` remains token-split standards follow-up only; the prefix/preposition lane still needs stronger standards evidence.
- `vocab_b1_1_r002_t001` for ברא remains follow-up because exact repo-local First 150 support is still not linked.
- `std_b1_2_r010` for מרחפת remains phrase-level standards follow-up because it still needs narrower token-level verb-form evidence.
- parent bundled phrase-level standards rows `std_b1_1_r002`, `std_b1_1_r003`, `std_b1_3_r013`, and `std_b1_5_r020` remain preserved as unresolved/superseded parent rows.

## G. Token-Split Standards Outcome

- Phrase-level standards rows were too broad because they bundled vocabulary, function-word, and morphology/prefix claims inside single review decisions.
- Token-split candidates fixed that by isolating exact token-level review decisions while keeping every safety gate closed.
- Verified token-level standards candidates:
  - ברא
  - first את
  - second את from surface ואת
  - ארץ
  - אור in יהי אור
  - אור in לאור
  - יום
- Token-level standards items still in follow-up:
  - שמים
  - יהי
  - prefixed ל

## H. Hebrew Encoding Correction

- Hebrew corruption was detected in the token-split TSV/CSV.
- source artifacts were corrected to real UTF-8 Hebrew.
- Markdown and CSV review sheets were regenerated from the corrected artifacts.
- validation now checks real Hebrew rendering so placeholder question-mark corruption does not silently return.

## I. Safety Gate Summary

- question generation remains blocked
- protected preview remains blocked
- reviewed bank remains blocked
- runtime remains blocked
- student-facing use remains blocked

No enrichment row in this pilot is question-ready, protected-preview-ready, reviewed-bank-ready, runtime-ready, or student-facing.

## J. Pattern For Scaling

1. generate candidate rows only from verified source-to-skill rows
2. keep candidates safety-closed
3. map skill/standard IDs through canonical contract
4. use token-level splits for standards where phrase-level row is too broad
5. create Yossi-friendly review sheets
6. apply only reviewed decisions
7. leave uncertain items follow-up

## K. Recommended Next Step

Commit this Bereishis 1:1-1:5 enrichment pilot milestone first, then expand enrichment to Bereishis 1:6-1:13 using the same pilot pattern only after this milestone is committed.
