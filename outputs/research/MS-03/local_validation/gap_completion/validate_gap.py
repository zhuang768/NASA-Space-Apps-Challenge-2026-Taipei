"""Portable offline checks. Ignored source downloads are optional, not prerequisites."""
from pathlib import Path
import csv,json,hashlib,subprocess,re,runpy,io,contextlib,sys
import numpy as np
from PIL import Image
from shapely import wkt
from shapely.geometry import Point,box
O=Path(__file__).resolve().parent;L=O.parent;ROOT=O.parents[4];BASE='ddd04cfcb5ea810d73304b1cf6ae064c1f77a1c5';checks=[]
PBASE=json.loads((O/'integration_state.json').read_text())['latest_main_preservation_base_sha'] if (O/'integration_state.json').exists() else BASE
def ck(name,ok):assert ok,name;checks.append(name)
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);data=list(r)
 ck(p.name+' rectangular',all(None not in x and all(v is not None for v in x.values()) for x in data));return data
for p in O.glob('*.json'):json.loads(p.read_text(),parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
ck('all new JSON parse without NaN or Infinity',True)
for p in O.glob('*.csv'):readcsv(p)
m=json.loads((O/'manifest.json').read_text());ck('fixed ROI unchanged',m['roi']==dict(lat_min=57.5,lat_max=58,lon_east_min=242,lon_east_max=242.5,latitude='planetocentric'))
ck('unknown ice/depth/fraction and no clock alignment',m['disposition']==dict(morphology='unknown',AD1='general_method_reference_only',ice_independently_confirmed=False,actual_ice_depth_m=None,ice_fraction=None,campbell_hobo_aligned=False))
for x in m['files']:
 raw=(ROOT/x['path']).read_bytes();assert len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256'],x['path']
ck('all retained new deliverable hashes match manifest',len(m['files'])>30)
requests=json.loads((O/'retrievals.json').read_text());ck('request IDs unique and all actual attempts retained',len(requests)>=52 and len({x['id'] for x in requests})==len(requests))
verified=0;optional_absent=0
for r in requests:
 p=O/r['file']
 if r.get('bytes') and p.exists():
  raw=p.read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],r['id'];verified+=1
 elif r.get('bytes'):optional_absent+=1
ck('available downloaded source bytes match retrieval hashes',verified>=20)
for req in json.loads((O/'requests_round13.json').read_text()):
 r=next(x for x in requests if x['id']==req['identifier']);s,e=map(int,req['headers']['Range'][6:].split('-'))
 ck(req['identifier']+' exact HTTP206 range and length',r['http_status']==206 and r['content_range'].startswith(f'bytes {s}-{e}/') and r['bytes']==e-s+1)
cat=json.loads((O/'daubar2022_summary.json').read_text());rows=readcsv(O/'daubar2022_membership.csv')
ck('original author XLSX MD5 equals provider',hashlib.md5((O/'sources/Daubar_2022_catalog_tableS1.xlsx').read_bytes()).hexdigest()=='4d1b49c2e62785a1b4efb73b2040de4d')
ck('1203 unique source Excel row IDs',len(rows)==1203 and len({r['source_excel_row'] for r in rows})==1203)
ck('zero impact-point membership actually computed',cat['point_hits']==sum(57.5<=float(r['latitude_deg_planetocentric'])<=58 and 242<=float(r['longitude_deg_east'])<=242.5 for r in rows)==0)
ck('original author flags preserved and not same selection as DundasS4',cat['original_ice_flag_counts']=={'n':1135,'possible':20,'y':48} and cat['Dundas_TableS4_replacement'] is False)
ck('conflicting source header labels explicitly retained','deg E' in cat['original_headers']['B'] and 'deg N' in cat['original_headers']['C'])
mo=json.loads((O/'moc_summary.json').read_text());im=np.asarray(Image.open(O/'MOC_S1700607_roi_native_DN.png'));r0,r1,c0,c1=mo['roi_crop_0based_inclusive']
ck('native masked crop dimensions and count',list(im.shape)==[r1-r0+1,c1-c0+1] and int(np.count_nonzero(im))==mo['roi_valid_nonzero_pixel_centres']==9272742)
# All nonzero retained pixel centres are inside the fixed cell under declared native projection.
for a in range(0,len(im),256):
 rr=np.arange(r0+a,min(r0+a+256,r1+1));cc=np.arange(c0,c1+1);x=(cc+2906)*mo['map_grid_m'];y=(-646450-rr)*mo['map_grid_m'];lat=90-np.degrees(2*np.arctan(np.hypot(x[None,:],y[:,None])/(2*mo['radius_m'])));lon=(242+np.degrees(np.arctan2(x[None,:],-y[:,None])))%360;mask=im[a:a+len(rr)]!=0
 assert np.all((lat[mask]>=57.5)&(lat[mask]<=58)&(lon[mask]>=242)&(lon[mask]<=242.5))
