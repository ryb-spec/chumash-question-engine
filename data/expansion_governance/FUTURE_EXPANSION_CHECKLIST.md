# Future Expansion Checklist

Use this checklist before creating or promoting expansion artifacts.

## 1. Before generating new content

- Decide whether the task is discovery, review, preview, reviewed-bank, or runtime work.
- Identify the Perek.
- Identify the skill layer.
- Identify whether this is horizontal expansion or vertical depth expansion.

## 2. Horizontal expansion rule

- Future-perek discovery defaults to `planning_only`.
- Set `runtime_allowed=false`.
- Set `protected_preview_allowed=false`.
- Set `reviewed_bank_allowed=false`.
- Set `runtime_active=false`.

## 3. Vertical depth rule

Do not deepen a word unless the base word has:

- `word_level_approved`
- simple question review or `teacher_approved`
- `observed_internally`

## 4. Review-packet rule

Review packets should be focused and use exactly one of:

- `word_bank_review`
- `simple_question_review`
- `depth_expansion_review`
- `protected_preview_observation`
- `reviewed_bank_decision`

Mixed review packets require explicit exception metadata, an explanation, separated decision fields, and closed runtime/promotion gates.

## 5. Runtime rule

- Runtime-active requires `reviewed_bank_approved` and `runtime_ready`.
- Protected preview is not runtime.
- Reviewed-bank candidate is not reviewed-bank approved.
- Planning-only is never runtime.

## 6. Validator rule

New governed expansion files must be validated with:

```powershell
python scripts/validate_streamlined_expansion_governance.py --path PATH_TO_FILE
```

Before release, run:

```powershell
python scripts/validate_streamlined_expansion_governance.py --strict
```
