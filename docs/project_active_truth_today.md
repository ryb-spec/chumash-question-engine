# Project Active Truth Today

Current as of April 27, 2026.

## Active Runtime Scope

- Active runtime scope: Bereishis 1:1-3:24
- Runtime scope ID: `local_parsed_bereishis_1_1_to_3_24`
- Source corpus ID: `source_bereishis_1_1_to_3_24_local`
- Parsed corpus ID: `parsed_bereishis_1_1_to_3_24_root`
- Supported runtime: `streamlit_app.py`
- Active reviewed question bank: `data/active_scope_reviewed_questions.json`
- Reviewed runtime question count: 238

## Canonical Source Files

- Canonical Hebrew source file: `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- Canonical Hebrew scope: Bereishis 1:1-50:26
- Canonical Hebrew SHA-256: `4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71`
- Active local source files: `data/source/bereishis_1_1_to_1_30.json` through `data/source/bereishis_3_17_to_3_24.json`

## Translation Source Policy

- Preferred primary translation source: Metsudah Chumash, Metsudah Publications, 2009
- Metsudah source platform: Sefaria
- Metsudah license: CC-BY
- Metsudah attribution: required
- Secondary translation support: The Koren Jerusalem Bible
- Koren source platform: Sefaria
- Koren license: CC-BY-NC
- Koren use: secondary noncommercial support only
- Koren commercial use: blocked unless direct written permission is obtained
- Sefaria availability is source metadata, not blanket approval for production/runtime use

## Preview-Only Artifacts

- `data/diagnostic_preview/`
- `data/standards/zekelman/preview/standard_3_mvp_protected_preview_packet.md`

These are not runtime-active and not student-facing.

## Review-Only Artifacts

- `data/curriculum_extraction/`
- `data/standards/zekelman/blueprints/`
- `data/standards/zekelman/reports/`
- `data/standards/zekelman/reviewed_bank_candidates/`
- `data/verified_source_skill_maps/`

These support planning, review, source verification, and future gates only.

## Trusted Source Packages

Trusted teacher/source materials include Zekelman standards and sample assessments, Dikduk resources/workbooks, Loshon Hakodesh resources, Metsudah, Koren secondary noncommercial support, and other clearly teacher-created Chumash/dikduk/assessment resources.

Trusted source material requires one Yossi extraction-accuracy pass before it can be treated as verified source-derived content. This does not make it runtime-ready, question-ready, reviewed-bank-ready, protected-preview-ready, or student-facing.

## Source-to-Skill Map Status

- First canonical source-to-skill directory: `data/verified_source_skill_maps/`
- Seed map: `data/verified_source_skill_maps/bereishis_1_1_to_3_24_metsudah_skill_map.tsv`
- Seed populated slice: Bereishis 1:1-1:5
- Proof-of-consolidation map: `data/verified_source_skill_maps/bereishis_1_1_to_1_5_source_to_skill_map.tsv`
- Proof map row count: 23 phrase-level rows
- Audit report: `data/verified_source_skill_maps/reports/source_to_skill_map_audit.json`
- Review packet: `data/verified_source_skill_maps/reports/bereishis_1_1_to_3_24_metsudah_skill_map_extraction_accuracy_review_packet.md`
- Current review status: `pending_yossi_extraction_accuracy_pass`
- Runtime/question/preview/reviewed-bank status: blocked

## Current Blockers

- Yossi still needs to confirm extraction accuracy for pending trusted source-derived rows.
- Source-to-skill maps are only seeded and not complete across the active scope.
- Zekelman Standard 3 planning artifacts remain separate from runtime activation.
- Generated questions, answer choices, answer keys, protected previews, reviewed-bank promotion, and runtime activation still require separate gates.

## Next Recommended Action

Complete Yossi extraction-accuracy review for the first source-to-skill seed map, then expand the same map pattern across the next trusted source-derived slice without changing runtime or generating questions.
