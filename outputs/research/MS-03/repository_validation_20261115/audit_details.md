# MS-03 independent validation

Audit date: 2026-11-15, Asia/Taipei. **Completion type B:** the bounded audit is complete; the proposed scientific comparison has not passed.

The repository supports reproducible image-support checks and published AD1 vector geometry, but it does not supply qualified, comparable sets of in-box Mars and Earth polygon contours. Cape Blossom's source files and claimed calculations were not found in the audited GitHub records.

| Decision | Status | What was verified |
|---|---|---|
| Earth contour validation | limited | AD1 contains 185 valid closed source polygons and reproducible geometry. Independent outline accuracy remains unverified. Cape Blossom specifically is insufficient. |
| In-box Mars-to-Earth comparison | insufficient | No accepted Mars outline population under the fixed sampling and traceability rules. |
| Novelty | insufficient | Prior AD1 Earth/Mars geomorphometry is recorded. A new Cape Blossom/MS-03 quantitative comparison is not established. |

## Versions and source availability

- Main actually read: `07dbe29203504ba0ccde5e379f42ecc16e4b1b4f`, 1,307 tracked files.
- PR #26 actually read: `ac39ed6810156feefd97f60647b95b754210a7da`, 1,114 tracked files. It was open and unmerged in the saved API snapshot, with base `1506ede572435588eb5e64f95f24639279b77e56`.
- The main/PR comparison covers 625 MS-03-related paths: 561 identical blobs, seven different blobs, 18 main-only paths and 39 PR-only paths. These are head-tree differences, not the PR's base-to-head change count. All morphology and local-validation inputs used in this audit are identical between those two snapshots.
- All 42 published branch-head trees were searched. A history pathname scan and nine unique ZIP/XLSX member inventories supplement text and pathname searches. Inaccessible or deleted commits are outside this bounded inventory.
- Eleven original numerical inputs exist on GitHub archival branches. This audit extracted them from `8f666d878fe0a3d97e41daa64fab43660174652f` and verified every byte count and SHA-256 against main's `config/raw_inputs_manifest.json`. They were used only after exact agreement. Their absence at main's raw-file paths was recorded; no external source was downloaded.
- Two Releases contain 226 asset records. Only three small metadata assets were downloaded: `EARTH-RAW-README.md`, `earth_inventory.csv` and `SHA256SUMS.txt`, totaling 34,091 bytes. The Earth inventory has 222 rows, including an ESA file explicitly not mirrored. No candidate-specific polygon imagery or annotation package is listed. Large Earth payloads and the 491,292,776-byte terrain archive were not downloaded or verified.
- The root `release_manifest.json` has a stale README hash. It does not certify the newer Cape Blossom claims. Exact Git commits and blob hashes govern this audit.

## Numerical checks actually executed

The requested `final_candidates.csv`, `COMPUTATION.md` and `numerical_validation.json` were read first. Seventy MS-03 numerical fields were independently recomputed from the 11 archived source products. All 70 match the retained fields within an absolute tolerance of `1e-10`.

These checks include longitude conversion, MOLA elevation/slope/relief, TES infill exclusion, both SWIM depth-zone summaries, nearest-native dust cells and same-bin MCS temperature contrasts. They do not repeat global candidate selection or validate polygons, local ice or engineering performance. The repository's recorded global validation was read; its full global Pareto/reselection procedure was not rerun.

Key reproduced values are mean MOLA slope 0.1627532209 degrees, relief 76 m, 79 of 100 non-infill TES cells and shallow SWIM consistency mean 0.9109040236. MOLA's finite grid cells can include interpolated values. TES thermal inertia is a different quantity from surface temperature. SWIM consistency is neither ice fraction nor calibrated probability, and its two depth maps share evidence.

Full field-level results and source locators are in `numeric_audit/ms03_numeric_checks.csv`. Exact archived inputs are documented in `numeric_audit/input_receipt.json`.

## Fixed image protocol and observations

The existing five CTX windows and three MOC windows were fixed before this audit's image review. Acceptance required all of the following:

- At least eight map samples across the narrowest dimension.
- At least three repeatably identifiable bends or intersections.
- At least two adjacent, completely traceable closed units.

No missing edges were inferred. No sharpening, interpolation, smoothing or new segmentation was applied. All eight full windows and the existing native D01 crop were opened. The images show tonal variation and fine surface texture, but no closed-unit set could be accepted under this rule. No independent blinded second-reader experiment was performed.

All window coordinates, source pixel ranges, observed areas and decisions are retained in `mars_audit/windows.csv`. The eight fixed windows and supplemental D01 crop are all marked `not_accepted`. Polygon width, area and density are `NA`. The count of zero accepted measurements does not mean zero polygons exist in the box.

## Four different meanings of coverage

| Quantity | Recomputed result | Meaning and limit |
|---|---:|---|
| Defined spherical ROI area | 468.710798 km² | Fixed box on the MOC label's sphere, radius 3,396,190 m. This is an area convention, not positional accuracy. |
| CTX catalogue corner union | 100% nominal containment | Three sparse corner polygons jointly contain the box. This is not actual valid-pixel coverage. |
| Retained nonzero MOC support | 9,272,742 samples; 71.140712 km²; 15.177955% | Counted across the retained masked PNG and corrected for local polar map scale. Nonzero is an encoding/support test, not feature QA. |
| Three fixed MOC windows reviewed | 6.033449 km²; 1.287244% | Three 512 × 512 native-DN windows, byte-exact crops of the retained PNG. |
| Five fixed CTX windows reviewed | 9.661103 km²; 2.061208% | Five 256 × 256 display tiles; 327,680 opaque pixels. Alpha opacity is not instrument QA. |
| Area with accepted polygon measurements | NA | No accepted contours. It is not a measured zero-area polygon population. |

