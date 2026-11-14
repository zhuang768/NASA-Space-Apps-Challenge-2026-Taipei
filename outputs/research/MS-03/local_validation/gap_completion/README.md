# MS-03: bounded gap-completion evidence

- Date: 2026-11-15, Asia/Taipei.
- Starting main: `ddd04cfcb5ea810d73304b1cf6ae064c1f77a1c5`.
- Working branch: `codex/ms03-gap-completion-20261115`; isolated clone; no edits to the concurrent parent working tree.
- Fixed cell: 57.50–58.00°N, 242.00–242.50°E, planetocentric/east-positive. No new site or moved boundary.
- Scope: source data, calculation diagnostics, figures, structured judgments and bullet handoff notes. No formal report, abstract, conclusion prose or slides.

- Concurrent main integrated at `521740108050ba16e406f8becb67a786179ff8bd`: existing `bd1500_audit/`, `production_history/` and `t1811_run_artifacts/` records are retained. Overlapping CAT diagnostics here are a cross-check, not an additional independent scientific result. Their documented extra summary optimization explains why delivered AL/SU need not preserve a simple formula relationship; exact T1811 run attribution remains unknown.
- Our precision perturbation uses a specified narrow expression variant; its ~1.26e-7 maximum and the earlier audit's broader ~1.35e-7 result are not identical test definitions. Neither is a bound on every producer operation.
- Original archival source bytes, including whitespace/line endings, are preserved; local attributes disable text normalization/style whitespace checks only for `sources/`.

## Read first

|Evidence|Actual addition|Limit|
|---|---|---|
|[Gap and handoff table](gap_status.csv)|All six outstanding topics have an explicit status and next requirement|A completed check does not mean an uncertainty is resolved|
|[MOC figure](F-GAP01_MOC_in_cell_review.png)|Actual processed S1700607_NA pixels, 2006-04-08; three fixed in-cell review windows|3.00034 m projected grid is not effective resolution; no reliable closed-boundary dataset|
|[Spectral diagnostic figure](F-GAP02_spectral_implementation_QA.png)|Official CAT reference functions and precision/formula checks on existing MRDR bytes|Not the verified producer execution; no ice classifier or detection limit|
|[Radar/clutter figure](F-GAP03_same_track_radar_clutter.png)|Same-observation US radargram and combined clutter pixels; 65 in-cell GEOM centres|Clutter predicts timing, not calibrated power; no subtraction or ice-depth inversion|
|[Original author catalogue summary](daubar2022_summary.json)|1,203 dated new-impact records parsed; zero point records inside this cell|Not all impacts, not all image footprints, not Dundas2021 Table S4, not absence of ice|
|[Evidence table](mars_ice_evidence.csv)|Separate measurements, products, calculations and unknowns|Actual ice presence, depth and content remain unknown|
|[Morphology comparability](morphology_comparability.csv)|Separate source support and missing Mars boundaries|No Earth/Mars distribution comparison is computed|
|[Analogue disposition](analog_validation.csv)|AD1 remains method-only; UV remains known-interface/data-QA reference|No Mars geometry distribution or Campbell–HOBO join|

## Provenance and reading scope

- [Retrievals](retrievals.json): 52 actual public HTTP attempts, UTC, original URL, response status, size and SHA256. A successful request alone does not validate content.
- `requests_round*.json`: exact bounded requests. Ranges in round13 reproduce the two original radar byte excerpts.
- [Reading log](source_read_log.csv): actual source sections, coordinate conventions and scope restrictions.
- [Search log](search_log.csv): additional web queries and failure states; historical queries remain in the parent log.
- `sources/Daubar_2022_catalog_tableS1.xlsx`: author release DOI `10.5281/zenodo.6604912`, CC-BY-4.0; checksum matches the provider. Original worksheet headers are preserved in the summary. Their parenthetical E/N labels conflict with the variable names; official HiRISE PSP_007561_1290 confirms the latitude/longitude orientation. Event coordinates need not equal the image centre.
- `sources/s1700607_na.lbl`: original PDS product geometry and quality flag. Original IMG checksum and PDS pixel sum were verified during extraction. The full 28.8 MB image is local-only and reproducible from its exact public URL; retained crop and review tiles preserve original RDR DN without sharpening or interpolation.
- MOC image checksum is for the complete downloaded file. Its label footprint bounds include padded image margins; retained nonzero-centre bounds need not equal those footprint extrema. The ODE 0–360 `Footprint_geometry` is used explicitly; `Footprint_C0_geometry` uses negative longitudes and is not silently substituted.
- `sources/edr_to_usrdr.csv`: official crosswalk. Four of the six earlier Italian RDR IDs have an exact US counterpart in this downloaded crosswalk; no counterpart was found there for R_1768301 or R_5476301. This is a crosswalk result, not proof of archive-wide absence.
- US GEOM coordinates are planetocentric/east-positive per the official processing document. Clutter `SpacecraftLat` is geodetic; it is not used for fixed-cell membership. `Column` is one-based; `NadirLine`/`FirstLine` are zero-based in the producer's Python example (guide PDF p20 / printed p19).
- The S_00796502 centre track misses the fixed cell even though its earlier catalogue footprint intersects it. S_04624502, S_06059201 and S_05882501 have 65, 64 and 65 centre records inside, respectively. Only S_04624502 radar pixels are analysed here. Centre membership does not confine the radar scattering footprint to the cell.
- Raw CAT ZIP/code, publisher HTML and complete PDFs are ignored, not relicensed or redistributed. Member hashes and reading locators are retained. CAT source was inspected and translated into explicit numerical diagnostics; IDL was not executed and MRDR producer binary 1.03.94 was not reproduced.
- Clutter guide §§1.1–1.3, 2.1–2.3, 3.1–3.2 and Appendix B were read. It expressly disallows power subtraction and notes missing clutter due to source topographic resolution/interpolation. The simulation is a model, not a second observation.