ck('all retained nonzero MOC centres inside fixed ROI',True)
r=json.loads((O/'sources/moc_NASDP.json').read_text())['ODEResults']['Products']['Product'];poly=wkt.loads(r['Footprint_geometry'])
ck('explicit east-positive footprint actually intersects cell',poly.bounds[0]>0 and poly.intersects(box(242,57.5,242.5,58)))
for t in mo['tiles']:
 assert poly.covers(Point(t['longitude_deg_E'],t['latitude_deg_N']))
 a,b=t['source_rows_0based_inclusive'];c,d=t['source_columns_0based_inclusive'];tile=np.asarray(Image.open(O/f'MOC_detail_{t["id"]}_native_DN.png'));assert np.array_equal(tile,im[a-r0:b-r0+1,c-c0:d-c0+1])
ck('three fixed review tiles contain exact retained source DN',True)
raw=O/'sources/s1700607_na.img'
if raw.exists():
 b=raw.read_bytes();src=np.frombuffer(b,dtype='u1',offset=8184).reshape(10565,2728)
 ck('optional full IMG matches PDS pixel checksum and recorded hash',int(src.sum(dtype=np.uint64))==1590142434 and hashlib.sha256(b).hexdigest()==mo['source_sha256'])
 ck('retained nonzero crop values equal original source pixels',np.array_equal(im[im!=0],src[r0:r1+1,c0:c1+1][im!=0]))
else:checks.append('full MOC IMG not present: optional source checks skipped, retained checks passed')
ck('MOC grid not presented as effective resolving power',mo['map_grid_is_effective_resolution'] is False)
s=json.loads((O/'spectral_diagnostics.json').read_text());a=np.load(O/'spectral_diagnostic_arrays.npz');ck('strict MRDR source-centre subset retained',int(a['strict'].sum())==s['strict_source_centres']==13169)
ck('precision diagnostic actually smaller than official residual',s['float32_minus_float64']['max_absolute']<1.27e-7 and np.max(abs(a['residual'][a['strict']]))>.0193)
ck('no spectral threshold or classified ice invented',s['detection_threshold'] is None and s['ice_presence']=='unknown' and s['actual_ice_depth_m'] is None)
r=json.loads((O/'radar_summary.json').read_text());a=np.load(O/'radar_local_arrays.npz');rr=readcsv(O/'radar_roi_columns.csv');ck('same observation original-grid radar and clutter shape',a['observed'].shape==a['simulated'].shape==(269,65) and len(rr)==65)
ck('all65 actual documented centre coordinates inside ROI',all(57.5<=float(x['latitude_deg_planetocentric'])<=58 and 242<=float(x['longitude_deg_E'])<=242.5 for x in rr))
ck('column and range-row origin explicit',a['column_1based'].tolist()==list(range(2185,2250)) and a['row_0based'].tolist()==list(range(2182,2451)))
ck('model not independent and no power subtraction/depth estimate',r['simulation_is_independent_observation'] is False and r['amplitude_subtraction_allowed'] is False and r['actual_ice_depth_m'] is None and r['ice_fraction'] is None)
tracks=readcsv(O/'radar_track_membership.csv');ck('four exact mapped tracks, two unresolved crosswalk cases',sum(bool(x['US_crosswalk_basename']) for x in tracks)==4 and sum(x['strict_GEOM_centre_hits']=='' for x in tracks)==2)
ck('catalogue-intersecting but outside-centre track not treated as in-cell',next(x for x in tracks if '0796502' in x['italian_product_id'])['strict_GEOM_centre_hits']=='0')
# No scientific data belonging to other roles or prior stages is rewritten.
base_files=subprocess.check_output(['git','ls-tree','-r','--name-only',PBASE,'--','outputs/research/MS-03/local_validation/crism/','outputs/research/MS-03/local_validation/official_resources/','outputs/research/MS-03/local_validation/original_tables_followup/','outputs/research/MS-03/local_validation/bd1500_audit/','outputs/research/MS-03/local_validation/production_history/','outputs/research/MS-03/local_validation/t1811_run_artifacts/'],cwd=ROOT,text=True).splitlines()
for name in base_files:assert (ROOT/name).read_bytes()==subprocess.check_output(['git','show',PBASE+':'+name],cwd=ROOT),name
ck('all '+str(len(base_files))+' existing scientific/supplement files byte-preserved',len(base_files)>100)
for n in ['observation_inventory.csv','local_prior_work.csv','mars_ice_evidence.csv','analog_validation.csv']:
 ck('original '+n+' unchanged',(L/n).read_bytes()==subprocess.check_output(['git','show',PBASE+':outputs/research/MS-03/local_validation/'+n],cwd=ROOT))
