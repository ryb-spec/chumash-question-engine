You are working in the chumash-question-engine repo.

TASK TITLE:
Create Perek 5-6 Candidate-Planning Review Checklist Only.

PURPOSE:
Start from `data/gate_2_source_discovery/bereishis_perek_5_6_candidate_planning.tsv` and create a candidate-planning review checklist for the seven eligible Perek 5-6 candidates only.

HARD RULES:
Do not activate Perek 5 or Perek 6. Do not widen active runtime scope. Do not create runtime content, reviewed-bank content, protected-preview packet content, internal protected-preview packet content, or student-facing content. Keep runtime, reviewed-bank, protected-preview, and student-facing permission fields false. Do not advance held/source-only/source-follow-up candidates.

WORK TO PERFORM:
- Inspect the candidate-planning TSV and teacher-review decisions-applied artifacts.
- Create a candidate-planning review checklist only.
- Preserve all Yossi revision, spacing, and source cautions.
- Keep all gates false.
- Add validator and tests.
- Stop if teacher decisions or source evidence are missing.
