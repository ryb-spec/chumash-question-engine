# Bereishis Hebrew Source Reconciliation Report

- Status: `reconciled`
- Key finding: the canonical Hebrew TSV had one extra misnumbered row labeled `Bereishis 35:30`
- Top blocker: resolved
- Recommended next action: rerun the Sefaria English translation pipeline against the corrected `1533`-ref canonical backbone

## Scope

- Source file audited: `data/source_texts/bereishis_hebrew_menukad_taamim.tsv`
- Suspicious ref: `Bereishis 35:30`
- Comparison source used to confirm chapter count: Sefaria API, Hebrew `Miqra according to the Masorah`

## Counts

- Original total row count: `1534`
- Corrected total row count: `1533`
- Original Genesis 35 row count: `30`
- Corrected Genesis 35 row count: `29`
- Original final Genesis 35 ref: `Bereishis 35:30`
- Corrected final Genesis 35 ref: `Bereishis 35:29`

## Suspicious row preserved

- Original row label: `Bereishis 35:30`
- Original source URL: `https://www.sefaria.org/Genesis.35.30?lang=he&aliyot=0`
- Original row text:

```text
וַיִּגְוַ֨ע יִצְחָ֤ק וַיָּ֙מׇת֙ וַיֵּאָ֣סֶף אֶל־עַמָּ֔יו זָקֵ֖ן וּשְׂבַ֣ע יָמִ֑ים וַיִּקְבְּר֣וּ אֹת֔וֹ עֵשָׂ֥ו וְיַעֲקֹ֖ב בָּנָֽיו׃
```

## Evidence

### Local canonical TSV before correction

- `Bereishis 35:27` existed
- `Bereishis 35:28` existed
- `Bereishis 35:29` existed
- `Bereishis 35:30` existed
- `Bereishis 36:1` followed immediately after

### Sefaria Hebrew API confirmation

- Endpoint family: `https://www.sefaria.org/api/v3/texts/Genesis.35`
- Requested version: `hebrew|Miqra according to the Masorah`
- `return_format=text_only`
- `fill_in_missing_segments=0`
- Returned verse count for Genesis 35: `29`
- Returned verse 29 text matched the suspicious local `Bereishis 35:30` row exactly
- Returned verse count for Genesis 36: `43`

## Decision

- Decision made: `remove invalid extra row`
- Reason:
  - the local `Bereishis 35:30` row was not a distinct additional pasuk
  - its Hebrew text matched Sefaria’s Genesis 35 verse 29
  - both Koren and Metsudah English pipelines also stopped chapter 35 at verse 29
  - leaving the extra row in place would force an artificial missing translation ref that does not exist in the aligned Sefaria source set

## Canonical file change

- Canonical Hebrew TSV changed: `true`
- Type of change: `removed one extra misnumbered row`
- English translation files need regeneration: `true`

## Outcome

- Corrected canonical total rows: `1533`
- Corrected chapter 35 rows: `29`
- No `Bereishis 35:30` row remains in the canonical TSV
- The translation pipeline should now align cleanly to `1533` canonical refs

## Next branch recommendation

- `feature/source-bereishis-english-translations-sefaria`
