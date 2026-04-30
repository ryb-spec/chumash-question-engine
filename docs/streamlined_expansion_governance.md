# Streamlined Expansion Governance

The Chumash bank should expand quickly, but each expansion layer has its own gate.

The default direction is horizontal first: more pesukim and more perakim. Vertical depth is allowed only when the base word has already earned the required review and observation evidence. Discovery may run ahead into future perakim, but activation may not run ahead.

## Content Layers

- `perek_based_bank`: per-perek source, vocabulary, and candidate inventory.
- `skill_based_bank`: skill-organized deepening on already-approved words.
- `reviewed_bank_content_layer`: content approved through reviewed-bank governance.
- `runtime_active_subset`: the smallest safe subset allowed in supported runtime.

## Approval Ladder

Items move through the ladder in order:

`planning_only` -> `word_level_candidate` -> `word_level_approved` -> `simple_question_candidate` -> `teacher_review_ready` -> `teacher_approved` -> `protected_preview_ready` -> `observed_internally` -> `reviewed_bank_candidate` -> `reviewed_bank_approved` -> `runtime_ready` -> `runtime_active`

The important separation is intentional: a word can be approved as a word without being approved as a question, and a reviewed question can remain outside runtime.

## Depth Rule

Stage 1 single-word vocabulary can begin with word-level review. Stage 2 and deeper skills require base-word approval, question review or teacher approval, and internal observation. Rashi or deeper pshat remains late-stage work and is not default expansion.

## Planning-Only Rule

Future-perek discovery files may exist, including Perek 5/6 planning while Perek 4 continues reviewed-bank work. Those files must default to planning-only and keep runtime, protected-preview, reviewed-bank, and runtime-active flags closed unless a later explicit gate changes them.

## Review Packet Rule

Review packets must declare a type: `word_bank_review`, `simple_question_review`, `depth_expansion_review`, `protected_preview_observation`, or `reviewed_bank_decision`. Mixed packets need an explicit exception, explanation, separated decision fields, and closed runtime/promotion gates.

Machine-readable contract:

- `../data/expansion_governance/streamlined_expansion_contract.json`