## What remains unresolved

- No validated closed Mars polygon boundaries; no AD1 geometry distribution, shared genesis, or specific pairing. Three fixed MOC windows were visually inspected, not the whole cell at full resolution.
- No validated in-cell ice reflector, dielectric inversion, independent shallow interface depth or ice fraction. SHARAD's 15 m vacuum range resolution cannot validate a conditional ~0.10 m thermal-model interface. Native delay sampling is not resolving power.
- MRDR formula/official residual remains unexplained. Float precision alone is insufficient; changing to a different historical parameter is not a correction. Local cloud/frost/instrument QA, calibrated detection limits and producer processing identity remain unresolved.
- Cohen-Zada2024 original data/header tables, Levy2009 full S1 and Dundas2021 full S4 remain unacquired. New alternate official routes returned 403/404; membership remains unknown. Daubar2022 has different inclusion rules and is not a replacement for these originals.
- UV original logger/calibration/deployment-clock files remain missing. No clock shift, cross-logger join, lag/diffusivity estimate, or Earth-to-Mars depth inversion was performed.
- Research contribution supported here: fixed-cell source tracing, real-data retrieval, coordinate/processing QA and bounded observability evaluation. No first-site, first-analogue, exhaustive novelty clearance or confirmed Mars ice claim.

## Reproduce

Python standard library is sufficient for acquisition and the original XLSX cached-cell parser. Scientific diagnostics/figures require NumPy, Pillow, Matplotlib and Shapely (`requirements.txt`). No shared environment is modified.

1. Acquire only the desired `requests_roundN.json` using `acquire.py`. The complete MOC IMG, CAT ZIP and PDF/HTML files are optional local inputs, not prerequisites for offline retained-evidence validation.
2. `analyze_catalogue.py`: verifies the author MD5, preserves original row IDs/headers/flags, and tests impact-point membership. It does not infer image-footprint non-overlap.
3. `analyze_moc.py`: requires the acquired full IMG, verifies PDS checksum, decodes declared unsigned pixels and masks ROI pixel centres using the native Mars spherical stereographic projection. No feature tracing.
4. `analyze_spectra.py`: uses the existing committed MRDR byte excerpts and actual wavelength definitions; does not change the original values.
5. `analyze_radar.py`: verifies the retained official range bytes/grid dimensions and extracts only strict GEOM-centre columns. No echo-to-depth conversion.
6. `make_figures.py`: renders the retained data with explicit display-only transformations; original arrays are preserved. Radar panels use separate relative-power scales; they must not be subtracted.
7. `validate_gap.py`: offline CSV/JSON, source-byte, geometry, missing-value and preservation checks. No branch-name assumption, credentials or missing ignored-response requirement. `finalize_delivery.py` refreshes evidence notes, logs and manifests; no Git or network mutation.

Actual publication/merge status is recorded by GitHub. Historical PR #7 and PR #15 were already merged; this is a separate main-based supplement.

## Executed verification

- Local evidence checks:57 passed, including the optional complete MOC checksum/source-pixel comparison.
- Fresh detached checkout with20 ignored payloads absent:56 retained-evidence checks passed. The catalogue, spectral, radar and figure scripts executed using only retained inputs; scientific tables/arrays/figures were byte-identical. See `validation_retained_only.json` for the tested commit.
- Earlier validators:26 and35 checks passed; concurrent-main retained validators:33,52 and67 checks passed. Their stored files were restored byte-for-byte after execution. These checks validate provenance/reproduction, not ice detection or analogue performance.
- All three figures were actually opened; footprint convention, caption clipping, tick crowding and legend placement were checked and corrected.
