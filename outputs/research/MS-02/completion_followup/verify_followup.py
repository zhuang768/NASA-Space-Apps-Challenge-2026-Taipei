"""Verify a pinned MS-02 research revision without regenerating historical tables."""
from pathlib import Path
import csv,hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f); rows=list(reader)
  assert reader.fieldnames and len(reader.fieldnames)==len(set(reader.fieldnames)),str(p)
  assert all(None not in row and all(v is not None for v in row.values()) for row in rows),str(p)
  return rows
checks=[]
def check(name,ok,detail):
 checks.append(dict(check=name,passed=bool(ok),detail=detail))
base=json.loads((HERE/'base_provenance.json').read_text())
report=ROOT/'docs/research/MS-02/report.md'
check('formal_report_preserved',digest(report)==base['formal_report_sha256'],'Original formal report byte hash; later scientific authority is follow-up evidence, not old prose.')
for name,key in [('candidates','candidate_id'),('evidence','evidence_id'),('prior_work','prior_id'),('claims','claim_id'),('footprint','footprint_id')]:
 rows=readcsv(ROOT/f'outputs/research/MS-02/{name}.csv')
 ids=[r[key] for r in rows]
 check(name+'_unique_ids',len(ids)==len(set(ids)),str(len(ids)))
candidates=readcsv(ROOT/'outputs/research/MS-02/candidates.csv')
check('fixed_candidate_ids',[r['candidate_id'] for r in candidates]==['MS-02-E01','MS-02-E02','MS-02-E03','MS-02-E04'],'No renamed or invented Earth sites.')
evidence=readcsv(ROOT/'outputs/research/MS-02/evidence.csv')
facets={'地形','熱性質','水/冰','大氣/沙塵'}
# Original facet labels are preserved; report actual coverage rather than assuming spelling.
coverage={c['candidate_id']:sorted({r['facet'] for r in evidence if r['candidate_id']==c['candidate_id']}) for c in candidates}
check('four_facets_per_earth_candidate',all(facets.issubset(v) for v in coverage.values()),coverage)
for p in sorted(HERE.rglob('*.csv')):
 try:rows=readcsv(p);check('csv:'+p.relative_to(HERE).as_posix(),True,len(rows))
 except Exception as e:check('csv:'+p.relative_to(HERE).as_posix(),False,str(e))
for p in sorted(HERE.rglob('*.json')):
 if p.name in {'verification.json','manifest.json'} and p.parent==HERE:continue
 try:json.loads(p.read_text(),parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Non-finite JSON token: '+x)));check('json:'+p.relative_to(HERE).as_posix(),True,'parsed')
 except Exception as e:check('json:'+p.relative_to(HERE).as_posix(),False,str(e))
manifest=json.loads((HERE/'manifest.json').read_text())
for item in manifest['files']:
 p=ROOT/item['path'];check('sha256:'+item['path'],p.is_file() and digest(p)==item['sha256'],item['sha256'])
status=json.loads((HERE/'completion_status.json').read_text())
check('scientific_completion_not_inferred_from_qa',status['all_ms02_problems_resolved'] is False and bool(status['unresolved_scientific_requirements']),'Pass here means transparent accounting; it never means scientific completion.')
check('publication_scope_only_ms02',all('/MS-02/' in r['path'] for r in manifest['files']),'No shared, other site, or website mutations.')
result={'base_commit':base['base_commit'],'checks':checks,'passed':all(c['passed'] for c in checks),'scientific_completion':False}
(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'checks':len(checks),'failed':[c for c in checks if not c['passed']]},ensure_ascii=False,indent=2))
sys.exit(0 if result['passed'] else 1)
