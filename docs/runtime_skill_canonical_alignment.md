# Runtime Skill Canonical Alignment

This note records the current review of supported runtime skills against the
foundation crosswalk layer.

The supported runtime remains `streamlit_app.py`. These mappings do not change
student-facing behavior. They only make the alignment between runtime skills and
the standards layer more explicit.

## Mapped to existing crosswalk rows

- `identify_prefix_meaning`
  - `PREFIX.BASIC_PREPOSITIONS`
- `identify_suffix_meaning`
  - `SUFFIX.FIRST_PERSON`
  - `SUFFIX.SECOND_PERSON`
- `identify_pronoun_suffix`
  - `SUFFIX.THIRD_PERSON`
  - `SUFFIX.KINUY`
- `identify_verb_marker`
  - `VERB.MARKER`
- `segment_word_parts`
  - `WORD.PARTS.SEGMENT`
- `identify_tense`
  - `VERB.TENSE.PAST`
  - `VERB.TENSE.PRESENT`
  - `VERB.TENSE.FUTURE`
- `identify_prefix_future`
  - `PREFIX.OTIYOT_EITAN`
  - `VERB.TENSE.FUTURE`
- `identify_suffix_past`
  - `VERB.TENSE.PAST`
- `identify_present_pattern`
  - `VERB.TENSE.PRESENT`
- `convert_future_to_command`
  - `VERB.COMMAND`
- `match_pronoun_to_verb`
  - `PRONOUN.SUBJECT_OBJECT_MATCH`
- `part_of_speech`
  - `WORD.PART_OF_SPEECH_BASIC`
  - rationale:
    closest external analogue; runtime coverage is a little broader because it
    can also surface particle/preposition distractors
- `shoresh`
  - `ROOT.IDENTIFY`
  - `ROOT.IDENTIFY_DROPPED`
  - rationale:
    runtime shoresh coverage now includes both clear three-letter roots and a
    reviewed subset of dropped-letter / weak-root cases
- `preposition_meaning`
  - `PREFIX.BASIC_PREPOSITIONS`
- `verb_tense`
  - `VERB.TENSE.PAST`
  - `VERB.TENSE.PRESENT`
  - `VERB.TENSE.FUTURE`
- `subject_identification`
  - `VERB.SUBJECT_OBJECT`
- `object_identification`
  - `VERB.SUBJECT_OBJECT`
  - rationale:
    the runtime covers this canonical clause-role work through two narrower
    lanes instead of one combined prompt family
- `suffix`
  - `SUFFIX.FIRST_PERSON`
  - `SUFFIX.SECOND_PERSON`
  - `SUFFIX.THIRD_PERSON`
  - rationale:
    the runtime suffix lane is meaning-oriented and lands on the defended
    person-suffix family rather than a pure form-recognition row

## Engine-extension rows added

These are explicit alignment shims for real runtime skills that were not
represented cleanly in the incoming seed package. They are marked
`system_layer = engine_extension` in the crosswalk so they do not masquerade as
external canonical truth.

Their catalog-governance review queue now lives in
`data/standards/internal/engine_extension_review_queue.v1.json`.

- `translation`
  - `WORD.MEANING_BASIC`
  - rationale:
    the live runtime has a foundational isolated-word meaning lane, but the seed
    crosswalk did not include a direct one-word meaning row
- `prefix`
  - `PREFIX.FORM_IDENTIFY`
  - rationale:
    the live runtime has a visible-prefix identification lane distinct from
    prefix-meaning translation
- `phrase_translation`
  - `PHRASE.UNIT_TRANSLATE`
  - rationale:
    the live runtime translates short phrases as units, which is not the same as
    importing benchmark context-translation rows into runtime truth

## Intentionally unmapped runtime skills

- none in the current review

## Deliberate non-mappings

- benchmark-only rows such as `COMP.CONTEXT_TRANSLATION` remain outside the
  runtime skill catalog
- teacher-ops, paradigm, and lexicon resources remain helper layers only
