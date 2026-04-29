# Bereishis 1:1-1:5 Morphology Enrichment Yossi Review Sheet

- Scope: Bereishis 1:1-1:5
- Candidate count: 5
- Current status: candidate enrichment only
- Yossi is reviewing enrichment candidates only.
- This is not question approval, not protected-preview approval, not reviewed-bank approval, not runtime approval, or not student-facing approval.
- All question, protected-preview, reviewed-bank, runtime, and student-facing gates remain closed.

Allowed Yossi decisions:

- `verified`
- `fix_morphology`
- `fix_standard`
- `fix_vocabulary`
- `source_only`
- `block_for_questions`
- `needs_follow_up`

## Review Instructions

Mark each row with one allowed decision. Use `verified` only when the enrichment candidate is accurate enough to record as enrichment-verified later. Use `needs_follow_up` when the evidence is not sufficient.

## Candidate Rows

| Candidate | Ref | Hebrew | Evidence | Confidence | Current Status | What to Check |
|---|---|---|---|---|---|---|
| `morph_b1_1_r002_t001` | Bereishis 1:1 | ברא | word_parse.bereishis_1_1.bara | low | pending_yossi_enrichment_review | proposed_shoresh=ברא; proposed_tense=past; proposed_person=3; proposed_gender=masculine; proposed_number=singular; proposed_part_of_speech=verb; proposed_dikduk_feature=qal verb parse candidate |
| `morph_b1_1_r002_t002` | Bereishis 1:1 | אלקים | word_parse.bereishis_1_1.elohim | low | pending_yossi_enrichment_review | proposed_gender=masculine; proposed_number=plural_form_singular_meaning; proposed_part_of_speech=noun; proposed_dikduk_feature=noun feature candidate |
| `morph_b1_2_r005_t001` | Bereishis 1:2 | היתה | word_parse.bereishis_1_2.hayetah | low | pending_yossi_enrichment_review | proposed_shoresh=היה; proposed_tense=past; proposed_person=3; proposed_gender=feminine; proposed_number=singular; proposed_part_of_speech=verb; proposed_dikduk_feature=past 3fs verb parse candidate |
| `morph_b1_2_r004_t001` | Bereishis 1:2 | והארץ | source_to_skill_map_row_004 | low | needs_follow_up | proposed_dikduk_feature=prefix/article split needs evidence |
| `morph_b1_3_r013_t001` | Bereishis 1:3 | יהי | source_to_skill_map_row_013 | low | needs_follow_up | proposed_part_of_speech=verb; proposed_dikduk_feature=jussive/verb-form candidate needs evidence |
