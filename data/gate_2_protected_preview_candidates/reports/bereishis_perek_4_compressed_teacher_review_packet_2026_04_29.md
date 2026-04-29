# Bereishis Perek 4 Compressed Teacher-Review Packet - 2026-04-29

## Purpose

This is the compressed teacher-review packet for existing Bereishis Perek 4 source-discovery candidates only, now updated with Yossi's explicit teacher-review decisions.

This packet remains teacher-review and next-gate planning only. It is not runtime content, not reviewed-bank content, not a protected-preview packet, and not student-facing content.

## Source inventory

- Source inventory: `data/gate_2_source_discovery/bereishis_perek_4_review_only_safe_candidate_inventory.tsv`
- Source discovery report: `data/gate_2_source_discovery/reports/bereishis_perek_4_source_discovery_report.md`
- Duplicate/session-balance warning report: `data/gate_2_source_discovery/reports/bereishis_perek_4_duplicate_session_balance_warnings.md`
- Excluded risk lanes: `data/gate_2_source_discovery/reports/bereishis_perek_4_excluded_risk_lanes.md`

## Yossi override boundary

Yossi explicitly approved moving forward to Perek 4 compressed teacher-review packet preparation now, despite the prior normal gate requiring a clean short Perek 3 re-pilot first.

This override allows Perek 4 teacher-review packet preparation only. It does not allow runtime activation or active scope expansion.

## Teacher decisions applied

Yossi's decisions are now applied in this packet and mirrored in `data/gate_2_protected_preview_candidates/reports/bereishis_perek_4_teacher_review_decisions_applied_2026_04_29.json`.

No runtime approval, reviewed-bank approval, protected-preview packet approval, or student-facing approval is applied by this packet.

## Candidate review cards

### g2srcdisc_p4_001 - Bereishis 4:1

- Candidate ID: `g2srcdisc_p4_001`
- Pasuk/ref: Bereishis 4:1
- Hebrew word/phrase: `אִישׁ` in `וַתֹּ֕אמֶר קָנִ֥יתִי אִ֖ישׁ אֶת־יְהֹוָֽה`
- Source context: `וַתֹּ֕אמֶר קָנִ֥יתִי אִ֖ישׁ אֶת־יְהֹוָֽה`
- Proposed skill: `basic_noun_recognition` / `WORD.PART_OF_SPEECH_BASIC`
- Proposed question wording: `In this phrase, what type of word is אִישׁ?`
- Expected answer: `noun`
- Proposed distractors if safe: `verb`, `adjective`, `prefix`
- Source/evidence note: Source-backed review-only candidate from data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl row pasuk_segment_batch_005_bereishis_4_1_003.
- Risk level: `medium`
- Risk note: Risk flags: source_literal_wording_review. Source confidence: canonical_hebrew_available;batch_005_reviewed_for_planning_non_runtime;record_confidence_low. Teacher must confirm that this is appropriate as basic noun recognition before any later gate.
- Teacher decision: `approve_with_revision`
- Teacher notes: Good noun-recognition target. Wording revised to make clear that the question asks for part of speech in context.
- Revision required: `true`
- Revision applied: `true`
- Source follow-up required: `false`
- Eligible for next gate: `true`
- Eligible for protected-preview-candidate planning: `true`
- Spacing note: No special spacing note beyond normal noun-recognition balance.
- Alias review note: Not applicable.
- Current gates: runtime_allowed=false; reviewed_bank_allowed=false; protected_preview_allowed=false; protected_preview_packet_allowed_now=false; student_facing_allowed=false; broader_use_allowed=false

### g2srcdisc_p4_002 - Bereishis 4:2

