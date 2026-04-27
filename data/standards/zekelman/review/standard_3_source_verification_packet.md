# Zekelman Standard 3 Source Verification Packet

Current branch: `feature/standard-3-source-verification-final-decisions`
Status: `human_review_support_only`
Runtime status: `not_runtime_ready`
Question-generation status: `not_question_ready`

## Purpose
- Prepare final human source verification for the remaining unresolved Zekelman Standard 3 strands.
- Help a teacher/reviewer compare the canonical Zekelman 2025 expectations against supplemental Loshon HaTorah / Loshon Hakodesh evidence.
- Preserve the boundary that source evidence can support review, but it does not itself create a teacher decision.

## Source Hierarchy
- Canonical authority: `docs/standards/zekelman/raw/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8.pdf`.
- Supplemental evidence: Loshon HaTorah / Loshon Hakodesh source files and extracted text.
- The answer booklet may clarify exercises or rule applications from the main book, but it must not override the main book or Zekelman 2025.
- If evidence is unclear, OCR-sensitive, or table-dependent, keep it unresolved and flag it for human review.

## Decision Boundary
- No reviewer decisions are recorded in this packet.
- Pending strands must remain pending until an explicit human reviewer decision is provided.
- Even if a reviewer approves a strand as a foundational diagnostic direction, it still remains `not_runtime_ready` and `not_question_ready`.

Allowed reviewer decisions:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

Conservative statuses:
- `needs_teacher_review`
- `source_match_needs_verification`
- `hebrew_needs_verification`
- `level_mapping_needs_review`
- `not_runtime_ready`
- `not_question_ready`

## Primary Review Target 1: 3.08 Grouping And Word Order
- Standard ID: `3.08`
- Strand name: Grouping and word order.
- Current reviewer decision status: pending; no reviewer decision recorded.
- Current review status: `needs_teacher_review`, `source_match_needs_verification`, `level_mapping_needs_review`, `not_runtime_ready`, `not_question_ready`.
- Canonical Zekelman expectation summary: Students group a פסוק into meaningful phrases and adjust Hebrew word order when translating into English, moving from learned פסוקים to unlearned פסוקים with increasing independence.
- Current draft skill mapping: `std3_08_syntax_phrase_structure` / "Group phrases and adjust Hebrew word order for translation".
- Evidence strength: `partial`. The Loshon evidence is strong for verb/noun order and English reordering, but only partial for the full Zekelman 3.08 range of phrase grouping in unlearned פסוקים.

Relevant Loshon evidence:
| Candidate ID | Evidence type | Source references | Short evidence summary |
| --- | --- | --- | --- |
| `lht_cand_word_order_variable` | `direct_support` | `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`, main extracted page 4 / printed p. 6, Lesson 1 | Explains that Torah wording can place the verb before or after the noun. |
| `lht_cand_natural_english_reordering` | `direct_support` | Main extracted page 4 / printed p. 6; answer booklet extracted pages 5, 14-15, 31-32 | Explains and practices translating literal Hebrew order into natural English order. |
| `lht_cand_smichus_construct_phrase` | `partial_support` | Main extracted page 6 / printed p. 10, Lesson 2; answer booklet extracted pages 6-7 | Supports phrase grouping through סמיכות / construct relationships. |
| `lht_cand_smichus_ambiguity` | `clarifies_rule` | Main extracted page 80 / printed p. 158, Lesson 16 | Shows why construct-like translation may need context and should not become an isolated prompt too quickly. |

What the reviewer must verify:
- Whether Loshon word-order evidence is close enough to Zekelman 3.08 wording to support a distinct diagnostic planning lane.
- Whether `3.08` should remain full-context only because grouping depends on phrase relationships and broader פסוק context.
- Whether סמיכות support belongs primarily under `3.04`, `3.08`, or both.
- Whether the extracted Loshon page references are reliable enough, given the partial OCR layer.

Specific reviewer questions:
- Is variable verb/noun order sufficient to treat `3.08` as a distinct reviewable diagnostic direction?
- Should natural English reordering be approved only for full-pasuk or phrase-translation review, rather than compact isolated questions?
- Should סמיכות-based grouping be reviewed as part of `3.08`, or should it remain under `3.04` until a later phase?
- Does the answer booklet clarify the main-book rule, or does it introduce practice patterns that should not guide planning yet?

