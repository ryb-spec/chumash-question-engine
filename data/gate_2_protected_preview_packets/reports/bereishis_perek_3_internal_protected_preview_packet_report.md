# Bereishis Perek 3 Internal Protected-Preview Packet Report

## Packet purpose

This is an internal protected-preview packet only. It is not runtime content, not reviewed-bank content, and not student-facing content.

The packet contains only the four Bereishis Perek 3 candidates that Yossi explicitly approved for an internal protected-preview packet. Every item still requires internal/post-preview review before any broader use.

## Source files

- Candidate TSV: `data/gate_2_protected_preview_candidates/bereishis_perek_3_protected_preview_candidates.tsv`
- Applied-decision report: `data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_protected_preview_candidate_yossi_review_applied.md`
- Perek 3 status index: `data/gate_2_protected_preview_candidates/reports/bereishis_perek_3_candidate_status_index.md`

## Included candidate IDs

- `g2ppcand_p3_003` / Bereishis 3:1 / עֵץ
- `g2ppcand_p3_004` / Bereishis 3:2 / עֵץ
- `g2ppcand_p3_007` / Bereishis 3:7 / עֲלֵה
- `g2ppcand_p3_008` / Bereishis 3:7 / תְאֵנָה

## Included packet items

| Packet item ID | Candidate ID | Ref | Hebrew token | Hebrew phrase | Skill family | Review status | Gates |
|---|---|---|---|---|---|---|---|
| `g2ppacket_p3_001` | `g2ppcand_p3_003` | Bereishis 3:1 | עֵץ | לֹא תֹאכְלוּ מִכֹּל עֵץ הַגָּן | `basic_noun_recognition` | `needs_internal_review` | `runtime=false; reviewed_bank=false; student_facing=false` |
| `g2ppacket_p3_002` | `g2ppcand_p3_004` | Bereishis 3:2 | עֵץ | מִפְּרִי עֵץ הַגָּן נֹאכֵל | `basic_noun_recognition` | `needs_internal_review` | `runtime=false; reviewed_bank=false; student_facing=false` |
| `g2ppacket_p3_003` | `g2ppcand_p3_007` | Bereishis 3:7 | עֲלֵה | וַיִּתְפְּרוּ עֲלֵה תְאֵנָה | `basic_noun_recognition` | `needs_internal_review` | `runtime=false; reviewed_bank=false; student_facing=false` |
| `g2ppacket_p3_004` | `g2ppcand_p3_008` | Bereishis 3:7 | תְאֵנָה | וַיִּתְפְּרוּ עֲלֵה תְאֵנָה | `basic_noun_recognition` | `needs_internal_review` | `runtime=false; reviewed_bank=false; student_facing=false` |

## Explicit excluded groups

- All 4 `approve_with_revision` items are excluded: `g2ppcand_p3_001`, `g2ppcand_p3_005`, `g2ppcand_p3_009`, `g2ppcand_p3_010`.
- All 2 `needs_follow_up` items are excluded: `g2ppcand_p3_002`, `g2ppcand_p3_006`.
- `source_only` rows excluded: 0 confirmed.
- `reject_for_preview` rows excluded: 0 confirmed.

## Decision counts

- Included approved rows: 4
- Excluded revision rows: 4
- Excluded follow-up rows: 2
- Rejected rows: 0
- Source-only rows: 0

## Safety boundary confirmation

- No runtime activation.
- No Perek 3 runtime activation.
- No reviewed-bank promotion.
- No student-facing content.
- No scoring, mastery, UI, runtime, or dynamic generation changes.
- Runtime, reviewed-bank, and student-facing gates remain `false` for every packet row.

## Validation notes

- `scripts/validate_gate_2_protected_preview_packet.py` enforces the exact four-ID Perek 3 packet set.
- `tests/test_gate_2_protected_preview_packet.py` verifies the Perek 3 row count, exact candidate IDs, exclusions, and closed gates.
- Validation is fail-closed: any extra, missing, revision, follow-up, source-only, or rejected candidate ID causes packet validation to fail.
