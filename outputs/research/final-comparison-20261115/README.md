# ZASA: reproducibility and comparison results

Scope: The goal is to finish comparisons supported by available data, not to
prove that the three designated Earth–Mars site pairings are valid. Three
supplied ZIP packages were obtained and checked for ZIP integrity; the main
numerical workflows were rerun in separate working copies. The two teammate
exports were text summaries. Their named Python and CSV attachments were not
available; the reachable claims were independently recomputed from the source
files identified in those summaries.

## Results

| Site | Recomputed comparison | Result | Interpretation |
|---|---|---|---|
| MS-01 | Victoria Valley versus Bull Pass, November daily-harmonic deep-to-shallow amplitude ratio, nominal depths near 8 and 31 cm | 2002: 0.03509 vs 0.06653. 2003: 0.03411 vs 0.06984. Each site and month contributes 720 hourly records. Earth package numerical replays agree within 3.32e-12. | Direct numerical comparison of the two Earth series, not a controlled ice/non-ice experiment. These nominal depths do not straddle Victoria's historically reported ~40 cm interface. |
| MS-01 | Single cutoff on change in annual attenuation from 30–45 cm to 45–60 cm | Victoria < Bull Pass < Mount Fleming in both 2021 (8,759 shared timestamps) and 2022 (8,290 timestamps), including all 24 leave-one-month-out fits. | No one-sided threshold on this metric separates these three historical classifications. Same sites, not newly measured ice labels. |
| MS-01 | Annual phase versus amplitude consistency | The supplied raw and portable-subset runs reproduced the same results: 8 base rows and 96 leave-one-month-out rows. Maximum difference from archived output: 3.99e-13. | An Earth thermal-model consistency check, not an independent ice classifier. Mars thermal inertia and SWIM are not the same measurands as probe time series. |
| MS-02 | Askja raw navigation and author-pick registration | Two radar traces are 0.320885 m apart in interpolated navigation; this is not a borehole offset or position uncertainty. Two unverified assignments yield author-pick depths of 0.938300 m (forward) and 0.616723 m (reverse). Six alignment outputs and four registration/GIS outputs matched byte-for-byte; the remaining JSON differs only in run time. | Neither assignment establishes the position of borehole B7. A candidate depth near its field depth cannot be used to select the direction. |
| MS-02 | Three SHARAD segments: 194 power columns and track geometry | Median along-track posting 465.43–465.45 m by segment. Median full width at half power 4.048 samples (~0.152 microseconds) with the explicitly specified nearest-crossing linear-power method. A hypothetical 0.45 m interface gives only 0.113–0.240 sample intervals for assumed relative permittivity 2–9. | Measured width of stored echoes and a distinct modeled delay. The available products do not resolve a separate interface at this scale. This does not establish ice absence. |
| MS-02 | Adventdalen core data | 12 cores; active-layer thickness about 58–197 cm, median 103 cm. All 12 have positive excess ice somewhere in the logged profile. | Field observations are usable as a core summary, not paired with the available radar lines. No independent blind classification was run. |
| MS-03 | Adventdalen AD1 polygon sampling | 185 published polygons × 4 spacings × 16 grid origins = 11,840 cases. Median geometric IoU at 0.5, 1, 3 and 6.11 m: 0.971650, 0.944232, 0.843474, 0.709662. At 6.11 m, 8/185 stay at or above 0.8 for every grid origin; 39/185 cross that cutoff when the grid origin changes. All three experiment CSVs match byte-for-byte. | Geometric rasterization sensitivity for known Earth outlines, not optical detection accuracy and not a Mars contour test. |
| MS-03 | Cape Blossom sampling and MS-03 CTX coverage replays | Same Earth brightness-contrast experiment: about 36% of the original median contrast remains at 6 m, in both flights. The two CTX scenes jointly cover ~84.81% by nonzero-image proxy; the previously reviewed windows total ~9.16 km². | Brightness is not shape or ice. CTX coverage is not interpreted area. The replay did not add a validated in-box Mars outline. |

## Replay and provenance

Start with the [replay guide](replay/README.md). The SHARAD/core and AD1
workflows use repository inputs. The MS-01 temperature and Askja workflows
require separately supplied inputs, as listed in the guide.

- Use the three original libraries' ZIPs. For MS-01 follow their embedded
  replay instructions, keeping raw input and portable subset runs separate.
  The MS-01 native Mars review uses delivered cropped cells, not a fresh
  reconstruction from complete original global rasters.
- Askja: from the separate package, run
  `python3 -I recompute_alignment.py inputs <output_dir>`. From the combined
  package MS-02 folder, run `recompute_sensitivity.py` and
  `recompute_gis.py` with the same argument pattern.
- For MS-03, use the combined package's `phase_test.py` and the supplied
  `polygons_Act-IWS_source.zip`. Match the rerun with the three archived CSVs.
- Source for MS-02 Mars data and radar inputs: GitHub commit
  `07dbe29203504ba0ccde5e379f42ecc16e4b1b4f`,
  `outputs/research/mars_reselection_20261114/final_candidates.csv`, and
  `outputs/research/MS-02/local_validation/radar_roi/`. Core and radar
  results have different spatial and temporal support.
- The validation replay did not modify the project report or website. No
  successful Earth–Mars match or detection accuracy is claimed.

## Files in this directory

- [MS-01 monthly thermal comparisons](ms01/thermal_month_comparison.csv) and
  [annual phase consistency](ms01/annual_phase_consistency.csv). Deeper
  channel assignments marked as scenarios are not verified sensor depths.
- [MS-02 Askja registration scenarios](ms02/askja_registration_scenarios.csv),
  [SHARAD per-column echo widths](ms02/sharad_echo_width.csv), and
  [velocity and resolution sensitivity](ms02/velocity_and_orbital_scale.csv).
  An Askja candidate row is not a named borehole trace.
- [MS-03 grid sensitivity summary](ms03/adventdalen_grid_summary.csv) and
  [per-polygon ranges](ms03/adventdalen_polygon_summary.csv). AD1 is an Earth
  reference dataset, not a measurement of MS-03 Mars.
- [Source attribution](SOURCES.md) and [file digests](SHA256SUMS).
  These are selected derived results, not copies of the original ZIPs,
  raw recordings, or source imagery.
