# MS-02 Earth evidence follow-up — source and identifiability notes

2026-11-15 Asia/Taipei. Working evidence notes for the human author, not formal report text. Baseline read: main `521740108050ba16e406f8becb67a786179ff8bd`, MS-02 local_validation notes. The original four candidate IDs and the fixed Mars ROI are unchanged.

## What was actually checked

| Evidence chain | New check | Consequence |
|---|---|---|
| Beacon Liu2018 original records | Read §4.1.2 and data availability. The 2 cm probe was disturbed; model forcing used 10 cm. Lower boundary came from another lower-Beacon borehole. The cited GCMD download returned 502 through the web tool; the supplement returned 403. | Preserve the published thermal/material subcase. No raw series, calibration file, or independent model reproduction was acquired. Tool failure is not proof that the archive no longer exists. |
| Beacon GTN-P `pt/681` | Read the actual catalog: −77.80318°,160.71384°; no datasets listed. | Metadata only, not the Liu hourly shallow profile. No transfer of its temperature or coordinates into Liu's station. |
| Haughton Thomson2012 | Re-read §§3.1–3.3,4.1,5.1 and supplement listing. The article pairs core and CMP focus after excavating the wet active layer. The only listed supplement is Table 1, a theoretical summary. | Published same-line validation design is supported. Machine-readable original traces/core-depth values and calibration records were not obtained. An excavated experiment does not validate undisturbed overburden or orbital SHARAD. |
| WISDOM2025 and 2026 | Read primary EPSC abstracts. The 2026 abstract explicitly assigns 3D truth to the Longyearbreen cave. | Cave geometry is not the independent ice truth for the Adventdalen polygon trough. Figures and simulations are not original radar/core files. |
| USAP-DC602028 | Actual catalog lists `g080_ground_sensor_data.zip`, 3.3 MB, MD5 `cad4c27d74f8becc4d8bd6840fb31f7f`; download asks for reCAPTCHA. | Cataloged wet/dry soil-control data are a separate 2022–25 study, not Liu1999–2011 or WISDOM. No download or file-hash verification is claimed. |

The author's University of Washington dissertation was also read at the data-availability passages and Appendix 3.B (printed pp96–99). It repeats the archive/author route and supplies comparison figures, not the original hourly records. Thesis figures and the later journal article are distinct versions; they were not merged into a new time series.

## Conditional calculation delivered

`python3 analyze_crim.py` evaluates the published modified two-component CRIM equation with **assumed** Ki=3, Ke=3.2 and several host permittivities. Multiple admissible ice fractions reproduce the same Ke. `crim_identifiability.csv/json` records both admitted and rejected algebraic solutions; negative fractions are flagged rather than clipped. This is an identifiability diagnostic, not a new ice observation or fit. The assumptions omit air, liquid water, losses and temperature dependence. It cannot quantify MS-02 ice or validate a WISDOM ε input.

## Remaining external evidence and precise next acquisition

| Chain | Exact missing records | Required before upgrading the claim |
|---|---|---|
| Beacon | Liu hourly temperature files, channel/depth metadata, original calibration and disturbance dates, exact station coordinates | Obtain the linked archive or author-supplied files; verify timestamps/calibration and keep lower-borehole boundary separate. Author contact has not been sent. |
| Haughton | Original PulseEKKO traces, CMP picks, core segment mass/volume data, survey/core georeferencing and pre/post-excavation geometry | Reproduce velocity/Dix correction and matching depth horizons; independently assess wet-overburden performance. |
| WISDOM polygon trough | Raw four-line radar data, coordinate frame, calibration, exact survey geometry and colocated independent core/exposure ice truth | Match the same target and depth. Model consistency and a different cave truth do not supply this chain. |

No public file was silently replaced with another valley, year, borehole or instrument. No finding of zero search results was used as proof of absence. Search/download outcomes are in `search_log.csv`; actual readings and limits are in `source_audit.csv`. Hashes in `manifest.json` cover the **local follow-up artifacts**, not unacquired remote originals. All retrieval failures remain acquisition gaps; the scientific missing observations are not marked resolved.

## Primary links

