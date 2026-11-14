# Mars reselection computation - 2026-11-14

This package is a new, isolated Mars regional research-candidate analysis. It does not modify the former discovery scores, old I-01/I-02 cards, Earth data, Elephant Head exports, workbook or website. Execution used the project's Mac CPU Python environment; no GPU, model training or generated observations were used.

## Reproduce

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scripts.research.mars_reselection_20261114
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scripts.research.mars_reselection_20261114 --finalize-targets outputs/research/mars_reselection_20261114/fixed_targets.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scripts.research.mars_reselection_20261114 --validate
```

The script requires the existing project numpy, pandas, xarray, scipy and rasterio dependencies and the local raw Mars files. It does not download new data. Native source URLs, byte counts and SHA-256 values are in `method.json` and `candidate_native_evidence.json`.

## What was screened

- 172,800 nominal 0.5 degree cells between 59.75 S and 59.75 N, covering both hemispheres in the available SWIM support.
- 172,581 cells had finite core descriptors. The exploratory pool contained 58,238 cells after requiring positive shallow and deeper SWIM descriptors, excluding the eight former ice-candidate cells and retaining exclusion of the old project's explicitly defined famous-site boxes.
- Positive SWIM consistency is an exploratory sign criterion, not an ice-content estimate, calibrated probability, ice truth or engineering threshold.
- Six objectives: higher SWIM 0-1 m and 1-5 m consistency, lower regional slope and relief, and lower MY34/MY35 reconstructed dust p95. No weights, target medians or composite score were used. The exact unweighted Pareto front contains 453 cells.
- 22 geographically spread examples from that front were delivered for independent prior-site review. The example-selection rule includes northern examples and low-slope/low-dust extremes. Its geographic spacing is a review/diversity convention, not a local hazard buffer, mission requirement or novelty test.
- TI, elevation, MCS adjusted-temperature summaries and dust seasonal/maximum/reliability information are retained as context and trade-offs. No unsupported universally favourable TI, elevation or temperature target was invented.

`screened_pool.csv.gz` and `pareto_front.csv.gz` preserve the comparison population and favourable percentiles. Percentiles describe that pool, not confidence or a success probability. Pareto status means no other pool cell is at least as good in every declared objective and strictly better in one. It does not establish mission optimality.

## Native evidence and four fixed review targets

`fixed_targets.json` records A, C and D as the requested primary detailed-review targets. B remains a held-out check near a previously studied ice exposure; proximity is not a ruling of exact duplication. Final site novelty is outside this computation and requires the separate source/footprint audit.

`candidate_native_evidence.json` and `candidate_metrics.csv` distinguish:

- Native MOLA elevation and slope from a halo-based derivative at about 3.7 km baseline; relief within the nominal 0.5 degree cell.
- Native TES thermal inertia excluding original mask-zero interpolation, plus the including-infill comparison and explicit valid/native counts.
- Native SWIM 0-1 m and 1-5 m statistics and positive-cell fractions. The two maps share underlying evidence and are not independent confirmations.
- Both MY34 and MY35 nearest-native 3 degree dust cells, each with 669 reconstructed sols, annual summaries, four Ls intervals, peak timing and provider reliability. `cdod610` is a pressure-normalized optical depth, not measured local pressure.
- Nearest-native 5 degree MCS MY29-36 bins, nominal 03:00/15:00 LTST adjusted by the provider's model-based correction. The 288 year/season slots per target include missing values. Populated-bin medians and paired contrasts are not annual means, daily amplitudes or engineering extremes.

Primary native summaries use actual native grid centres inside half-open nominal bounds and cosine-latitude weights. Old stack values are retained separately, with `stack_minus_native` explaining the differences. In particular, the SWIM stack is a coarsened-then-interpolated descriptor; it is not silently substituted for the nominal cell's native mean.

## Files

| File | Purpose |
|---|---|
| `method.json` | Exact scope, screening choices, input hashes and final script hash |
| `screened_pool.csv.gz` | Full 58,238-row comparison pool |
| `pareto_front.csv.gz` | Exact 453-row unweighted front |
| `exploratory_candidates.csv` | 22 examples supplied for literature/footprint review |
| `fixed_targets.json` | Four reproducible detailed-review coordinates and their review roles |
| `candidate_native_evidence.json` | Source-scale evidence, units, native support, missingness and limits |
| `candidate_metrics.csv` | Flat native and stack comparison table |
| `candidate_dust_series.csv.gz` | 5,352 candidate/year/sol rows, including the held-out target |
| `candidate_mcs_bins.csv.gz` | 1,152 candidate/MY/Ls rows with missingness retained |
| `numerical_validation.json` | Read-back, provenance, series and brute-force Pareto checks |

## Limits that remain

The MCS derivative has no distributed QA, per-bin count or uncertainty fields. It is context only and does not close the formal local temperature-quality requirement. The Jezero MEDA pilot has only rover-local support and its existing full-quality screen yielded no qualified rows; it is inventoried in the source record and is not transplanted to new coordinates. Local pressure, wind, mineralogy, material strength, hazards, independent ice truth and equipment-specific operating limits remain unknown. None is filled with zero or inferred from TI, CDOD or SWIM.

Data years and footprints differ. Repeated coarse grid values are not independent observations. A successful numerical validation only confirms the stated extraction/provenance/reproduction checks; it does not validate novelty, resource quantity, field safety, landing suitability or Earth-to-Mars equipment performance.
