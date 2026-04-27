# Standard 3 Source Verification Final Decisions Report

## 1. Current Branch
- `feature/standard-3-source-verification-final-decisions`

## 2. Files Created
- `data/standards/zekelman/review/standard_3_source_verification_packet.md`
- `data/standards/zekelman/review/standard_3_source_verification_tracking.json`
- `data/standards/zekelman/reports/standard_3_source_verification_final_decisions_report.md`

## 3. Files Modified
- `PLANS.md`
- `data/standards/zekelman/review/zekelman_2025_standard_3_review_tracking.json`
- `data/standards/zekelman/review/zekelman_2025_standard_3_review_decision_sheet.md`
- `data/standards/zekelman/review/zekelman_2025_standard_3_teacher_review_packet.md`
- `data/standards/zekelman/review/standard_3_source_verification_tracking.json`
- `data/standards/zekelman/reports/standard_3_source_verification_final_decisions_report.md`

## 4. Decisions Recorded
- `3.08` Grouping and Word Order: `approve_with_wording_revision`.
- Reviewer notes: Approve as a diagnostic planning direction only when narrowed to phrase-level translation and basic Hebrew-to-English word-order adjustment. Do not yet use as a broad independent full-pasuk grouping skill. סמיכות may support this lane, but should remain separately tracked under 3.04 as well.
- Remaining source checks: Verify Loshon page references and examples visually in the PDFs.
- Recommended next action: Create a narrowed 3.08 diagnostic planning lane after source verification.

- `3.04` Parts of Speech / Nouns / סמיכות: `approve_with_wording_revision`.
- Reviewer notes: Approve with wording revision. Split into at least two planning lanes: noun/adjective features and סמיכות recognition. Noun gender, number, and common form changes are suitable for diagnostic planning after source examples are verified. Irregular forms and adjective agreement should remain later-level or review-required.
- Remaining source checks: Verify Hebrew examples, nekudos, and level placement against Zekelman and Loshon PDFs.
- Recommended next action: Add separate planning lanes for noun features and סמיכות.

- `3.10` Understanding ניקוד: `defer_to_later_phase`.
- Reviewer notes: Defer to later phase. Current evidence is too narrow and OCR-sensitive to support 3.10 as a diagnostic lane. Limited nikud-sensitive examples may be used as caution notes under 3.06, but full ניקוד systems such as תנועות, שבאים, דגשים, syllables, and טעמי המקרא require direct source review before diagnostic planning.
- Remaining source checks: Directly verify Zekelman 3.10 levels and Loshon nikud/pausal references in the PDFs.
- Recommended next action: Keep 3.10 out of MVP diagnostic blueprint except as a caution note.

## 5. Runtime And Question-Ready Boundary Confirmation
- No `runtime_ready` status was added.
- No `question_ready` status was added.
- `not_runtime_ready` was preserved for `3.08`, `3.04`, and `3.10`.
- `not_question_ready` was preserved for `3.08`, `3.04`, and `3.10`.
- `3.08` and `3.04` are approved only as planning directions and remain blocked from runtime use.
- `3.10` remains deferred and must not appear in the MVP diagnostic blueprint except as a caution note.

## 6. Remaining Source Checks
- `3.08`: Verify Loshon page references and examples visually in the PDFs.
- `3.04`: Verify Hebrew examples, nekudos, and level placement against Zekelman and Loshon PDFs.
- `3.10`: Directly verify Zekelman 3.10 levels and Loshon nikud/pausal references in the PDFs.

## 7. Remaining Blockers Before Diagnostic Blueprint
- Source verification still needs to be completed before the narrowed `3.08` planning lane is drafted.
- `3.04` must be split into noun/adjective feature and סמיכות planning lanes before blueprint use.
- `3.10` must stay out of the MVP diagnostic blueprint except as a caution note.
- No student-facing questions, answer keys, active templates, runtime hooks, reviewed-bank content, or production data may be created from these decisions without a separate explicit prompt.

## 8. Validation Results
- `python -m json.tool data/standards/zekelman/review/zekelman_2025_standard_3_review_tracking.json`: passed.
- `python -m json.tool data/standards/zekelman/review/standard_3_source_verification_tracking.json`: passed.
- `python scripts/validate_source_texts.py`: passed.
- `python scripts/validate_curriculum_extraction.py`: passed.
- `python scripts/validate_standards_data.py`: passed.
- `python -m pytest tests/test_standards_data_validation.py`: `9 passed`.
- `python -m pytest`: `574 passed`, `1 failed`.
- Unrelated full-suite failure: `tests/test_source_texts_validation.py::SourceTextsValidationTests::test_validator_reports_expected_sha256_for_real_file`; current SHA is `4d96c615ab63e0419bff079db250d71ea9b5de266ff9ab8d589ae80e4afd0b71`, while the test expects `0dedb854e1e8b59fa5dc08f93be5baffe4c1faaa09d00c148c8ef3113b065913`.

## 9. Recommended Next Step
- After source verification, create a non-runtime diagnostic planning-lane draft for the narrowed `3.08` lane and separated `3.04` noun-feature / סמיכות lanes, while keeping `3.10` deferred.
