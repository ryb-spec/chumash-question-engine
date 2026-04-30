# Perek 4 Limited Protected-Preview Build Gate

## Purpose

Build the bounded Perek 4 limited protected-preview candidate packet from the Content Expansion Planning Gate V1 recommendation without activating runtime content.

## Source planning basis

- `data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.md`
- `data/pipeline_rounds/content_expansion_planning_gate_2026_04_30.json`
- `data/content_expansion_planning/content_expansion_candidate_plan_2026_04_30.json`
- `data/content_expansion_planning/content_expansion_inventory_2026_04_30.json`

Primary candidate: `cepg_primary_bereishis_perek_4_limited_protected_preview_build`.

## Packet created

Created a two-item limited protected-preview build packet:

- `g2srcdisc_p4_001` / אִישׁ / Bereishis 4:1
- `g2srcdisc_p4_002` / צֹאן / Bereishis 4:2

These two items come from the existing Perek 4 two-item limited internal packet iteration and are ready for the next bounded protected-preview build layer only.

## Selected item cards

### g2srcdisc_p4_001 / אִישׁ

- Pasuk: Bereishis 4:1
- Question: In this phrase, what type of word is אִישׁ?
- Expected answer: noun
- Distractors: verb, adjective, prefix
- Prior internal decision: approve_for_later_packet_iteration
- Build gate status: limited_protected_preview_build_ready
- Runtime allowed: false
- Reviewed-bank allowed: false
- Student-facing allowed: false

### g2srcdisc_p4_002 / צֹאן

- Pasuk: Bereishis 4:2
- Question: What type of word is צֹאן?
- Expected answer: noun
- Distractors: verb, adjective, prefix
- Prior internal decision: approve_for_later_packet_iteration
- Build gate status: limited_protected_preview_build_ready
- Runtime allowed: false
- Reviewed-bank allowed: false
- Student-facing allowed: false

## Revision-watch items preserved

- `g2srcdisc_p4_003` / אֲדָמָה: preserve spacing/session-balance note; do not place close to similar noun-recognition items.
- `g2srcdisc_p4_004` / מִנְחָה: keep strictly part-of-speech only; preserve Minchah/offering alias review and spacing/session-balance warning.

## Blockers preserved

- Protected preview is not reviewed bank.
- Teacher/internal review artifacts do not authorize runtime activation.
- Extraction verification does not mean question approval.
- No Perek 4 runtime activation is authorized by this build gate.

## Next gate

The next safe step is bounded teacher review/observation of this two-item Perek 4 protected-preview build packet. Any reviewed-bank promotion or runtime activation requires a separate explicit gate.

## Safety confirmation

- runtime scope widened: no
- Perek activated: no
- reviewed-bank promoted: no
- runtime content promoted: no
- student-facing content created: no
- scoring/mastery changed: no
- question generation changed: no
- question-selection changed: no
- Runtime Learning Intelligence weighting changed: no
- source truth changed: no
- fake teacher approval created: no
- fake student data created: no
- raw logs exposed: no
- validators weakened: no
