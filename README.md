# Chumash Question Engine

## Project Purpose

This repo is a Chumash/Torah assessment engine with a Streamlit UI, a local
Torah parsing pipeline, structured Hebrew word analysis, quiz generation, and
review-aware translation metadata.

## Supported Runtime

The supported student-facing runtime is the Streamlit app:

```powershell
streamlit run streamlit_app.py
```

`run_quiz.py` is kept only as a legacy/dev CLI wrapper. Static preview and
export artifacts live under `artifacts/preview/` and `legacy/`; they are not
the supported app runtime.

## High-Level Architecture

- `streamlit_app.py`
  - supported runtime entrypoint
  - renders Learn Mode, Practice Mode, and Pasuk Flow
- `assessment_scope.py`
  - defines the active dataset scope and shared repo/data paths
- `pasuk_flow_generator.py`
  - shared question-generation engine for the active runtime
- `foundation_resources.py`
  - loaders and validators for versioned foundation seed resources
- `torah_parser/`
  - normalization, tokenization, candidate analysis, Torah rules, and export helpers
- `progress_store.py`
  - unified learner progress/mastery persistence
- `skill_tracker.py`
  - mastery and exposure update logic over the shared progress state
- `data/`
  - active parsed dataset, word bank, occurrences, reviews, and validation artifacts
  - also contains non-runtime foundation layers for standards, benchmarks, paradigms, lexicon policy, and teacher ops

See [docs/foundations_layers.md](docs/foundations_layers.md) for the foundation-layer boundaries and source-of-truth rules.

## How To Run The App

1. Install dependencies.
2. Start Streamlit:

```powershell
streamlit run streamlit_app.py
```

3. Open the local URL shown by Streamlit.

## Current Recommended Validation

Fast local validation for curriculum quality and guard behavior:

```powershell
python -m pytest tests/test_curriculum_extraction_validation.py
python -m pytest tests/test_curriculum_quality_checks.py
```

Run the non-runtime curriculum quality control orchestrator:

```powershell
python scripts/run_curriculum_quality_checks.py
```

Run the full suite before commit:

```powershell
python -m pytest
```

The curriculum quality orchestrator writes non-runtime validation and review-governance reports. Those reports do not activate content, promote reviewed-bank items, create protected-preview packets, or create student-facing content. Standalone validators remain important for focused work, and Perek 3 activation or reviewed-bank promotion require separate explicit tasks.

Legacy unittest commands may still be useful for historical characterization, but the primary local and CI path is pytest.

## Legacy And Dev-Only Pieces

- `run_quiz.py`
  - legacy/dev CLI wrapper
- `question_generator.py`
  - legacy static preview generator
- preview/export JSON and HTML artifacts in `artifacts/preview/`
  - useful for inspection, not the supported runtime
- `legacy/`
  - legacy exported HTML and other non-runtime artifacts kept out of the repo root