- Liu2018: https://doi.org/10.1029/2017JF004535 (§4.1.2; acknowledgments; supplementary-file listing).
- GTN-P: https://data.gtn-p.org/view/pt/681 (location; dataset table).
- Thomson2012: https://doi.org/10.1029/2012JE004053 (§§3.1–3.3,4.1,5.1; Table 1 and supplement listing).
- WISDOM2025: https://doi.org/10.5194/epsc-dps2025-710 (field locations; results).
- WISDOM2026: https://doi.org/10.5194/epsc2026-988 (Ice cave dataset; Figures 2–3).
- USAP-DC602028: https://doi.org/10.15784/602028 (catalog, data-file list and download gate).

- Liu dissertation: https://dev-www.ess.washington.edu/content/people/student_publications_files/liu--lu/Liu_washington_0250E_14999.pdf (chapter3 data availability; Appendix3.B).

## 2026 literature and available-export follow-up

McKay2026 (DOI10.1017/S0954102025100448; online2025-11-27, print2026) reuses the University Valley archive. Its surface-ice-relative-humidity threshold is a snow **proxy**. The14/40 equivalent-day cases and17/66cm depths are perturbed/scaled model outcomes, not measured snow-treatment controls. One-year representativeness is assumed. This directly overlaps the UV moisture/ice-stability use; it does not deliver independent material or ice-free controls.

Levy2026 (DOI10.1080/15230430.2026.2617687) provides a partial thermal-method precedent:17 MDV samples, triplicate wetting levels and lab TI. The retrieved publisher text does not establish correspondence with UV-W or Liu's Beacon point. Room-lab wetting and orbital apparent TI do not validate frozen field ice content or supply site-specific material truth. Supplement numbers were not acquired.

Actual read-only inspection of the known09_10 Campbell export found17,705 continuous half-hour records, printed2009-12-04 19:30 to2010-12-08 15:30. The text changes date formatting (17,089 US-format rows and616 ISO rows); no clock correction was made. The decoded release MD5 and SHA256 match the prior source manifest. Only4,137 rows fall within the paper's November2009–February2010 window. More decisively, Campbell RH is measured in air at1.2m, whereas surface RH used a separate hourly Onset sensor. Therefore `snow_proxy_equivalent_days` is **null**: applying the98% surface rule to these air channels or inventing November observations would be invalid.

The same file supplies an actual atmospheric descriptor: wind at1.08m, all17,705 finite values, median1.82m/s, p957.72m/s, range0–14.65m/s. These summarize the available author-calibrated export, not annual climatology. The4,949 records below the nominal1m/s instrument threshold are retained and flagged, not certified as calm winds. The derived source-line-linked series is `uv_wind_records.csv.gz`; `uv_export_support.json` and `inspect_uv_support.py` preserve provenance, time support and interpretation. No raw logger/calibration or new remote download is claimed.

Primary follow-up links: [McKay2026](https://doi.org/10.1017/S0954102025100448), [Levy2026](https://doi.org/10.1080/15230430.2026.2617687), [Marinova2022](https://doi.org/10.1017/S0954102022000025).

### Alternate hourly surface-RH export

The separate09_10 HOBO W export **does** contain `Surf_RHIce` (column6), sampled hourly. Its decoded release hash matches the prior source manifest. The available part of the paper's summer window is2009-12-10 00:00 through2010-02-28 23:00:1,944 finite samples,78 at or above98% (4.01235%). Dividing78 hourly samples by24 gives **3.25 nominal hourly-sample-equivalent days**, not a measured continuous snow-cover duration. The paper's48-samples/day divisor was not applied.

This is a bounded descriptive result, **not reproduction of the paper's approximately24 days**: November and December1–9 are absent, the archive is hourly rather than the paper's30-minute surface series, and that processing/version relationship remains unknown. The file's decimal-day values differ from printed timestamps by+1hour throughout8,625rows; the original printed axis was retained without automatic repair or UTC assignment. No missing hour was treated as snow-free or extrapolated. `uv_surface_RH_support.json` and `uv_surface_RH_available_summer.csv.gz` preserve the checkpoint; `inspect_uv_surface_support.py` reproduces it from the pinned author export. Campbell's null snowcount remains correct for its air-RH-only schema.
