"""Checks current revision facts, byte provenance, ROI masks, and change scope.
Does not classify ice or treat passed numerical checks as scientific validation.
"""
from pathlib import Path
import csv,json,hashlib,subprocess
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[3]
def table(n):return list(csv.DictReader((P/n).open(encoding='utf-8-sig')))
def main():
 checks=[]
 def check(name,cond):
  checks.append(dict(check=name,passed=bool(cond)))
  if not cond:raise AssertionError(name)
 geo=json.loads((P/'geography_check.json').read_text());t=json.loads((P/'thermal_pixel.json').read_text())
 check('fixed ROI and archived thermal pixel',t['pixel_bounds']==[168,52.5,168.5,53] and abs(t['depth_m']-.4499824941)<1e-10)
 check('original GIS fullROI mAl',geo['unit']['Unit']=='mAl' and abs(geo['unit_roi_area_fraction']-1)<1e-10)
 check('named-feature polygon not bounding rectangle',not geo['arcadia_MDIM21_polygon_intersects'] and geo['arcadia_MDIM20_bbox_intersects'])
 radar=json.loads((P/'radar_checks.json').read_text());check('three observed segments and194posted columns',len(radar)==3 and sum(r['columns'] for r in radar)==194)
 for r in radar:
  a=np.load(P/'radar_roi'/('s_'+r['orbit_segment']+'.npz'))
  check('radar ROI mask '+r['orbit_segment'],np.all((a['latitude']>=52.5)&(a['latitude']<=53)&(a['longitude']>=168)&(a['longitude']<=168.5)) and a['power'].shape==(3600,r['columns']) and np.isfinite(a['power']).all())
 a=np.load(P/'crism_roi.npz');check('CRISM geometry+sample count',a['if_spectra'].shape==(55,912) and np.all((a['latitude']>=52.5)&(a['latitude']<=53)&(a['longitude']>=168)&(a['longitude']<=168.5)))
 check('CRISM missing values retained',np.sum(a['if_spectra']==65535)==2100 and not a['numeric_valid'][a['if_spectra']==65535].any())
 check('12individually located cores and2unclamped flags',len(table('wendt_core_locations.csv'))==12 and len(table('wendt_quality_flags.csv'))==2)
 check('legacy workbook32sheets',len(table('workbook_inventory.csv'))==32)
 for fn in ['local_prior_work.csv','mars_ice_evidence.csv','analog_validation.csv','search_log.csv','claim_corrections.csv']:
  rows=table(fn);ids=[next(iter(r.values())) for r in rows];check('unique IDs '+fn,len(ids)==len(set(ids)) and all(ids))
 ev={r['evidence_id']:r for r in table('mars_ice_evidence.csv')};check('unknown amount and retractedbinary not filled',not ev['MV-03']['value'] and not ev['ME-06']['value'])
 check('four prior-work classes',set(r['relation_class'] for r in table('local_prior_work.csv'))=={'格內同用途','格內不同用途','附近／大區域','位置不明'})
 manifest=json.loads((P/'manifest.json').read_text());verified=0
 for f in manifest['files']:
  p=R/f['path']
  if not p.exists():
   check('only local-only files may be absent',f['storage']=='local_only');continue
  check('hash '+f['path'],hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']);verified+=1
 # Compare against latest preserved remote snapshot, not base containing others' work.
 paths=subprocess.check_output(['git','diff','--name-only','ef5eb162b1df0919b8d6dd780782896188607b2c'],cwd=R,text=True).splitlines()
 paths+=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines()
 prefixes=('docs/research/MS-02/local_validation/','outputs/research/MS-02/local_validation/')
 check('all modified/untracked deliverables within allowed directories',all(x.startswith(prefixes) for x in paths))
 check('original branch',subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()=='research/ms-02-earth-analogs')
 out=dict(check_date='2026-11-15',all_passed=True,checks_count=len(checks),hashed_files_verified=verified,checks=checks,limits='Numerical/provenance checks only; no validated ice detection; original historical verifiers not rerun')
 (P/'revision_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},ensure_ascii=False))
if __name__=='__main__':main()
