# Verified Source-to-Skill Maps

This directory holds canonical source-to-skill maps.

A source-to-skill map is the bridge between trusted source material and future question planning. It records the Hebrew word or phrase, trusted translation source, skill classification, standards mapping status, review status, and safety status.

These files are source-derived planning artifacts only. They are not generated questions, reviewed-bank records, runtime records, or student-facing content.

## Current Seed Map

- `bereishis_1_1_to_3_24_metsudah_skill_map.tsv`
- Scope target: active Bereishis runtime scope, Bereishis 1:1-3:24
- Populated seed slice: Bereishis 1:1-1:5
- Primary translation source: Metsudah Chumash, Metsudah Publications, 2009
- Secondary comparison source: The Koren Jerusalem Bible, noncommercial support only
- Review status: `pending_yossi_extraction_accuracy_pass`
- Runtime status: blocked
- Question-generation status: blocked
- Protected-preview status: blocked unless separately authorized by a future gate
- Reviewed-bank status: blocked

## Proof-of-Consolidation Map

- `bereishis_1_1_to_1_5_source_to_skill_map.tsv`
- Scope: Bereishis 1:1-1:5
- Row count: 23 phrase-level rows
- Purpose: prove how existing trusted source-derived data can join into one canonical map shape
- Source ingredients:
  - Linear Chumash phrase-level extraction from curriculum extraction Batch 001
  - Metsudah verse-level translation context
  - Koren verse-level secondary noncommercial translation context
  - source/review/runtime statuses from existing manifests
- Review status: `yossi_extraction_verified`
- Verification report: `reports/bereishis_1_1_to_1_5_yossi_extraction_verification_report.md`
- Runtime status: blocked
- Question-generation status: blocked
- Protected-preview status: blocked unless separately authorized by a future gate
- Reviewed-bank status: blocked

The proof map deliberately leaves shoresh, prefixes, suffixes, tense, part of speech, Zekelman standard, difficulty, and question-type eligibility blank where the repo does not yet have a safe row-level join. Those rows carry `uncertainty_reason`.

## Verified Expansion Slice

- `bereishis_1_6_to_1_13_source_to_skill_map.tsv`
- Scope: Bereishis 1:6-1:13
- Row count: 37 phrase-level rows
- Built by: `scripts/build_source_to_skill_map.py`
- Build report: `reports/bereishis_1_6_to_1_13_source_to_skill_map_build_report.md`
- Exceptions review packet: `reports/bereishis_1_6_to_1_13_source_to_skill_map_exceptions_review_packet.md`
- Verification report: `reports/bereishis_1_6_to_1_13_yossi_extraction_verification_report.md`
- Source ingredients:
  - Linear Chumash phrase-level extraction from curriculum extraction Batch 002
  - Metsudah verse-level translation context
  - Koren verse-level secondary noncommercial translation context
  - canonical Hebrew source coverage for the refs
- Review status: `yossi_extraction_verified`
- Runtime status: blocked
- Question-generation status: blocked
- Protected-preview status: blocked unless separately authorized by a future gate
- Reviewed-bank status: blocked
- Next required action: see the pending Bereishis 1:24-1:31 slice below

## Verified Expansion Slice

- `bereishis_1_14_to_1_23_source_to_skill_map.tsv`
- Scope: Bereishis 1:14-1:23
- Row count: 39 phrase-level rows
- Built by: `scripts/build_source_to_skill_map.py`
- Build report: `reports/bereishis_1_14_to_1_23_source_to_skill_map_build_report.md`
- Exceptions review packet: `reports/bereishis_1_14_to_1_23_source_to_skill_map_exceptions_review_packet.md`
- Verification report: `reports/bereishis_1_14_to_1_23_yossi_extraction_verification_report.md`
- Source ingredients:
  - Linear Chumash phrase-level extraction from curriculum extraction Batch 002
  - Metsudah verse-level translation context
  - Koren verse-level secondary noncommercial translation context
  - canonical Hebrew source coverage for the refs
- Review status: `yossi_extraction_verified`
- Runtime status: blocked
- Question-generation status: blocked
- Protected-preview status: blocked unless separately authorized by a future gate
- Reviewed-bank status: blocked
- Next required action: Yossi reviews the next pending slice, Bereishis 1:24-1:31

## Verified Expansion Slice

- `bereishis_1_24_to_1_31_source_to_skill_map.tsv`
- Scope: Bereishis 1:24-1:31
- Row count: 38 phrase-level rows
- Built by: `scripts/build_source_to_skill_map.py`
- Build report: `reports/bereishis_1_24_to_1_31_source_to_skill_map_build_report.md`
- Exceptions review packet: `reports/bereishis_1_24_to_1_31_source_to_skill_map_exceptions_review_packet.md`
- Verification report: `reports/bereishis_1_24_to_1_31_yossi_extraction_verification_report.md`
- Source ingredients:
  - Linear Chumash phrase-level extraction from curriculum extraction Batch 002
  - Metsudah verse-level translation context
  - Koren verse-level secondary noncommercial translation context
  - canonical Hebrew source coverage for the refs
- Review status: `yossi_extraction_verified`
- Runtime status: blocked
- Question-generation status: blocked
- Protected-preview status: blocked unless separately authorized by a future gate
- Reviewed-bank status: blocked
- Next required action: Create a Bereishis Perek 1 source-to-skill completion report

## Bereishis Perek 1 Completion Milestone

- Completion report: `reports/bereishis_perek_1_source_to_skill_completion_report.md`
- Scope: Bereishis 1:1-1:31
- Total row count: 137 phrase-level rows
- Milestone status: extraction-verified source-to-skill coverage complete for Bereishis Perek 1
- Safety status: question, protected-preview, reviewed-bank, runtime, and student-facing gates remain closed

