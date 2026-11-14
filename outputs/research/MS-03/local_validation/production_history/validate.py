"""Offline provenance checks, not a production-runtime or ice-detection test."""
from pathlib import Path
import csv,hashlib,json,sys,subprocess
O=Path(__file__).resolve().parent
retained='--retained-only' in sys.argv;checks=[];omitted=[]
def check(name,ok):
    assert ok,name
    checks.append(name)
for r in json.loads((O/'retrievals.json').read_text()):
    if r['status']!='acquired':continue
    f=O/r['file'];ignored=subprocess.run(['git','check-ignore','-q',str(f)]).returncode==0
    if ignored and (retained or not f.exists()):omitted.append(r['file']);continue
    check(f.name+' source SHA256',f.exists() and hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'])
d=json.loads((O/'history_sections.json').read_text())
check('2022 documented version predates actual product',d[0]['document_version']=='1.3.7.6' and d[0]['document_date']<'2023-07-18')
check('independent historical capture dated20220930',json.loads((O/'sources/wayback_dpsis_2022_2023.json').read_text())[1][1]=='20220930185840')
check('section8 complete normalized hashes match',d[0]['section8_sha256']==d[1]['section8_sha256'] and all(x['section8_character_count']==738 for x in d))
if not retained and (O/d[0]['file']).exists():
    from inspect_history import visible
    for x in d:
        s=visible(O/x['file'])[x['section8_start_offset']:x['section8_end_offset']].strip()
        check(x['source_id']+' reproducible section hash',hashlib.sha256(s.encode()).hexdigest()==x['section8_sha256'] and 'applied a second time' in s)
p=json.loads((O/'product_metadata.json').read_text())
check('AL and SU actual software1.03.94',len(p)==2 and all(x['inspected_fields']['program_version']==['1.03.94'] for x in p))
check('actual2023 product timestamps',all(x['inspected_fields']['program_stop_date_time']==['2023-07-18T18:12:54Z'] for x in p))
for name,key,n in [('source_audit.csv','source_id',7),('processing_stages.csv','stage_id',5),('version_history.csv','version',4),('availability.csv','item_id',9),('search_log.csv','log_id',None)]:
    with (O/name).open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f))
    check(name+' rectangular/unique',all(None not in x and all(v is not None for v in x.values()) for x in r) and len({x[key] for x in r})==len(r) and (len(r)==n if n else len(r)>20))
q=json.loads((O/'results.json').read_text());old=json.loads((O.parent/'bd1500_audit/results.json').read_text())
check('residual numbers are referenced unchanged',q['prior_strict_residual_unchanged']==old['cat64_minus_official_strict'])
check('quantitative attribution and local ice remain unknown',all(q[k]=='unknown' for k in ['quantitative_attribution','local_ice_presence','local_ice_depth_m','local_ice_fraction']))
check('no execution/settings/prepost/coefficient claim',not any(q[k] for k in ['exact_1_03_94_source_obtained','execution_settings_obtained','normalization_coefficients_obtained','paired_pre_post_data_obtained','production_runtime_executed']))
check('no fitted or original-data corrections',not q['fitted_correction_applied'] and not q['original_scientific_values_changed'])
for x in json.loads((O/'preserved_inputs.json').read_text()):
    p=O.parent/x['path'];ignored=subprocess.run(['git','check-ignore','-q',str(p)]).returncode==0
    if retained and ignored:omitted.append(x['path']);continue
    check(x['path']+' preserved data hash',p.stat().st_size==x['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'])
for f in O.glob('*.json'):json.loads(f.read_text())
for f in O.glob('*.py'):compile(f.read_text(),str(f),'exec')
check('JSON and Python parse',True)
(O/('validation_retained_only.json' if retained else 'validation.json')).write_text(json.dumps(dict(status='passed',check_count=len(checks),checks=checks,omitted_local_only=omitted,not_executed=['exact production runtime','stage-by-stage numerical reconstruction','ice detection validation']),indent=2)+'\n')
print('Passed',len(checks),'provenance checks; retained-only',retained)
