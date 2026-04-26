# Standard 3 Teacher Review Instructions

## 1. Purpose Of Review
- This review confirms whether selected Zekelman 2025 Standard 3 strands are suitable as future foundational diagnostic directions.
- This review does not activate runtime behavior, create student questions, or make anything question-ready.
- The goal is to make later blueprint work safer by recording teacher judgment clearly and conservatively.

## 2. What The Reviewer Is Verifying
- Whether the canonical 2025 Standard 3 wording was captured accurately enough for planning use.
- Whether the listed supplemental sources really support the strand, partially support it, or leave uncertainty.
- Whether the level range in the current review item is fair, too broad, or needs narrowing.
- Whether the draft skill mapping is directionally useful for diagnostics without over-claiming readiness.
- Whether Hebrew, nikud, OCR, or table-structure uncertainty is still too high for the strand to move forward.

## 3. How To Use The Two Review Files
- Read `data/standards/zekelman/review/zekelman_2025_standard_3_teacher_review_packet.md` first.
- Use it to understand the strand summary, source support, known uncertainty, and the questions that still need teacher judgment.
- Then update `data/standards/zekelman/review/zekelman_2025_standard_3_review_tracking.json`.
- Record only what the review actually established. Do not fill in guesses just to complete every field.

## 4. How To Fill `reviewer_decision`
- Use exactly one of these values when a decision is ready:
- `approve_as_foundational_skill`
- `approve_with_wording_revision`
- `approve_with_level_adjustment`
- `needs_more_source_review`
- `not_suitable_for_diagnostic_use_yet`
- `defer_to_later_phase`
- If the review has not happened yet, keep `reviewer_decision` blank or `null`.
- Use `approve_as_foundational_skill` only when the strand is directionally approved for later diagnostic planning.
- Use `approve_with_wording_revision` when the direction is acceptable but the current wording overstates certainty or needs teacher-friendly correction.
- Use `approve_with_level_adjustment` when the strand seems sound but the level range should be narrowed, shifted, or split.
- Use `needs_more_source_review` when the source evidence or extraction still needs more checking before a real decision.
- Use `not_suitable_for_diagnostic_use_yet` when the strand is too uncertain, too context-heavy, or too broad right now.
- Use `defer_to_later_phase` when the strand may become useful later but should not be part of the current planning wave.

## 5. How To Write `reviewer_notes`
- Write short factual notes.
- Name what was checked: canonical page, supplemental page, Hebrew example, or level wording.
- Say what changed in understanding: confirmed, narrowed, still uncertain, or blocked.
- If you revise wording or level fit, describe the change plainly.
- Avoid student-question wording and avoid final-answer language.
- Good notes are concrete:
- "Confirmed page 30 row C should stay grouped with taught noun-family recognition, not broad semantic clustering."
- "Weak-root expectation appears too advanced for the first approval pass; keep simple shoresh recognition only."

## 6. How To Handle Hebrew Or OCR Uncertainty
- Do not resolve OCR uncertainty by guesswork.
- If Hebrew display, nikud, row boundaries, or table structure are unclear, check the raw PDF directly.
- If the raw PDF still leaves uncertainty, keep the strand conservative and record that uncertainty in `reviewer_notes`.
- When uncertainty remains, prefer:
- `needs_more_source_review`
- `defer_to_later_phase`
- Do not mark Hebrew as verified unless it was actually reviewed against the source.

## 7. How To Handle Level Disagreement
- If the strand seems valid but the current level range is too wide, use `approve_with_level_adjustment`.
- Note which levels look secure and which levels should stay blocked.
- If the disagreement is substantial and source review is incomplete, use `needs_more_source_review` instead.
- Do not stretch lower or higher level expectations just to keep the strand intact.

## 8. How To Handle Source Mismatch
- If the canonical 2025 wording and the older sources do not line up cleanly, do not force agreement.
- Record the mismatch in `reviewer_notes`.
- Use `needs_more_source_review` if the mismatch affects trust in the strand wording.
- Use `defer_to_later_phase` if the strand may still be useful later but cannot be trusted enough now.
- Older supplemental organization should not override the 2025 canonical source, but it may affect wording, level, or scope decisions.

## 9. What Not To Approve Yet
- Do not approve anything as runtime-ready.
- Do not approve anything as question-ready.
- Do not approve active question templates.
- Do not approve reviewed-bank promotion.
- Do not invent teacher review decisions for strands that were not actually checked.
- Do not treat "foundational diagnostic direction" as production approval.

## 10. Review Order
- Review in this order:
- `3.01`
- `3.02`
- `3.05`
- `3.06`
- `3.07`
- `3.08`
- Then review `3.04` and `3.10`
- This order keeps the first pass focused on the strands most likely to matter for later diagnostic planning.

## 11. Clear Rule
- Teacher review may approve a skill as a foundational diagnostic direction, but that still does not make it runtime-ready or question-ready.
