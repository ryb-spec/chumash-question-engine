# Approved Question Template Policy

## Purpose

This document creates a safe scaffold for future reusable question-template approval. It does not approve any template for use, generate questions, create answer choices, create answer keys, or authorize runtime activation.

## Hard Boundaries

- Runtime status: `not_runtime_ready`
- Question-generation status: `not_question_ready`
- Reviewed-bank status: `not_reviewed_bank_ready`
- Student-facing status: `not_student_facing`
- Protected-preview status: `blocked_pending_future_gate`

Trusted source-derived rows may support future template planning only after extraction accuracy is verified. AI-generated questions, answer choices, answer keys, protected previews, reviewed-bank promotion, runtime activation, and student-facing release still require separate full review gates.

## Template Approval Fields

Future template records should include:

- `template_id`
- `skill_primary`
- `allowed_source_status`
- `required_review_status`
- `allowed_input_fields`
- `required_distractor_rules`
- `blocked_cases`
- `yossi_approval_needed_before_use`
- `runtime_status`
- `protected_preview_status`

## Template Categories

| Category | Skill primary | Allowed source status | Required review status | Allowed input fields | Required distractor rules | Blocked cases | Yossi approval needed before use | Runtime status | Protected preview status |
|---|---|---|---|---|---|---|---|---|---|
| translation | translation_context | `yossi_extraction_verified` | future template approval required | Hebrew source, trusted translation, source reference | Must use approved same-scope meanings only | unverified translation, context-heavy ambiguity | yes | `not_runtime_ready` | `blocked_pending_future_gate` |
| shoresh | shoresh_identification | `yossi_extraction_verified` | future template approval required | Hebrew form, root, source reference | Must use approved roots only | weak roots, altered roots, full parsing unless separately approved | yes | `not_runtime_ready` | `blocked_pending_future_gate` |
| prefix | prefix_meaning | `yossi_extraction_verified` | future template approval required | visible prefix, Hebrew form, source reference | Must use approved visible prefixes only | ו ההיפוך, ה השאלה, ה המגמה unless separately approved | yes | `not_runtime_ready` | `blocked_pending_future_gate` |
| suffix | suffix_meaning | `yossi_extraction_verified` | future template approval required | suffix form, person/gender/number, source reference | Must use approved suffix examples only | ambiguous suffixes, context-heavy suffix inference | yes | `not_runtime_ready` | `blocked_pending_future_gate` |
| tense | verb_clue | `yossi_extraction_verified` | future template approval required | verb form, tense clue, source reference | Must use approved forms only | full parsing, בנינים, passive, ציווי, מקור, שם הפועל | yes | `not_runtime_ready` | `blocked_pending_future_gate` |
| noun/verb/part-of-speech | part_of_speech | `yossi_extraction_verified` | future template approval required | Hebrew form, classification, source reference | Must use approved classifications only | ambiguous part-of-speech without context | yes | `not_runtime_ready` | `blocked_pending_future_gate` |
| possessive suffix | possessive_suffix | `yossi_extraction_verified` | future template approval required | noun + suffix, possessive meaning, source reference | Must use approved suffix meanings only | plural endings treated as suffixes, ambiguous ownership | yes | `not_runtime_ready` | `blocked_pending_future_gate` |
| vav hahipuch | vav_hahipuch | `yossi_extraction_verified` | future template approval required | Hebrew form, source reference, teacher-approved boundary | Must be separately approved | all ו ההיפוך cases until separately approved | yes | `not_runtime_ready` | `blocked_pending_future_gate` |
| את as object marker | et_object_marker | `yossi_extraction_verified` | future template approval required | source phrase, function, source reference | Must distinguish only approved function | two functions of את until separately approved | yes | `not_runtime_ready` | `blocked_pending_future_gate` |

## Non-Approval Statement

No template in this document is approved for question generation. This is only the canonical place to define what future approval must record before templates can be used.
