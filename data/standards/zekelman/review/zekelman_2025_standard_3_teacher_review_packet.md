# Zekelman 2025 Standard 3 Teacher Review Packet

Current branch: `feature/standard-3-source-verification-final-decisions`
Status: `review_only`
Runtime status: `not_runtime_ready`
Question-generation status: `not_question_ready`

## Scope
- This packet prepares teacher review for the most question-relevant Zekelman 2025 Standard 3 strands before any runtime use or question generation.
- It is based only on existing local source-backed artifacts:
  - `data/standards/zekelman/structured/zekelman_2025_standard_3_vocabulary_language_skills.json`
  - `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_supplemental_crosswalk.json`
  - `data/standards/zekelman/crosswalks/zekelman_2025_standard_3_skill_mapping_draft.json`
  - `data/standards/zekelman/reports/zekelman_2025_standard_3_supplemental_crosswalk_report.md`
- Canonical raw source:
  - `docs/standards/zekelman/raw/2025_zekelman_chumash_standards_v2_5_complete_levels_1_8.pdf`
- Supplemental raw sources:
  - `docs/standards/zekelman/raw/2014_intro_vocabulary_language_skills_zekelman_chumash.pdf`
  - `docs/standards/zekelman/raw/2014_appendix_free_resource_packet_zekelman_chumash.pdf`
  - `docs/standards/zekelman/raw/2016_sample_assessment_questions_standards_1_2_zekelman_chumash.pdf`

## Reviewer Guidance
- Use this packet to confirm source matches, Hebrew wording, level fit, and whether a strand is mature enough for later diagnostic planning.
- Do not treat any item here as reviewed truth, runtime-active content, or question-ready content.
- Do not create or approve active student questions from this packet alone.

Reviewer decision options:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

Current default review statuses:
- `needs_teacher_review`
- `source_match_needs_verification`
- `hebrew_needs_verification`
- `level_mapping_needs_review`
- `not_runtime_ready`
- `not_question_ready`

## Teacher Review Findings
- Reviewer: `Yossi Bassman`
- Review type: `teacher/educational review`
- Review documentation status: `approved_for_documentation_only`
- Runtime status: `not_runtime_ready`
- Question-generation status: `not_question_ready`
- Overall reviewer decision: The proposed review direction is supported for the highest-priority Standard 3 strands, but only as teacher-review guidance for documentation and later diagnostic planning boundaries.

### Approved Foundational Planning Lane
- `3.01` Nouns: clear foundational diagnostic lane for taught noun recognition, translation, and controlled multiple-meaning work, with a required source wording check and approved vocabulary-list boundaries.

### Approved With Wording Revision
- `3.05` Pronouns: strong diagnostic direction, but it must be split into separate lanes for pronoun referent tracking and pronominal suffix decoding.
- `3.06` Prefixes / articles / prepositions: visible prefix and article identification may move forward for planning, but the two functions of `את` stay deferred until context rules and teacher-approved wording are added.

### Approved With Level Adjustment
- `3.02` Shorashim: simple shoresh identification may move forward as foundational, while weak-letter roots, altered-root recognition, and advanced contextual shoresh interpretation stay deferred to later levels or later review.
- `3.07` Verbs: foundational tense/person/form clues may move forward for planning, while binyan, passive, command, `מקור`, and `שם הפועל` remain separate later lanes.

### Deferred And Context-Sensitive Boundaries
- None of these findings authorize runtime activation, reviewed-bank promotion, student-facing use, or question generation.
- `3.08`, `3.04`, and `3.10` now have explicit final reviewer decisions recorded below; all remain review-only and not runtime-ready or question-ready.
- Context-sensitive subareas remain deferred even within approved strands, including broader multiple-meaning expansion, weak-root interpretation, bundled pronoun-plus-suffix handling, the two functions of `את`, and advanced verb-form analysis.

### Final Recommendation
> Teacher review supports limited foundational diagnostic planning for 3.01, 3.02, 3.05, 3.06, and 3.07, with the boundaries listed above. This review does not authorize runtime activation or student-facing question generation.

## Final Source Verification Decisions
- These are final reviewer decisions recorded exactly for documentation and planning support only.
- They do not authorize runtime activation, question generation, active templates, reviewed-bank promotion, or production use.

