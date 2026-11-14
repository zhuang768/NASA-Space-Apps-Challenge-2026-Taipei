# Regional Mars day/night temperature context

2026-11-14. New source: Wang and Jin's MCS-derived surface-temperature grid, corrected to nominal 03:00 and 15:00 LTST using model-based time adjustment. This is actual downloaded research data, not demonstration data or uncorrected raw measurements.

- Version DOI: https://doi.org/10.5281/zenodo.17947556
- Paper: https://doi.org/10.1029/2025JE009381
- Author methods/code: https://github.com/YuleWork/Mars-surface-temperature-JGR2025
- Attribution: Yu Wang and Shuanggen Jin, 2025 dataset; 2026 paper.
- Source and derived temperature data: CC-BY-4.0, https://creativecommons.org/licenses/by/4.0/ . Changes here: nearest-coordinate extraction, MY29–36 selection, missing-value handling, same-MY/Ls day/night contrasts and summary counts. This notice does not license project code or unrelated datasets.

## What was obtained

The 14,940,903-byte NetCDF matches the provider's MD5 `921ebf89ba5f1ac35d89d62f83369c27`. SHA-256, version and source metadata are in [context.json](context.json). The file contains `tsurf_correct(MY,Ls,ltst,Lat,Lon)` with 10 Mars years (28–37), 36 seasonal coordinates (0–350°, 10° spacing), two nominal local times and a 5° latitude/longitude grid.

All variable/global metadata attributes in this file are empty. Units in kelvin are interpreted from the publication and author plotting code, not an encoded NetCDF units attribute. Coordinate datum, grid-center/edge semantics, footprints, per-bin counts, QA and uncertainty are not encoded. These limitations prevent promoting the data to a QA-qualified 100 km observation product.

## Extracted support

| Mars target | Requested center | Selected native coordinate | Finite day bins | Finite night bins | Paired MY/Ls bins |
|---|---|---|---:|---:|---:|
| Jezero | 18.44,77.45 | 20,75 | 151 | 155 | 129 |
| Gale | -4.59,137.44 | -5,135 | 90 | 71 | 54 |
| Arcadia | 40,-170 | 40,-170 | 180 | 155 | 115 |

Each has 288 possible year–season pairs for MY29–36. Counts are finite populated bins, not original observation counts or calibrated reliability. A 5° latitude interval on Mars is about 296 km, larger than the terrain window. Selected coordinates are not confirmed exact observation footprints. No spatial interpolation or 100 km averaging was performed.

The contrast is 15:00 minus 03:00 for the same MY/Ls grid coordinate only when both values are finite and positive. It is not a same-sol pair, daily amplitude, annual average or engineering extreme. Missing values remain null. Storm seasons are retained; we did not copy the author's trend-specific global-density or outlier masks into a regional product without validation.

## Matching integration

`outputs/matching_handoff/matching_data.json.regional_temperature_context` now carries this independent context package. Each target is marked `context_only_metadata_incomplete` and `scoring_eligible=false`. Existing `mars_profiles.*.surface_temperature` remains missing for the formal comparable observation requirement; the original terrain ranking is unchanged. Reporting must explicitly consume the new context key. No frontend code was changed.

Recommended UI label: **MCS time-corrected surface temperature · coarse context**.

Required visible caveat: **5° grid; nominal 03:00/15:00 LTST; model-adjusted; QA/counts/uncertainty absent from distributed file; not scored.**

Do not display this as raw temperature, fully validated kinetic LST, an exact site mean or directly interchangeable with MODIS, MEDA, POWER or TES thermal inertia.

## Reproduce

```bash
.venv/bin/python -m scripts.process_regional_temperature --download
.venv/bin/python -m scripts.export_matching_handoff
.venv/bin/pytest -q -p no:cacheprovider
```

The version-pinned downloader checks the MD5 before accepting a new file. Existing files are also checked. Metadata version and license are checked; shape/coordinates/time labels must match. A malformed or changed dataset raises an error. No external queries requiring an email or private account were submitted.

## Other sources investigated

| Source | Finding | Decision |
|---|---|---|
| [THEMIS BTR/PBT](https://viewer.mars.asu.edu/glossary/themis/btr) | Real brightness-temperature products; band can vary, not always IR9. Static PDS archive and ODE spatial query accessible | Useful finer-scale future route; requires georeferencing, calibration/QA, timing, seasonal and footprint pairing. Not integrated as regional temperature this round |
| [THEMIS global mosaics](https://www.mars.asu.edu/data/) | Thermal-IR image mosaics are available; not established here as calibrated temperature grids | Do not infer kelvin from PNG/DN/color scale |
| [TES data service](https://tes.asu.edu/data_tool/) | Query service requires email delivery; local access encountered a certificate hostname mismatch | No email query sent; original TES archive remains a larger processing route |
| [MEDA pilot](../../docs/mars_temperature.md) | Rover-local brightness temperature with incomplete quality flags | Retained as separate provisional context; no substitution for regional Gale/Arcadia |

Discovery note: the initial ODE trial used unsupported `minlon/maxlon` keys and was rejected as a region selection after checking the returned label (center 168.757E instead of Gale). A subsequent query used `westernlon/easternlon` and returned Gale-region PBT links. No trial BTR/PBT image or its pixel values entered the exported results. The main MCS source was selected because its small, published grid could be obtained and audited without heavy imagery processing.

## Still needed

1. Confirm the distributed grid's geodetic convention, center/edge semantics and aggregation footprints; inspect the complete correction/retrieval method.
2. Obtain original bin counts, QA and uncertainty, or a documented defensible validation route. Finite values alone do not establish quality.
3. For a 100 km regional test, obtain compatible finer observation support or explicitly change the thermal analysis scale with a versioned method.
4. Agree on Ls/Mars-year/observation-time comparison and event handling. A seasonal coordinate is not an Earth calendar month or equal-duration interval.
5. Receive Earth MODIS QA-controlled LST, actual observation-time/coverage information and a validated cross-instrument comparison before temperature scoring.
6. Website teammate integrates and tests the new context display; Matching does not claim website build/deployment validation.
