# Team zasa research presentation

An eight-slide Traditional Chinese oral presentation integrating MS-01, MS-02 and MS-03. It uses completed research, existing data and conservative candidate dispositions; it adds no sites or scientific analysis.

- [PowerPoint deck](team_zasa_research.pptx): editable slide text, four native tables, scientific images and eight embedded speaker-notes pages.
- [PDF deck](team_zasa_research.pdf): eight pages, converted from the validated PPTX with selectable Chinese text.
- [Speaker notes and full source links](../../../docs/integration/presentation/speaker_notes.md).
- [Figure index](figure_index.csv): sources, fixed commits, periods, units, spatial support, processing and limits.
- [Manifest](manifest.json): starting main SHA, verified PR heads, copied-input hashes, export method and outstanding confirmations.
- [Validation record](validation.json): actual structural checks and individual PDF-page visual review.
- [Production instructions](../../../docs/integration/presentation/README.md).

## Research inputs

| Input | PR | Verified head |
|---|---|---|
| MS-01 | [#8](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/8) | `b4b6929e890018668ef4faa9a74128a4ce5aa8df` |
| MS-02 | [#6](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/6) | `38b8fa0dea527b1cc47aeb02dc260e039da37122` |
| MS-03 | [#7](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/7) | `8fa07afac4a98096958880f6a5ece16f35abc4db` |

Starting `origin/main`: `3cc8488577535e2fa4d146021fde51f8ff6cc667`. MS-03 advanced beyond the initially supplied head; its latest evidence and downgrade are retained. PR #6 targets `handoff/verified-data-20261114`; reading its pinned files does not merge that branch. These research PRs were open at the version check; the deck does not represent them as merged or finally accepted on main.

## What was produced

1. Research question and selection purpose.
2. Three fixed Mars cells and four distinct data themes.
3. University Valley thermal-response evidence for MS-01.
4. Supported MS-02 use and the non-colocation problem in Adventdalen.
5. MS-03 image observability and AD1 downgrade; morphology remains unknown.
6. Prior work versus the team's reproducible QA and applicability checks.
7. Dispositions, common limitations and missing evidence.
8. Currently supported value and proposed validation needs.

F01 replots four already delivered thermal-amplitude ratios and leave-one-day-out ranges. F02 is a native evidence-support table using existing findings. F03 replots delivered catalogue corner footprints and displays the existing processed CTX patch unchanged. No model refitting, time alignment, new image interpretation or GIS intersection was performed. No generative research imagery was used.

## Checks actually completed

All eight PPTX slides were rendered by Artifact Tool; the PPTX package was validated and reimported. Four native tables and eight notes parts were checked. The PDF was converted with LibreOffice, all eight pages were rendered with Poppler and individually inspected, and Chinese text/source footers were extracted from every page. The CSV parses and its figure IDs are unique. Initial missing-font and synthesized-bold rendering problems were repaired before delivery. Native Microsoft PowerPoint UI operation was not tested.

## Pending confirmations

- This is the requested **eight-page presentation**, not a claim of compliance with the official submission page limit. If the seven-page requirement is confirmed, the final submission needs compression.
- UV S/D coordinate versions and historical logger/export timing remain unresolved. No Campbell–HOBO pairing or cross-instrument phase inference is made.
- Adventdalen radar-line location and independent trough ice truth are missing; the radar evidence is abstract-level.
- MS-03 morphology remains unknown. Catalogue coverage does not establish usable pixels, and unresolved imagery does not establish absence.
- There is no local independent ice-depth, ice-content or resource validation for these Mars cells.

Third-party material retains its source terms. The figure index preserves CC0 UV data, CC BY 4.0 AD1 GIS attribution, and NASA/JPL/MSSS CTX credit. This delivery does not impose a blanket license on third-party sources or change the team's pending software-license decision.