### 3.08 Grouping and Word Order
- reviewer_decision: `approve_with_wording_revision`
- reviewer_notes: Approve as a diagnostic planning direction only when narrowed to phrase-level translation and basic Hebrew-to-English word-order adjustment. Do not yet use as a broad independent full-pasuk grouping skill. סמיכות may support this lane, but should remain separately tracked under 3.04 as well.
- remaining_source_checks: Verify Loshon page references and examples visually in the PDFs.
- recommended_next_action: Create a narrowed 3.08 diagnostic planning lane after source verification.

### 3.04 Parts of Speech / Nouns / סמיכות
- reviewer_decision: `approve_with_wording_revision`
- reviewer_notes: Approve with wording revision. Split into at least two planning lanes: noun/adjective features and סמיכות recognition. Noun gender, number, and common form changes are suitable for diagnostic planning after source examples are verified. Irregular forms and adjective agreement should remain later-level or review-required.
- remaining_source_checks: Verify Hebrew examples, nekudos, and level placement against Zekelman and Loshon PDFs.
- recommended_next_action: Add separate planning lanes for noun features and סמיכות.

### 3.10 Understanding ניקוד
- reviewer_decision: `defer_to_later_phase`
- reviewer_notes: Defer to later phase. Current evidence is too narrow and OCR-sensitive to support 3.10 as a diagnostic lane. Limited nikud-sensitive examples may be used as caution notes under 3.06, but full ניקוד systems such as תנועות, שבאים, דגשים, syllables, and טעמי המקרא require direct source review before diagnostic planning.
- remaining_source_checks: Directly verify Zekelman 3.10 levels and Loshon nikud/pausal references in the PDFs.
- recommended_next_action: Keep 3.10 out of MVP diagnostic blueprint except as a caution note.

## Loshon HaTorah Enrichment Evidence
- Source status: the raw Loshon Hakodesh main book PDF and answer booklet PDF are now present in `docs/sources/loshon_hatorah/raw/`, alongside the existing source-modeled JSONL file at `data/dikduk_rules/rules_loshon_foundation.jsonl`.
- Evidence policy: this material is supplemental enrichment only. It does not override Zekelman 2025, create teacher decisions, or change runtime/question readiness.
- Extraction status: page-delimited extracted text was created for both PDFs, but the main-book OCR layer is partial and the answer booklet remains review-only evidence, not an active answer key.
- Source artifacts refreshed for this enrichment pass:
- `data/sources/loshon_hatorah/loshon_hatorah_source_inventory.json`
- `docs/sources/loshon_hatorah/indexes/loshon_hatorah_document_index.json`
- `docs/sources/loshon_hatorah/extracted/loshon_hakodesh_book_ocr_raw_text.md`
- `docs/sources/loshon_hatorah/extracted/loshon_answe_2_combined_raw_text.md`
- `data/sources/loshon_hatorah/structured/loshon_hatorah_rule_candidates.json`
- `data/standards/zekelman/crosswalks/loshon_hatorah_to_zekelman_standard_3_crosswalk.json`

### Strongest Loshon Enrichment Areas
- `3.08` Grouping and Word Order: the main book directly supports variable Hebrew word order and natural English reordering on extracted page 4, and the answer booklet repeatedly practices literal-to-natural translation order. The final reviewer decision approves only a narrowed diagnostic planning direction; it still does not make the strand runtime-ready or question-ready.
- `3.04` Nouns and Adjectives: extracted main-book pages support noun gender/number, common plural endings, סמיכות as a construct phrase, and common סמיכות form changes. This helps reviewers decide whether noun-feature work and סמיכות should be split.
- `3.06` Prefixes, Articles, and Prepositions: extracted evidence supports visible ה, ו, prepositions, prefix prepositions, and context-sensitive את-family cautions. This reinforces the current boundary that visible prefix/article work is safer than the deferred functions of את.
- `3.05` Pronouns and Suffixes: main-book summary text and answer-booklet exercises support possessive-suffix decoding as a separate review lane from pronoun referent tracking.
- `3.07` Verbs: Loshon evidence now supports foundational agreement, shoresh-plus-added-letter analysis, past/future evidence, weak-letter boundary cautions, ו׳ ההיפוך as context-sensitive, and later review boundaries for present tense and command forms.

