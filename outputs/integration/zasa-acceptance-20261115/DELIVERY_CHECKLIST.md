# TerraMatch / ZASA — delivery checklist

This checklist is a technical handoff. It is not the team-authored report or presentation, an award-eligibility determination, or a submitted-project receipt.

## Submission fields and sources

| Official field | Verified entry or remaining action |
|---|---|
| Project title | TerraMatch |
| Final Project | https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev/ |
| Project Demo | https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev/demo (24 seconds; no login) |
| Summary and detailed description | Team supplies/approves its own text. Do not state that the three regions contain verified ice or that three new terrestrial analog matches were established. |
| NASA data and other references | Cite the sources actually used, including the exact display sources below, plus any additional analysis data and tools actually included in the submission. Use the repository's [data attribution inventory](../../../DATA_LICENSES.md) and primary-source manifests as cross-checks, not a replacement for the form. |
| AI/SI tools | Disclose the tools the team actually used and their roles. |
| Terms and Submit | Team owner and, as applicable, parent/guardian review the terms and rights, verify the actual form, and submit. Save the confirmation screen or the official receipt if provided. No receipt was found in the mailbox check; portal status through the team's account was not verified. |

- NASA MGS MOLA digital elevation data: [NASA PDS MEGDR](https://doi.org/10.17189/1519460); separate [NASA Ames MOLA map image](https://marsoweb.nas.nasa.gov/globalData/datamaps.html) resized for display.
- NASA MGS TES: [PDS TES TIMAP](https://pds-geosciences.wustl.edu/missions/mgs/tes-timap.html), nighttime thermal inertia and interpolation mask (`global_ti_night_2007.img`, `global_ti_msk_night_2007.img`).
- NASA-funded PSI SWIM 2.0: [SWIM products](https://swim.psi.edu/SWIM2Products.php), `SWIM2_c0_1.tif`. The index can be negative; 0–1 m is the depth interval, not the range of the index. Full downloads from the provider were not verified in this pass.
- Conditional model: [Piqueux et al. archive](https://doi.org/10.22002/D1.1316). Earth methods: [University Valley](https://zenodo.org/records/10553882), [Haughton](https://doi.org/10.1029/2012JE004053); DOI resolves, but Wiley returned HTTP 403 when opening the latter in one test.

[Organizer field checklist](https://github.com/nasa/spaceapps/discussions/1858) · [Demo requirements](https://github.com/nasa/spaceapps/discussions/1991) · [Global Awards resource rule](https://github.com/nasa/spaceapps/discussions/1827) · [Challenge Resources tab](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources) · [2026 terms](https://www.spaceappschallenge.org/legal/). The official Resources list could not be read in this check; confirmed use of MOLA does not itself establish a match to the challenge-specific list. Under the published terms, absent a specified OSI-compliant license NASA uses Apache 2.0 for original content in posted Solutions. This checklist does not grant rights, change the project's license, or expose the private repository.

## Research and site cross-check

Pinned originals (unchanged): [MS-01](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/89e448dcf083f3d3dd3cdf9f8dababc020ebef5f/docs/research/MS-01/report.md), [MS-02](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/89e448dcf083f3d3dd3cdf9f8dababc020ebef5f/docs/research/MS-02/report.md), [MS-03](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/89e448dcf083f3d3dd3cdf9f8dababc020ebef5f/docs/research/MS-03/report.md). See the [integrated data and evidence index](README.md), [published Earth handoff and source boundaries](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/bd290759a80d40227fa1aab0b99e7b68edd4cc3b/docs/earth-source-handoff/README.md), and [current public R4 showcase receipt](web/r4/RECEIPT.md). The site is a scoped public demonstration, not a publication of all analyses, original data or private reports.

Across the three records, 18 source values (coordinates and four displayed measures per record) were checked against the candidate/model snapshots. The browser displays rounded card values; source tables retain full precision. This audit does not certify that every cited source is currently downloadable. The pre-audit GitHub Cloudflare Workers Builds check remains red; the separate production release is verified independently by public readback, not by that status.

## Current data handoff

- Main contains the [23,035,176-byte integrated workbook](../../consolidated/NASA_Space_Apps_2026_All_Data.xlsx) and [7,702,846-byte full screening output](../../research/mars_reselection_20261114/screened_pool.csv.gz). Older local-only notices are historical.
- [Historical handoff snapshot](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/tree/108cbe9808f4d085497341ebf44750d71539cee7/archive/project_assets_20261114) lists 186 records: 185 payload files and one source-only reference.
- [Private Earth-input release](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/releases/tag/earth-raw-inputs-2026-11-14) contains 221 NASA raw inputs and three handoff files. The one ESA CCI item in that 222-input inventory remains provider-link-only by design. This is not a claim that every project raw input has been mirrored.

## Recorded scientific limits

- The evidence snapshots and source-mapped live view are separate from the original reports. MS-02 #22/#25 merged; #26 accepted evidence went into main independently without replacing the original MS-03 report. #27 remains a draft supporting archive; its 32 unique file paths are not merged and its older status language must not be treated as current.
- Unknown across all three Mars boxes: actual ice depth, fraction, recoverable amount. The heat-model interface depths are conditional, not ice ground truth; SWIM consistency is not concentration, probability or reserve.
- Clock and deployments: fixed-window same-recorder phase results can be reproduced, but original clocks, logger identities/synchronization and certain deployment details remain unverified. Do not infer them.
- Historical artifacts: record unavailable source tables/control settings by identity; labels and DOI metadata do not substitute for original observations or executable replay. Only reopen upon genuine new primary artifacts.
- Novelty: known precedents are documented; no exhaustive global novelty or confirmed new terrestrial analog pairing is claimed. The implemented contribution is the reproducible comparison and explicit handling of measurement limits.
- No new field or laboratory experiments were conducted by the team for this delivery. Literature observations are credited to their investigators and are not team measurements.

The science items in the second section are closed as limitations for this handoff, not stated to be experimentally resolved.
