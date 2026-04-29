# Bereishis Perek 3 Protected-Preview Candidate Yossi Review Applied

## Purpose

This report records Yossi's decisions for the Bereishis Perek 3 Gate 2 protected-preview candidate review layer. The decisions were applied to the candidate TSV, but this is still not a final/internal protected-preview packet task.

## Decision Application Statement

Yossi decisions were applied to the 10 Bereishis Perek 3 protected-preview candidate rows. Runtime, reviewed-bank, protected-preview packet, and student-facing gates remain closed.

## Decision Summary Counts

- Total candidates reviewed: 10
- `approve_for_internal_protected_preview_packet`: 4
- `approve_with_revision`: 4
- `needs_follow_up`: 2
- `reject_for_preview`: 0
- `source_only`: 0

## Candidate Status Counts

- `yossi_approved_for_internal_protected_preview_packet`: 4
- `yossi_approved_with_revision_before_internal_protected_preview_packet`: 4
- `needs_follow_up`: 2

## Per-Candidate Decision Table

| Candidate ID | Ref | Hebrew token | Decision | Candidate status | Exact Yossi note |
|---|---|---|---|---|---|
| `g2ppcand_p3_001` | Bereishis 3:1 | וְהַנָּחָשׁ | `approve_with_revision` | `yossi_approved_with_revision_before_internal_protected_preview_packet` | Good noun candidate, but revise future wording to normalize/target the base noun נחש, not the prefixed/article form וְהַנָּחָשׁ. Keep item limited to noun recognition only. |
| `g2ppcand_p3_002` | Bereishis 3:1 | חַיַּת | `needs_follow_up` | `needs_follow_up` | Construct form חַיַּת is risky for first-layer noun recognition. Needs follow-up because it may confuse noun recognition with construct/phrase translation. |
| `g2ppcand_p3_003` | Bereishis 3:1 | עֵץ | `approve_for_internal_protected_preview_packet` | `yossi_approved_for_internal_protected_preview_packet` | Clean simple noun-recognition candidate. Keep target limited to עֵץ. |
| `g2ppcand_p3_004` | Bereishis 3:2 | עֵץ | `approve_for_internal_protected_preview_packet` | `yossi_approved_for_internal_protected_preview_packet` | Clean repeated noun-recognition candidate. Acceptable if later packet avoids overuse/repetition. |
| `g2ppcand_p3_005` | Bereishis 3:3 | הָעֵץ | `approve_with_revision` | `yossi_approved_with_revision_before_internal_protected_preview_packet` | Good noun candidate, but surface form includes article. Future wording should target the base noun עץ, not article recognition. |
| `g2ppcand_p3_006` | Bereishis 3:6 | מִפִּרְיוֹ | `needs_follow_up` | `needs_follow_up` | Too morphologically loaded for first-layer noun recognition because it includes prefix + noun + suffix. Do not use for suffix decoding without a later gate. |
| `g2ppcand_p3_007` | Bereishis 3:7 | עֲלֵה | `approve_for_internal_protected_preview_packet` | `yossi_approved_for_internal_protected_preview_packet` | Clean noun-recognition candidate. Keep target limited to עֲלֵה. |
| `g2ppcand_p3_008` | Bereishis 3:7 | תְאֵנָה | `approve_for_internal_protected_preview_packet` | `yossi_approved_for_internal_protected_preview_packet` | Good concrete noun candidate. Keep target limited to תְאֵנָה and confirm later wording is school-appropriate. |
| `g2ppcand_p3_009` | Bereishis 3:8 | קוֹל | `approve_with_revision` | `yossi_approved_with_revision_before_internal_protected_preview_packet` | Good noun candidate, but phrase contains שם ה'. Future wording must be careful and avoid full phrase translation. |
| `g2ppcand_p3_010` | Bereishis 3:9 | הָאָדָם | `approve_with_revision` | `yossi_approved_with_revision_before_internal_protected_preview_packet` | Good noun/person-label candidate, but surface form includes article. Future wording should target אדם and not article/prefix recognition. |

## Approved for a Later Internal Protected-Preview Packet Task Only

- `g2ppcand_p3_003` / Bereishis 3:1 / עֵץ: Clean simple noun-recognition candidate. Keep target limited to עֵץ.
- `g2ppcand_p3_004` / Bereishis 3:2 / עֵץ: Clean repeated noun-recognition candidate. Acceptable if later packet avoids overuse/repetition.
- `g2ppcand_p3_007` / Bereishis 3:7 / עֲלֵה: Clean noun-recognition candidate. Keep target limited to עֲלֵה.
- `g2ppcand_p3_008` / Bereishis 3:7 / תְאֵנָה: Good concrete noun candidate. Keep target limited to תְאֵנָה and confirm later wording is school-appropriate.

## Approved With Revision Before Any Later Packet Task

- `g2ppcand_p3_001` / Bereishis 3:1 / וְהַנָּחָשׁ: Good noun candidate, but revise future wording to normalize/target the base noun נחש, not the prefixed/article form וְהַנָּחָשׁ. Keep item limited to noun recognition only.
- `g2ppcand_p3_005` / Bereishis 3:3 / הָעֵץ: Good noun candidate, but surface form includes article. Future wording should target the base noun עץ, not article recognition.
- `g2ppcand_p3_009` / Bereishis 3:8 / קוֹל: Good noun candidate, but phrase contains שם ה'. Future wording must be careful and avoid full phrase translation.
- `g2ppcand_p3_010` / Bereishis 3:9 / הָאָדָם: Good noun/person-label candidate, but surface form includes article. Future wording should target אדם and not article/prefix recognition.

## Needs Follow-Up

- `g2ppcand_p3_002` / Bereishis 3:1 / חַיַּת: Construct form חַיַּת is risky for first-layer noun recognition. Needs follow-up because it may confuse noun recognition with construct/phrase translation.
- `g2ppcand_p3_006` / Bereishis 3:6 / מִפִּרְיוֹ: Too morphologically loaded for first-layer noun recognition because it includes prefix + noun + suffix. Do not use for suffix decoding without a later gate.

## Safety Boundaries

- This is not runtime approval.
- This is not reviewed-bank approval.
- This is not student-facing approval.
- This is not broad protected-preview release approval.
- No final protected-preview packet was created.
- `protected_preview_allowed` remains `false`.
- `reviewed_bank_allowed` remains `false`.
- `runtime_allowed` remains `false`.
- `student_facing_allowed` remains `false`.

## What Was Not Approved

No Perek 3 candidate was approved for reviewed-bank use, runtime use, student-facing use, or broad protected-preview release use. Revision and follow-up rows are not eligible for any later packet task until the required review/revision work is completed.

## Next Step

A later task may generate an internal protected-preview packet only from explicitly approved Perek 3 candidates, and only if all validators pass. That later packet task must continue to keep reviewed-bank, runtime, and student-facing gates closed.