### Still Weak Or Unresolved After Loshon Enrichment
- `3.10` Understanding ניקוד: raw-source evidence is stronger than the prior pass because pausal/vowel-change notes and את-family nikud cautions were found, but the final reviewer decision defers this strand to a later phase and keeps it out of the MVP diagnostic blueprint except as a caution note.
- Weak-letter roots, ו׳ ההיפוך, command forms, present tense, and pausal forms are now documented as supplemental evidence, but they remain deferred/context-sensitive lanes requiring direct teacher and source review.
- The main-book OCR layer is incomplete; many pages still require direct PDF inspection rather than relying on extracted text.
- All Loshon examples and Hebrew terms need human source verification before any later diagnostic blueprint work.

## High-Priority Review Items

### 3.01 Vocabulary: שמות עצם (nouns)
- Standard ID: `3.01`
- Level range: `Levels 1-8`
- Canonical 2025 expectation summary: Builds a cumulative noun vocabulary from 25 nouns in Level 1 up to 200 total nouns by Level 8, then expects English-to-Hebrew recall, grouping of taught nouns, transfer into unlearned פסוקים, and contextual choice when one noun has more than one learned translation.
- Supplemental support summary: The 2014 intro gives direct noun-foundation instruction, the 2014 appendix supplies noun-frequency and grade-sequencing tables, and the 2016 sample assessments show noun-vocabulary assessment patterns. The main caution is table-structure and Hebrew verification, not lack of support.
- Draft engine skill mapping: `std3_01_noun_vocabulary_recognition` -> "Recognize and translate taught noun vocabulary" (`vocabulary_recognition`, diagnostic `high`, question-generation `high`).
- Why this matters for diagnostics: This is one of the clearest foundational strands for measuring taught-word retention, transfer into new פסוקים, and multiple-meaning control without changing runtime behavior.
- What a teacher/reviewer must verify: Confirm the cumulative noun-count progression, the exact meaning of row C on the canonical page, and whether contextual multiple-meaning work is still limited to previously taught noun sets.
- Specific review questions:
- Does page 30 row C clearly mean grouping nouns by shared taught noun family, and is the extracted wording accurate enough for later internal use?
- Should contextual multiple-meaning work stay limited to taught examples such as `ראש` and `רוח` before any broader planning?
- Do the appendix noun-grade tables align cleanly enough with the 2025 cumulative counts to support later teacher-approved scope planning?
- Known uncertainty: OCR and line wrapping on page 30 may blur row boundaries; appendix table relationships still need manual confirmation; Hebrew examples should be checked directly in the PDF.
- Teacher review finding: Documentation-only approval as a foundational planning lane for taught noun recognition, translation, and controlled multiple-meaning work. Keep it limited to approved vocabulary lists and source-verified wording.
- Recommended decision options:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

### 3.02 Vocabulary: שורשים (for verbs)
- Standard ID: `3.02`
- Level range: `Levels 1-8`
- Canonical 2025 expectation summary: Builds cumulative verb-root vocabulary from 15 roots in Level 1 to 190 total roots by Level 8, then expects English-to-shoresh recall, root-family grouping, contextual root translation, and progressively harder weak-letter or altered-root recognition.
- Supplemental support summary: The 2014 intro directly teaches what a shoresh is and how weak-letter roots behave, the 2014 appendix adds high-frequency shoresh lists, and the 2016 sample assessments show root-identification and contextual-root tasks. Support is strong, but the level split between simple and weak-root work still needs teacher confirmation.
- Draft engine skill mapping: `std3_02_shoresh_identification` -> "Identify a shoresh and connect it to meaning" (`shoresh_identification`, diagnostic `high`, question-generation `high`).
- Why this matters for diagnostics: Shoresh work is one of the strongest bridges from source-backed curriculum language to future diagnostic checking, but it becomes unsafe quickly if simple root recognition is mixed with weak-root interpretation too early.
- What a teacher/reviewer must verify: Confirm when weak-letter and altered-root recognition actually become fair expectations, and whether contextual root translation belongs in the same foundational decision or later verb review.
- Specific review questions:
- Which parts of `3.02` should count as foundational in the first review phase: simple shoresh identification only, or also weak-letter and altered-root recognition?
- Should contextual root translation be reviewed together with shoresh identification, or later with verb-feature review?
- Do the appendix root lists and the 2025 cumulative counts align well enough to support later level mapping?
- Known uncertainty: OCR-sensitive Hebrew root examples and weak-letter terminology need direct PDF checking; the 2016 sample source supports assessment patterns, but not the full later 2025 parsing range.
- Teacher review finding: Documentation-only approval with level adjustment. Simple shoresh identification may move forward as foundational, while weak-letter roots, altered-root recognition, and advanced contextual shoresh interpretation stay deferred.
- Recommended decision options:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