CTX and MOC supports overlap. Their areas must not be added as unique combined coverage. Full-strip MOC feature inspection and a full-box survey were not performed.

### MOC

Product `S1700607_NA` was observed on 2006-04-08, from 00:22:40.473 to 00:22:50.285 UTC. The retained label specifies planetocentric latitude, east-positive longitude and north polar stereographic projection. Map spacing is 3.000339463 m. Corresponding local ground spacing across the box is approximately 2.7654 to 2.7724 m; neither is a verified optical resolution. Original summing was 3 × 3.

Producer quality ID `1000000000` records complete pointing-kernel coverage and no extraction repair flags. It does not certify polygon detectability. The full original IMG is absent from the audited trees, so full original-RDR parsing and checksum reproduction were not executed. The retained masked PNG, source label, count, geolocation and fixed-window byte equality were checked separately.

### CTX

The KML display tiles have approximately 5.41 to 5.45 m display sampling while their source products have nominal sampling around 6.08 to 6.09 m. Rendering onto a smaller display grid adds no optical detail. Their source dates are mixed, and the tiles are not a synchronized repeat-imaging experiment.

The D01 native subset is genuinely stored: 1,024 × 5,056 unsigned 8-bit SQROOT samples, or 5,177,344 decompressed bytes. Its hash and 1,024-square displayed crop reproduce exactly. The values remain uncalibrated and visibly striped. The corner-based bilinear locator is approximate, so its precise ground area is `NA`.

The three CTX catalogue footprints' individual stored fractions reproduce using the documented clip-then-LAEA procedure. Reversing projection and clipping changes sparse-corner estimates by about seven to eight percentage points. This sensitivity reinforces why these polygons cannot substitute for valid-pixel masks.

### HiRISE

The retained 305-row latitude-eligible extract gives zero fixed-box bounding-box intersections. All 615 legacy flagged rows exclude the box by latitude. The superseded statement “615 positions unknown” was not restored. The full cumulative TAB is absent, so a fresh complete-index reparse was not executed. Zero retained catalogue hits do not prove that a landform is absent.

## Earth reference and common-scale limits

The AD1 ZIP contains 185 valid, single-part Polygon records, each with one explicitly closed ring. Its PRJ declares WGS84 / UTM Zone 33N in metres. Its bytes are identical on main and PR #26.

Independent recalculation reproduces all 185 retained areas, perimeters, equivalent-circle diameters and circularities exactly. Maximum differences in minimum rotated-rectangle width and length are 0.002243 m and 0.003001 m, respectively; these small implementation differences are disclosed. The current rerun also logged geometry-library runtime warnings in `earth_audit/geometry_warnings.json`. Every reported metric remained finite and positive; the warning cause is unknown. Numerical readback does not independently validate the original mapping accuracy.

Median area is 268.360572 m². Median minimum Feret width is 16.340278 m. The latter is a global caliper span and an upper bound on local narrow widths. A failure of that upper bound is a sufficient reason to reject a shape under the eight-sample rule; passing it is insufficient to accept an image contour.

- At nominal CTX 6 m sampling, 184 of 185 source outlines fail the 48 m necessary width bound. One is merely not excluded by size.
- At MOC local ground sampling, 152 of 185 fail the approximately 22.123 to 22.179 m bound. Thirty-three are merely not excluded by size.

These are analytical size bounds, not recognition rates. They have no sampling-grid origin to vary. No real-image degradation, brightness-contrast, anonymous retracing, independent IoU or repeat-flight experiment was possible without a source Earth raster and independent labels.

The AD1 source XML contains a stale longitude box around 16.36°E. The actual geometry, transformed using its declared CRS, lies at 15.913914 to 15.933673°E and 78.184157 to 78.188066°N. Actual coordinates were used. The DBF has no persistent FID, so source ZIP hash plus 1-based shapefile record order defines the output identity.

Cape Blossom's claimed 1,927 centres, 400 grid offsets and associated calculations occur in the current main narrative. The underlying centre coordinates, closed annotations, georeferenced imagery, second flight and numeric outputs were not located in the searched records. A DOI link was treated as a citation, not as archived source bytes. A centre-point set could not validate outline areas or IoU even if it were supplied.

## Existing use, ice and novelty

The AD1 ZIP's embedded original metadata and `local_prior_work.csv`, row `LV-PW06`, record published Svalbard/western-Utopia polygon geomorphometry. The four retained named Mars product rows are outside MS-03. They were not substituted for in-box imagery. The original paper is not stored, and no missing full text was claimed as read.

This audit adds fixed-box support checks, explicit window acceptance, numeric readback and AD1 size bounds. It does not establish a first Earth/Mars analogue or a new Cape Blossom comparison. Novelty remains insufficiently documented.

Shape alone cannot distinguish thermal contraction from desiccation, tectonic or other origins. Ice existence, depth and content each require separate, colocated evidence. Neither Earth polygon geometry, positive SWIM consistency nor low regional slope supplies that truth.

No Campbell/HOBO alignment, Earth-derived Mars ice-depth inversion, Phoenix substitution, new site or new scientific qualification threshold was used.

## Missing tests and evidence

`unmeasured_items.csv` lists ten specific blockers. Independent Earth outline accuracy, two-flight registration, real-image degradation, brightness contrast, the claimed Cape offset experiment, an accepted Mars contour population and common-scale distribution comparison remain unexecuted or insufficient. The missing full native images and optical-resolution/registration fields are explicit. None of these tests is labeled pass.

No repository, PR, website or total report was changed. No commit, push or merge was created.
