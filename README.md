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

`run_quiz.py` is kept only as a legacy/dev CLI wrapper. Static preview
artifacts such as `questions.json`, `generated_questions_preview.json`,
`pasuk_flows.json`, and `pasuk_flow_questions.json` are not the supported app
runtime.

## High-Level Architecture

- `streamlit_app.py`
  - supported runtime entrypoint
  - renders Learn Mode, Practice Mode, and Pasuk Flow
- `assessment_scope.py`
  - defines the active dataset scope and shared repo/data paths
- `pasuk_flow_generator.py`
  - shared question-generation engine for the active runtime
- `torah_parser/`
  - normalization, tokenization, candidate analysis, Torah rules, and export helpers
- `progress_store.py`
  - unified learner progress/mastery persistence
- `skill_tracker.py`
  - mastery and exposure update logic over the shared progress state
- `data/`
  - active parsed dataset, word bank, occurrences, reviews, and validation artifacts

## How To Run The App

1. Install dependencies.
2. Start Streamlit:

```powershell
streamlit run streamlit_app.py
```

3. Open the local URL shown by Streamlit.

## Tests

Run the current characterization and active-engine test suite with:

```powershell
python -m unittest tests.test_supported_runtime tests.test_paths tests.test_progress_store tests.test_progress_migration tests.test_streamlit_runtime_scope tests.test_streamlit_modes_smoke tests.test_question_target_selection tests.test_question_types_contract tests.test_normalization tests.test_tokenization tests.test_candidate_generation -v
```

## Legacy And Dev-Only Pieces

- `run_quiz.py`
  - legacy/dev CLI wrapper
- `question_generator.py`
  - legacy static preview generator
- preview/export JSON and HTML artifacts in the repo root
  - useful for inspection, not the supported runtime