### 3.05 Pronouns
- Standard ID: `3.05`
- Level range: `Levels 1-8 (summary)`
- Canonical 2025 expectation summary: Moves from basic English and Hebrew subjective pronouns into referent tracking, possessive and objective pronouns, demonstrative and interrogative forms, suffixes embedded in words, prepositional pronouns, and the use of `איתן` and `תהימון` as pronoun clues.
- Supplemental support summary: This is one of the best-supported strands in the source set. The 2014 intro covers pronoun categories and referents, the 2014 appendix adds pronoun-family charts and suffix families, and the 2016 sample assessments give extensive referent and suffix patterns. The caution is context sensitivity and table/Hebrew verification, not source absence.
- Draft engine skill mapping:
- `std3_05_pronoun_referent_identification` -> "Identify pronouns and their referents"
- `std3_05_pronominal_suffix_identification` -> "Identify pronominal suffixes on nouns and particles"
- Why this matters for diagnostics: Pronoun and suffix errors often reveal whether a learner can track subject, object, and referent relationships inside a פסוק, which makes this strand highly diagnostic when reviewed carefully.
- What a teacher/reviewer must verify: Decide whether referent tracking and suffix decoding should be approved separately, how far referents may extend across פסוקים, and whether verb-linked clue systems should remain here or move to verb review.
- Specific review questions:
- Should referent tracking and pronominal-suffix decoding be treated as separate foundational approvals?
- At what point is cross-pasuk referent tracking fair, rather than local referent identification only?
- Should `איתן` and `תהימון` clue use stay with pronoun review, or shift to `3.07` verb review?
- Known uncertainty: Appendix pronoun charts remain table-structure sensitive; embedded suffix interpretation can become context-heavy quickly; OCR can blur person/gender/number forms.
- Teacher review finding: Documentation-only approval with wording revision. Split this strand into separate lanes for pronoun referent tracking and pronominal suffix decoding, and do not treat the full strand as one bundled skill.
- Recommended decision options:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

### 3.06 Prepositions, Conjunctions and the Definite Article
- Standard ID: `3.06`
- Level range: `Levels 1-8 (summary)`
- Canonical 2025 expectation summary: Builds from recognition of conjunctive `ו` and the definite article into distinguishing `ו ההיפוך`, `ה הידיעה`, `ה השאלה`, `ה המגמה`, inseparable prefixes such as `ב-כ-ל-מ`, retained `ש`, and the two functions of `את`.
- Supplemental support summary: The 2014 intro and 2014 appendix strongly support conjunctions, prefixes, article rules, and `את`. The 2016 assessment source is useful mostly as historical context because it still groups much of this material under `3.3 Other Vocabulary` rather than the later `3.06` split.
- Draft engine skill mapping:
- `std3_06_prefix_function_identification` -> "Identify prefix letters and article functions"
- `std3_06_direct_object_marker_resolution` -> "Distinguish the two functions of את"
- Why this matters for diagnostics: This strand contains many visible, discrete, high-value form clues that could later support safe diagnostic review, but some subparts, especially `את`, are context-sensitive and should stay protected until a teacher approves the wording.
- What a teacher/reviewer must verify: Decide which prefix/article distinctions are truly foundational now, which items are too interpretation-heavy, and how to handle the historical `3.3` versus `3.06` labeling split in older materials.
- Specific review questions:
- Should the first review phase approve only visible prefix/article identification and defer the two functions of `את`?
- How should the 2025 `3.06` split be reconciled with the older 2016 assessment material that still groups this content under `3.3`?
- Which nikud-dependent distinctions, especially `ו ההיפוך` and article-prefix shifts, are source-clear enough to review now?
- Known uncertainty: Appendix rule charts need manual Hebrew checking; nikud-sensitive prefix rules are OCR-sensitive; `את` remains more context-dependent than basic visible-form work.
- Teacher review finding: Documentation-only approval with wording revision. Visible prefix and article identification may move forward for planning, but the two functions of `את` remain deferred until context rules and teacher-approved wording are added.
- Recommended decision options:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

