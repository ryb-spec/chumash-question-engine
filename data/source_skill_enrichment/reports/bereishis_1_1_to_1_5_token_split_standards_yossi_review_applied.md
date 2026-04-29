# Bereishis 1:1-1:5 Token-Split Standards Yossi Review Applied

## Summary

- total token-split candidates reviewed: 10
- verified candidates: 7
- needs_follow_up candidates: 3
- parent bundled rows preserved unresolved: yes
- Hebrew rendering check result: token-split TSV and CSV were corrected to real UTF-8 Hebrew tokens, and the Markdown review sheet was regenerated from the corrected review artifacts.
- safety gates confirmed closed: yes
- what was not approved: `????`, `???`, and prefixed `?` remain follow-up only; parent phrase-level rows remain unresolved and unverified.

## Decisions Applied

- `stdtok_b1_1_r002_t001` | ברא | `verified` | Yossi approved token-level 3.02 / ROOT.IDENTIFY for ברא only; the parent phrase remains unresolved.
- `stdtok_b1_1_r003_t001` | את | `verified` | Yossi approved token-level direct-object-marker mapping for את under 3.03 / PARTICLE.DIRECT_OBJECT_MARKER.
- `stdtok_b1_1_r003_t002` | שמים | `needs_follow_up` | Yossi kept שמים as follow-up until stronger noun-vocabulary evidence is linked.
- `stdtok_b1_1_r003_t003` | את | `verified` | Yossi approved token-level direct-object-marker mapping for את from surface ואת; conjunction handling remains separate.
- `stdtok_b1_1_r003_t004` | ארץ | `verified` | Yossi approved token-level 3.01 / WORD.MEANING_BASIC for base noun ארץ.
- `stdtok_b1_3_r013_t001` | יהי | `needs_follow_up` | Yossi kept יהי follow-up pending stronger morphology / verb-form evidence.
- `stdtok_b1_3_r013_t002` | אור | `verified` | Yossi approved token-level 3.01 / WORD.MEANING_BASIC for אור.
- `stdtok_b1_5_r020_t001` | אור | `verified` | Yossi approved base אור from לאור as 3.01 / WORD.MEANING_BASIC only; prefixed ל remains separate.
- `stdtok_b1_5_r020_t002` | יום | `verified` | Yossi approved token-level 3.01 / WORD.MEANING_BASIC for יום.
- `stdtok_b1_5_r020_t003` | ל | `needs_follow_up` | Yossi kept prefixed ל follow-up pending stronger 3.06 prefix/preposition evidence.

## Safety Reminder

- This applied review is standards enrichment only. It is not question approval, not protected-preview approval, not reviewed-bank approval, not runtime approval, and not student-facing approval.
- No source-to-skill map rows were changed.
- All token-split candidates kept `question_allowed=needs_review`, `protected_preview_allowed=false`, `reviewed_bank_allowed=false`, and `runtime_allowed=false`.