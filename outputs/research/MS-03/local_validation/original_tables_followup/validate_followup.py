"""Offline checks; the validator does not acquire data or fabricate observations."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
LOCAL = HERE.parent
ROOT = HERE.parents[4]
BASE = '778af696c654a191fe2a720f24d9f30ebd7d247b'
INTEGRATION_BASE = 'fbfa780cf587a0787739200898e80b4d27fea8d1'
checks = []

def check(name, condition):
    assert condition, name
    checks.append(name)

def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f)
        fields, rows = r.fieldnames, list(r)
    check(str(path.relative_to(ROOT))+' rectangular', all(None not in row and all(v is not None for v in row.values()) for row in rows))
    for row in rows:
        for key, value in row.items():
            if key.endswith('_json'):
                json.loads(value)
    return fields, rows

_, tables = read_csv(HERE/'table_acquisition.csv')
check('exactly three unique target tables', len(tables) == len({r['table_id'] for r in tables}) == 3)
check('all three keep actual acquisition and membership unknown', all(r['original_table_acquired']=='false' and r['roi_test_performed']=='false' and r['roi_membership']=='unknown' for r in tables))
check('uncomputed row/point/footprint counts stay blank', all(r[k]=='' for r in tables for k in ['original_data_row_count','roi_point_hit_count','roi_footprint_hit_count']))
check('no fake original-file location', all(r['file_in_this_checkout']=='' for r in tables))
_, cols = read_csv(HERE/'source_column_notes.csv')
check('nine metadata fields, no measurement rows', len(cols)==9 and all(r['measurement_values_acquired']=='false' for r in cols))
check('CRISM missing data does not become negative evidence', any(r['field_name']=='CRISM ice?' and 'no appropriate data' in r['definition_from_official_metadata'] for r in cols))

_, logs = read_csv(LOCAL/'search_log.csv')
check('search IDs unique', len(logs)==len({r['log_id'] for r in logs}))
old = subprocess.check_output(['git','show',BASE+':outputs/research/MS-03/local_validation/search_log.csv'],cwd=ROOT).decode('utf-8-sig')
old_rows = list(csv.DictReader(old.splitlines()))
current = {r['log_id']:r for r in logs}
check('all 174 baseline search rows retained unchanged', len(old_rows)==174 and all(current[r['log_id']]==r for r in old_rows))
reqs = []
for file in sorted(HERE.glob('requests_round*_retrievals.json')):
    reqs.extend(json.loads(file.read_text()))
check('29 uniquely identified public requests', len(reqs)==len({r['id'] for r in reqs})==29)
check('all request records referenced in main search log', all('LV-TABREQ-'+r['id'] in current for r in reqs))
body_checks = 0
for row in reqs:
    if row.get('file') and (HERE/row['file']).exists():
        raw = (HERE/row['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==row['sha256']
        assert len(raw)==row['bytes']
        body_checks += 1
check('all available retained response bytes match request records', body_checks>0)

content = json.loads((HERE/'content_checks.json').read_text())
check('content classifications cover exactly the requests', {r['request_id'] for r in content['checks']}=={r['id'] for r in reqs})
check('no response mislabeled acquired scientific table', content['original_tables_acquired']==0 and all(r['original_table_acquired'] is False for r in content['checks']))
check('HTTP200 sign-in response explicitly excluded', any(r['request_id']=='L-author-research-old' and r['classification']=='http_200_sign_in_not_public_research_content' for r in content['checks']))
for label, expected in [('data','Data Set 1.tab'),('headers','Data Set Header Descriptions.tab'),('si','SI_Revised.pdf')]:
    obj = json.loads((HERE/'metadata'/('cz_'+label+'.json')).read_text())['data']['attributes']
    check(label+' exact DataCite file identity', obj['titles'][0]['title']==expected)
    original = next(r for r in reqs if r['id']=='CZ-datacite-'+label)
    check(label+' metadata bytes match acquisition', hashlib.sha256((HERE/'metadata'/('cz_'+label+'.json')).read_bytes()).hexdigest()==original['sha256'])

_, prior = read_csv(LOCAL/'local_prior_work.csv')
check('prior-work IDs unique and original candidates retained', len(prior)==len({r['prior_work_id'] for r in prior})==10 and {f'LV-PW{i:02d}' for i in range(1,11)}=={r['prior_work_id'] for r in prior})
_, ice = read_csv(LOCAL/'mars_ice_evidence.csv')
exposure = next(r for r in ice if r['evidence_id']=='LV-ICE08')
check('no local exposure/depth/abundance invented', all(exposure[k]=='unknown' for k in ['value','ice_presence_assessment','actual_ice_depth_m','ice_content_fraction']))
manifest = json.loads((LOCAL/'manifest.json').read_text())
check('fixed cell unchanged', manifest['roi']=={'lat_min':57.5,'lat_max':58,'lon_east_min':242,'lon_east_max':242.5,'latitude':'planetocentric'})
check('morphology unknown, AD1 downgraded, clocks unaligned', manifest['disposition']['morphology']=='unknown' and manifest['disposition']['AD1']=='general_method_reference_only' and manifest['disposition']['campbell_hobo_aligned'] is False)
notes = ROOT/'docs/research/MS-03/local_validation/research_notes.md'
for target in re.findall(r'\]\(([^)]+)\)', notes.read_text()):
    if not target.startswith(('http:','https:','#')):
        assert (notes.parent/target.split('#')[0]).exists(), target
check('all research-note local links resolve', True)
changed = subprocess.check_output(['git','diff','--name-only',INTEGRATION_BASE],cwd=ROOT,text=True).splitlines()
check('tracked edits confined to two local_validation directories', all(x.startswith(('docs/research/MS-03/local_validation/','outputs/research/MS-03/local_validation/')) for x in changed))
check('dedicated follow-up branch used', subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='codex/ms03-original-tables-followup')
base_search = list(csv.DictReader(subprocess.check_output(['git','show',INTEGRATION_BASE+':outputs/research/MS-03/local_validation/search_log.csv'],cwd=ROOT).decode('utf-8-sig').splitlines()))
check('all '+str(len(base_search))+' latest-main search records retained unchanged', len(base_search)>=204 and all(current[r['log_id']]==r for r in base_search))
base_search_bytes = subprocess.check_output(['git','show',INTEGRATION_BASE+':outputs/research/MS-03/local_validation/search_log.csv'],cwd=ROOT)
check('latest-main search-log bytes retained as exact prefix', (LOCAL/'search_log.csv').read_bytes().startswith(base_search_bytes))
crism = subprocess.check_output(['git','ls-tree','-r','--name-only',INTEGRATION_BASE,'--','outputs/research/MS-03/local_validation/crism/'],cwd=ROOT,text=True).splitlines()
for name in crism:
    assert (ROOT/name).read_bytes()==subprocess.check_output(['git','show',INTEGRATION_BASE+':'+name],cwd=ROOT), name
check('all '+str(len(crism))+' CRISM files byte-identical to latest integration base', len(crism)>0)
resources = subprocess.check_output(['git','ls-tree','-r','--name-only',INTEGRATION_BASE,'--','outputs/research/MS-03/local_validation/official_resources/'],cwd=ROOT,text=True).splitlines()
for name in resources:
    assert (ROOT/name).read_bytes()==subprocess.check_output(['git','show',INTEGRATION_BASE+':'+name],cwd=ROOT), name
check('all '+str(len(resources))+' official-resource files byte-identical to latest integration base', len(resources)>0)
name='outputs/research/MS-03/local_validation/observation_inventory.csv'
check('acquired-spectrum inventory retained unchanged', (ROOT/name).read_bytes()==subprocess.check_output(['git','show',INTEGRATION_BASE+':'+name],cwd=ROOT))
result = {'status':'passed','date_taipei':'2026-11-15','starting_sha':BASE,'integration_base_sha':INTEGRATION_BASE,'checks':checks,'available_response_bodies_verified':body_checks,'not_performed':['original-table row parsing or fixed-cell membership computation','new ice or morphology analysis'],'publication_status':'GitHub records actual commit, PR and merge; this validator performs no remote mutations'}
(HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Passed',len(checks),'follow-up checks; raw target tables acquired: 0; no spatial membership test performed.')
