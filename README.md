# ZASA | Mars Reconnaissance Candidates

NASA Space Apps 2026 · Team zasa

Three regional targets for follow-up investigation of shallow subsurface ice. The team selected **MS-01, MS-02 and MS-03** on 14 November 2026 after a new inventory of available Mars data, unweighted trade-off screening, native-grid checks and a bounded prior-site review.

**These are conditional research targets.** A non-hit in the inspected catalogs does not establish that a place has never been studied or proposed. Ice presence, depth, quantity, extractability and landing safety remain unverified.

## The three selected targets

| Target | Center (planetocentric latitude, east-positive longitude) | Why retain it? | Main trade-off |
|---|---|---|---|
| **MS-01** | **56.75°N, 72.75°E** | Positive, relatively strong ice-consistency descriptors in both depth zones; low regional relief | 73/100 native TES cells remain after excluding interpolation; local material and ice truth unknown |
| **MS-02** | **52.75°N, 168.25°E** | Lowest latitude of this three-case set; positive ice descriptors and the most complete TES support | Higher MY34 dust p95 and greater regional relief than the other two |
| **MS-03** | **57.75°N, 242.25°E** | Lowest regional mean slope and reconstructed dust in this set; strong shallow-ice descriptor | Lower 1-5 m consistency; partial TES support and coarse, sparse temperature context |

![Selected research targets and published ice-exposing impact points](outputs/research/mars_reselection_20261114/candidate_map.png)

## Read the results

- [English report](docs/REPORT.md) · [中文報告 PDF](outputs/research/mars_reselection_20261114/mars_three_candidates_report_zh.pdf)
- [Target table](outputs/research/mars_reselection_20261114/final_candidates.csv) · [Data usage](outputs/research/mars_reselection_20261114/all_data_usage.csv)
- [Reproduce](docs/REPRODUCE.md) · [Data attribution](DATA_LICENSES.md) · [Status](CURRENT_STATUS.json)

## Where things are

| Path | Contents |
|---|---|
| `outputs/research/mars_reselection_20261114/` | Target selection, tables, checks |
| `outputs/research/MS-01/`, `MS-02/`, `MS-03/` | Per-target evidence and local validation (see [index](outputs/research/README.md)) |
| `outputs/consolidated/` | Excel workbook of all data |
| `docs/`, `scripts/` | Reports and reproduction code |

Large source grids are downloaded from their providers (see the input manifest). The pre-cleanup history is in the [archive branch](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/tree/archive/pre-msr-cleanup-20261114).

Independent team research; not NASA endorsement or certification. Original observations remain attributed to their providers. AI assisted code, checks and writing.
