# Streamlined Expansion Governance

This folder records the project's durable expansion policy in a machine-readable contract.

Primary contract:

- `streamlined_expansion_contract.json`

The contract makes the expansion model explicit:

- Expand horizontally across more pesukim and perakim.
- Expand vertically only when deeper skills are attached to already-approved words.
- Let discovery and planning move ahead, including future perakim, while keeping activation closed.
- Treat word approval, question approval, reviewed-bank approval, and runtime activation as separate gates.
- Keep runtime-active content as the smallest safe subset, not the full discovery or reviewed-bank planning inventory.

This folder does not create runtime content, reviewed-bank entries, Streamlit UI changes, scoring changes, or question-serving behavior.

## Governed file opt-in

New expansion artifacts enter Streamlined Expansion Governance enforcement when they either live under `data/expansion_governance/` or explicitly declare an opt-in field such as `expansion_governance_contract`, `streamlined_expansion_contract`, `governance_contract`, or `governed_by`. Path-specific validation with `scripts/validate_streamlined_expansion_governance.py --path ...` also treats recognizable governance fields as governed so draft artifacts can be checked before broader adoption.

Legacy pipeline, protected-preview, vocabulary-bank, diagnostic-preview, and reviewed-bank planning artifacts that do not opt into this contract remain unmanaged by this validator until they are deliberately migrated. Once a file opts in, planning-only content must keep runtime and promotion flags closed, protected preview must not be treated as runtime, reviewed-bank candidates must not be treated as reviewed-bank approved, and vertical depth must show the required base-word approval and observation evidence.
