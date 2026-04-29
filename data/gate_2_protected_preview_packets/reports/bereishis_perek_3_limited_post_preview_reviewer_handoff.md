# Bereishis Perek 3 limited post-preview reviewer handoff

## Purpose

This is an internal reviewer handoff packet for the three Bereishis Perek 3 items that are ready for limited post-preview iteration.

- Internal reviewer handoff only.
- Not runtime.
- Not reviewed bank.
- Not student-facing.
- Does not apply decisions.
- Does not revise items.
- Does not activate or promote content.

## Source files

- Readiness report: `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_iteration_readiness.md`
- Readiness TSV: `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_iteration_readiness.tsv`
- Blocked register: `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_blocked_from_broader_use_register.md`
- Observation template: `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_template.tsv`
- Applied review decisions report: `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_internal_protected_preview_review_decisions_applied.md`
- Original packet report: `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_internal_protected_preview_packet_report.md`

## Included active review items

These are the only active items in this limited reviewer handoff:

- `g2ppacket_p3_001` / `g2ppcand_p3_003` / Bereishis 3:1 / `עֵץ`
- `g2ppacket_p3_003` / `g2ppcand_p3_007` / Bereishis 3:7 / `עֲלֵה`
- `g2ppacket_p3_004` / `g2ppcand_p3_008` / Bereishis 3:7 / `תְאֵנָה`

## Blocked item warning

`g2ppacket_p3_002` / `g2ppcand_p3_004` / Bereishis 3:2 / `עֵץ` is blocked and should not be used in this limited review lane.

- It remains blocked because it duplicates the same target word `עֵץ` and the same prompt pattern as `g2ppcand_p3_003`.
- It is not rejected.
- It is not revised.
- It requires future spacing metadata, wording/wrapping revision, or a replacement/revision task before broader use.

## Reviewer instructions

For each active item, the reviewer should look for:

- Prompt clarity.
- Hebrew token clarity.
- Whether "type of word" is understandable.
- Whether noun recognition is actually what is being tested.
- Answer choice fairness.
- Explanation accuracy.
- Whether the item feels too easy, too repetitive, or confusing.
- Whether any item accidentally becomes translation/context testing.

## Observation instructions

Use `data/gate_2_protected_preview_packets/reports/bereishis_perek_3_limited_post_preview_observation_template.tsv` to record real post-iteration observations later.

Observation fields must remain blank until real observations are recorded.

## Next possible decisions after observation

These are possible later observation decisions, not decisions applied by this handoff packet:

- `keep_limited_iteration`
- `revise_before_next_iteration`
- `needs_follow_up`
- `reject_for_broader_use`
- `candidate_for_future_reviewed_bank_consideration`

These decisions are not applied by this handoff packet.

## Item review cards

### g2ppacket_p3_001 / g2ppcand_p3_003

- Ref: Bereishis 3:1
- Hebrew token: `עֵץ`
- Hebrew phrase: `לֹא תֹאכְלוּ מִכֹּל עֵץ הַגָּן`
- Prompt/question: What type of word is עֵץ?
- Answer choices: noun | action word | describing word | prefix
- Expected answer: noun
- Explanation: Review-only candidate: עֵץ is proposed as a basic noun-recognition item based on verified Bereishis Perek 3 source mapping. Yossi/teacher review is required before any later draft or preview use.
- Skill family: basic_noun_recognition
- Review focus: Confirm the prompt is clear, the token is displayed accurately, the answer choices are fair, and the item remains noun recognition rather than translation/context testing.

### g2ppacket_p3_003 / g2ppcand_p3_007

- Ref: Bereishis 3:7
- Hebrew token: `עֲלֵה`
- Hebrew phrase: `וַיִּתְפְּרוּ עֲלֵה תְאֵנָה`
- Prompt/question: What type of word is עֲלֵה?
- Answer choices: noun | action word | describing word | prefix
- Expected answer: noun
- Explanation: Review-only candidate: עֲלֵה is proposed as a basic noun-recognition item based on verified Bereishis Perek 3 source mapping. Yossi/teacher review is required before any later draft or preview use.
- Skill family: basic_noun_recognition
- Review focus: Confirm the item works as a clear concrete-noun target and that the nearby `תְאֵנָה` phrase context does not turn it into phrase translation.

### g2ppacket_p3_004 / g2ppcand_p3_008

- Ref: Bereishis 3:7
- Hebrew token: `תְאֵנָה`
- Hebrew phrase: `וַיִּתְפְּרוּ עֲלֵה תְאֵנָה`
- Prompt/question: What type of word is תְאֵנָה?
- Answer choices: noun | action word | describing word | prefix
- Expected answer: noun
- Explanation: Review-only candidate: תְאֵנָה is proposed as a basic noun-recognition item based on verified Bereishis Perek 3 source mapping. Yossi/teacher review is required before any later draft or preview use.
- Skill family: basic_noun_recognition
- Review focus: Confirm the item stays focused on noun recognition and that the paired `עֲלֵה` / `תְאֵנָה` context is helpful rather than confusing.

## Safety boundary confirmation

- No runtime activation.
- No Perek 3 runtime activation.
- No reviewed-bank promotion.
- No protected-preview packet creation.
- No student-facing content creation.
- No item content revision.
- No runtime/UI/scoring/mastery/assessment-flow changes.
