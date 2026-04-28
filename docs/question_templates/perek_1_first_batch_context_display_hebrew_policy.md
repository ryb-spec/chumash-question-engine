# Bereishis Perek 1 First-Batch Context Display and Hebrew Rendering Policy

This policy is context-display and Hebrew-rendering planning only. It creates no rendered student item, protected-preview content, runtime content, or student-facing content.

## Context Display

Phrase context may be shown only when it helps disambiguate the reviewed token and after context-display review. Token-only display is enough when the token is clean and context-independent.

## Hebrew Rendering

Hebrew must remain real UTF-8 Hebrew, never placeholder corruption. Reviewers must check display of nikud-sensitive and punctuation-sensitive fields before preview.

## Articles and Prefixes

For article/prefix tokens such as `המים`, `האדמה`, or `הארץ`, context display and answer-key review must decide whether the article is shown or explained.

## Direct-Object Marker

For `את`, context may be needed so the function is visible. Wording and display must not teach `את` as a simple translation.

## Shoresh Rows

Shoresh rows must display the surface word separately from the target shoresh. For `הבדיל`, display must preserve that the target shoresh is `בדל`.

## Required Review Before Preview

Yossi/teacher must review context display, Hebrew rendering, exact wording, answer-key language, distractor constraints, and protected-preview gate status before any preview draft.

## Yossi review status: policy decision applied

- Context-display/Hebrew-rendering policy approved. Policy decision recorded in the planning layer only.
- Row-level review is required before any generation.
- Required row-level review fields: `exact_wording_review_status`, `answer_key_language_review_status`, `distractor_constraints_review_status`, `context_display_review_status`, `hebrew_rendering_review_status`, `protected_preview_gate_review_status`.
- This decision does not approve questions, answer choices, answer keys, generated distractors, protected-preview generation, reviewed-bank use, runtime use, or student-facing use.
- All gates remain closed.