### 3.07 Verbs
- Standard ID: `3.07`
- Level range: `Levels 1-8 (summary)`
- Canonical 2025 expectation summary: Moves from identifying verbs in learned words into future and past tense recognition, present forms, `ציווי`, `מקור`, `שם הפועל`, active and passive `בנינים`, and verb-linked objective suffixes, with translation expected to follow the form clues.
- Supplemental support summary: The 2014 intro strongly supports foundational verb recognition, tense markers, and weak-root behavior. The appendix helps with high-frequency verbs and `ו ההיפוך`, but the full 2025 upper-level binyan/passive range is broader than the older support. The 2016 sample source is useful for root-centered patterns, not full later verb parsing.
- Draft engine skill mapping: `std3_07_verb_features` -> "Identify verb tense, person, and form clues" (`verb_features`, diagnostic `high`, question-generation `high`).
- Why this matters for diagnostics: Verb form analysis is central to accurate translation and parsing, but the strand is too broad to treat as a single safe future lane without teacher review that separates foundational form clues from later advanced parsing.
- What a teacher/reviewer must verify: Identify the smallest foundational verb-feature subset that is safe for later planning, and confirm which higher-level areas should stay deferred.
- Specific review questions:
- Where should review split foundational tense/person/form clues from later `בנין`, passive, command, and infinitive analysis?
- Is the supplemental evidence strong enough for the full upper-level 2025 verb range, or only for foundational tense/root-sensitive work?
- Should verb translation precision stay blocked until the approved form-clue boundaries are clear?
- Known uncertainty: The 2025 scope is broader than the older extracted support at the top end; conjugation charts are OCR-sensitive; level mapping across upper grades needs human confirmation.
- Teacher review finding: Documentation-only approval with level adjustment. Foundational tense/person/form clues may move forward for planning, while advanced verb-form areas remain separate later lanes.
- Recommended decision options:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

### 3.08 Grouping and Word Order
- Standard ID: `3.08`
- Level range: `Levels 1-8 (summary)`
- Canonical 2025 expectation summary: Expects students to group a פסוק into meaningful two- and three-word phrases and to change Hebrew word order appropriately when translating into English, including work in unlearned פסוקים.
- Supplemental support summary: Support is only partial. The 2014 intro directly explains that Hebrew and English word order differ, and the 2016 `3.4` assessment material indirectly supports phrase-level relationship work through adjective and סמיכות examples. The older sources do not mirror the full later `3.08` wording one-to-one.
- Draft engine skill mapping: `std3_08_syntax_phrase_structure` -> "Group phrases and adjust Hebrew word order for translation" (`syntax_phrase_structure`, diagnostic `high`, question-generation `medium`).
- Why this matters for diagnostics: This strand is highly relevant to translation quality and phrase-construction errors, but it is also one of the easiest places to over-claim support without a strong teacher check.
- What a teacher/reviewer must verify: Confirm whether the partial source support is enough for later diagnostic planning at all, and whether this strand must remain full-context only.
- Specific review questions:
- Is the partial supplemental support strong enough to treat `3.08` as a distinct later diagnostic strand now?
- Should grouping and word-order work remain full-context only, rather than ever being prepared for compact or isolated formats?
- Do the 2025 level descriptions map cleanly enough to later internal wording where literal translation is provided but grouping is not?
- Known uncertainty: This strand currently has only partial support from the older sources; the strongest older parallels are indirect; level descriptions depend heavily on exact phrasing from page 48.
- Final reviewer decision: `approve_with_wording_revision`
- Final reviewer notes: Approve as a diagnostic planning direction only when narrowed to phrase-level translation and basic Hebrew-to-English word-order adjustment. Do not yet use as a broad independent full-pasuk grouping skill. סמיכות may support this lane, but should remain separately tracked under 3.04 as well.
- Remaining source checks: Verify Loshon page references and examples visually in the PDFs.
- Recommended next action: Create a narrowed 3.08 diagnostic planning lane after source verification.
- Recommended decision options:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

## Secondary Review Items

