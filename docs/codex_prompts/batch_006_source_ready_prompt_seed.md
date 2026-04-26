# Batch 006 Source-Ready Prompt Seed

```text
You are working in the chumash-question-engine repo.

TASK TYPE:
new curriculum extraction batch

Suggested branch:
feature/curriculum-batch-006-bereishis-4-17-to-4-26

Prerequisites before running:
- Confirm the current branch is the Batch 006 extraction branch.
- Confirm `data/source_texts/bereishis_hebrew_menukad_taamim.tsv` is present and validated.
- Confirm `data/source_texts/source_text_manifest.json` marks Bereishis as safe for extraction planning.
- Confirm the previous reviewed batch state is still correct in the curriculum manifest.

Source files to use:
- `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- `data/source_texts/source_text_manifest.json`
- `data/source_texts/reports/bereishis_hebrew_menukad_taamim_validation.md`
- approved local English or translation source material for the selected Batch 006 range

Forbidden files:
- `streamlit_app.py`
- `runtime/`
- `engine/`
- scoring/mastery/UI files
- reviewed production question-bank files
- prior batch extraction JSONL
- prior batch preview JSONL
- release-check logic and artifacts

Validation commands:
- `git branch --show-current`
- `git status --short`
- `python scripts/validate_source_texts.py`
- `python scripts/validate_curriculum_extraction.py`
- `python -m pytest tests/test_source_texts_validation.py`
- `python -m pytest tests/test_curriculum_extraction_validation.py tests/test_curriculum_question_preview.py`

Stop conditions:
- stop immediately if the branch is wrong
- stop if source text validation fails
- stop if reliable local translation or source material is missing
- stop if continuing would require touching runtime or inventing Hebrew

Reminders:
- do not touch runtime
- do not invent Hebrew
- use canonical `data/source_texts/` when the pasuk is present there
- create the manual-review packet as part of the extraction branch
- stop before commit, push, or PR creation
```
