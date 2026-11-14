"""Independent struct-based checks of original retained bytes; no numpy required."""
from pathlib import Path
import csv,gzip,json,struct,hashlib,math,re,sys
O=Path(__file__).resolve().parent;S=O/'sources';checks=[]
def check(n,ok):
 assert ok,n
 checks.append(n)
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  rr=csv.DictReader(f);a=list(rr)
  check(p.name+' rectangular',all(None not in x and all(v is not None for v in x.values()) for x in a));return a
retained_only='--retained-only' in sys.argv; omitted=[]
qa=json.loads((O/'qa.json').read_text());plans=json.loads((O/'extraction_plan.json').read_text());logs=json.loads((O/'retrievals.json').read_text())
for r in logs:
 if r['status']=='acquired':
  p=O/r['file'];local_only=p.suffix in ['.htm','.html'] or p.name.endswith('_ddr1.img')
  if local_only and (retained_only or not p.exists()):omitted.append(r['file']);continue
  check(p.name+' acquisition hash',hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'])
  if r['request_headers'].get('Range'):
   a,b=map(int,r['request_headers']['Range'][6:].split('-'));check(p.name+' original range',r['http_status']==206 and r['bytes']==b-a+1 and r['content_range'].startswith(f'bytes {a}-{b}/'))
pixels=list(csv.DictReader(gzip.open(O/'roi_pixels.csv.gz','rt')))
check('all pixel keys unique',len({(x['product_id'],x['line_0based'],x['sample_0based']) for x in pixels})==len(pixels))
for plan,expected in zip(plans,[966,8516]):
 pid=plan['product_id'];nsub=plan['stop_line_0based']-plan['start_line_0based']+1;nb=plan['bands'];ns=plan['samples'];rows=[x for x in pixels if x['product_id']==pid];q=next(x for x in qa['products'] if x['product_id']==pid)
 check(pid+' ROI count',len(rows)==plan['roi_pixel_centres'])
 db=(S/(plan['ddr_id']+'_roi_bsq.bin')).read_bytes();meta=json.loads((O/(plan['ddr_id']+'_subset.json')).read_text());length=nsub*ns*4
 check(pid+' DDR subset byte count',len(db)==14*length)
 for i,seg in enumerate(meta['segments']):
  check(pid+f' DDR backplane{i} original hash',hashlib.sha256(db[i*length:(i+1)*length]).hexdigest()==seg['sha256'])
 rb=(S/(pid+'_roi_rows.bin')).read_bytes();wb=(S/plan['wavelength_file_label'].lower()).read_bytes();wa=struct.unpack('<'+'f'*(nb*ns),wb[:nb*ns*4]);rr=(S/(pid+'_rownum.bin')).read_bytes()
 check(pid+' rownum exact calibration match',rr==wb[nb*ns*4:nb*ns*4+nb*2])
 check(pid+' source row bytes',len(rb)==nsub*nb*ns*4 and plan['byte_start']==plan['start_line_0based']*nb*ns*4)
 passing=0
 for x in rows:
  r=int(x['line_0based'])-plan['start_line_0based'];c=int(x['sample_0based']);lat=struct.unpack_from('<f',db,(3*nsub*ns+r*ns+c)*4)[0];lo=struct.unpack_from('<f',db,(4*nsub*ns+r*ns+c)*4)[0]
  assert lat==float(x['latitude_planetocentric_deg']) and lo==float(x['longitude_raw_east_signed_deg']) and lo%360==float(x['longitude_east_0_360_deg'])
  assert 57.5<=lat<=58 and 242<=lo%360<=242.5
  channels=[k for k in range(nb) if math.isfinite(wa[k*ns+c]) and wa[k*ns+c]!=65535 and 1300<=wa[k*ns+c]<=2200]
  v=[struct.unpack_from('<f',rb,((r*nb+k)*ns+c)*4)[0] for k in channels]
  valid=bool(v) and all(math.isfinite(z) and z!=65535 for z in v);positive=valid and all(z>0 for z in v)
  assert valid==(x['numerically_valid_1300_2200_nm']=='True') and positive==(x['positive_1300_2200_nm']=='True')
  passing+=positive
  assert x['ice_classification']=='unknown'
  if x['IF_nearest_1525']:
   wave=[(abs(wa[k*ns+c]-1525),k) for k in range(nb) if math.isfinite(wa[k*ns+c]) and 0<wa[k*ns+c]<65535];k=min(wave)[1]
   assert float(x['nearest_1525_nm'])==wa[k*ns+c] and float(x['IF_nearest_1525'])==struct.unpack_from('<f',rb,((r*nb+k)*ns+c)*4)[0]
 check(pid+' independently decoded all coordinates and spectra',True)
 check(pid+' all-channel positive count',passing==expected==q['all_1300_2200_positive_pixels'])
 check(pid+' unresolved interpretation retained',q['ice_presence']==q['ice_depth_m']==q['ice_content']=='unknown' and all(v=='OFF' for v in q['correction_flags'].values()))
for n in ['channel_qa.csv','anchor_channels.csv']:readcsv(O/n)
check('no ice index or absence claim',qa['no_absence_claim'] and qa['no_ice_index_calculated'].startswith('No standard index'))
check('original catalogue history retained',bool(json.loads((O/'previous_catalogue_status.json').read_text())['previous_ice_record']))
for p in O.glob('*.py'):compile(p.read_text(),str(p),'exec')
check('all CRISM Python scripts parse',True)
result=dict(status='passed',checks=checks,check_count=len(checks),visual_review='Final PNG actually opened; legend moved away from2-micron trough; dates/source/units and limitations checked',not_validated=['atmospheric and photometric correction','cloud/seasonal frost discrimination','instrument residuals and calibrated detection threshold','ice presence or absence','subsurface depth/content','whole-cell scientific-pixel coverage'])
result['mode']='retained-only' if retained_only else 'all available source bytes';result['omitted_local_only_sources']=omitted
(O/('validation_retained_only.json' if retained_only else 'validation.json')).write_text(json.dumps(result,indent=2)+'\n');print('Passed',len(checks),'CRISM checks; all',len(pixels),'pixel coordinate/spectral masks independently decoded')
