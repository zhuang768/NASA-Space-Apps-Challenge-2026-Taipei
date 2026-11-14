"""Refresh only scoped manifests, preserving earlier records and files."""
from pathlib import Path
import hashlib,json,subprocess
O=Path(__file__).resolve().parent;P=O.parent;ROOT=P.parents[3]
def included(p):return subprocess.run(['git','check-ignore','-q',str(p)],stdout=subprocess.DEVNULL).returncode!=0
def entries(base,exclude):return [dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in sorted(base.rglob('*'))if p.is_file()and p!=exclude and included(p)]
q=json.loads((O/'replay_readiness.json').read_text());v=json.loads((O/'validation.json').read_text());vr=json.loads((O/'validation_retained_only.json').read_text());r=json.loads((O/'retrievals.json').read_text())
m=dict(starting_main_sha=q['starting_main_sha'],branch='codex/ms03-t1811-run-artifacts',date_taipei='2026-11-15',subject='T1811 actual settings/coefficients/paired-array acquisition audit',status='actual run artifacts not obtained; replay not performed; quantitative attribution unknown',scientific_values_changed=False,production_runtime_executed=False,tests=dict(full=v['check_count'],retained_only=vr['check_count']),visual_review='author PDF pp24-26 rendered and opened; original figures not redistributed',source_records=['source_audit.csv','retrievals.json','request_plan.json','inventory_audit.json','paper_read_scope.json'],local_only=[x for x in r if x['status']=='acquired'and not included(O/x['file'])],files=entries(O,O/'manifest.json'))
(O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
mp=P/'manifest.json';old=json.loads(mp.read_text());old['files']=entries(P,mp)
d=ROOT/'docs/research/MS-03/local_validation/research_notes.md';old['files'].append(dict(path=str(d.relative_to(ROOT)),bytes=d.stat().st_size,sha256=hashlib.sha256(d.read_bytes()).hexdigest()))
updates=[x for x in old.get('updates',[])if x.get('package')!='t1811_run_artifacts/manifest.json'];updates.append(dict(starting_sha=q['starting_main_sha'],date_taipei='2026-11-15',package='t1811_run_artifacts/manifest.json',change='official bundle/index/labels cross-checked; original author paper acquired and selected pages read; run coefficients/settings/paired arrays still unknown; no numerical replay/correction'))
old['updates']=updates;mp.write_text(json.dumps(old,indent=2)+'\n');print('Package:',len(m['files']),'files; parent:',len(old['files']))
