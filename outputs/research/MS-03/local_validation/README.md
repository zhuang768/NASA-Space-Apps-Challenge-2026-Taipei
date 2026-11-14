# MS-03 local-validation evidence package

- Scope: fixed 57.50–58.00 N, 242.00–242.50 E, Mars planetocentric/east-positive. Research notes and data only; no formal report or presentation.
- Primary tables: `local_prior_work.csv`, `mars_ice_evidence.csv`, `analog_validation.csv`, `search_log.csv` (UTF-8 with BOM).
- Source requests and failures: `retrievals.json`; source details and read scopes are retained in tables and research notes.
- Native archived thermal-model value is conditional, not an observed ice interface. Actual ice presence, depth and content remain unconfirmed locally. No new thermal fit or spectral/radar interpretation was performed.
- Five fixed CTX display samples do not establish whole-cell scientific-pixel coverage. No reliable complete Mars polygon boundaries were traced. AD1 remains a general-method reference.
- Small PDS label/RDR segments and CTX display/seam materials retain original source attribution. Source documents and metadata do not receive a new blanket license here.
- Caltech ASCII grids/Notes and publication HTML/PDF are local acquisition inputs excluded from Git; no redistribution permission is inferred. Global USGS geometry and large compressed members are also excluded. Provider checksums/ZIP CRCs, URLs and extracted numerical facts are retained.
- `acquire.py` records bounded public HTTP retrievals. Failed ScienceBase/Dataverse requests and an HTTP200 CAPTCHA are not scientific content or zero-coverage results.

## Reproduce

- Python dependencies: numpy, rasterio, shapely, pyshp, matplotlib, Pillow (tested using the existing science environment).
- Restore ignored Caltech inputs from exact URLs in `piqueux_qa.json`; verify provider MD5. `remote_geology.py` acquires original ZIP members with byte ranges and CRC checks. `acquire_ctx_samples.py` follows author KML; `acquire_sharad_sample.py` retrieves the documented original RDR ranges.
- Run `analyze.py --mars-raw-dir /path/to/data/raw/mars` after source acquisition; SWIM inputs are read-only and SHA-checked against the pinned baseline.
- Run `build_tables.py`, then `plot.py`, then `validate.py`. The latter checks this package offline using retained small inputs; full source extraction also requires the ignored large/local inputs.
- Acquisition is sequential: the request-log append operation is not designed for parallel writers.
- `F-LV01_CTX_samples.png`: actual fixed local display patches, dates and observability limitations.
- `F-LV02_observation_support.png`: real catalogue sub-spacecraft tracks and acquired RDR geometry segment; echoes not interpreted.
- Source instrument dates/solar times are preserved as supplied. No Earth logger clock correction or Campbell–HOBO alignment is performed.

## 2026-11-15 CRISM acquisition update

- Two local I/F subsets, exact wavelength calibration and DDR geolocation are now acquired; the earlier catalogue-only status for these two products is retained in `crism/previous_catalogue_status.json` and superseded in current tables.
- Start with `crism/README.md`, `crism/qa.json` and `crism/F-CRISM01_pixel_QA_spectra.png`. Ice classification remains unknown; basic numeric checks are not final scientific validity.
- If regenerating parent tables with `build_tables.py`, run `crism/refresh_crism_evidence.py` afterwards to apply the new acquisition statuses while preserving prior history.
