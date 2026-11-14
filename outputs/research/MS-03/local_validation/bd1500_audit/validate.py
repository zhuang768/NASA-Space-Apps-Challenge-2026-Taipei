"""Evidence and arithmetic diagnostics, not scientific detection validation."""
from pathlib import Path
import csv,json,hashlib,struct,zipfile,sys,subprocess,math
O=Path(__file__).resolve().parent;P=O.parent/'official_resources';retained='--retained-only' in sys.argv;checks=[];skip=[]
def check(n,v):
 assert v,n
 checks.append(n)
for r in json.loads((O/'retrievals.json').read_text()):
 if r['status']!='acquired':continue
 f=O/r['file'];ignored=subprocess.run(['git','check-ignore','-q',str(f)]).returncode==0
 if ignored and (retained or not f.exists()):skip.append(r['file']);continue
 check(f.name+' source SHA',hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'])
 if r.get('request_headers',{}).get('Range'):check(f.name+' exact original point bytes',r['http_status']==206 and r['bytes']==4 and r['content_range'].startswith('bytes '+r['request_headers']['Range'][6:]+'/'))
inv=json.loads((O/'disclosed_source_inventory.json').read_text());check('bounded source search records production flow unknown',inv['readable_members_scanned']==320 and not inv['production_flow_text_matches'])
archive=O/'sources/CAT_v7_4_codeonly.zip'
if archive.exists() and not retained:
 z=zipfile.ZipFile(archive)
 for x in inv['members']:
  b=z.read(x['member']);check(x['member'].split('/')[-1]+' original CRC/SHA',hashlib.sha256(b).hexdigest()==x['sha256'] and z.getinfo(x['member']).CRC==x['crc32'])
for x in json.loads((O/'jcat_provenance.json').read_text()):
 f=O/x['local_file']
 if retained and f.suffix in ['.java','.xml']:continue
 if not f.exists():skip.append(x['local_file']);continue
 b=f.read_bytes();check(f.name+' Git blob identity',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob_sha1'] and hashlib.sha256(b).hexdigest()==x['sha256'])
q=json.loads((O/'results.json').read_text());check('ported formula equals retained existing calculation',q['reference_port_minus_existing_calculation']['max_abs']==0)
check('float roundoff cannot account for full residual',q['float32_minus_float64']['max_abs']<2e-7 and q['cat64_minus_official_strict']['max_abs']>.019)
check('supplied LBL and HDR order agrees',q['header_label_band_order_identical'] and q['band_count']==60 and q['BD1500_band_index_0based']==24)
plan=json.loads((P/'mrdr_extraction_plan.json').read_text());r0=plan['roi_rows_0based'][0]
for x in q['point_checks']:
 old=(O/x['compare_range_file']).read_bytes();new=(O/x['file']).read_bytes();o=((x['map_row_0based']-r0)*plan['native_samples']+x['map_col_0based'])*4;check(x['file']+' independent point equality',new==old[o:o+4] and x['matches_retained_bytes'])
# Independently check disclosed ICER identity on original fields at first, middle and last cells.
nr=plan['roi_rows_0based'][1]-r0+1;nc=plan['roi_columns_0based'][1]-plan['roi_columns_0based'][0]+1
su={x['quantity']:(P/'sources'/x['subset_file']).read_bytes() for x in plan['requests'] if x['type']=='su'}
for r,c in [(0,0),(nr//2,nc//2),(nr-1,nc-1)]:
 off=(r*plan['native_samples']+plan['roi_columns_0based'][0]+c)*4;v={k:struct.unpack_from('<f',b,off)[0] for k,b in su.items()};d=1-(1-v['BD1435'])/(1-v['BD1500_2'])-v['ICER1_2'];check(f'ICER point{r},{c} finite diagnostic',math.isfinite(d))
check('identity difference retained without causal claim',q['ICER_identity_minus_official']['max_abs']>.001 and q['ICER_float32_perturbation']['max_abs']<2e-7 and q['cause_of_production_residual']=='unknown')
check('scientific values and unknowns unchanged',not q['original_scientific_data_modified'] and q['ice_status']=='unknown' and not q['production_1_03_94_source_obtained'])
for name,key,n in [('version_comparison.csv','source_id',6),('hypothesis_checks.csv','check_id',6),('source_group_residuals.csv','source_product',5)]:
 with (O/name).open(encoding='utf-8-sig',newline='') as f:a=list(csv.DictReader(f))
 check(name+' rectangular/unique',len(a)==n and len({x[key] for x in a})==n and all(None not in x and all(v is not None for v in x.values()) for x in a))
for f in O.glob('*.py'):compile(f.read_text(),str(f),'exec')
check('all audit scripts parse',True)
(O/('validation_retained_only.json' if retained else 'validation.json')).write_text(json.dumps(dict(status='passed',check_count=len(checks),checks=checks,omitted_ignored_sources=skip,not_executed=['original IDL/CAT runtime','MRDR1.03.94 production runtime','normalization causal reconstruction','ice detection validation']),indent=2)+'\n');print('Passed',len(checks),'audit checks; retained-only',retained)
