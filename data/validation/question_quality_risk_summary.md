# Question quality risk summary

This report uses existing audit evidence only. It does not change runtime behavior, question generators, or validation thresholds.

## Key risk metrics

- Translation/context safe-valid rate: 223 / 1109 (20.1%)
- Suffix safe-valid rate: 94 / 258 (36.4%)

## Top rejection reasons

- `placeholder_translation`
- `low_instructional_value`
- `grammatical_particle`
- `compound_morphology`
- `no_clear_suffix`
- `lexical_plural_ending`

## Recommendation categories

- safe_reviewed_lanes: basic_noun_recognition where reviewed
- teacher_review_required: translation/context, suffix forms, shoresh pools, phrase translation
- engineering_review_required: runtime exposure reporting, standards evidence dashboard
- do_not_expand_yet: vav hahipuch, advanced verb forms, Rashi/commentary, higher-order inference
