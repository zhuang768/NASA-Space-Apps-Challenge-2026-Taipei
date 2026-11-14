"""Audit disclosed reference equations; not execution of IDL or MRDR production software."""
from pathlib import Path
import numpy as np,csv,json,re,hashlib,zipfile
O=Path(__file__).resolve().parent;P=O.parent/'official_resources';plan=json.loads((P/'mrdr_extraction_plan.json').read_text());z=np.load(P/'mrdr_selected_arrays.npz');inside=z['source_inside'];shape=inside.shape;r0,r1=plan['roi_rows_0based'];c0,c1=plan['roi_columns_0based'];w={str(x['quantity']):x['actual_wavelength_nm'] for x in plan['requests'] if x['type']=='al'}
# Explicit CAT port: hyper is false -> nearest single bands; actual sampled wavelengths.
def cat_multi(dtype):
 L=z['AL_1367'].astype(dtype);H=z['AL_1808'].astype(dtype);ans=[]
 for target in ['1505','1558']:
  WL,WC,WH=map(dtype,[w['1367'],w[target],w['1808']]);a=dtype((WC-WL)/(WH-WL));b=dtype(1)-a;ans.append(dtype(1)-z['AL_'+target].astype(dtype)/(b*L+a*H))
 return dtype(.5)*ans[0]+dtype(.5)*ans[1]
cat64=cat_multi(np.float64);cat32=cat_multi(np.float32).astype(float);ref=z['recalculated_BD1500_2'];official=z['official_BD1500_2'];roundoff=cat32-cat64;d=cat64-official
su={}
for x in plan['requests']:
 if x['type']=='su':su[str(x['quantity'])]=np.fromfile(P/'sources'/x['subset_file'],dtype='<f4').reshape(shape[0],plan['native_samples'])[:,c0:c1+1].astype(float)
identity=1-(1-su['BD1435'])/(1-su['BD1500_2']);identity_delta=identity-su['ICER1_2'];f32identity=(np.float32(1)-(np.float32(1)-su['BD1435'].astype('f4'))/(np.float32(1)-su['BD1500_2'].astype('f4'))).astype(float)
lbl=(P/'sources/t1811_mrrsu_60n243_0327_4.lbl').read_text();hdr=(P/'sources/t1811_mrrsu_60n243_0327_4.hdr').read_text();a=re.findall(r'"([^"]+)"',re.search(r'BAND_NAME\s*=\s*\((.*?)\)\s*MISSING_CONSTANT',lbl,re.S)[1]);b=[x.strip() for x in re.search(r'band names\s*=\s*\{([^}]+)',hdr,re.S)[1].split(',')]
point_results=[]
for x in json.loads((O/'point_checks.json').read_text()):
 local=(O/x['file']).read_bytes();big=(O/x['compare_range_file']).read_bytes();offset=((x['map_row_0based']-r0)*plan['native_samples']+x['map_col_0based'])*4;point_results.append({**x,'matches_retained_bytes':local==big[offset:offset+4]})
def stats(v):return dict(n=int(v.size),median=float(np.median(v)),max_abs=float(np.max(np.abs(v))),p05=float(np.percentile(v,5)),p95=float(np.percentile(v,95)))
source=[]
for row in csv.DictReader((P/'source_observations.csv').open(encoding='utf-8-sig')):
 mask=inside&(z['target_id']==int(row['target_id_decimal']));v=d[mask];iv=identity_delta[mask];source.append(dict(source_product=row['product_id'],source_date=row['utc_start'],strict_pixels=int(mask.sum()),BD1500_recalculated_minus_official_median=float(np.median(v)),BD1500_difference_p05=float(np.percentile(v,5)),BD1500_difference_p95=float(np.percentile(v,95)),BD1500_difference_max_abs=float(np.max(abs(v))),ICER_identity_difference_max_abs=float(np.max(abs(iv))),interpretation='Source-group association only; source, position, era and processing are confounded; not causal or an ice indicator'))
with (O/'source_group_residuals.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=source[0].keys());wr.writeheader();wr.writerows(source)
np.savez_compressed(O/'diagnostic_arrays.npz',cat64_minus_official=d,float32_minus_float64=roundoff,ICER_identity_minus_official=identity_delta,source_inside=inside,target_id=z['target_id'])
q=dict(starting_main_sha='fbfa780cf587a0787739200898e80b4d27fea8d1',units='dimensionless summary-index differences; map-centre counts are not independent observations',input_provenance='official_resources/manifest.json and original MRDR URL/member locators in version_comparison.csv',cat_port_not_original_runtime=True,production_1_03_94_source_obtained=False,original_scientific_data_modified=False,ice_status='unknown',cause_of_production_residual='unknown',all_map_cells=int(inside.size),strict_source_cells=int(inside.sum()),reference_port_minus_existing_calculation=stats((cat64-ref)[inside]),float32_minus_float64=stats(roundoff[inside]),cat64_minus_official_all=stats(d),cat64_minus_official_strict=stats(d[inside]),ICER_identity_minus_official=stats(identity_delta[inside]),ICER_float32_perturbation=stats((f32identity-identity)[inside]),header_label_band_order_identical=a==b,band_count=len(a),BD1500_band_index_0based=a.index('BD1500_2'),point_checks=point_results,limits=['CAT7.4 disclosed formula is not evidence of the exact MRDR1.03.94 caller/build/options.','ICER identity discrepancy is algebraically established; its processing cause is not.','Spatial/source grouping is confounded; no fitted gain/offset correction.','No change to prior numerical products or ice classification; no independent ice truth.'])
(O/'results.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps({k:v for k,v in q.items() if k!='point_checks'},indent=2))
