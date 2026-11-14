# Research display figures: pinned compute handoff

Team zasa · 2026-11-14 · branch `reporting/team1-final-figures`.

**F01–F03 are now rendered as PNG and PDF.** They are display editions for review, not final mainline acceptance. The user explicitly selected compute commit `14f65509bbf3358a50ef866c65e2b5d42fe8c467` (PR #5) for this continuation. The final `elephant_head_final/` package and `final_research_summary_en.md` remain unreceived; neither is marked as received or accepted.

## Figures and changes

| ID | Files | Purpose and transformation |
|---|---|---|
| F01 | [PNG](F01_case_context.png) / [PDF](F01_case_context.pdf) | Sourced coordinate context for I-02 and EARTH-002. Original illustration; no new measurement or terrain analysis. |
| F02 | [PNG](F02_EH_temperatures.png) / [PDF](F02_EH_temperatures.pdf) | 3 cm and 49 cm temperatures. Same published values and original summer mask as compute `plot_eh`, separated from the original combined chart into its own panel; colours, type and spacing revised. |
| F03 | [PNG](F03_EH_temperature_difference.png) / [PDF](F03_EH_temperature_difference.pdf) | Same-row `T(3 cm) − T(49 cm)`, using the original plotting expression. The descriptive mean is read from `window_summaries.csv`, not recalculated. No confidence interval or performance statistic. |

Both depth curves use all 2,160 common hourly observations. No smoothing, filling, resampling, timezone conversion or raw-PDF parsing was performed. Original `plot_eh` performs same-row subtraction for display; this renderer repeats only that plotting expression, with no new summary statistics or scientific analysis. The mean comes from the export's `summer / T_3cm_minus_49cm_C / observed_mean = 3.274851851851852`, displayed as **+3.2749°C**. No values were adjusted to match a target.

The earlier `templates/` files are retained as data-free historical layouts, clearly labelled **NOT A RESULT FIGURE**. They are superseded by root F02/F03 and excluded from the current figure manifest. Do not include them in a submission.

## Versions and intact inputs

- Context documents: main `ab1da697ad2093ca8185d29932e3fc5b85e7f80b`, MR-20261114-v2. Read the main research cards, synthesis, Team 1 matching report/candidate CSV and Team 2 audit. The figure brief fixes I-02 / EARTH-002 as the main display case; University Valley remains a known-use comparison and Linnaeus remains inactive.
- Calculation input: [`14f6550 / outputs/compute/EARTH-002`](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/tree/14f65509bbf3358a50ef866c65e2b5d42fe8c467/outputs/compute/EARTH-002), on `compute/candidate-extraction-20261114`, [PR #5](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/5). User selection permits figure preparation; it is not a final acceptance receipt.
- Byte-identical copies of `station_observations.csv.gz`, `window_summaries.csv`, `qa_report.json`, `data_dictionary.json`, `inputs_manifest.csv`, and the original combined PNG are retained under [inputs/14f6550/](inputs/14f6550/). They were read from the pinned Git objects without modifying or rerunning compute code. Source paths, byte counts and SHA-256 values are in [input_lock.json](input_lock.json).
- The original plotting method is `scripts/compute/eh_adapter.py`, `plot_eh`, at the same pinned commit. Its summer selection and row-subtraction expression are attributed in the presentation script. No compute source file is edited.
- The compute QA reports 8,922 publication-table rows and previously executed checks. Those remain the compute team's results, not new figure-owner data QA. Our rendering checks are separate in [render_checks.json](render_checks.json).

The following requested final-mainline files remain absent from the received main baseline: `docs/research/final_research_summary_en.md`, and `outputs/research/elephant_head_final/{README.md,manifest.json,qa.json,summer_temperatures.png,summer_temperature_difference.png}`. The `outputs/compute/` package is received from the fixed branch, not from main. No other version is silently mixed into F02/F03.

## Coordinates, time and interpretation

**F01 Mars:** I-02 center 53.75°N, 42.25°E; nominal cell 53.5–54°N / 42–42.5°E. Planetocentric latitude and east-positive longitude. Regional locator view: 52.75–54.75°N / 40.75–43.75°E. Display aspect is corrected at the center latitude; it is not a new terrain map or instrument footprint. No Earth-distance formula is used for Mars.

**F01 Earth:** station anchor 79.820216667°S, 83.314333333°W; source DMS 79°49.213′S, 83°18.860′W. Datum and positioning error are unstated. Decimal precision reflects the supplied conversion, not survey accuracy. The south-polar coordinate locator uses radius `90 + latitude` and signed east longitude displayed clockwise from 0°. It is a coordinate diagram, not a metric survey projection or coastline map. The view spans 60–90°S. Marker size is symbolic; no trial-area radius or common Earth–Mars distance scale is assigned.

**F02/F03:** first printed time `[2017-12-01, 2018-03-01)`, 2,160 same-row pairs. The export retains label “GMT-07:00” and unresolved UTC/solar-time meaning. No time conversion is made. Nominal 3 cm subsurface temperature is not radiometric land-surface temperature. The historical 49 cm probe is not a new ice-depth measurement or independent held-out truth. N describes observational support, not independent replication. The plots do not infer ice depth, quantity, extractability, causation or Mars equipment performance; terrestrial temperature is distinct from TES thermal inertia.

## Appearance and reproduction

White background, DejaVu Sans, 14 × 8 inches; PNG 3080 × 1760 at 220 dpi and vector PDF. 3 cm is teal `#007F8B`; 49 cm is orange `#C16A16`. The difference is purple with a dashed dark descriptive-mean line. Labels name the depth as well as colour. F01 uses location accents; its colours are not depth measurements.

Run from repo root, with matplotlib/numpy:

```sh
python scripts/reporting/final_figures/build_figures.py
```

The script verifies pinned input hashes, reads the exported CSV/gzip, selects the original plot window, renders curves and refreshes the manifest. It never opens the raw PDF, runs the compute pipeline, fits a model, computes an average or changes scientific values. `path.simplify=False` preserves all plotted vertices. The original input package remains intact. PDF metadata can change between runs; output hashes are refreshed in the manifest.

Executed checks: byte identity against the pinned Git input objects; input/output SHA-256; 2,160 selected pairs against export valid N; all plotted y-vertices against source temperatures / original subtraction expression; coordinate DMS arithmetic; CSV/JSON parsing; PNG/PDF output; visual review of the original combined chart and F01/F02/F03, including correction of label overlaps. These are rendering/provenance checks, not a repeat of statistical or sensor QA. Mainline acceptance and Team 2's consolidated science/caption review remain pending. Detailed text is best placed full-page/landscape or read in vector PDF; no mobile/interface test is claimed.

## Photography / orbital imagery inventory

Existing source: McKay et al. (2019), [NASA author PDF](https://www.nasa.gov/wp-content/uploads/2019/09/mckay_etal_2019_dry_permafrost_ellsworth_land21.pdf), DOI [10.1017/S0954102019000269](https://doi.org/10.1017/S0954102019000269). The cached PDF page 2 was rendered and inspected for the asset inventory only. Methods/Fig. 1 identify the monitored station. Figure 1 has a map, satellite view and station photograph; its red X identifies the monitored site, while S is another site about 1.5 km east.

The PDF's 2019-07-30 download stamp is not the image acquisition date. Acquisition dates, product/sensor IDs, exact image footprint and individual third-party reuse exceptions are not established by the inspected figure. Team 1 records the article as CC BY 4.0; per-image clearance remains pending. No image panel was copied or redistributed. A dated, location-verified station photo and satellite/orbital image with verified reuse terms remain optional missing assets. No suitable I-02 orbital image with acquisition metadata/footprint was identified in the supplied package. No other place's image or generated image is substituted; F01 remains a sourced coordinate locator. No expanded search was undertaken.

## Review and final handoff

Team 2: provide one consolidated review of scientific labels, coordinate conventions, source attribution, limits and full captions for F01–F03. No feedback has yet been received or claimed as resolved. Main: confirm the final accepted plot version once the mainline package is published; if it differs, identify the exact replacement and QA. The figure owner will apply one concentrated correction pass within this package. Main performs the final merge. No new sites, analysis or other presentation tasks are opened.

[figure_manifest.csv](figure_manifest.csv) records each scientific output, input version, source, data period, conditions, changes and limitations. No new project-wide license is selected: original layout/code follows the team's eventual license decision, while published measurements retain their source attribution and applicable source terms.
