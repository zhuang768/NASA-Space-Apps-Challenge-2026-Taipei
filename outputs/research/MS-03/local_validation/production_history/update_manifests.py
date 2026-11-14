"""Update scoped manifests while retaining all earlier provenance records."""
from pathlib import Path
import hashlib,json,subprocess
O=Path(__file__).resolve().parent;P=O.parent;ROOT=P.parents[3]
def included(p):return subprocess.run(['git','check-ignore','-q',str(p)],stdout=subprocess.DEVNULL).returncode!=0
def entries(base,exclude):
    return [dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(base.rglob('*')) if p.is_file() and p!=exclude and included(p)]
r=json.loads((O/'results.json').read_text());v=json.loads((O/'validation.json').read_text());vr=json.loads((O/'validation_retained_only.json').read_text())
retrievals=json.loads((O/'retrievals.json').read_text())
m=dict(starting_main_sha=r['starting_main_sha'],synchronized_main_sha='2b3984047b8983a1db8b9f15a585d88651d74a5b',branch='codex/ms03-production-history',date_taipei='2026-11-15',
    subject='MRDR1.03.94 author/public history and normalization artifacts',
    status='second summary optimization documented before product; numerical attribution unknown',
    scientific_values_changed=False,production_runtime_executed=False,
    visual_review='F-PH01 opened; overflow corrected; final figure opened again',
    tests=dict(full=v['check_count'],retained_only=vr['check_count']),
    source_records=['retrievals.json','request_plan.json','source_audit.csv','history_sections.json','product_metadata.json','search_log.csv'],
    local_only=[x for x in retrievals if x['status']=='acquired' and not included(O/x['file'])],
    files=entries(O,O/'manifest.json'))
(O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
mp=P/'manifest.json';old=json.loads(mp.read_text());old['files']=entries(P,mp)
d=ROOT/'docs/research/MS-03/local_validation/research_notes.md';old['files'].append(dict(path=str(d.relative_to(ROOT)),bytes=d.stat().st_size,sha256=hashlib.sha256(d.read_bytes()).hexdigest()))
updates=old.get('updates',[]);updates=[x for x in updates if x.get('package')!='production_history/manifest.json']
updates.append(dict(starting_sha=r['starting_main_sha'],date_taipei='2026-11-15',package='production_history/manifest.json',change='dated historical documentation confirms second summary optimization; exact build/config/prepost/coefficient records not obtained; no numerical changes'))
old['updates']=updates;mp.write_text(json.dumps(old,indent=2)+'\n')
print('Package:',len(m['files']),'files; parent:',len(old['files']))