Unresolved Hebrew/OCR/table concerns:
- Main-book text extraction is partial; direct PDF inspection is needed.
- Hebrew examples and printed page references should be verified visually in the PDF.
- Answer-booklet evidence should not be converted into an active answer key or question template.

Recommended decision options:
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `defer_to_later_phase`

## Primary Review Target 2: 3.04 Parts Of Speech / Nouns And Adjectives
- Standard ID: `3.04`
- Strand name: Parts of speech, noun/adjective features, and סמיכות.
- Current reviewer decision status: pending; no reviewer decision recorded.
- Current review status: `needs_teacher_review`, `source_match_needs_verification`, `hebrew_needs_verification`, `level_mapping_needs_review`, `not_runtime_ready`, `not_question_ready`.
- Canonical Zekelman expectation summary: Students move from identifying nouns and adjectives in learned words to recognizing gender, number, irregular forms, and סמיכות in unlearned פסוקים.
- Current draft skill mappings: `std3_04_noun_features`; `std3_04_smichut_recognition`.
- Evidence strength: `partial`. Loshon evidence is strong for noun features and סמיכות, but it does not by itself settle the full Zekelman level map or all adjective/part-of-speech boundaries.

Relevant Loshon evidence:
| Candidate ID | Evidence type | Source references | Short evidence summary |
| --- | --- | --- | --- |
| `lht_cand_noun_gender_number` | `direct_support` | Main extracted page 81 / printed p. 160 summary; answer booklet extracted pages 9-10, Lesson 4 | Supports noun gender, number, common plural endings, and noun-ending exercises. |
| `lht_cand_smichus_construct_phrase` | `direct_support` | Main extracted page 6 / printed p. 10, Lesson 2; answer booklet extracted pages 6-7 | Explains two nouns side by side as a construct phrase with "the __ of __" meaning. |
| `lht_cand_smichus_form_changes` | `clarifies_rule` | Main extracted page 6 and page 81 summary | Supports common construct-form changes such as final ה or ים shifts. |
| `lht_cand_plural_looking_singular_english` | `clarifies_rule` | Main extracted page 81 / printed p. 160 summary | Flags irregular or exception-like noun forms and English number mismatch. |

What the reviewer must verify:
- Whether `3.04` should be split into separate final-review decisions for noun/adjective features and סמיכות.
- Whether סמיכות is suitable for standalone diagnostic planning or must remain tied to fuller phrase translation.
- Whether Loshon noun-feature evidence aligns with Zekelman 2025 level progression.
- Whether irregular noun forms and adjective agreement should be foundational, later-level, or deferred.

Specific reviewer questions:
- Should `std3_04_noun_features` and `std3_04_smichut_recognition` receive separate decisions?
- Does Loshon support enough of סמיכות to help review `3.08`, or should it stay only under `3.04`?
- Are plural-looking singular English forms suitable for diagnostic planning, or only a caution note?
- How should OCR-sensitive Hebrew examples be verified before any later blueprint uses them?

Unresolved Hebrew/OCR/table concerns:
- סמיכות examples require direct PDF verification of Hebrew forms and nekudos.
- The main-book summary page is helpful but compressed; original rule pages should be visually checked.
- Answer-booklet examples are useful for review but not for active answer-key use.

Recommended decision options:
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `defer_to_later_phase`

## Primary Review Target 3: 3.10 Understanding ניקוד
- Standard ID: `3.10`
- Strand name: Understanding ניקוד.
- Current reviewer decision status: pending; no reviewer decision recorded.
- Current review status: `needs_teacher_review`, `source_match_needs_verification`, `hebrew_needs_verification`, `level_mapping_needs_review`, `not_runtime_ready`, `not_question_ready`.
- Canonical Zekelman expectation summary: Advanced students explain systems of תנועות, שבאים, דגשים, syllables, and the interaction between ניקוד and טעמי המקרא. Lower levels show no clearly scoped expectation in the current extraction.
- Current draft skill mapping: `std3_10_nikud_reading` / "Recognize advanced ניקוד patterns and syllable rules".
- Evidence strength: `weak`. Loshon adds nikud-sensitive examples and pausal/vowel-change cautions, but does not support the full advanced Zekelman `3.10` scope.

