"""Independent retained-byte, projection and continuum arithmetic checks; not an ice validation."""
from pathlib import Path
import json,csv,gzip,struct,hashlib,math,re,sys,subprocess
O=Path(__file__).resolve().parent;S=O/'sources';checks=[];skip=[];retained='--retained-only' in sys.argv

def check(n,v):
 assert v,n
 checks.append(n)
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  a=list(csv.DictReader(f));check(p.name+' rectangular',all(None not in x and all(v is not None for v in x.values()) for x in a));return a
for r in json.loads((O/'retrievals.json').read_text()):
 if r['status']!='acquired':continue
 p=O/r['file'];ignored=subprocess.run(['git','check-ignore','-q',str(p)]).returncode==0
 if ignored and (retained or not p.exists()):skip.append(r['file']);continue
 check(p.name+' source hash',hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'])
 if r.get('request_headers',{}).get('Range'):
  a,b=map(int,r['request_headers']['Range'][6:].split('-'));check(p.name+' original range',r['http_status']==206 and r['bytes']==b-a+1 and r['content_range'].startswith(f'bytes {a}-{b}/'))
links=readcsv(O/'resources_links.csv');check('actual official resources PDS anchor',any(x['resource_name']=='NASA Planetary Data System (PDS)' and x['canonical_without_tracking']=='https://pds.nasa.gov/' for x in links))
chain=json.loads((O/'resource_chain.json').read_text());check('official Resources independently decoded',chain['official_resources_verified'] and len(links)==11)
for typ in ['TER','MTRDR']:
 a=json.loads((S/f'ode_{typ}.json').read_text())['ODEResults'];check(typ+' bounded zero catalogue response',a['Status']=='Success' and a['Count']=='0')
a=json.loads((S/'ode_MRDR.json').read_text())['ODEResults'];check('invalid MRDR query is not zero coverage',a['Status']=='ERROR' and 'Invalid IIPT' in a['Error'])
q=json.loads((O/'mrdr_qa.json').read_text());p=json.loads((O/'mrdr_extraction_plan.json').read_text());nrows=p['roi_rows_0based'][1]-p['roi_rows_0based'][0]+1;ns=p['native_samples'];requests=p['requests'];by={(x['type'],str(x['quantity'])):x for x in requests};data={k:(S/v['subset_file']).read_bytes() for k,v in by.items()}
for k,b in data.items():
 check(str(k)+' exact subset size and local numeric values',len(b)==nrows*ns*4 and all(math.isfinite(v) and v!=65535 for row in range(nrows) for (v,) in struct.iter_unpack('<f',b[(row*ns+p['roi_columns_0based'][0])*4:(row*ns+p['roi_columns_0based'][1]+1)*4])))
rows=list(csv.DictReader(gzip.open(O/'mrdr_roi_pixels.csv.gz','rt')));check('13284 unique map centres',len(rows)==13284 and len({(x['map_row_0based'],x['map_column_0based']) for x in rows})==13284)
hdr=(S/'t1811_mrral_60n243_0327_4.hdr').read_text();mp=[x.strip() for x in re.search(r'map info\s*=\s*\{([^}]+)',hdr)[1].split(',')];ox,oy,sx,sy=map(float,mp[3:7]);R=p['radius_m'];lp=p['line_projection_offset'];sp=p['sample_projection_offset'];sc=p['pixel_scale_m'];lon0=p['central_meridian_east_deg'];lat_ts=p['standard_parallel_deg'];inside=0;residual=[]
for x in rows:
 r=int(x['map_row_0based']);c=int(x['map_column_0based']);offset=((r-p['roi_rows_0based'][0])*ns+c)*4
 def value(k):return struct.unpack_from('<f',data[k],offset)[0]
 # Independent ENVI corner plus half-pixel inverse, versus PDS offset implementation.
 la=(oy-(r+.5)*sy)/R*180/math.pi;lo=(lon0+(ox+(c+.5)*sx)/(R*math.cos(math.radians(lat_ts)))*180/math.pi)%360
 assert abs(la-float(x['map_latitude_deg']))<1e-7 and abs(lo-float(x['map_longitude_east_deg']))<1e-7
 assert 57.5<=la<=58 and 242<=lo<=242.5
 sl=value(('de','Latitude - areocentric - deg N'));so=value(('de','Longitude - areocentric - deg E'))%360;mask=57.5<=sl<=58 and 242<=so<=242.5
 assert mask==(x['source_centre_inside_roi']=='True');inside+=mask
 assert int(value(('de','Target ID')))==int(x['target_id']) and int(value(('de','Segment ID (Counter)')))==int(x['segment_id'])
 official=value(('su','BD1500_2'));assert official==float(x['BD1500_2_official'])
 L=value(('al','1367'));H=value(('al','1808'));WL=by['al','1367']['actual_wavelength_nm'];WH=by['al','1808']['actual_wavelength_nm'];bds=[]
 for nm in ['1505','1558']:
  W=by['al',nm]['actual_wavelength_nm'];a=(W-WL)/(WH-WL);cont=L*(1-a)+H*a;bds.append(1-value(('al',nm))/cont)
 calc=sum(bds)/2;assert abs(calc-float(x['BD1500_2_recalculated']))<1e-12;residual.append(calc-official)
 assert x['ice_presence']=='unknown'
check('all pixels independently geolocated by HDR',True);check('all native values and formula calculations independently decoded',True);check('strict source-centre filter excludes115 boundary remaps',inside==13169==q['map_and_source_centres_inside_fixed_roi']);check('unresolved formula/product discrepancy retained',abs(max(map(abs,residual))-q['formula_comparison']['max_abs_calculated_minus_official'])<1e-12 and max(map(abs,residual))>.01)
source=readcsv(O/'source_observations.csv');assert all(json.loads(x['segments_json'])==[int(x['product_id'].split('_')[1],16)] for x in source);check('five traced source observations retain all cells',len(source)==5 and sum(int(x['mapped_grid_centres']) for x in source)==13284 and sum(int(x['source_centres_in_fixed_roi']) for x in source)==13169)
check('source dates span2006–2014 not product2023 date',min(x['utc_start'] for x in source).startswith('2006') and max(x['utc_start'] for x in source).startswith('2014'))
check('unknowns retained and negative not absence',q['ice_presence']==q['ice_depth_m']==q['ice_fraction']=='unknown' and q['negative_indices_not_absence'] and not q['full_scientific_pixel_quality_confirmed'])
check('native product sphere respected',R==3381164.4 and R!=3396190 and p['pixel_scale_m']==180.4662)
for f in O.glob('*.py'):compile(f.read_text(),str(f),'exec')
check('all new Python parses',True)
result=dict(status='passed',check_count=len(checks),checks=checks,omitted_local_only=skip,mode='retained-only' if retained else 'all available original bytes',visual_review='F-RES01 opened; axes, native grid/source dates, masks, units and unknown status checked',not_validated=['ice presence/absence','pixel cloud/frost classification','full vendor1.03.94 pipeline reproduction','cause of summary/recomputed parameter mismatch','covered ice depth/content','new geomorphic analogy'])
(O/('validation_retained_only.json' if retained else 'validation.json')).write_text(json.dumps(result,indent=2)+'\n');print('Passed',len(checks),'checks;',len(rows),'map rows independently decoded; source-in-ROI',inside)