- Candidate ID: `g2srcdisc_p4_002`
- Pasuk/ref: Bereishis 4:2
- Hebrew word/phrase: `צֹאן` in `וַֽיְהִי־הֶ֙בֶל֙ רֹ֣עֵה צֹ֔אן`
- Source context: `וַֽיְהִי־הֶ֙בֶל֙ רֹ֣עֵה צֹ֔אן`
- Proposed skill: `basic_noun_recognition` / `WORD.PART_OF_SPEECH_BASIC`
- Proposed question wording: `What type of word is צֹאן?`
- Expected answer: `noun`
- Proposed distractors if safe: `verb`, `adjective`, `prefix`
- Source/evidence note: Source-backed review-only candidate from data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl row pasuk_segment_batch_005_bereishis_4_2_002.
- Risk level: `low`
- Risk note: Risk flags: nearby_suffix_form_not_safe_candidate. Source confidence: canonical_hebrew_available;batch_005_reviewed_for_planning_non_runtime;record_confidence_low. Teacher must confirm that this is appropriate as basic noun recognition before any later gate.
- Teacher decision: `approve_for_protected_preview`
- Teacher notes: Clear noun target in context. Appropriate for basic noun recognition; distractors are acceptable for this simple part-of-speech question.
- Revision required: `false`
- Revision applied: `false`
- Source follow-up required: `false`
- Eligible for next gate: `true`
- Eligible for protected-preview-candidate planning: `true`
- Spacing note: Use normal packet spacing.
- Alias review note: Not applicable.
- Current gates: runtime_allowed=false; reviewed_bank_allowed=false; protected_preview_allowed=false; protected_preview_packet_allowed_now=false; student_facing_allowed=false; broader_use_allowed=false

### g2srcdisc_p4_003 - Bereishis 4:2

- Candidate ID: `g2srcdisc_p4_003`
- Pasuk/ref: Bereishis 4:2
- Hebrew word/phrase: `אֲדָמָה` in `וְקַ֕יִן הָיָ֖ה עֹבֵ֥ד אֲדָמָֽה`
- Source context: `וְקַ֕יִן הָיָ֖ה עֹבֵ֥ד אֲדָמָֽה`
- Proposed skill: `basic_noun_recognition` / `WORD.PART_OF_SPEECH_BASIC`
- Proposed question wording: `What type of word is אֲדָמָה?`
- Expected answer: `noun`
- Proposed distractors if safe: `verb`, `adjective`, `prefix`
- Source/evidence note: Source-backed review-only candidate from data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl row pasuk_segment_batch_005_bereishis_4_2_003.
- Risk level: `medium`
- Risk note: Risk flags: repeated_token_cluster. Duplicate-token/session-balance warning must be considered before any future packet planning. Source confidence: canonical_hebrew_available;batch_005_reviewed_for_planning_non_runtime;record_confidence_low. Teacher must confirm that this is appropriate as basic noun recognition before any later gate.
- Teacher decision: `approve_with_revision`
- Teacher notes: Clear noun target. Preserve duplicate/session-balance warning before any protected-preview packet planning; do not serve too close to similar noun-recognition items.
- Revision required: `true`
- Revision applied: `true`
- Source follow-up required: `false`
- Eligible for next gate: `true`
- Eligible for protected-preview-candidate planning: `true`
- Spacing note: Required: preserve duplicate/session-balance warning and avoid placing too close to similar noun-recognition items in any future packet planning.
- Alias review note: Not applicable.
- Current gates: runtime_allowed=false; reviewed_bank_allowed=false; protected_preview_allowed=false; protected_preview_packet_allowed_now=false; student_facing_allowed=false; broader_use_allowed=false

### g2srcdisc_p4_004 - Bereishis 4:3