Relevant Loshon evidence:
| Candidate ID | Evidence type | Source references | Short evidence summary |
| --- | --- | --- | --- |
| `lht_cand_limited_nikud_sensitive_et` | `unclear` | Main extracted page 81 / printed p. 160 summary, citing pg. 9; answer booklet extracted page 29 / Lesson 15 | Notes את-family nikud/function distinctions, but this is narrow and OCR-sensitive. |
| `lht_cand_pausal_forms_nikud_boundary` | `partial_support` | Answer booklet extracted pages 22 and 29; notes citing main-book p. 96 | Mentions pausal form or end-of-sentence vowel changes, but main-book page verification is still needed. |

What the reviewer must verify:
- Whether `3.10` should remain deferred until direct canonical and Loshon PDF review confirms the advanced-only level gate.
- Whether any small nikud-sensitive subskill should be reviewed with `3.06`, or whether all `3.10` content should stay in a later phase.
- Whether the answer booklet's pausal/vowel notes are enough to guide review questions, or only enough to flag an unresolved area.
- Whether OCR and nekudos are reliable enough to cite without direct visual review.

Specific reviewer questions:
- Are levels 1-4 intentionally out of scope for `3.10`, or does the canonical extraction need another manual pass?
- Does the limited את-family nikud evidence belong under `3.06` only, under `3.10`, or under both as a caution boundary?
- Should pausal-form evidence be considered source support for `3.10`, or only a signal for later review?
- Which parts of תנועות, שבאים, דגשים, syllables, and טעמי המקרא are actually present in the canonical Zekelman source at each level?

Unresolved Hebrew/OCR/table concerns:
- Nekudos and table relationships are high-risk for OCR error.
- The Loshon main-book p. 96 reference comes through answer-booklet notes and should be checked directly in the raw PDF.
- This strand should not be marked approved based on the current supplemental evidence.

Recommended decision options:
- `needs_more_source_review`
- `defer_to_later_phase`
- `not_suitable_for_diagnostic_use_yet`

## Secondary Verification Target: 3.07 Verbs
- Existing documented decision: `approve_with_level_adjustment` for foundational tense/person/form planning only.
- Loshon evidence strengthens: foundational agreement, shoresh-plus-added-letter analysis, past/future markers, weak-letter cautions, ו׳ ההיפוך as context-sensitive, and later-lane evidence for present tense and command forms.
- Caution remaining: advanced בנינים, passive forms, ציווי, מקור, שם הפועל, weak roots, present tense, and ו׳ ההיפוך should remain separate later lanes unless a reviewer explicitly narrows and approves them.
- Should existing reviewer notes be revisited? Yes, to decide whether the new Loshon weak-letter and ו׳ ההיפוך evidence requires clearer wording around deferred sublanes.

## Secondary Verification Target: 3.06 Prefixes / Articles / Prepositions
- Existing documented decision: `approve_with_wording_revision` for visible prefix and article identification only.
- Loshon evidence strengthens: definite ה, conjunctive ו, full-word prepositions, prefix prepositions, and context-sensitive את-family cautions.
- Caution remaining: the two functions of את, nikud-dependent prefix shifts, and ו׳ ההיפוך remain context-sensitive and should not be treated as simple visible-prefix diagnostics.
- Should existing reviewer notes be revisited? Yes, mainly to clarify whether את-family nikud evidence stays under `3.06`, feeds later `3.10`, or both.

## Secondary Verification Target: 3.05 Pronouns And Suffixes
- Existing documented decision: `approve_with_wording_revision` requiring at least two lanes: pronoun referent tracking and pronominal suffix decoding.
- Loshon evidence strengthens: possessive suffix decoding on singular and plural noun forms, plus person/gender/number terminology.
- Caution remaining: referent tracking is not resolved by suffix tables; cross-pasuk referents and pronoun clues from verb forms still need teacher boundary-setting.
- Should existing reviewer notes be revisited? Yes, to decide whether suffix decoding can be documented as a separate foundational planning lane while referent tracking remains context-bound.

## Reviewer Worksheet
| Standard ID | Reviewer decision | Reviewer notes | Remaining source checks | Recommended next action |
| --- | --- | --- | --- | --- |
| `3.08` | `________________` | `________________` | `________________` | `________________` |
| `3.04` | `________________` | `________________` | `________________` | `________________` |
| `3.10` | `________________` | `________________` | `________________` | `________________` |

## Final Boundary Reminder
- This packet prepares human review only.
- It does not generate questions, answer keys, active templates, runtime hooks, or reviewed-bank content.
- It does not record approval for `3.08`, `3.04`, or `3.10`.