### 3.04 Nouns and Adjectives
- Standard ID: `3.04`
- Level range: `Levels 1-8 (summary)`
- Canonical 2025 expectation summary: Moves from identifying nouns and adjectives in learned material into form-based identification in unlearned פסוקים, gender/number awareness, irregular-looking forms, adjective matching, and increasing recognition of `סמיכות`.
- Supplemental support summary: The 2014 intro covers nouns, adjectives, and word-order differences, the 2014 appendix adds gender/number heuristics, and the 2016 assessments include noun/adjective and `סמיכות` patterns. Support is strong, but some of the phrase-structure uses are still context-heavy.
- Draft engine skill mapping:
- `std3_04_noun_features` -> "Identify noun and adjective features"
- `std3_04_smichut_recognition` -> "Recognize סמיכות / construct-chain structures"
- Why this matters for diagnostics: This strand supports later phrase-structure review, especially where noun/adjective matching and `סמיכות` affect translation quality and grouping.
- What a teacher/reviewer must verify: Confirm whether noun/adjective feature work and `סמיכות` should stay bundled in this packet or split in a later review phase, and decide how much irregular-form knowledge counts as foundational.
- Specific review questions:
- Should noun/adjective feature review and `סמיכות` review remain bundled for this packet?
- Is standalone `סמיכות` identification suitable for later diagnostic preparation, or should it remain tied to full phrase context?
- How much irregular-form knowledge from `3.04` should count as foundational before later planning?
- Known uncertainty: `סמיכות` examples depend on precise Hebrew and nikud; some extracted form-based cues need direct PDF confirmation; the bridge from `3.04` to `3.08` is real but should not be over-compressed.
- Final reviewer decision: `approve_with_wording_revision`
- Final reviewer notes: Approve with wording revision. Split into at least two planning lanes: noun/adjective features and סמיכות recognition. Noun gender, number, and common form changes are suitable for diagnostic planning after source examples are verified. Irregular forms and adjective agreement should remain later-level or review-required.
- Remaining source checks: Verify Hebrew examples, nekudos, and level placement against Zekelman and Loshon PDFs.
- Recommended next action: Add separate planning lanes for noun features and סמיכות.
- Recommended decision options:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

### 3.10 Understanding ניקוד
- Standard ID: `3.10`
- Level range: `Advanced upper levels only (summary)`
- Canonical 2025 expectation summary: For advanced students, expects differentiation of `תנועות`, `שבאים`, and `דגשים`, plus syllable division and the interaction between ניקוד and `טעמי המקרא`. The canonical source explicitly flags this strand as advanced.
- Supplemental support summary: The 2014 intro offers strong rule-teaching support for vowels, sheva, dagesh, and syllables. The 2014 appendix adds applied nikud charts tied to prefixes and articles, but those charts remain table-sensitive and need manual verification.
- Draft engine skill mapping: `std3_10_nikud_reading` -> "Recognize advanced ניקוד patterns and syllable rules" (`nikud_reading`, diagnostic `medium`, question-generation `medium`).
- Why this matters for diagnostics: Nikud reading can eventually sharpen upper-level parsing and translation review, but it is not a safe first-pass strand and should remain clearly gated behind teacher confirmation.
- What a teacher/reviewer must verify: Confirm the advanced-only level gate, whether levels 1-4 are intentionally out of scope, and whether any nikud subskills belong in the same later phase as `3.06` prefix/article nikud rules.
- Specific review questions:
- Are levels 1-4 intentionally outside `3.10`, or does the extracted table need another manual pass?
- Which advanced ניקוד subskills, if any, belong in the same phase as `3.06` nikud-dependent prefix/article distinctions?
- How much trust should later reviewers place in OCR-sensitive nekudos and chart structure before checking the raw PDF directly?
- Known uncertainty: Nikud and chart extraction are especially OCR-sensitive; lower-level absence must be confirmed manually; the appendix support is helpful but not self-validating.
- Final reviewer decision: `defer_to_later_phase`
- Final reviewer notes: Defer to later phase. Current evidence is too narrow and OCR-sensitive to support 3.10 as a diagnostic lane. Limited nikud-sensitive examples may be used as caution notes under 3.06, but full ניקוד systems such as תנועות, שבאים, דגשים, syllables, and טעמי המקרא require direct source review before diagnostic planning.
- Remaining source checks: Directly verify Zekelman 3.10 levels and Loshon nikud/pausal references in the PDFs.
- Recommended next action: Keep 3.10 out of MVP diagnostic blueprint except as a caution note.
- Recommended decision options:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`

## What This Packet Intentionally Does Not Do
- It does not change runtime behavior.
- It does not change Streamlit or UI behavior.
- It does not create student questions, answer keys, or active question templates.
- It does not modify reviewed-bank files or production data.
- It does not mark any strand as question-ready or runtime-ready.
- It does not replace teacher review; it only prepares that review.
