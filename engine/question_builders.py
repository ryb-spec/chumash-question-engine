"""Compatibility access to question-builder entry points."""

from .flow_builder import (
    build_flow_question,
    build_phrase_question,
    build_pr_question,
    build_reasoning_question,
    build_shoresh_question,
    build_subject_question,
    build_substitution_question,
    build_tense_question,
    build_translation_question,
    generate_diagnostic_questions,
    generate_letter_meaning_question,
    generate_question,
    generate_static_skill_question,
    generate_word_structure_question,
)
