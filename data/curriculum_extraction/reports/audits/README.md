# Governed curriculum extraction audit reports

This directory is the governed home for overnight and curriculum-quality audit artifacts.

Allowed audit artifact file types in this directory:

- `.md`
- `.pdf`

Root-level audit artifacts are intentionally not allowed by the curriculum extraction git-diff guard. Audit reports belong here so they can be preserved without weakening runtime protections.

These audit artifacts are non-runtime, non-preview, non-reviewed-bank, and non-student-facing. Creating or preserving an audit artifact here does not activate Perek 3, promote reviewed-bank content, create protected-preview packets, or change runtime behavior.

Curriculum-quality control summaries and generated governance indexes live under `data/validation/`, starting with:

- `data/validation/curriculum_quality_control_index.md`
- `data/validation/curriculum_quality_check_summary.md`
- `data/validation/curriculum_quality_check_summary.json`
