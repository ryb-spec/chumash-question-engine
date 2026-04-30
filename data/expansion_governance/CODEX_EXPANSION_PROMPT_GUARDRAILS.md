# Codex Expansion Prompt Guardrails

Paste this into future expansion prompts.

```text
Streamlined Expansion Governance guardrails:

- Do not activate planning-only content.
- Do not skip approval statuses.
- Do not mix discovery with runtime.
- Do not deepen words before the depth gate is satisfied.
- Do not create mixed review packets unless explicit exception metadata is present.
- Do not change runtime behavior unless explicitly requested.
- New expansion files must use governed fields or clearly explain why they are legacy/unmanaged.
- Protected preview is not runtime.
- Reviewed-bank candidate is not reviewed-bank approved.
- Planning-only is never runtime.

Run before final response:
python scripts/validate_streamlined_expansion_governance.py --strict

If creating a new governed expansion file, also run:
python scripts/validate_streamlined_expansion_governance.py --path PATH_TO_FILE
```
