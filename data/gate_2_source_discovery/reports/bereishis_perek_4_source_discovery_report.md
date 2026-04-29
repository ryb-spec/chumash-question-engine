# Bereishis Perek 4 source discovery report

## Purpose

This is Perek 4 source-to-skill discovery only. It is review-only. It creates no runtime activation, no reviewed-bank promotion, no protected-preview packet creation, and no student-facing content.

This report intentionally starts Perek 4 only. It does not include Perek 5 and does not create packet IDs or approved question rows.

## Source files inspected

- `data/pipeline_rounds/bereishis_perek_3_to_perek_4_launch_gate.md`
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- `data/source/bereishis_4_1_to_4_16.json`
- `data/curriculum_extraction/normalized/batch_005_linear_chumash_bereishis_4_1_to_4_16_pasuk_segments.jsonl`
- `data/curriculum_extraction/curriculum_extraction_manifest.json`
- `data/curriculum_extraction/reports/batch_005_summary.md`
- `data/curriculum_extraction/reports/batch_005_review_resolution.md`
- `data/standards/canonical_skill_contract.json`
- `data/validation/standards_evidence_gap_matrix.json`
- `data/validation/protected_preview_source_lineage_matrix.tsv`

## Perek 4 source coverage

- Canonical Hebrew source text is available for Bereishis Perek 4 in `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`.
- Batch 005 curriculum extraction covers Bereishis 4:1 through Bereishis 4:16 and is reviewed for planning only, not runtime.
- No verified Perek 4 source-to-skill map was found in `data/verified_source_skill_maps/`.
- No Perek 4 source-skill enrichment layer was found in `data/source_skill_enrichment/`.
- Bereishis 4:17 through Bereishis 4:26 have canonical Hebrew source text, but they do not yet have Batch 005 curriculum-extraction source-to-skill discovery rows.

## Candidate discovery method

Possible candidates were selected only when they had traceable source rows in Batch 005 and visible Hebrew tokens suitable for a conservative first-pass skill family. The selected lane is `basic_noun_recognition`, mapped to canonical skill `WORD.PART_OF_SPEECH_BASIC`.

The selection rules were intentionally narrow:

- Source-backed row required.
- Perek must be 4.
- Candidate remains review-only.
- Gates stay closed for runtime, reviewed bank, protected preview, student-facing use, and broader use.
- Duplicate-token/session-balance warnings are recorded before any packet planning.
- Translation/context, suffix/compound morphology, advanced verbs, vav hahipuch, Rashi/commentary, and higher-order comprehension are deferred.

## Safe candidate summary

- Review-only candidate rows created: 5
- Skill-family counts: `basic_noun_recognition`: 5
- Source-confidence summary: all rows are source-backed from canonical Hebrew plus Batch 005 planning-only extraction; all still require review.
- Candidate rows with duplicate-token warnings: 2
- Duplicate/session-balance warning rows in warning report: 4
- Excluded/deferred risk lanes: 8

## Excluded or deferred lanes

- Translation/context: deferred because isolated source-backed noun recognition is the safe starting lane and contextual meaning requires teacher review.
- Suffix/compound morphology: deferred because Perek 4 has nearby suffixed/compound forms such as צֹאנ֖וֹ and מִנְחָת֖וֹ.
- Advanced verbs: deferred because many Perek 4 forms are not safe simple noun-recognition targets.
- Vav hahipuch: deferred pending explicit lane support and review.
- Rashi/commentary: deferred because this task uses Chumash source/provenance only.
- Higher-order comprehension: deferred pending teacher review and assessment design.
- Ambiguous particles/direct-object markers: deferred as low-safety targets for this lane.
- Perek 4:17-4:26 candidates: deferred until source-to-skill discovery/provenance rows exist.

## Safety boundary confirmation

- No runtime activation.
- No Perek 4 runtime activation.
- No reviewed-bank promotion.
- No protected-preview packet creation.
- No student-facing content.
- No source-truth changes.
- No runtime/UI/scoring/mastery/assessment-flow changes.
