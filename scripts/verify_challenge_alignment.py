#!/usr/bin/env python3
"""Read-only checks for the current evidence-status handoff and preserved inputs."""
from pathlib import Path
import ast,csv,json,subprocess,hashlib
R=Path(__file__).resolve().parents[1]
BASE='07dbe29203504ba0ccde5e379f42ecc16e4b1b4f'
A=R/'outputs/research/MS-03/repository_validation_20261115'
protected=['outputs/research/mars_reselection_20261114/final_candidates.csv','outputs/research/mars_reselection_20261114/candidate_native_evidence.json','outputs/research/MS-01/candidates.csv','outputs/research/MS-02/candidates.csv','outputs/research/MS-03/candidates.csv','outputs/research/MS-03/polygons_Act-IWS_source.zip']
for p in protected:
 old=subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=R)
 assert old==(R/p).read_bytes(),p
for p in A.rglob('*.csv'):
 rows=list(csv.reader(p.open(encoding='utf-8-sig',newline='')))
 assert rows and all(len(x)==len(rows[0]) for x in rows),str(p)
for p in A.rglob('*.json'):json.load(p.open())
for p in A.rglob('*.py'):ast.parse(p.read_text())
checks=list(csv.DictReader((A/'numeric_audit/ms03_numeric_checks.csv').open()))
assert len(checks)==70 and all(r['pass_check']=='True' for r in checks)
windows=list(csv.DictReader((A/'mars_audit/windows.csv').open()))
assert len(windows)==9 and all(r['acceptance']=='not_accepted' and r['polygon_area_m2']=='NA' and r['polygon_width_m']=='NA' for r in windows)
g=json.load((A/'earth_audit/AD1_Earth_reference_contours.geojson').open())
assert len(g['features'])==185 and all(f['geometry']['type']=='Polygon' and all(r[0]==r[-1] for r in f['geometry']['coordinates']) for f in g['features'])
ledger=list(csv.DictReader((R/'docs/earth_submission_status.csv').open()))
for name in ['Edson Hills','Bethel','Cape Blossom']:
 r=next(r for r in ledger if r['earth_case']==name)
 assert r['repository_data_status']=='source_package_not_found_in_checked_GitHub_records'
 assert r['novelty_status']=='novelty_unverified'
print('PASS: 6 protected science inputs unchanged; 70 retained numeric checks; 9 explicit NA window decisions; 185 Earth-only closed source vectors; proposal ledger and CSV/JSON/Python structure.')
