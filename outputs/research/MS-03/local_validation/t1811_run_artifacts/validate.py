"""Validate evidence scope and preserved values; no optimizer runtime executed."""
from pathlib import Path
import csv,hashlib,json,subprocess,sys
O=Path(__file__).resolve().parent;P=O.parent;retained='--retained-only'in sys.argv;checks=[];skipped=[]
def check(n,v):
    assert v,n
    checks.append(n)
def sha(b):return hashlib.sha256(b).hexdigest()
for r in json.loads((O/'retrievals.json').read_text()):
    if r['status']!='acquired':continue
    f=O/r['file'];ignored=subprocess.run(['git','check-ignore','-q',str(f)]).returncode==0
    if ignored and(retained or not f.exists()):skipped.append(r['file']);continue
    check(f.name+' source bytes/SHA',f.stat().st_size==r['bytes']and sha(f.read_bytes())==r['sha256'])
    check(f.name+' successful official download',r.get('http_status')==200)
q=json.loads((O/'inventory_audit.json').read_text());p=json.loads((O/'paper_read_scope.json').read_text());r=json.loads((O/'replay_readiness.json').read_text())
check('inventory parsed count matches declared count',q['data_inventory_records']==7056 and q['T1811_members']==4)
check('bundle scope preserved',len(q['bundle_members'])==5 and not q['global_absence_claim'])
check('four labels and physical listing consistent',q['T1811_physical_listing_files']==15)
b=(O/'sources/T1811_original_index_records.tab').read_bytes();check('original index excerpt hash/length',len(b)==4*792 and sha(b)==q['index_source']['excerpt_sha256'])
old=P/q['index_source']['path']
if old.exists() and not retained:
    a=old.read_bytes();check('pinned original index',len(a)==q['index_source']['bytes']and sha(a)==q['index_source']['sha256'])
    check('exact original record extraction',b==b''.join(a[i*792:(i+1)*792]for i in q['index_source']['selected_records_0based']))
check('57 field definitions',q['index_column_count']==57)
for filename,key,n in [('T1811_inventory_members.csv','lidvid',4),('T1811_product_files.csv','product_family',4),('source_audit.csv','source_id',11),('artifact_status.csv','evidence_id',7),('replay_inputs_needed.csv','request_id',5),('search_log.csv','log_id',None)]:
    with (O/filename).open(encoding='utf-8-sig',newline='')as f:a=list(csv.DictReader(f))
    check(filename+' rectangular/unique',all(None not in x and all(v is not None for v in x.values())for x in a)and len({x[key]for x in a})==len(a)and(len(a)==n if n else len(a)>15))
    for x in a:
        for k,v in x.items():
            if k.endswith('_json'):json.loads(v)
with (O/'T1811_product_files.csv').open(encoding='utf-8-sig',newline='')as f:
    for x in csv.DictReader(f):check(x['product_family']+' pinned original label SHA',sha((P/x['source_path']).read_bytes())==x['source_sha256'])
with (O/'T1811_index_fields.csv').open(encoding='utf-8-sig',newline='')as f:a=list(csv.DictReader(f))
check('four complete index-field rows',len(a)==4*57 and len({(x['record_0based'],x['field'])for x in a})==4*57)
check('local illustrated pair rejected by latitude',p['fig23_support']['latitude_N'][1]<57.5 and not p['fig23_support']['overlaps_fixed_MS03_roi']and not p['fig23_support']['usable_MS03_BD1500_pre_post_pair'])
check('paper read scope and repository receipt',p['provider_md5_verified']and p['pdf_pages']==34 and p['record_file_count']==1 and p['embedded_file_count']==0 and [x['pdf_page_1based']for x in p['read_pages']]==[24,25,26,32])
if not retained and (O/'sources/seelos2024_overview.pdf').exists():
    raw=(O/'sources/seelos2024_overview.pdf').read_bytes();record=json.loads((O/'sources/caltech_record.json').read_text());f=record['files']['entries']['1-s2.0-S0019103523001896-main.pdf']
    check('original author PDF provider MD5',hashlib.md5(raw).hexdigest()==f['checksum'].split(':')[1] and len(raw)==f['size']and sha(raw)==p['pdf_sha256'])
check('no recovered run/prepost/coefficient or replay claim',not any(r[k]for k in ['stage_replay_performed','actual_run_settings_obtained','actual_coefficients_obtained','paired_local_pre_post_data_obtained','scientific_values_changed','fitted_correction_applied']))
check('ice and quantitative attribution unknown',all(r[k]=='unknown'for k in ['quantitative_attribution','ice_presence','ice_depth_m','ice_fraction']))
prior=json.loads((P/'bd1500_audit/results.json').read_text());check('prior residual statistics unchanged',r['old_strict_residual_unchanged']==prior['cat64_minus_official_strict'])
for x in json.loads((O/'preserved_inputs.json').read_text()):
    f=P/x['path'];ignored=subprocess.run(['git','check-ignore','-q',str(f)]).returncode==0
    if retained and ignored:skipped.append(x['path']);continue
    check(x['path']+' preserved data',len(f.read_bytes())==x['bytes']and sha(f.read_bytes())==x['sha256'])
for f in O.glob('*.json'):json.loads(f.read_text())
for f in O.glob('*.py'):compile(f.read_text(),str(f),'exec')
check('all JSON/Python parse',True)
(O/('validation_retained_only.json'if retained else'validation.json')).write_text(json.dumps(dict(status='passed',check_count=len(checks),checks=checks,skipped_local_only=skipped,not_executed=['actual1.03.94 runtime','optimizer numerical replay','ice detection validation']),indent=2)+'\n')
print('Passed',len(checks),'checks; retained-only',retained)
