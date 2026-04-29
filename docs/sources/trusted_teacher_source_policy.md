# Trusted Teacher Source Review Policy

## Purpose

This policy clarifies how the project reviews trusted educational source materials. It reduces unnecessary review loops without weakening runtime, question-generation, or student-facing safety gates.

## Core Rule

Trusted teacher-approved source materials need one Yossi extraction-accuracy pass, not a full educational approval cycle.

The project should not re-approve the pedagogy of trusted educational source materials from scratch. It should verify that the system extracted, classified, and mapped those materials accurately.

## Trusted Teacher Source Categories

The following source categories may be treated as teacher-approved educational source material when they are used as source references, not as AI-generated content:

- Zekelman Chumash Standards resources
- Zekelman sample assessment questions
- Dikduk review resources and workbooks
- Loshon Hakodesh / Loshon HaTorah resources
- Metsudah translation source material
- Koren translation source material for secondary noncommercial support only
- Other clearly teacher-created Chumash, dikduk, or assessment resources used as source references

## Translation Source Policy

Metsudah is the preferred primary translation source where available:

- Source platform: Sefaria
- Version title: `Metsudah Chumash, Metsudah Publications, 2009`
- License: `CC-BY`
- Preference: primary preferred translation source
- Attribution required: yes
- Yossi extraction-accuracy pass required: yes
- Runtime-ready by default: no
- Question-ready by default: no

Koren may be used only as secondary noncommercial translation support:

- Source platform: Sefaria
- Version title: `The Koren Jerusalem Bible`
- License: `CC-BY-NC`
- Preference: secondary noncommercial translation support
- Attribution required: yes
- Commercial use: requires direct written permission
- Yossi extraction-accuracy pass required: yes
- Runtime-ready by default: no
- Question-ready by default: no

Exact version-level license tracking is required for all translation-source rows. Sefaria availability is not blanket approval for production, commercial, runtime, or student-facing use. Generated questions and runtime use still require separate gates.

## What This Means

`trusted_teacher_source` means:

- The educational content itself is trusted as a source.
- The system does not need to re-approve the pedagogy from scratch.
- Review focuses on extraction accuracy, source matching, Hebrew fidelity, classification, and mapping.
- A single Yossi extraction-accuracy pass can move accurately extracted content to `yossi_extraction_verified`.

## What This Does Not Mean

`trusted_teacher_source` does not mean:

- runtime-ready
- question-ready
- student-facing
- copyright-cleared for redistribution
- free from OCR errors
- free from table, Hebrew, nikud, or source-page extraction errors
- approved for reviewed-bank promotion

## Review Flow

Trusted educator or standards-body source material moves through this flow:

1. Source material is uploaded or ingested.
2. The system extracts content.
3. The system maps extracted content into structured data.
4. Yossi performs one extraction-accuracy pass.
5. If accurate, the content may be marked `yossi_extraction_verified`.
6. Verified source-derived content may support future standards mapping, protected preview planning, or question-generation planning.

Question generation, preview generation, reviewed-bank promotion, runtime activation, and student-facing use still require separate gates.

## Future Packet Language

Future extraction and review packets for trusted teacher-source material should use the template in:

- `docs/sources/trusted_teacher_source_extraction_review_packet_template.md`

Those packets should ask Yossi for an extraction-accuracy confirmation pass. They should not ask Yossi to re-approve the educational value of trusted source content from scratch.

Use this language for trusted source extraction packets:

- Confirm that the copied or OCRed source text matches the source.
- Confirm that Hebrew spelling, nikud, and table layout are faithful where relevant.
- Confirm that translations, explanations, answer keys, or examples were extracted accurately.
- Confirm that classification and standards/skill mapping are reasonable.
- Flag any unclear item for specific confirmation.

Do not use this lighter language for:

- AI-generated or system-generated questions
- protected preview question packets
- reviewed-bank promotion gates
- runtime activation gates
- student-facing release decisions

Those paths still require their own explicit review gates.

Future extraction scripts that create review packets for trusted teacher-source material should call:

- `scripts/generate_trusted_source_extraction_review_packet.py`

Do not call that trusted-source packet generator for generated questions, protected previews, answer-key review, reviewed-bank promotion, runtime activation, or student-facing release work.

## Validator Requirement Before `yossi_extraction_verified`

Pending trusted-source extraction batches should link a generated trusted-source extraction accuracy review packet in `review_artifacts`.

A batch may not use `yossi_extraction_verified` unless:

- the trusted-source extraction accuracy packet exists and is linked
- the manifest records who completed the extraction-accuracy pass
- the manifest records the verification date
- the manifest links the review artifact that records Yossi's confirmation

This verification still does not make content runtime-ready, question-ready, reviewed-bank-ready, protected-preview-ready, or student-facing. Generated questions and runtime promotion still require separate full review gates.

## Status Meanings

- `trusted_teacher_source`: The source category is trusted educational material.
- `pending_yossi_extraction_accuracy_pass`: The source is trusted, but extraction/mapping accuracy still needs Yossi confirmation.
- `yossi_extraction_verified`: Yossi confirmed that the extraction/classification/mapping accurately represents the trusted source.
- `needs_specific_confirmation`: The system needs a targeted answer before choosing a status.
- `blocked_unclear_source`: The source cannot be used until source authority or provenance is clarified.
- `not_runtime_ready`: The content must not be loaded into runtime.
- `not_question_ready`: The content must not be used as active question content.
- `protected_preview_ready`: The content may support a protected preview only after the relevant preview gate explicitly allows it.

## Targeted Confirmation Workflow

When source status or extraction accuracy is unclear, the system should create a targeted confirmation item instead of blocking the entire workflow.

Each confirmation item should include:

- source name
- file path
- unclear issue
- exact question for Yossi
- recommended status after confirmation

Example:

> This file appears to be a dikduk workbook, but the source author/teacher status is unclear. Confirm whether it should be treated as a trusted teacher source.

## Generated Questions Are Different

AI-generated or system-generated questions are not trusted source material. They still require full review before any promotion or runtime use.

Generated previews must remain:

- non-runtime
- not student-facing
- not reviewed-bank approved
- not question-ready until explicitly reviewed and promoted

## Runtime Promotion Is Different

Even verified source-derived content does not become runtime content automatically. Runtime promotion requires a separate explicit gate that checks reviewed-bank status, active scope, loader behavior, rollback, and student-facing approval.
