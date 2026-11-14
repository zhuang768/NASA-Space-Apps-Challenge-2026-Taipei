"""Deterministic CRISM numeric-support audit; no wavelength or mineral inference.

Run from any cwd: python3 /path/to/this/analyze.py
Inputs are preserved main-5217401 ROI and original PDS labels two levels above.
"""
from pathlib import Path
import csv, hashlib, json, re
import numpy as np

P = Path(__file__).resolve().parent
REPO = P.parents[4]
V = P.parent.parent / 'local_validation'
ROI = V / 'crism_roi.npz'
LABEL = V / 'sources/products/msp0001565d_01_if213l_trr3.lbl'
DDR = V / 'sources/products/msp0001565d_01_de213l_ddr1.lbl'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_csv(name, rows):
    with (P/name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, list(rows[0])); w.writeheader(); w.writerows(rows)
def scalar(s, key):
    m = re.search(r'^'+re.escape(key)+r'\s*=\s*([^\r\n]+)', s, re.M)
    return m.group(1).strip().strip('"') if m else None

with np.load(ROI, allow_pickle=False) as z:
    x, lat, lon, provided = (z[k] for k in ['if_spectra','latitude','longitude','numeric_valid'])
    x, lat, lon, provided = x.copy(),lat.copy(),lon.copy(),provided.copy()
finite = np.isfinite(x)
sentinel = x == 65535
numeric = finite & (np.abs(x) < 1e20) & ~sentinel
negative = numeric & (x < 0)
assert x.shape == (55, 912)
assert np.array_equal(numeric, provided), 'Stored numeric mask does not reproduce'
rows=[]
for b in range(x.shape[0]):
    vals=x[b,numeric[b]]
    quant=np.quantile(vals,[0,.01,.5,.99,1]) if vals.size else [None]*5
    rows.append(dict(band_index_zero=b,wavelength_nm='',detector_row='',
        total_pixels=int(x.shape[1]),numeric_supported=int(numeric[b].sum()),
        sentinel_65535=int(sentinel[b].sum()),nonfinite=int((~finite[b]).sum()),
        negative_if=int(negative[b].sum()),numeric_fraction=float(numeric[b].mean()),
        min_if=quant[0],p01_if=quant[1],median_if=quant[2],p99_if=quant[3],max_if=quant[4],
        interpretation='numeric QA only; wavelength and science validity unassigned'))
write_csv('band_quality.csv', rows)
pixel=[]
for j in range(x.shape[1]):
    pixel.append(dict(roi_index_zero=j,latitude_areocentric_degN=float(lat[j]),longitude_degE=float(lon[j]),
        numeric_bands=int(numeric[:,j].sum()),sentinel_bands=int(sentinel[:,j].sum()),
        negative_if_bands=int(negative[:,j].sum()),
        all55_numeric=bool(numeric[:,j].all()),all_bands1to54_numeric=bool(numeric[1:,j].all()),
        material_class='unclassified'))
write_csv('pixel_quality.csv',pixel)
label=LABEL.read_text(); ddr=DDR.read_text()
keys=['PRODUCT_ID','PRODUCT_VERSION_ID','START_TIME','STOP_TIME','SAMPLING_MODE_ID',
 'PIXEL_AVERAGING_WIDTH','MRO:WAVELENGTH_FILE_NAME','MRO:ATMO_CORRECTION_FLAG',
 'MRO:THERMAL_CORRECTION_MODE','MRO:PHOTOCLIN_CORRECTION_FLAG',
 'MRO:SPATIAL_RESAMPLING_FLAG','MRO:SPECTRAL_RESAMPLING_FLAG',
 'MRO:HDF_SOFTWARE_NAME','MRO:HDF_SOFTWARE_VERSION_ID','MRO:IF_MIN_VALUE','MRO:IF_MAX_VALUE']
write_csv('label_processing_audit.csv',[dict(keyword=k,value=scalar(label,k),source=LABEL.relative_to(REPO).as_posix()) for k in keys])
all_invalid=~numeric.any(axis=0)
summary=dict(schema='MS02-CRISM-numeric-support-v1',base_commit='521740108050ba16e406f8becb67a786179ff8bd',
 product=scalar(label,'PRODUCT_ID'),shape=list(x.shape),
 input_roi_sha256=sha(ROI),input_roi_git_blob_sha1=hashlib.sha1(b'blob '+str(ROI.stat().st_size).encode()+b'\0'+ROI.read_bytes()).hexdigest(),
 label_sha256=sha(LABEL),ddr_label_sha256=sha(DDR),
 numeric_mask_reproduces_stored=True,numeric_values=int(numeric.sum()),total_values=int(x.size),
 numeric_fraction=float(numeric.mean()),sentinel_values=int(sentinel.sum()),
 all55_numeric_pixel_count=int(numeric.all(axis=0).sum()),all54_except_band0_numeric_pixel_count=int(numeric[1:].all(axis=0).sum()),
 zero_numeric_pixel_count=int(all_invalid.sum()),all_invalid_band_indices=np.flatnonzero(~numeric.any(axis=1)).tolist(),
 negative_if_count=int(negative.sum()),negative_band_indices=np.flatnonzero(negative.any(axis=1)).tolist(),
 negative_supported_pixel_fraction=float(negative.any(axis=0).sum()/(~all_invalid).sum()),
 pixel_bounds=dict(lat_min=float(lat.min()),lat_max=float(lat.max()),lon_min=float(lon.min()),lon_max=float(lon.max())),
 sampling_support_note='912 pixel centres in narrow northern subset; count is not area coverage or 912 independent mineral detections',
 wavelength_assignment=None,material_classification=None,ice_detection=None,
 interpretation='Numeric QA strengthened. Entire band0 missing; no complete55-band spectra. Science validity, absorption bands and material/ice identification remain unproven.',
 missing=['55 detector-row numbers appended to original IF cube (record49501,110 bytes)',
 'Exact WA calibration CDR450924300802_WA0300010L_3.IMG and its label',
 'Original scene sample/line linkage for per-pixel wavelength calibration',
 'Per-band quality masks and validated smile/atmospheric/thermal/photometric treatment',
 'Independent calibrated same-location spectral interpretation/reference'])
(P/'quality_summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
manifest=dict(base_commit=summary['base_commit'],inputs=[dict(path=str(p.relative_to(REPO)),sha256=sha(p)) for p in [ROI,LABEL,DDR]],
 artifacts=[dict(path=p.name,sha256=sha(p),bytes=p.stat().st_size) for p in sorted(P.iterdir()) if p.is_file() and p.name not in ['manifest.json','verification.json']])
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(summary,indent=2))