log=readcsv(L/'search_log.csv');ck('all search IDs remain unique',len(log)==len({r['log_id'] for r in log}))
old=subprocess.check_output(['git','show',BASE+':outputs/research/MS-03/local_validation/search_log.csv'],cwd=ROOT);ck('starting main search log retained as exact byte prefix',(L/'search_log.csv').read_bytes().startswith(old))
latestlog=subprocess.check_output(['git','show',PBASE+':outputs/research/MS-03/local_validation/search_log.csv'],cwd=ROOT);ck('integrated main search-log bytes retained as exact prefix',(L/'search_log.csv').read_bytes().startswith(latestlog))
notes=ROOT/'docs/research/MS-03/local_validation/research_notes.md'
prior_notes=subprocess.check_output(['git','show',PBASE+':docs/research/MS-03/local_validation/research_notes.md'],cwd=ROOT,text=True);ck('concurrent main research-note body retained verbatim',prior_notes.split('\n',1)[1].strip() in notes.read_text())
for target in re.findall(r'\]\(([^)]+)\)',notes.read_text()):
 if not target.startswith(('http:','https:','#')):assert (notes.parent/target.split('#')[0]).exists(),target
ck('all research-note links resolve',True)
# The old validators intentionally describe earlier stages; execute and preserve their stored outputs.
outputs=[L/'validation.json',L/'original_tables_followup/validation.json'];snap={p:p.read_bytes() for p in outputs}
legacy=[]
try:
 for p in [L/'validate.py',L/'original_tables_followup/validate_followup.py']:
  stream=io.StringIO()
  with contextlib.redirect_stdout(stream):runpy.run_path(str(p),run_name='__main__')
  legacy.append(stream.getvalue().strip())
finally:
 for p,b in snap.items():p.write_bytes(b)
ck('both earlier-stage validators actually pass; prior outputs preserved',len(legacy)==2)
concurrent=[]
saved_argv=list(sys.argv)
try:
 for folder in ['bd1500_audit','production_history','t1811_run_artifacts']:
  p=L/folder/'validation_retained_only.json';saved=p.read_bytes();stream=io.StringIO()
  try:
   sys.argv=[str(L/folder/'validate.py'),'--retained-only']
   with contextlib.redirect_stdout(stream):runpy.run_path(str(L/folder/'validate.py'),run_name='__main__')
   concurrent.append(stream.getvalue().strip())
  finally:p.write_bytes(saved)
finally:sys.argv=saved_argv
ck('three concurrent upstream retained validators pass; their stored outputs preserved',len(concurrent)==3)
result=dict(status='passed',date_taipei='2026-11-15',starting_sha=BASE,preservation_base_sha=PBASE,checks=checks,source_payloads_verified_when_present=verified,ignored_optional_payloads_absent=optional_absent,legacy_validation_stdout=legacy,concurrent_validation_stdout=concurrent,branch_name_required=False,network_required=False,not_validated=['ice presence/depth/fraction','complete-cell morphology or closed boundaries','spectral cloud/frost classification and detection limits','origin of radar patterns','complete novelty clearance','UV cross-logger timing'])
(O/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('Passed',len(checks),'retained-evidence checks; previous validators:',legacy)
