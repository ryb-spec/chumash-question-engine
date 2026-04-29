# Bereishis Perek 4 duplicate/session-balance warnings

This report is required because the Perek 3 protected-preview layer surfaced a duplicate עֵץ/session-balance problem after packet creation. Perek 4 records duplicate-token and small-packet balance risks during source discovery, before any protected-preview packet exists.

## Warning summary

| Warning ID | Hebrew token | Related candidate IDs | Warning | Future spacing note |
|---|---|---|---|---|
| `p4dup_001` | אֲדָמָה | `g2srcdisc_p4_003` | repeated Hebrew target token cluster | Do not place multiple אֲדָמָה noun-recognition items in the same small packet without teacher-reviewed spacing rationale. |
| `p4dup_002` | מִנְחָה | `g2srcdisc_p4_004` | repeated token with nearby suffix forms | Use at most one minchah-form item in a small packet until teacher review. |
| `p4dup_003` | קַיִן | `not_in_safe_inventory` | repeated name cluster | Excluded from current basic noun-recognition inventory. |
| `p4dup_004` | הֶבֶל | `not_in_safe_inventory` | repeated name cluster | Excluded from current basic noun-recognition inventory. |

## Packet-planning implication

No Perek 4 protected-preview packet was created by this task. If a later task plans a small packet, it must use this warning report to avoid repeating the Perek 3 duplicate-token/session-balance issue.

## Safety boundary confirmation

- No runtime activation.
- No reviewed-bank promotion.
- No protected-preview packet creation.
- No student-facing content.
