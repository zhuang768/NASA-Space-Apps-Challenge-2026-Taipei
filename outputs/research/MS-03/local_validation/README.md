# MS-03 local-validation evidence package

- Scope: fixed 57.50–58.00 N, 242.00–242.50 E, Mars planetocentric/east-positive. Research notes and data only; no formal report or presentation.
- Primary tables: `local_prior_work.csv`, `mars_ice_evidence.csv`, `analog_validation.csv`, `search_log.csv` (UTF-8 with BOM).
- Source requests and failures: `retrievals.json`; source details and read scopes are retained in tables and research notes.
- Native archived thermal-model value is conditional, not an observed ice interface. Actual ice presence, depth and content remain unconfirmed locally. No new thermal fit or spectral/radar interpretation was performed.
- Five fixed CTX display samples do not establish whole-cell scientific-pixel coverage. No reliable complete Mars polygon boundaries were traced. AD1 remains a general-method reference.
- Small PDS label/RDR segments and CTX display/seam materials retain original source attribution. Source documents and metadata do not receive a new blanket license here.
- Caltech ASCII grids/Notes and publication HTML/PDF are local acquisition inputs excluded from Git; no redistribution permission is inferred. Global USGS geometry and large compressed members are also excluded. Provider checksums/ZIP CRCs, URLs and extracted numerical facts are retained.
- `acquire.py` records bounded public HTTP retrievals. Failed ScienceBase/Dataverse requests and an HTTP200 CAPTCHA are not scientific content or zero-coverage results.

## 2026-11-15 original-table supplement

- [Supplement and exact missing files](original_tables_followup/README.md), [three-table status](original_tables_followup/table_acquisition.csv), and [actual checks](original_tables_followup/validation.json).
- The three target tables remain unacquired; no fixed-cell membership or new ice result was computed. Public DataCite metadata and USGS field definitions were obtained and retained separately from observations.
- The initial local-only checkpoint was superseded by the user's authorization to push and merge. PR #7 had already merged, so this supplement is submitted as a follow-up from main `fbfa780cf587a0787739200898e80b4d27fea8d1`, preserving its CRISM updates. GitHub records the actual publication/merge status.
- If rebuilding the earlier primary tables, run `original_tables_followup/integrate_tables.py` afterwards to restore this supplement, before validation. The supplement does not regenerate the original science analysis.

## Reproduce

- Python dependencies: numpy, rasterio, shapely, pyshp, matplotlib, Pillow (tested using the existing science environment).
- Restore ignored Caltech inputs from exact URLs in `piqueux_qa.json`; verify provider MD5. `remote_geology.py` acquires original ZIP members with byte ranges and CRC checks. `acquire_ctx_samples.py` follows author KML; `acquire_sharad_sample.py` retrieves the documented original RDR ranges.
- Run `analyze.py --mars-raw-dir /path/to/data/raw/mars` after source acquisition; SWIM inputs are read-only and SHA-checked against the pinned baseline.
- Run `build_tables.py`, then `crism/refresh_crism_evidence.py`, then `official_resources/refresh_resources.py`, then `original_tables_followup/integrate_tables.py`, then `plot.py`, then `validate.py`. The latter checks this package offline using retained small inputs; full source extraction also requires the ignored large/local inputs. The supplement can be checked separately with `original_tables_followup/validate_followup.py`.
- Acquisition is sequential: the request-log append operation is not designed for parallel writers.
- `F-LV01_CTX_samples.png`: actual fixed local display patches, dates and observability limitations.
- `F-LV02_observation_support.png`: real catalogue sub-spacecraft tracks and acquired RDR geometry segment; echoes not interpreted.
- Source instrument dates/solar times are preserved as supplied. No Earth logger clock correction or Campbell–HOBO alignment is performed.

## 2026-11-15 CRISM acquisition update

- Two local I/F subsets, exact wavelength calibration and DDR geolocation are now acquired; the earlier catalogue-only status for these two products is retained in `crism/previous_catalogue_status.json` and superseded in current tables.
- Start with `crism/README.md`, `crism/qa.json` and `crism/F-CRISM01_pixel_QA_spectra.png`. Ice classification remains unknown; basic numeric checks are not final scientific validity.
- If regenerating parent tables with `build_tables.py`, run `crism/refresh_crism_evidence.py` afterwards to apply the new acquisition statuses while preserving prior history.

## Official Resources / MRDR v4 follow-up

- `official_resources/README.md` records the verified challenge→PDS source chain, acquired local corrected-band/summary data, source dates, native projection and unresolved ice interpretation.
- Official MRDR parameters and a documented multispectral recalculation are now available in that separate package. This supersedes neither the original raw-product OFF flags nor the retained historical acquisition records. Negative parameters and numeric coverage are not an ice-absence result.

## BD1500_2 disclosed-code / version audit

- `bd1500_audit/README.md` documents official CAT/JCAT source/version distinctions, numerical checks and remaining missing production files. Existing values are retained; no cause-specific correction is applied.
- When regenerating parent tables, run the prior CRISM and official-resource refresh scripts, followed by `bd1500_audit/refresh_parent.py` to retain the additive LV-ICE13 audit record.
