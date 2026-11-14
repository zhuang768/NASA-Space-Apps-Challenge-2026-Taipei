"""Implementation diagnostics on acquired MRDR pixels; no ice classifier or tuning."""
from pathlib import Path
import csv,json,hashlib
import numpy as np
O=Path(__file__).resolve().parent;P=O.parent/'official_resources'
plan=json.loads((P/'mrdr_extraction_plan.json').read_text());nr=164;nc=81;ns=plan['native_samples'];c0,c1=plan['roi_columns_0based']
arrays={};inputs=[]
for x in plan['requests']:
    f=P/'sources'/x['subset_file'];raw=f.read_bytes()
    assert len(raw)==nr*ns*4
    arrays[x['type'],str(x['quantity'])]=np.frombuffer(raw,dtype='<f4').reshape(nr,ns)[:,c0:c1+1]
    inputs.append(dict(path=str(f.relative_to(O.parent)),sha256=hashlib.sha256(raw).hexdigest()))
w={str(x['quantity']):x['actual_wavelength_nm'] for x in plan['requests'] if x['type']=='al'}
low=arrays['al','1367'];high=arrays['al','1808'];official=arrays['su','BD1500_2']
srclat=arrays['de','Latitude - areocentric - deg N'];srclon=arrays['de','Longitude - areocentric - deg E']%360
strict=(srclat>=57.5)&(srclat<=58)&(srclon>=242)&(srclon<=242.5)
def calc(waves,dtype):
    lo=low.astype(dtype);hi=high.astype(dtype);r=[]
    for nm in ['1505','1558']:
        a=dtype((waves[nm]-waves['1367'])/(waves['1808']-waves['1367']))
        r.append(dtype(1)-arrays['al',nm].astype(dtype)/((dtype(1)-a)*lo+a*hi))
    return dtype(.5)*(r[0]+r[1])
variants={
    'documented_CAT74_multispectral_float64':calc(w,np.float64),
    'same_CAT_formula_float32_precision_diagnostic':calc(w,np.float32),
    'nominal_wavelengths_diagnostic_not_official_replacement':calc({k:float(k) for k in w},np.float64),
    'legacy_CAT_BD1500_different_parameter_not_replacement':1-(arrays['al','1505'].astype(float)+arrays['al','1558'])/(low.astype(float)+high)}
cat=variants['documented_CAT74_multispectral_float64'];rows=[]
def stats(z):return dict(n=int(len(z)),median=float(np.median(z)),median_absolute=float(np.median(np.abs(z))),p95_absolute=float(np.percentile(np.abs(z),95)),max_absolute=float(np.max(np.abs(z))))
for name,v in variants.items():
    m=strict&np.isfinite(v)&np.isfinite(official)&(official!=65535)
    rows.append(dict(diagnostic=name,comparison='calculated minus original official BD1500_2',unit='dimensionless',**stats(v[m]-official[m]),interpretation='implementation comparison only; no scientific detection threshold'))
precision=stats((variants['same_CAT_formula_float32_precision_diagnostic']-cat)[strict])
target=arrays['de','Target ID'];groups=[]
for tid in np.unique(target[strict]):
    m=strict&(target==tid)
    groups.append(dict(target_id_hex=f'{int(tid):08x}',scope='source DDR centres inside fixed ROI',**stats((cat-official)[m]),unit='dimensionless; descriptor not calibrated error'))
ratio=1-(1-arrays['su','BD1435'].astype(float))/(1-official.astype(float))
ratio_check=stats((ratio-arrays['su','ICER1_2'])[strict])
for name,data in [('parameter_formula_diagnostics.csv',rows),('parameter_residual_by_source.csv',groups)]:
    with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=data[0].keys(),lineterminator='\n');wr.writeheader();wr.writerows(data)
q=dict(input_files=inputs,strict_source_centres=int(strict.sum()),formula_source='Official PDS CAT_v7_4_codeonly.zip: SummaryParams2014/crism_summary_bd1500_2.pro lines7–17; crism_sumutil_band_depth.pro lines47–57; July2026 reference pp1–2,5',cat_producer_binary_identity='not established; CAT is an implementation reference, not the verified MRDR1.03.94 production execution',float32_minus_float64=precision,official_ICER1_2_identity_residual=ratio_check,root_cause='unknown; diagnostics exclude some simple numerical explanations, not a replacement product',ice_presence='unknown',actual_ice_depth_m=None,ice_fraction=None,cloud_frost_mask='not validated',detection_threshold=None)
(O/'spectral_diagnostics.json').write_text(json.dumps(q,indent=2)+'\n')
np.savez_compressed(O/'spectral_diagnostic_arrays.npz',official=official,calculated=cat,residual=cat-official,strict=strict,target_id=target)
print(json.dumps({'strict':int(strict.sum()),'diagnostics':rows,'precision':precision,'official_ratio_residual':ratio_check},indent=2))
