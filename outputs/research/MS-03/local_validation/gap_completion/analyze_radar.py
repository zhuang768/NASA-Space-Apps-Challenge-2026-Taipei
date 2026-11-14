"""Same-US-observation echo/clutter crop and coordinate QA. No ice/depth inversion."""
from pathlib import Path
import numpy as np,csv,json,hashlib,re,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;S=O/'sources';plan=json.loads((O/'radar_extraction_plan.json').read_text());k='04624502';n=plan['samples_per_row'];a,b=plan['source_rows_0based_inclusive'];cols=np.array(plan['roi_columns_1based'])-1
geom=list(csv.reader((S/f's_{k}_geom.tab').open()));ret=list(csv.DictReader((S/f's_{k}_rtrn.csv').open()));data={};inputs=[]
for name,fn in [('observed',f's_{k}_rgram_rows.bin'),('simulated',f's_{k}_sim_combined_rows.bin')]:
 raw=(S/fn).read_bytes();assert len(raw)==(b-a+1)*n*4
 data[name]=np.frombuffer(raw,dtype='<f4').reshape(b-a+1,n)[:,cols]
 assert np.isfinite(data[name]).all() and np.min(data[name])>=0
 inputs.append(dict(path='sources/'+fn,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
# Confirm exact sample dimensions and combined simulation object offset from original XML.
root=ET.parse(S/f's_{k}_sim.xml').getroot();ns={'p':'http://pds.nasa.gov/pds4/pds/v1'}
arrays=root.findall('.//p:Array_2D_Image',ns);assert len(arrays)==3
assert int(arrays[2].find('p:offset',ns).text)==plan['simulation_combined_array_offset']
assert [[int(e.text) for e in ar.findall('p:Axis_Array/p:elements',ns)] for ar in arrays]==[[3600,n]]*3
rtrn=[ret[c] for c in cols];nadir=np.array([int(r['NadirLine']) for r in rtrn]);first=np.array([int(r['FirstLine']) for r in rtrn]);rows=[]
for c,nd,fr in zip(cols,nadir,first):
 g=geom[c];assert int(g[0])==c+1 and int(ret[c]['Column'])==c+1
 lat=float(g[2]);lon=float(g[3])%360;assert 57.5<=lat<=58 and 242<=lon<=242.5
 rows.append(dict(column_1based=c+1,utc=g[1],latitude_deg_planetocentric=lat,longitude_deg_E=lon,model_nadir_row_0based=int(nd),model_first_return_row_0based=int(fr),source='official GEOM v2 for position; same-observation rtrn for model rows',ice_presence='unknown'))
with (O/'radar_roi_columns.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
# Power maximum is a descriptive index only: neither fitted surface nor subsurface pick.
maxrow=np.argmax(data['observed'],axis=0)+a
q=dict(product_id='S_04624502_RGRAM',clutter_product='s_04624502_sim.img combined array',source_observation_utc=[rows[0]['utc'],rows[-1]['utc']],source_inputs=inputs,array_shape=list(data['observed'].shape),strict_roi_centre_count=len(cols),columns_1based=[int(cols[0]+1),int(cols[-1]+1)],original_rows_0based=[a,b],row_sampling_us=.0375,sampling_is_range_resolution=False,native_USRDR_bandwidth_MHz=10,vacuum_range_resolution_m=15,typical_material_vertical_resolution_m='5–8 per official processing document; depends on dielectric model, not local measurement',maximum_power_row_minus_model_nadir_min_max=[int(np.min(maxrow-nadir)),int(np.max(maxrow-nadir))],maximum_is_not_subsurface_pick=True,coordinates='GEOM planetocentric/east-positive; rtrn geodetic latitude never used for ROI membership',index_convention_source='Clutter user guide PDF p20 (printed19), Python example: Column minus1; NadirLine/FirstLine used directly as zero-based array indices',membership_scope='65 footprint centres inside ROI; off-nadir scattering extends outside ROI',simulation_is_independent_observation=False,amplitude_subtraction_allowed=False,quality_limit='Simulation predicts timing, not calibrated amplitude; 128ppd MOLA DSM interpolation can omit actual clutter. No validated subsurface reflector, SNR/detection calibration or dielectric inversion.',ice_presence='unknown',actual_ice_depth_m=None,ice_fraction=None)
(O/'radar_summary.json').write_text(json.dumps(q,indent=2)+'\n')
np.savez_compressed(O/'radar_local_arrays.npz',**data,nadir=nadir,first=first,column_1based=cols+1,row_0based=np.arange(a,b+1));print(json.dumps(q,indent=2))
