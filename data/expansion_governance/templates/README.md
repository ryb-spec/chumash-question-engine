# Governed Expansion Templates

Use `governed_expansion_items_template.tsv` when creating new expansion bank, review, or planning artifacts that should participate in Streamlined Expansion Governance.

The example rows are examples only. They are not Torah bank content, not reviewed-bank entries, and not runtime content.

Default planning-only posture:

- `review_status=planning_only`
- `runtime_status=planning_only`
- `planning_only=true`
- `runtime_allowed=false`
- `protected_preview_allowed=false`
- `reviewed_bank_allowed=false`
- `runtime_active=false`

Before finalizing a new governed file, validate it directly:

```powershell
python scripts/validate_streamlined_expansion_governance.py --path PATH_TO_FILE
```

Before release or merge, run strict governance validation:

```powershell
python scripts/validate_streamlined_expansion_governance.py --strict
```
