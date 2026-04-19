# AGENTS.md

## Project Purpose

This repo is a Chumash quiz engine with a growing Torah parsing pipeline. It supports quiz generation, skill tracking, structured Hebrew word analysis, and a Mesorah-aligned context translation review workflow.

## Important Files

- `streamlit_app.py` - supported live quiz UI/runtime.
- `run_quiz.py` - legacy/dev CLI wrapper.
- `pasuk_flow_generator.py` - dynamic pasuk, word, grammar, and skill-question generation.
- `pasuk_flow_planner.py` - Pasuk Flow progression, diversity, tiering, and completion logic.
- `pasuk_flow_audit.py` - developer-facing Pasuk Flow simulation/audit helpers.
- `skill_tracker.py` - mastery, scoring, and progress updates.
- `question_generation_audit.py` - developer-facing safe-candidate coverage/reporting.
- `scripts/` - report generation, audit helpers, fake-attempt generation, validation artifacts.
- `data/` - local JSON data: pesukim, word bank, occurrences, translation reviews, authority notes, and skill question data.
- `artifacts/preview/` - legacy preview/export JSON and HTML artifacts, not the supported runtime.
- `legacy/` - legacy exported/reference artifacts kept out of the repo root.
- `torah_parser/` - local parsing helpers for normalization, tokenization, candidate analysis, disambiguation, Torah rules, review helpers, and export utilities.

## Working Agreements

- Finish the current task completely before starting a new one.
- Do not interrupt the current task because a new idea seems attractive.
- Do not switch to a different subtask unless the current task is blocked in a way that makes further work unsafe, meaningless, or purely speculative.
- If a new instruction arrives while work is in progress, treat it as a note for later unless it explicitly says to abandon the current task.
- Keep patches small, focused, and reversible.
- Prefer evidence, tests, reports, and summaries over broad speculative refactors.
- Prefer blocking an unsafe or ambiguous question over generating a broader but less reliable one.

## Do Not

- Do not change UI unless explicitly asked.
- Do not change scoring unless explicitly asked.
- Do not change mastery logic unless explicitly asked.
- Do not do unrelated refactors.
- Do not start a new task until the current one is fully finished under the Done Criteria below.
- Do not run git commit, git push, gh pr create, or any merge/publish command.
- Do not ask for permission to push, commit, or open a PR.
- Do not loosen validators, safety rails, repetition protections, debug instrumentation, or audit tooling just to increase coverage.
- Do not broaden compound morphology handling just to create more candidates.
- Do not treat plural endings or irregular number forms as pronominal suffixes.
- Do not force contextual translation answers into isolated-word meaning questions.
- Do not invent unsupported student-facing skill lanes without full support structure.

## Worktree / Branch Discipline

- Stay in the current worktree/branch only.
- Prefer one coherent task per worktree.
- Do not begin a second major task inside the same branch until the current one is fully finished and reported.
- When a task is done, summarize it cleanly before moving on.

## Parsing Conventions

- Preserve surface Hebrew with nekudos in source text and display fields.
- Store undotted normalized forms for matching.
- `data/word_bank.json` is keyed by exact surface form.
- Each word-bank value must be a list of analyses, even when there is only one.
- Prefixes and suffixes must be structured arrays of objects, not plain strings.
- Prefer using existing candidate metadata before introducing new heuristic fallback logic.
- Keep disambiguation improvements conservative and readable.
- Do not widen noun/verb normalization broadly when a narrow metadata-aware fallback will do.

## Quiz Engine Safety Rules

- Candidate scoring must only compare already-safe survivors.
- Repetition protection should remain active unless explicit reteach or a genuinely limited safe candidate pool requires reuse.
- Keep simple morphology questions compact; reserve full pasuk display for genuinely context-dependent tasks.
- Keep Pasuk Flow safety-first:
  - avoid repeated target reuse when safe unseen targets still exist
  - avoid repeated prompt-family reuse when fresher prompt families still exist
  - avoid repeated low-tier skill-family reuse when other safe skill families still exist
  - complete only after meaningful coverage or true limited-pool exhaustion
- If a form is compound or ambiguous, prefer a clear block or a narrow dedicated lane over shoving it into a simple prefix/suffix lane.

## Skill-Lane Expansion Rules

Before adding or widening a skill lane, ensure it has all of:
- classifier
- candidate detector
- validator
- distractor rules
- compact/full-context display policy
- debug trace visibility
- audit/report visibility
- tests

If all of the above are not present, do not ship that lane.

## Authority Rules

- Metzudah is the human review authority for context translation.
- Runtime must use local data only; no scraping, browsing, or live external lookup.
- Unresolved translation-review items stay marked `needs_review`.

## Commands to Use

### Full test suite
- `python -m pytest`

### Common targeted slices
- `python -m pytest tests/test_pasuk_flow_planner.py tests/test_streamlit_pasuk_flow_completion.py tests/test_pasuk_flow_audit.py tests/test_streamlit_debug_instrumentation.py`
- `python -m pytest tests/test_gold_shoresh_accuracy.py tests/test_gold_affix_handling.py`
- `python -m pytest tests/test_streamlit_quiz_experience.py tests/test_streamlit_candidate_quality.py tests/test_question_followup_ui.py`

### Local app
- `python -m streamlit run streamlit_app.py`

### Debug mode (browser)
- `?assessment_debug=1`

### Validation / reporting helpers
- `python scripts/generate_fake_attempts.py`
- `python scripts/generate_insights.py`
- `python scripts/write_test_summary.py`
- `python scripts/generate_daily_review.py`

## Nightly Review / Audit Discipline

When a task changes generation, parsing, Pasuk Flow, or repeated-trouble-word handling:
- update relevant tests
- run targeted tests
- run full pytest
- update developer-facing audits/reports if the change affects candidate depth, repetition, or question quality
- summarize whether audit/debug outputs changed

## ExecPlans for Multi-Hour Work

When the task is expected to run for a long time, span multiple files, or require several milestones:
- create or update `PLANS.md` before major edits
- keep the plan short, concrete, and checklist-style
- update the plan as milestones complete
- finish the current plan before starting a different major plan

Use `PLANS.md` especially for:
- Pasuk Flow overhauls
- validator framework changes
- parser/disambiguation improvements that touch several files
- skill-lane expansion
- daily review / audit pipeline changes

## Definition of Finished

A task is only considered finished when all of the following are done:
- the intended code change is completed
- relevant tests are added or updated
- targeted tests are run
- full pytest is run
- a concise summary is prepared including:
  - files changed
  - what was added or tightened
  - what was intentionally not broadened
  - tests added or updated
  - targeted test results
  - full pytest result
  - anything still unfinished or blocked
  - the single next highest-value recommended task

## Reporting Style

When a task is finished, report in this order:
1. Current task completed
2. Files changed
3. What was added or tightened
4. What was intentionally not broadened
5. Tests added or updated
6. Targeted test results
7. Full pytest result
8. Anything still unfinished or blocked
9. Single next highest-value recommended task
