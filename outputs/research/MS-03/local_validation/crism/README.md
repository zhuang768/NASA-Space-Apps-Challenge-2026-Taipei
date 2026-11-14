# MS-03 acquired CRISM spectra: basic QA

- Starting branch SHA: `778af696c654a191fe2a720f24d9f30ebd7d247b`; fixed ROI unchanged.
- Products: `HSP0002DE65_03_IF218L_TRR3` (2014-02-10, Ls88.051829) and `MSP00018FDA_01_IF214L_TRR3` (2010-05-25, Ls95.410373).
- Selection: two northern-summer L-detector mapping strips with relatively low catalogue incidence angles (46.54/44.55 degrees); not a complete search of all12 available L-detector IF products or all seasons. Selection does not use an ice-signal score.
- Acquisition: original PDS3 labels; full matching DDR1; native TRR3 I/F byte ranges covering all64 samples/all channels for ROI-intersecting rows; appended detector-row tables; exact label-specified WA CDR3 images/tables.
- Two initial guessed DDR paths returned404, followed by successful exact ODE product lookups. Science-venv TLS verification failed; system Python successfully downloaded the same planned sources using certificate verification. Failures retained in `retrievals.json`; no TLS bypass.

|Product|DDR centres in ROI|Centres passing all sampled1300–2200nm numeric/calibration checks|Approx. adjacent cross-track centre spacing|
|---|---:|---:|---:|
|HSP0002DE65_03_IF218L_TRR3|1350|966|187.80m|
|MSP00018FDA_01_IF214L_TRR3|9056|8516|187.44m|

- Passing means finite I/F, not PDS65535 sentinel, finite positive non-sentinel WA wavelength; positive signal is checked separately. All966/8516 also have positive I/F in that sampled window. These are pixel counts, not area coverage, ice probabilities or validated detector independence.
- WA non-scene wavelengths explain384/540 excluded centres at the diagnostic anchor. Geometry alone includes non-scene sensor samples; an empty INVALID_PIXEL_LOCATION label is not an all-clear mask.
- No full-cell effective-area percentage is calculated. Maps display actual DDR centres, not fabricated polygons or validated per-band footprints.
- DDR longitude values are signed east longitude; modulo360 conversion is explicit. IR DDR coordinates represent wavelengths near2300nm; cross-wavelength keystone and absolute pointing errors remain uncorrected. Nominal10x binning and measured centre spacing do not establish a point-spread function or crack-detection resolution.
- TRR3 atmospheric, thermal, photometric and spectral-resampling flags are OFF. No cloud/frost mask, atmospheric inversion, per-pixel instrument residual validation or ice-detection calibration was completed.
- WA and TRR3 detector-row lists match exactly. Actual transmitted wavelengths are retained; no spectral gaps are filled. Wavelength values vary across columns.
- No standard ice index was computed. The hyperspectral5/11/5 BD1500_2 kernel is not applied as if these sparse mapping channels were contiguous; a documented mapping-mode implementation would need separate justification. No claim that a mapping-mode index is inherently impossible.
- Raw I/F depressions may include atmospheric gas absorption, clouds/frost, surface composition and instrument effects. Neither ice detection nor an ice-absence limit follows from this screening. Optical data do not measure covered subsurface ice depth/content.
- `roi_pixels.csv.gz`: per-pixel coordinates, geometry, masks and selected raw I/F values; missing values remain empty, ice classification unknown.
- `channel_qa.csv`: native-channel valid counts, wavelengths and I/F spatial percentiles. Percentiles are spatial spread, not confidence intervals.
- `anchor_channels.csv`: actual nearest channel to each requested wavelength, with wavelength mismatch exposed; not a standard ice index.
- `qa.json`: definitions, periods, geometry ranges and explicit unknowns.
- `F-CRISM01_pixel_QA_spectra.png`: actual pixel-centre map and uncorrected spectra; transmitted sample points shown without interpolation.
- `previous_catalogue_status.json`: prior catalogue-only table rows retained; updated statuses supersede only those two product rows and LV-ICE06.

## Source/read scope

- [PDS CRISM DPSIS v1.3.7.7, 2024-11-05](https://pds-geosciences.wustl.edu/mro/mro-m-crism-3-rdr-targeted-v1/mrocr_2110/document/crism_dpsis.htm): selected §§2.5.1–2.5.3 (missing data/quality),3.2.1 (DDR one-to-one relation and wavelength-dependent position),3.4.1 (TRDR IMAGE and selected detector rows),3.9.1/AppendixE (WA layout), and Table3-3 (summary-product wavelength/kernel definitions). Downloaded HTML is not a claim that every section was read.
- Original TRR3 labels: IMAGE/ROWNUM_TABLE and correction flags. Original DDR labels: IMAGE/BAND_NAME. Original WA labels: IMAGE unitNM, ROWNUM_TABLE and non-scene sentinel note.
- Exact product URLs, UTC requests, byte counts, ranges and SHA256 are in `retrievals.json`. `candidate_products.json` retains the earlier catalogue candidates and footprints.
- Sources: NASA/MRO CRISM, JHU/APL and PDS Geosciences Node; no new blanket license imposed on original materials.

## Reproduce

- Use system Python with working verified TLS for acquisition; scientific Python requires numpy/matplotlib for analysis. Do not disable certificate checks.
- `python3 acquire_crism.py`; `python3 acquire_support.py`; scientific Python `acquire_pixels.py` plans ranges offline; `python3 fetch_planned.py`; `python3 fetch_wavelengths.py`.
- Scientific Python `analyze_crism.py`, then `plot_crism.py`; set `MPLCONFIGDIR` to a writable temporary path if necessary. `python3 refresh_crism_evidence.py` updates parent tables while retaining previous entries.
- `validate_crism.py` checks retained local subsets offline; original full-DDR bytes are also checked when present. `validation.json` records actual results.
- Full DDR images (~9.68MB each) and original HTML documents are local-only, ignored from Git. Retained DDR subsets concatenate exact original row-byte segments from each BSQ backplane; original offsets and per-segment hashes are in `*_subset.json`. They are not claimed to be original contiguous files or separately fetched HTTP ranges.
- TRR3 excerpts retain exact HTTP206 bytes and original line offsets. The small WA calibration images and row tables are retained. Do not apply full-file line/record offsets directly to a cropped subset.
- No new Earth processing, Campbell–HOBO alignment, polygon tracing or radar interpretation is performed.