Verified slice maps:

- `bereishis_1_1_to_1_5_source_to_skill_map.tsv`
- `bereishis_1_6_to_1_13_source_to_skill_map.tsv`
- `bereishis_1_14_to_1_23_source_to_skill_map.tsv`
- `bereishis_1_24_to_1_31_source_to_skill_map.tsv`

Verification reports:

- `reports/bereishis_1_1_to_1_5_yossi_extraction_verification_report.md`
- `reports/bereishis_1_6_to_1_13_yossi_extraction_verification_report.md`
- `reports/bereishis_1_14_to_1_23_yossi_extraction_verification_report.md`
- `reports/bereishis_1_24_to_1_31_yossi_extraction_verification_report.md`

This completion milestone is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing release.

## Verified Perek 2 Opening Slice

- `bereishis_2_1_to_2_3_source_to_skill_map.tsv`
- Scope: Bereishis 2:1-2:3
- Row count: 9 phrase-level rows
- Built by: `scripts/build_source_to_skill_map.py`
- Build report: `reports/bereishis_2_1_to_2_3_source_to_skill_map_build_report.md`
- Exceptions review packet: `reports/bereishis_2_1_to_2_3_source_to_skill_map_exceptions_review_packet.md`
- Yossi Markdown review sheet: `reports/bereishis_2_1_to_2_3_yossi_review_sheet.md`
- Yossi CSV review sheet: `reports/bereishis_2_1_to_2_3_yossi_review_sheet.csv`
- Verification report: `reports/bereishis_2_1_to_2_3_yossi_extraction_verification_report.md`
- Source ingredients:
  - Linear Chumash phrase-level extraction from curriculum extraction Batch 002
  - Metsudah verse-level translation context
  - Koren verse-level secondary noncommercial translation context
  - canonical Hebrew source coverage for the refs
- Review status: `yossi_extraction_verified`
- Runtime status: blocked
- Question-generation status: blocked
- Protected-preview status: blocked unless separately authorized by a future gate
- Reviewed-bank status: blocked
- Next required action: generate the next safe Perek 2 source-to-skill slice, likely Bereishis 2:4-2:17 unless a smaller slice is safer

## Verified Perek 2 Expansion Slice

- `bereishis_2_4_to_2_17_source_to_skill_map.tsv`
- Scope: Bereishis 2:4-2:17
- Row count: 54 phrase-level rows
- Built by: `scripts/build_source_to_skill_map.py`
- Build report: `reports/bereishis_2_4_to_2_17_source_to_skill_map_build_report.md`
- Exceptions review packet: `reports/bereishis_2_4_to_2_17_source_to_skill_map_exceptions_review_packet.md`
- Yossi Markdown review sheet: `reports/bereishis_2_4_to_2_17_yossi_review_sheet.md`
- Yossi CSV review sheet: `reports/bereishis_2_4_to_2_17_yossi_review_sheet.csv`
- Yossi extraction verification report: `reports/bereishis_2_4_to_2_17_yossi_extraction_verification_report.md`
- Source ingredients:
  - Linear Chumash phrase-level extraction from curriculum extraction Batch 003
  - Metsudah verse-level translation context
  - Koren verse-level secondary noncommercial translation context
  - canonical Hebrew source coverage for the refs
- Review status: `yossi_extraction_verified`
- Planning note: all rows remain source-only for future question/protected-preview planning until a separate question eligibility gate
- Runtime status: blocked
- Question-generation status: blocked
- Protected-preview status: blocked unless separately authorized by a future gate
- Reviewed-bank status: blocked
- Next required action: generate the next safe Perek 2 source-to-skill slice after Bereishis 2:17

## Yossi Review Artifact Standard

Every future pending source-to-skill slice must include:

- build report
- exceptions packet
- Yossi Markdown review sheet
- Yossi CSV review sheet

The Markdown and CSV review sheets are the primary human-review surfaces. They must be concise, decision-based, and extraction-accuracy focused. A `verified` Yossi decision means extraction accuracy only; it is not question approval, protected-preview approval, reviewed-bank approval, runtime approval, or student-facing release.

## Audit Artifact

- `reports/source_to_skill_map_audit.json`

The audit records existing ingredients, field coverage, duplication risks, and the current recommendation. Current finding: the full canonical map is partially built in scattered form, but only a small proof-of-consolidation map is safe today.

## Required Safety Rules

- Metsudah source rows must carry `source_license: CC-BY`.
- Koren secondary rows must carry `secondary_source_license: CC-BY-NC`.
- Koren must not be marked commercial-use approved.
- Rows with source translations must require attribution.
- Pending rows must remain pending Yossi extraction-accuracy confirmation.
- Rows marked `yossi_extraction_verified` must have linked extraction-verification evidence.
- No row may be runtime allowed unless a separate future runtime gate explicitly authorizes it.
- No row may be question allowed unless a separate future question/protected-preview gate explicitly authorizes it.
- No row may be student-facing.
- Rows with uncertainty must explain the uncertainty.

## Review Model

Yossi is not being asked to re-approve the educational value of trusted source material from scratch. Yossi is being asked to confirm extraction accuracy:

- source matching
- Hebrew fidelity
- Metsudah translation extraction accuracy
- Koren secondary comparison accuracy, if included
- skill classification accuracy
- standards mapping accuracy
- uncertainty items

Generated questions, answer choices, answer keys, protected previews, reviewed-bank promotion, runtime activation, and student-facing release still require separate gates.
