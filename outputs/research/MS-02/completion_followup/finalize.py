"""Refresh only revision accounting; never regenerate old scientific tables."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=json.loads((HERE/'base_provenance.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
status=json.loads((HERE/'completion_status.json').read_text())
for relative in ['outputs/research/MS-02/manifest.json','outputs/research/MS-02/local_validation/manifest.json']:
 p=ROOT/relative;obj=json.loads(p.read_text())
 # Update only existing, locally present registered files. Absent local-only sources retain their historical metadata.
 for row in obj.get('files',[]):
  q=ROOT/row['path']
  if q.is_file():row.update(bytes=q.stat().st_size,sha256=sha(q))
 obj['completion_followup']={'date_taipei':'2026-11-15','base_commit':BASE['base_commit'],'manifest':'outputs/research/MS-02/completion_followup/manifest.json','status':'outputs/research/MS-02/completion_followup/completion_status.json','all_ms02_problems_resolved':False,'formal_report_status':'Preserved byte-for-byte as requested. Old prose contains historical superseded claims; use current structured corrections and follow-up notes pending human revision.','verification_scope':'Historical verification outputs were not rerun or relabeled as current; use completion_followup/verify_followup.py and each analysis verifier.'}
 if relative=='outputs/research/MS-02/manifest.json':
  obj.setdefault('historical_unresolved_gaps_before_completion_followup',obj.get('unresolved_gaps',[]))
  obj['unresolved_gaps']=status['unresolved_scientific_requirements']
  obj['common_data_check']['outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx']['opened']='Current follow-up verified exact Git blob and all ZIP CRC; workbook.xml contains 32 sheets. Historical report statement of 33 is superseded.'
  obj['common_data_check']['current_reproduction']='completion_followup/audit/current_handoff_check.json: 14 same-quantity comparisons, 58238 pool rows, unique MS-02, four exact input blobs; this is lineage consistency, not independent physical truth.'
  obj['disposition_summary']={'MS-02-E01':'Retain W-station seasonal thermal/interface reference with independent material/clock limits','MS-02-E02':'Retain Liu2018 located thermal-material subcase only; original series/calibration not acquired','MS-02-E03':'Retain CS-1 aeolian/syngenetic-ice process; ADE and WISDOM separate; no colocated radar validation','MS-02-E04':'Retain Thomson2012 excavated same-line core/GPR method subcase only; no undisturbed or orbital validation'}
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
# The parent manifest hashes revision outputs and both refreshed manifests. It excludes itself and its verifier output.
paths=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.b64','.tmp'} and p.name!='.DS_Store' and p not in {HERE/'manifest.json',HERE/'verification.json'}]
paths += [ROOT/'outputs/research/MS-02'/n for n in ['candidates.csv','evidence.csv','claims.csv','footprint.csv','prior_work.csv','manifest.json','local_validation/mars_ice_evidence.csv','local_validation/manifest.json']]
files=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(set(paths))]
manifest={'schema_version':1,'base_commit':BASE['base_commit'],'base_tree':BASE['base_tree'],'date_taipei':'2026-11-15','fixed_roi':BASE['fixed_roi'],'formal_report_sha256':BASE['formal_report_sha256'],'scientific_completion':False,'files':files,'excluded_self_hashes':['outputs/research/MS-02/completion_followup/manifest.json','outputs/research/MS-02/completion_followup/verification.json'],'meaning':'A hash/QA pass proves reproducible research records only. It does not turn missing observations into resolved scientific questions.'}
(HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'registered_files':len(files),'scientific_completion':False}))
