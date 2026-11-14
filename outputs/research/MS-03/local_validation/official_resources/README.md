# Official Resources follow-up: local MRDR v4 evidence

- Start SHA: `44c2e03b8617c7bb536ad712b85f4716dd190d7c`; branch `research/ms-03-earth-analogs`; this task does not merge main.
- Fixed ROI:57.50–58.00N,242.00–242.50E, planetocentric/east-positive.
- Official challenge Resources actually acquired via HTTP200 HTML. The web-reader initially failed; Next flight text was decoded without executing scripts. `resourcesTabContent` points to11 resource links, including NASA PDS. `resources_links.csv` retains exact listed URLs plus canonical URLs without tracking parameters.
- Source chain: [challenge Resources](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources) → [NASA PDS](https://pds.nasa.gov/) → PDS Geosciences → [CRISM products](https://pds-geosciences.wustl.edu/missions/mro/crism.htm). The challenge names the PDS gateway, not these specific products or a validation of this analysis.

## Delivery-state update

- Final check found PR7 already MERGED at2026-11-14T19:38:25Z with old head44c2e03. This task performed no merge. New science/acquisition commits are not in verified main08d2740 and the new package is absent there.
- The original branch contains the new delivery; PR7 description links to it, but a merged PR diff cannot absorb later branch commits. `delivery_state.json` records the checked refs. No new PR was created.

## Actual acquisitions and checks

|Item|Acquired or checked|Scope and limits|
|---|---|---|
|MRDR v4 tileT1811|Original AL/SU/DE labels+headers, wavelength table,15 original band byte ranges|6 Lambert-albedo bands,3 official parameters,6 source-trace fields; not the entire72-band cube|
|Native projection|Original PDS offsets independently checked against ENVI header|Radius3,381,164.4m, grid180.4662m; no Earth or generic Mars projection|
|Native map centres|13,284 centres in fixed ROI; all retrieved fields have numeric non-sentinel values|Not full scientific-pixel QA or independent observations|
|Strict source support|13,169 also have source DDR centres in the ROI;115 remapped boundary cases excluded from strict maps|Source optical footprints, keystone and PSF are not fully established|
|Source observations|5 IDs traced to raw product metadata;2006-12-01 through2014-07-26|Not a single date or repeated independent confirmation;11,359 unique reported source tuples in strict subset, not proof of detector independence|
|Official BD1500_2|Retained original negative values, approximately−0.03692 to−0.001752|Negative does not demonstrate ice absence; no threshold or ice probability assigned|
|Documented formula|PDS July2026 reference pp1–2,5, multispectral branch|BD1500_2=.5RB1505+.5RB1558; anchors1367/1808nm, actual nearest sampled wavelengths|
|Formula/product check|Median calculated-minus-official≈+0.0007165; max absolute≈0.01935|Differences remain; no tuning or claim of full vendor-pipeline reproduction|
|TER/MTRDR|Valid ODE fixed-ROI catalogue queries each returned0|Bounded indexed-result statement; does not establish all archive data absent|
|MRDR catalogue class|Initial MRDR class invalid; official IIPT list identifiesMRDR4|ValidMRDR4 query returns134 bbox candidates; faulty source bbox prevents treating them as134 true intersections|

- The source tile EASTERNMOST_LONGITUDE=+113.32495 conflicts with projected eastern centres near−113.328. Original files remain unchanged; pixel selection uses PDS projection, independently checked against the header. An initial unnormalised bbox filter was rejected, not published as zero coverage (`index_bbox_diagnostic.json`).
- MRDR v4 catalogue documents opacity downselection, atmospheric/photometric correction, noise/smile processing and strip normalization. Correction indicators in the labels are comments, not executable per-pixel QA flags.
- Before May2012, the documented branch uses radiative-transfer inputs and MARCI aerosol estimates. After May2012, volcano-scan correction removes gases without itself correcting aerosols; subsequent normalization uses reference strips. These procedures do not supply a validated local cloud/frost mask or independent ice truth.
- The official site explicitly says greater-binning raw TRDR products are not covered by the targeted hyperspectral noise filter. A TRR3 version suffix alone is not evidence that mapping-mode noise was removed. This strengthens the earlier raw-product quality limit; MRDR v4 has its own separate processing description.
- Recalculation follows the actual multispectral formulation, not the hyperspectral1525nm kernel. Continuum interpolation is the parameter's mathematical definition; no missing measured spectral bands are filled.
- SIS §3.5.1 says MRDR v4 Lambert-albedo and summary-product strips are normalized before assembly. Product software1.03.94 and the July2026 reference may have processing differences. These are possible contexts for the measured discrepancy; its actual cause is **unknown**.
- No raw-to-corrected paired difference is claimed: the MRDR combines five observations, while the previous raw-excerpt package covered two specific strips. Overlap/reuse is tracked rather than counted as independent evidence.
- Ice presence/depth/content, cloud-versus-surface discrimination and local detector residuals remain **unknown**. AD1 stays a general-method reference; no Mars polygon tracing, Earth clock alignment or new sites.

## Files

- `resource_chain.json`, `resources_links.csv`: official-list provenance.
- `mrdr_extraction_plan.json`: exact native rows1471–1634, columns327–407 (zero-based), source bands/URLs/ranges/projection.
- `mrdr_roi_pixels.csv.gz`: all selected map centres, original source geometry/provenance, original official parameters, recalculation and unknown classification. Strict-support flag retained; no unknowns replaced by0.
- `mrdr_band_qa.csv`, `source_observations.csv`, `mrdr_qa.json`: units, periods, source products, numeric counts and interpretation limits.
- `F-RES01_MRDR_quality_and_parameters.png`: source dates, official parameter, selected AL samples and unresolved formula/product differences. Not an ice-detection map.
- `retrievals.json`: actual URLs, UTC requests, HTTP status/ranges, byte counts and SHA256. Failed/invalid queries remain distinct from successful zero-count catalogues.
- `validation.json`, `validation_retained_only.json`:90/79 actual checks; all13,284 pixel rows independently decoded using struct and ENVI-based coordinates. Scientific ice interpretation is not a passed test.

## Sources actually read

- Official challenge Resources flight block, not only a search summary.
- PDS CRISM page: derived-product descriptions, tools and Version3 reprocessing note (mapping vs targeted filtering).
- [MRDR v4 catalogue](https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/catalog/mrdr_ds.cat): processing sections, time-dependent atmospheric correction, noise filtering, strip normalization and data structure; [errata](https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/errata.txt):2022/2023 v4 entries.
- Original tileAL/SU/DE labels: IMAGE/BAND_NAME, IMAGE_MAP_PROJECTION, software/version and commented processing indicators; original ENVI header and WV table/label.
- [PDS parameter reference](https://pds-geosciences.wustl.edu/missions/mro/crism_summary_parameter_reference.pdf), July2026: PDF pages1–2 and5, plus table row BD1500_2; selected sections only.
- Previously acquired PDS SIS v1.3.7.7 §3.5.1–3.5.2, and previous raw-product inventory used as a pinned metadata join. Source IDs and segment counters match; source line/sample indexing conventions are not silently assumed.
- Sources credited to NASA/MRO CRISM, JHU/APL and PDS Geosciences Node. No blanket new license applies to original materials.

## Reproduce

- System Python with verified TLS: `acquire_resources.py`, `fetch_products.py`, `fetch_mrdr.py`, `fetch_local_labels.py`.
- `parse_resources.py` extracts the listed links without executing page scripts. `plan_mrdr.py` plans native pixel ranges; `fetch_mrdr_ranges.py` retrieves exact HTTP206 bytes.
- Scientific Python (numpy/matplotlib): `analyze_mrdr.py`, `plot_mrdr.py`. Use a writable `MPLCONFIGDIR` if necessary.
- System Python: `validate_resources.py` and `validate_resources.py --retained-only`; `refresh_resources.py` appends LV-ICE12 and request history to parent tables without changing prior records.
- If rebuilding parent tables, apply `crism/refresh_crism_evidence.py` first and `official_resources/refresh_resources.py` afterwards.
- Full original HTML/PDF, global index and large bbox-response snapshots are local-only and ignored. Original byte-range excerpts, small labels and checksums are retained; repeat URLs to restore omitted inputs. No full multi-hundred-MB MRDR image is downloaded.
