"""Read-only independent check of CRISM support tables against pinned ROI bytes."""
from pathlib import Path
import csv,hashlib,json
import numpy as np
P=Path(__file__).resolve().parent; V=P.parent.parent/'local_validation'
b=(V/'crism_roi.npz').read_bytes()
checks=[]
def check(name,passed):
 checks.append(dict(check=name,passed=bool(passed)))
def read(name):return list(csv.DictReader((P/name).open()))
check('exact_git_input_blob',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()=='c4cf29f4a9c86bbd48a268eaf47920d417b0b6fd')
z=np.load(V/'crism_roi.npz',allow_pickle=False);x=z['if_spectra']
check('shape55by912',x.shape==(55,912))
valid=(x!=65535)&np.isfinite(x)&(abs(x)<1e20)
band=read('band_quality.csv');pix=read('pixel_quality.csv');s=json.loads((P/'quality_summary.json').read_text())
check('band_support_reconciles',len(band)==55 and all(int(r['numeric_supported'])==int(valid[i].sum()) and int(r['sentinel_65535'])==int((x[i]==65535).sum()) and int(r['negative_if'])==int(((x[i]<0)&valid[i]).sum()) for i,r in enumerate(band)))
check('pixel_support_reconciles',len(pix)==912 and all(int(r['numeric_bands'])==int(valid[:,i].sum()) and int(r['sentinel_bands'])==int((x[:,i]==65535).sum()) and float(r['latitude_areocentric_degN'])==float(z['latitude'][i]) and float(r['longitude_degE'])==float(z['longitude'][i]) for i,r in enumerate(pix)))
check('no_fabricated_wavelength_or_mineral',all(r['wavelength_nm']=='' and r['detector_row']=='' for r in band) and all(r['material_class']=='unclassified' for r in pix) and s['material_classification'] is None and s['wavelength_assignment'] is None)
check('completeness_counts',s['all55_numeric_pixel_count']==0 and s['all54_except_band0_numeric_pixel_count']==890 and s['zero_numeric_pixel_count']==22 and s['all_invalid_band_indices']==[0])
check('negative_if_preserved_not_clipped',s['negative_if_count']==43 and s['negative_band_indices']==[9] and float(band[9]['min_if'])<0)
check('processing_flags_uninvented',all(r['value']=='OFF' for r in read('label_processing_audit.csv') if r['keyword'] in ['MRO:ATMO_CORRECTION_FLAG','MRO:THERMAL_CORRECTION_MODE','MRO:PHOTOCLIN_CORRECTION_FLAG']))
manifest=json.loads((P/'manifest.json').read_text())
check('manifest_inputs_match_bytes',all(hashlib.sha256((P.parents[4]/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in manifest['inputs']))
out=dict(scope='numeric support and provenance only',checks=checks,all_checks_passed=all(c['passed'] for c in checks),scientific_material_gap_closed=False,
 remaining_blocker='Exact wavelength/row/sample linkage, validated quality and atmospheric/photometric treatment are unavailable; surface material and ice remain unclassified.')
(P/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
assert out['all_checks_passed']
