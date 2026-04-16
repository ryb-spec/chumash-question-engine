# AGENTS.md

## Project Purpose

This repo is a Chumash quiz engine with a growing Torah parsing pipeline. It supports quiz generation, skill tracking, structured Hebrew word analysis, and a Mesorah-aligned context translation review workflow.

## Important Files

- `run_quiz.py` - CLI quiz runner and runtime entry point.
- `pasuk_flow_generator.py` - dynamic pasuk, word, grammar, and skill-question generation.
- `skill_tracker.py` - mastery, scoring, and progress updates.
- `data/` - local JSON data: pesukim, word bank, occurrences, translation reviews, authority notes, and skill question data.
- `torah_parser/` - local parsing helpers for normalization, tokenization, candidate analysis, disambiguation, Torah rules, review helpers, and export utilities.

## Do Not

- Do not change UI unless explicitly asked.
- Do not change scoring unless explicitly asked.
- Do not do unrelated refactors.
- Keep patches small and focused.

## Parsing Conventions

- Preserve surface Hebrew with nekudos in source text and display fields.
- Store undotted normalized forms for matching.
- `data/word_bank.json` is keyed by exact surface form.
- Each word-bank value must be a list of analyses, even when there is only one.
- Prefixes and suffixes must be structured arrays of objects, not plain strings.

## Authority Rules

- Metzudah is the human review authority for context translation.
- Runtime must use local data only; no scraping, browsing, or live external lookup.
- Unresolved translation-review items stay marked `needs_review`.

## Done Criteria

- No schema drift.
- Backward compatibility is preserved where existing code expects legacy fields.
- Changed files are summarized after each task.
