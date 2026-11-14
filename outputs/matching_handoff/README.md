# Matching handoff for the website teammate

Updated 2026-11-14 (Taipei). Scope: Earth–Mars only, four themes retained. This package exports existing matching results and adds explanatory figures. It does not rerank candidates, integrate unreceived Earth datasets, or continue candidate geological investigation. Website code remains owned by Reporting.

## What is ready

- Three Mars reference profiles: Jezero, Gale and the project-defined Arcadia center.
- A terrain-only Earth search: 2,611 eligible windows, 12 spatially separated candidates per target, 36 target–candidate records.
- POWER environmental context for the first two candidates per target, six records total. It does not affect ranking.
- Mars TES thermal inertia, SWIM ice consistency and MY34/MY35 dust context, with native support and limitations.
- Existing maps, terrain panels and sensitivity outputs; new distance-component and sensitivity figures below.
- A machine-readable export with input hashes, source records, target profiles, all candidates and explicit per-theme scoring status.

## Start here

1. Read `matching_data.json`; keep target IDs and candidate IDs unchanged.
2. Use `candidates` for cards/tables and `targets` for Mars centers. Candidate coordinates are Earth coordinates; target coordinates are Mars coordinates.
3. Use the existing [Earth footprints](../analysis/candidates.geojson), not a point marker alone, to explain the 100 km support.
4. Preserve source units, statuses and missing reasons. Display environmental context separately from terrain distance.
5. Use the figures with their complete captions. Integrating this package into the web bundle is Reporting's next step; it has not happened automatically.

## Current top-two results

| Target | Candidate | Earth lat, lon | Terrain D | POWER T2M °C | POWER precipitation mm/day |
|---|---|---|---:|---:|---:|
| Jezero | jezero-01 | 57,161 | 0.1341 | -2.47 | 2.513 |
| Jezero | jezero-02 | 13,37 | 0.1362 | 25.56 | 7.692 |
| Gale | gale-01 | 39,75 | 0.2319 | 0.72 | 0.300 |
| Gale | gale-02 | 35,75 | 0.3459 | -1.91 | 2.108 |
| Arcadia | arcadia-01 | 29,-105 | 0.0252 | 21.38 | 0.346 |
| Arcadia | arcadia-02 | 35,57 | 0.0448 | 19.31 | 0.289 |

D is dimensionless and lower is closer in the defined terrain statistics. It is not percent similarity or mission success. POWER is day-weighted 2023–2024 monthly context for a coarse cell near the center, not a window-wide surface-temperature measurement. Do not rank different Mars missions by their D values.

Gale 39,75 remains a research-priority case from the existing report, not a newly validated complete analog. Jezero top-two precipitation demonstrates why terrain matches do not establish a dry-environment analog. Arcadia is a design target at 40N,170W, not an approved landing site or confirmed extractable-ice location.

## Asset manifest and captions

| Asset | Use | Caption / restriction |
|---|---|---|
| [candidate_map.png](../analysis/figures/candidate_map.png) | Earth overview | Regional terrain shortlists; sparse 2° center search between 60S and 60N, with explicit exclusions and gaps. Not an exhaustive global optimum. |
| [gale_terrain_comparison.png](../analysis/figures/gale_terrain_comparison.png) | Gale and top-two Earth terrain | Same 100 km extent and color scale; elevation relative to each window median, in meters. 4 km samples, 8 km slope stencil. Not satellite photography or fine-scale safety evidence. |
| [jezero_terrain_comparison.png](../analysis/figures/jezero_terrain_comparison.png) | Jezero terrain panel | Same limitations as Gale panel. |
| [arcadia_terrain_comparison.png](../analysis/figures/arcadia_terrain_comparison.png) | Arcadia terrain panel | Same limitations; target center is a project design assumption. |
| [terrain_distance_components.png](terrain_distance_components.png), [SVG](terrain_distance_components.svg) | Explain why each stored top-two match ranks | Stacked terms sum to D. Panels have independent x scales. Three correlated terrain statistics are not three independent mission requirements. |
| [top2_sensitivity.png](top2_sensitivity.png), [SVG](top2_sensitivity.svg) | Show sensitivity | Count of baseline top-two retained, out of two. Weight variants fix the candidate set; 10 km sampling changes eligibility. Not confidence. |
| [mars_quicklook.png](../figures/mars_quicklook.png) | Mars source overview only | Source-grid visualization, not Earth matching evidence. Preserve each layer's units and support. |
| [mars_selftest_arcadia.png](../figures/mars_selftest_arcadia.png) | Optional diagnostic | Mars-to-Mars internal self-test, not external Earth–Mars validation. Dust-derived portions have separate CC-BY-SA terms. |

