# Final research figures: version-controlled handoff

Team zasa · 2026-11-14 · main input `ab1da697ad2093ca8185d29932e3fc5b85e7f80b`.
Research framing: MR-20261114-v2; the user-specified figure brief fixes I-02 / EARTH-002 as the main case. This package makes no change to candidate purposes, measurements, analysis windows or conclusions.

## Delivery status

| Figure | Status | Files and intended use |
|---|---|---|
| F01 | Coordinate-context graphic completed; science/caption review pending | [PNG](F01_case_context.png) / [PDF](F01_case_context.pdf). Separates the Mars nominal screening cell from the Earth station anchor. No photo, terrain background or test-area polygon. |
| F02 | Blocked: accepted source figure absent from main | [PNG layout template](templates/F02_EH_temperatures_TEMPLATE.png) / [PDF](templates/F02_EH_temperatures_TEMPLATE.pdf). These contain no observations and must not be used as result figures. |
| F03 | Blocked: accepted source figure absent from main | [PNG layout template](templates/F03_EH_temperature_difference_TEMPLATE.png) / [PDF](templates/F03_EH_temperature_difference_TEMPLATE.pdf). These contain no difference curve or mean line and must not be used as result figures. |

**The three-figure scientific result set is not complete.** F02/F03 have no formal output filenames at the package root, so a downstream exporter cannot mistake templates for accepted results. No existing science image has been recolored, cropped, smoothed or substituted. F01 is a new coordinate illustration, not a new measurement or terrain analysis.

## Input audit and exact missing items

All these paths are absent from the checked main commit:

- `docs/research/final_research_summary_en.md`
- `outputs/research/elephant_head_final/README.md`
- `outputs/research/elephant_head_final/manifest.json`
- `outputs/research/elephant_head_final/qa.json`
- `outputs/research/elephant_head_final/summer_temperatures.png`
- `outputs/research/elephant_head_final/summer_temperature_difference.png`
- `outputs/compute/README.md`
- `outputs/compute/EARTH-002/`

The remote branch `origin/compute/candidate-extraction-20261114` at `14f65509bbf3358a50ef866c65e2b5d42fe8c467` does contain the compute README, EH QA/data and `EARTH-002_paired_summer.png`. The branch's README and EH QA header were inspected using `git show`; the time-series file was not parsed. The named mainline final package was not found on that branch or the research-mainline branch. There is no explicit mainline acceptance/selection record in the received files. Compute outputs were not copied into this package or presented as the mainline final result. Main must identify the accepted version before F02/F03 replacement. This is an input dependency, not a request to redo data analysis.

Read inputs: `docs/research/main_mars_research_cards.md`, `main_project_synthesis.md`, `team1_earth_analog_matching.md`, Team 1 candidate CSV and Team 2 audit. These preserve historical/provisional states; the figure brief supplies the current display roles. University Valley is a known-use comparison and Linnaeus Terrace remains inactive. Neither is added as a new case.

## Coordinates, scales and visual contract

- Mars: I-02 center 53.75°N, 42.25°E; nominal cell 53.5–54°N / 42–42.5°E. Planetocentric latitude, east-positive longitude. F01 uses a local longitude/latitude locator, with the display aspect corrected at the center latitude. It does not use Earth distances for Mars. The regional locator view is 52.75–54.75°N / 40.75–43.75°E; that view is not a study footprint.
- Earth: EH point anchor 79.820216667°S, 83.314333333°W. Original DMS values: 79°49.213′S, 83°18.860′W. The original source does not state datum or positioning error; no WGS84 claim or areal radius is assigned. Decimal precision reflects the supplied conversion, not survey accuracy.
- Earth panel is a south-polar **coordinate locator**, radial coordinate `90 + latitude` and angle signed east longitude, displayed clockwise from 0°. It is not an orthophoto, geodetic survey, coastline map or metric polar projection. Its view spans 60–90°S. Marker size is symbolic. No distance scale bar is asserted.
- White background, DejaVu Sans, 14 × 8 inches, PNG 3080 × 1760 at 220 dpi, vector PDF. Teal `#007F8B` is reserved for the 3 cm series; orange `#C16A16` for 49 cm. F01 uses these as location accents, not depth measurements. F02/F03 templates contain no data encodings yet.
- On receipt, preserve the accepted summer window: first printed time `[2017-12-01, 2018-03-01)`, 2,160 same-row pairs. The approximately +3.2749°C descriptive mean is a receipt-check reference only; it has not been recalculated or drawn here.
- F03 must retain `T(3 cm) − T(49 cm)` and label any mean as descriptive. No confidence band, accuracy or performance statistic is authorized. Do not convert unresolved printed time labels to UTC/solar time. Station temperature is distinct from Mars TES thermal inertia.

## Photography and orbital imagery inventory

Existing source: McKay et al. (2019), [NASA-hosted author PDF](https://www.nasa.gov/wp-content/uploads/2019/09/mckay_etal_2019_dry_permafrost_ellsworth_land21.pdf), DOI [10.1017/S0954102019000269](https://doi.org/10.1017/S0954102019000269). The local cached PDF's page 2 was rendered and inspected; Methods and Fig. 1 identify the station. Fig. 1 contains (a) a map, (b) satellite imagery and (c) a station photograph; its red X marks the monitored site, while S is another site about 1.5 km east. The displayed 1 km scale and north arrow belong to the original image, not to our locators.

The cached PDF has a publisher download stamp dated 2019-07-30. This is **not** the photograph or satellite acquisition date. The inspected figure does not establish those acquisition dates, sensor/product IDs or precise image footprint. Team 1's recorded article reuse basis is CC BY 4.0; per-image third-party credits/exceptions have not been fully checked for this package. Therefore no figure panel or photograph has been copied or redistributed. A field/station photograph with verified date and reuse basis, and a location-verified satellite image with acquisition metadata, remain optional missing assets.

No location-verified I-02 orbital image/product with acquisition date and exact footprint was identified in the received case package. No unrelated region, generic Antarctica photo or generated image is substituted. Imagery is not a blocker for F01's sourced coordinate locator. No open-ended image search was undertaken.

## Reproduction and checks

Run from repo root using Python with matplotlib and numpy:

```sh
python scripts/reporting/final_figures/build_figures.py
```

This script only constructs coordinate locators and data-free layout templates. It never opens the raw PDF or temperature observations. The original PDF was inspected separately for the asset inventory, not reparsed for data. No new dependencies or source data are committed.

Executed: PNG generation, PDF generation, F01 visual inspection (corrected an initial text overlap), template visual inspection, candidate DMS arithmetic check, JSON/CSV input parsing and manifest/hash verification. Full figure captions and science review by Team 2 are pending; no feedback has been received or claimed as addressed. At 180 mm width the 12 pt base font scales to about 6.1 pt; use full-page/landscape placement for detailed reading, or vector PDF zoom. No mobile/interface testing is claimed.

## One consolidated review and finish

Team 2 should review the labels, coordinate conventions, scale distinction, source statements and limitations together, then provide one consolidated caption/science correction list. Main should supply the accepted F02/F03 PNGs, manifest, QA and plotting source if re-export is requested. The figure owner will apply that one review to these files only, preserving the accepted curves and data. Until then, no completed scientific three-figure set or accepted captions are claimed. No new sites, analysis or other presentation tasks are opened.

[figure_manifest.csv](figure_manifest.csv) records inputs, periods, constraints, statuses and output hashes. This package is on `reporting/team1-final-figures`; main integration is left to the main conversation. Original illustration code/assets inherit the repository's eventual team-approved license; no new project license is chosen here. Cite the underlying research even when using the original locators.
