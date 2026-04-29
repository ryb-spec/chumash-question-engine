# Bereishis Perek 3 Item 004 Revision Plan

## Purpose

This is a planning artifact only.

- It does not revise the item.
- It does not apply a new decision.
- It does not activate runtime.
- It does not promote reviewed-bank content.
- It does not create student-facing content.

## Source status

- Item: `g2ppacket_p3_002`
- Candidate: `g2ppcand_p3_004`
- Ref: Bereishis 3:2
- Token: עֵץ
- Current decision: `approve_with_revision`
- Current gate state: runtime=false, reviewed_bank=false, student_facing=false

## Revision problem

- repetition/session-balance concern.
- Same target word עֵץ as `g2ppcand_p3_003`.
- Same prompt pattern: "What type of word is עֵץ?"
- Risk: in a 4-item packet, this may feel like duplicate practice rather than meaningful evidence.

## Allowed revision paths

1. Keep both עֵץ items but require session-spacing metadata so they are not served together.
2. Keep `g2ppcand_p3_004` as source evidence only until a broader noun-recognition packet needs repeated target-word checks.
3. Revise future usage/wrapping so the second עֵץ item tests recognition in a different controlled context without changing the protected packet item yet.
4. Replace the item only in a future explicit replacement task, using a different approved candidate/source-backed noun, if available.

## Recommended path

Do not rewrite the current packet item yet. Keep g2ppcand_p3_004 broader use blocked pending either session-spacing metadata or a future replacement/revision task. Keep it available only as internal evidence that עֵץ appears as a simple noun in Bereishis 3:2.

## Required future acceptance criteria

- It must no longer create an unbalanced duplicate עֵץ experience with g2ppcand_p3_003.
- A future revision must state whether the fix is spacing, wording/wrapping, or replacement.
- All source/provenance fields must remain intact.
- runtime_allowed must remain false unless a later explicit runtime task changes it.
- reviewed_bank_allowed must remain false unless a later explicit reviewed-bank task changes it.
- student_facing_allowed must remain false unless a later explicit student-facing approval task changes it.

## Safety boundary confirmation

- No item content revision.
- No runtime activation.
- No Perek 3 runtime activation.
- No reviewed-bank promotion.
- No protected-preview packet creation.
- No student-facing content creation.
- No runtime/UI/scoring/mastery/assessment-flow changes.