New chart source: ETOPO 2022 / MGS MOLA, existing candidate features and sensitivity results. Full captions are also in `matching_data.json.captions`. No dust values enter the new charts. For dust-derived data reused from profiles, retain [the existing license notice](../mars_profiles/LICENSE-data.md).

## Four-theme display contract

| Theme | May display now | Must not imply | Remaining input |
|---|---|---|---|
| Terrain | Actual D, component terms, target/candidate features and footprints | Landing safety, wheel-scale trafficability, same geomorphic origin | Optional finer data only if required by an explicit test |
| Temperature | TES TI with native valid fraction; POWER air-temperature context | TI equals LST, or regional day/night Mars LST is complete | QA-controlled Earth LST and compatible regional Mars surface temperature / validated comparison method |
| Water/Ice | SWIM consistency by depth; POWER precipitation context | Ice amount/probability, dry equals icy, low NDVI equals lifeless | Earth candidate precipitation, soil-moisture, vegetation and PFR summaries with QA and support |
| Atmosphere & Dust | Mars native 3° reconstructed dust series, separate MY34/MY35 | Earth 550 nm extinction equals Mars 9.3 µm absorption, wind speed substitutes for dust | Earth QA-controlled dust/aerosol context and defensible comparison definition |

Per-theme `not_scored` means not part of the current ranking; it does not mean no contextual information exists. Unknown values must render as unknown, not zero. `1/4 scored` is a completion count, not confidence. MEDA is Jezero-local brightness temperature; the conservative complete-QA accepted count remains zero. Do not use provisional MEDA to fill Gale/Arcadia regional temperature.

## Matching gaps and ownership

| Priority | Gap | Owner / next deliverable | What Matching can do after receipt |
|---|---|---|---|
| P1 | Earth files are on the data teammate's machine; inventory is not a completed local QA run | Data: cloud handoff or small candidate feature bundle | Check units, footprint, QA and provenance; then integrate only justified indicators |
| P1 | No common feature contract for all themes | Matching + Data: use the minimal contract below | Validate handoff before changing scores |
| P1 | Regional Mars day/night surface temperature absent | Data: product/time/quantity/QA assessment | Evaluate comparability; keep unknown until verified |
| P1 | Four-theme score is not validated or implemented | Matching: define comparable quantities, thresholds, weights and missing-data policy before rerun | Version a new analysis and compare with the terrain baseline, if inputs suffice |
| P1 | Current ranking can change with scale and weights | Matching: retain present sensitivity; broaden only when changes justify it | Explain recommendation changes without confidence claims |
| P2 | Limited external reference validation | Matching: expand a mission-specific independent reference set | Existing two-window diagnostic is not classification accuracy |
| Paused | Candidate geological/mineral evidence gaps | No further candidate deep-dive this round | Reuse existing research links without promoting partial evidence |
| Website | New export and chart integration; final browser checks | Reporting | Keep scientific outputs unchanged; ask Matching before altering conclusions |

The teammate Earth inventory was previously counted as 222 files / about 12.33 GB. Treat file size as an inventory report, not proof all raw files are currently available or quality-controlled here. Do not commit multi-GB raw Earth files.

### Minimal Data → Matching contract

A small JSON/CSV per target/candidate is preferable to transferring all raw files initially. Required fields: `candidate_id`, variable/physical quantity, value (or null), unit, product ID/version, period, native resolution, CRS/body, aggregation footprint, processing/QA method, valid/expected cell and month counts, missing reason, source URL and file hash. Include a footprint GeoJSON and an explicit statement of point versus window support. Preserve the original product's depth, wavelength and time definition. No private credentials.

## Reproduction and verification

```bash
.venv/bin/python -m scripts.export_matching_handoff
.venv/bin/pytest -q -p no:cacheprovider
.venv/bin/ruff check . --no-cache
```

The export recalculates all 36 stored distances, verifies component sums and unique IDs, and checks footprint count. It does not recalculate raw DEM features or alter ranking. Input SHA-256 values are in the export. Existing source records preserve dataset versions and units. New PNG/SVG charts were visually inspected; website integration, build, deployment and browser operation are not verified by this export.

For exact science details use [the terrain method](../../docs/earth_pipeline.md), [Mars profiles](../mars_profiles/handoff.md) and [temperature limitations](../../docs/mars_temperature.md). Candidate geology remains in the existing research report and was not investigated further this round.
