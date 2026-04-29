# Repo hygiene inventory — 2026-04-29

This is an inventory only. No files were deleted, renamed, moved, or marked safe to delete.

## Summary

The repo contains several legacy-looking root files, doubled-extension files, log files, and worktree folders. Many may be harmless or historically useful, but none should be deleted without a separate verification task.

## Inventory

| Path | What it appears to be | Runtime-relevance guess | Risk | Recommendation | Evidence used |
|---|---|---|---|---|---|
| `run_quiz.py.py` | doubled-extension Python file, likely old wrapper/copy | likely dev/migration | medium | later move to legacy after verification | root listing shows both `run_quiz.py` and `run_quiz.py.py`; `run_quiz.py` is identified as legacy/dev CLI in AGENTS.md |
| `prompt.txt.txt` | doubled-extension text artifact | likely dev/migration | low | later move to legacy or delete after verification | root listing shows both `prompt.txt` and `prompt.txt.txt` |
| `progress.json.txt` | doubled-extension progress placeholder/text artifact | unknown | medium | leave for now | root listing shows `progress.json` and `progress.json.txt`; progress files can affect local pilot state |
| `question_ui.py` | root-level UI helper/module | likely runtime | high | leave for now | root listing plus filename suggests UI/runtime relevance; no import trace was performed in this inventory |
| `.worktrees/debug-replay-layer/` | local worktree directory | likely dev/migration | low | leave for now | `.worktrees` listing |
| `.worktrees/freshness-ranking-guard/` | local worktree directory | likely dev/migration | low | leave for now | `.worktrees` listing |
| `.worktrees/gold-parser-followup/` | local worktree directory | likely dev/migration | low | leave for now | `.worktrees` listing |
| `.worktrees/pasuk-flow-live-fix/` | local worktree directory | likely dev/migration | low | leave for now | `.worktrees` listing |
| `.worktrees/plural-form-lane/` | local worktree directory | likely dev/migration | low | leave for now | `.worktrees` listing |
| `.worktrees/question-generation-audit/` | local worktree directory | likely dev/migration | low | leave for now | `.worktrees` listing |
| `.worktrees/validation-framework-safety-gates/` | local worktree directory | likely dev/migration | low | leave for now | `.worktrees` listing |
| `validate_level5_append.py` | standalone validation script outside `scripts/` | likely dev/migration | medium | later move to scripts after verification | root listing shows standalone validator-like file |
| `append_selected_level5.py` | root-level data/update helper | likely dev/migration | medium | later move to scripts or legacy after verification | root listing; script-like name |
| `import_new_questions.py` | root-level import helper | unknown | medium | leave for now | root listing; may affect question data if used |
| `upgrade_grammar_layer.py` | root-level migration/helper script | likely dev/migration | medium | later move to scripts after verification | root listing; migration-like name |
| `update_menukad_word_bank.py` | root-level data update helper | likely dev/migration | medium | later move to scripts after verification | root listing; source/data-affecting name |
| `generate_html.py` | root-level output generator | likely dev/migration | low | later move to scripts after verification | root listing; generator-like name |
| `streamlit*.log` and `streamlit*.err.log` | local Streamlit logs | likely dev/migration | low | later delete after verification | root listing shows multiple dated local logs |
| `tmp_*streamlit*.log` and `tmp_live_tunnel*.log` | local temporary logs | likely dev/migration | low | later delete after verification | root listing shows temporary log names |
| `temp_unicode_test.txt` | local scratch artifact | likely dev/migration | low | later delete after verification | root listing; scratch-like filename |

## Caution

This inventory uses filenames, root listing, AGENTS.md guidance, and visible local path patterns only. It does not prove that any file is safe to delete.
