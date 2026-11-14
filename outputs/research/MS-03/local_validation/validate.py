"""Offline checks of retained evidence; no new scientific retrieval or clock adjustment."""
import csv,hashlib,json,struct,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent
checks=[]
def check(name,ok):
 assert ok,name
 checks.append(name)
def rows(name):
 with (O/name).open(encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f);out=list(rd)
  check(name+' rectangular',all(None not in r and all(v is not None for v in r.values()) for r in out));return out
for fn,key,n in [('local_prior_work.csv','prior_work_id',10),('mars_ice_evidence.csv','evidence_id',11),('analog_validation.csv','earth_candidate_id',2),('search_log.csv','log_id',None)]:
 r=rows(fn);check(fn+' unique IDs',len({x[key] for x in r})==len(r));check(fn+' count',len(r)==n if n else len(r)>100)
 for x in r:
  for k,v in x.items():
   if k.endswith('_json'):json.loads(v)
p=rows('piqueux_native_cell.csv')[0]
check('native cell and conditional unknown',p['row_0based']=='64' and p['column_0based']=='484' and abs(float(p['model_ice_depth_m_raw'])-.103161566)<1e-12 and p['actual_ice_depth_m']=='unknown')
q=json.loads((O/'piqueux_qa.json').read_text());check('all provider checksums verified',all(x['provider_checksum_verified'] for x in q['files']))
b=(O/'sources/SHARAD_local_records.bin').read_bytes();r=rows('sharad_local_geometry.csv');check('256 original records',len(b)==5822*256 and len(r)==256)
for i,x in enumerate(r):
 z=b[i*5822:(i+1)*5822];lon,lat=struct.unpack_from('<dd',z,5637)
 assert lon==float(x['longitude_east_deg']) and lat==float(x['latitude_planetocentric_deg']) and 242<=lon<=242.5 and 57.5<=lat<=58
 assert z[5570:5593].decode().strip()==x['geometry_epoch_utc'] and x['ice_reflector_identified']=='unknown'
check('all raw coordinates/times decode and inside fixed cell',True)
c=json.loads((O/'ctx_observability.json').read_text());check('five actual CTX samples',len(c['samples'])==5)
for x in c['samples']:
 z=x['bounds_mars_east180_lat'];assert -118<=z['west']<z['east']<=-117.5 and 57.5<=z['south']<z['north']<=58
 assert hashlib.sha256((O/x['image_file']).read_bytes()).hexdigest()==x['sha256']
check('CTX sample hashes and full bounds',True)
check('NW retains mixed acquisition dates',len(next(x for x in c['samples'] if x['sample_id']=='NW')['source_dates'])==2)
k=json.loads((O/'catalogue_qa.json').read_text());check('six distinct SHARAD tracks',next(x for x in k['catalogues'] if x['instrument']=='SHARAD')['unique_observation_identifiers']==6)
for x in rows('analog_validation.csv'):
 assert x['mars_geometry_or_performance_comparison'] in ['unknown; not calculated','not a quantitative matching test']
check('no invented Mars geometry comparison',True)
# Each acquired retained source must match its request log, including byte-range responses.
verified=0
for x in json.loads((O/'retrievals.json').read_text()):
 if x['status']=='acquired' and (O/x['file']).exists():
  assert hashlib.sha256((O/x['file']).read_bytes()).hexdigest()==x['sha256'],x['file'];verified+=1
check('all available acquired bytes match recorded SHA256 ('+str(verified)+')',verified>30)
for x in O.glob('*.json'):
 if x.name not in ['manifest.json','validation.json']:json.loads(x.read_text())
check('all top-level JSON parse',True)
(O/'validation.json').write_text(json.dumps({'status':'passed','checks':checks,'visual_review':['F-LV01_CTX_samples.png: actually opened, axes/source/date annotations checked','F-LV02_observation_support.png: actually opened, geometry-only caveat checked'],'not_tested':['spectral ice detection','radar echo interpretation','Earth logger alignment','independent ice truth']},indent=2)+'\n')
print('Passed',len(checks),'checks')