- Candidate ID: `g2srcdisc_p4_004`
- Pasuk/ref: Bereishis 4:3
- Hebrew word/phrase: `מִנְחָה` in `מִנְחָ֖ה לַֽיהֹוָֽה`
- Source context: `מִנְחָ֖ה לַֽיהֹוָֽה`
- Proposed skill: `basic_noun_recognition` / `WORD.PART_OF_SPEECH_BASIC`
- Proposed question wording: `What type of word is מִנְחָה?`
- Expected answer: `noun`
- Proposed distractors if safe: `verb`, `adjective`, `prefix`
- Source/evidence note: Source-backed review-only candidate from data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl row pasuk_segment_batch_005_bereishis_4_3_003.
- Risk level: `medium`
- Risk note: Risk flags: repeated_token_cluster;accepted_alias_review_minchah. Duplicate-token/session-balance warning must be considered before any future packet planning. Source confidence: canonical_hebrew_available;batch_005_reviewed_for_planning_non_runtime;record_confidence_low. Teacher must confirm that this is appropriate as basic noun recognition before any later gate.
- Teacher decision: `approve_with_revision`
- Teacher notes: Valid noun target. Preserve Minchah/offering alias review and duplicate/session-balance warning; keep the question part-of-speech only, not vocabulary translation.
- Revision required: `true`
- Revision applied: `true`
- Source follow-up required: `false`
- Eligible for next gate: `true`
- Eligible for protected-preview-candidate planning: `true`
- Spacing note: Required: preserve duplicate/session-balance warning and avoid clustering with nearby noun-recognition items.
- Alias review note: Required: preserve Minchah/offering alias review; do not convert this into a vocabulary translation item without later review.
- Current gates: runtime_allowed=false; reviewed_bank_allowed=false; protected_preview_allowed=false; protected_preview_packet_allowed_now=false; student_facing_allowed=false; broader_use_allowed=false

### g2srcdisc_p4_005 - Bereishis 4:15

- Candidate ID: `g2srcdisc_p4_005`
- Pasuk/ref: Bereishis 4:15
- Hebrew word/phrase: `אוֹת` in `וַיָּ֨שֶׂם יְהֹוָ֤ה לְקַ֙יִן֙ א֔וֹת`
- Source context: `וַיָּ֨שֶׂם יְהֹוָ֤ה לְקַ֙יִן֙ א֔וֹת`
- Proposed skill: `basic_noun_recognition` / `WORD.PART_OF_SPEECH_BASIC`
- Proposed question wording: `What type of word is אוֹת?`
- Expected answer: `noun`
- Proposed distractors if safe: `verb`, `adjective`, `prefix`
- Source/evidence note: Source-backed review-only candidate from data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl row pasuk_segment_batch_005_bereishis_4_15_004.
- Risk level: `medium`
- Risk note: Risk flags: accepted_alias_review_ot. Source confidence: canonical_hebrew_available;batch_005_reviewed_for_planning_non_runtime;record_confidence_low. Teacher must confirm that this is appropriate as basic noun recognition before any later gate.
- Teacher decision: `needs_source_follow_up`
- Teacher notes: Needs teacher/source follow-up. אוֹת may confuse beginners with אֶת or broader sign/letter meanings; do not advance until intended explanation and alias handling are clear.
- Revision required: `true`
- Revision applied: `false`
- Source follow-up required: `true`
- Eligible for next gate: `false`
- Eligible for protected-preview-candidate planning: `false`
- Spacing note: Not eligible for packet spacing until source follow-up is resolved.
- Alias review note: Required: clarify intended handling of אוֹת, possible confusion with אֶת, and sign/letter aliases before any advancement.
- Current gates: runtime_allowed=false; reviewed_bank_allowed=false; protected_preview_allowed=false; protected_preview_packet_allowed_now=false; student_facing_allowed=false; broader_use_allowed=false

## Safety boundary confirmation

- Perek 4 activated: no.
- Runtime scope widened: no.
- Reviewed-bank promotion: no.
- Protected-preview packet created: no.
- Student-facing content created: no.
- Fake teacher decisions created: no; these are Yossi's explicit decisions.
- Fake student observations created: no.
- Source truth changed: no.
- Question selection changed: no.
- Scoring/mastery changed: no.
