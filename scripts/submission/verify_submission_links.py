"""Check the final submission index and active local links without fetching providers."""
from pathlib import Path
import csv,json,re,subprocess,urllib.parse
ROOT=Path(__file__).resolve().parents[2]
rows=list(csv.DictReader((ROOT/'outputs/submission/references.csv').open(newline='')))
assert len(rows)>=120
assert len({r['url'] for r in rows})==len(rows)
assert len({r['source_id'] for r in rows})==len(rows)
for r in rows:
 u=urllib.parse.urlsplit(r['url'])
 assert u.scheme in ('http','https') and u.netloc,r
 assert not u.username and not u.password,r['source_id']
 assert not any(k.lower() in ('access_token','authorization','signature','password') for k,v in urllib.parse.parse_qsl(u.query)),r['source_id']
 assert r['use_status'] and r['limits'],r['source_id']
 for locator in r['evidence_path'].split(';'):
  assert (ROOT/locator.strip().split(':',1)[0]).is_file(),(r['source_id'],locator)
 assert r['source_id'] in (ROOT/'docs/SUBMISSION_REFERENCES.md').read_text(),r['source_id']
files=['README.md','DATA_LICENSES.md','docs/REPORT.md','docs/REPRODUCE.md','docs/CHALLENGE_ALIGNMENT.md','docs/SUBMISSION_REFERENCES.md','docs/submission/FINAL_CHECKLIST.md','docs/submission/AI_USAGE.md','docs/submission/deck_review.md','outputs/research/mars_reselection_20261114/README.md']
links=0
for name in files:
 p=ROOT/name
 for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if '://' in link or link.startswith(('#','mailto:')):continue
  target=link.split('#',1)[0]
  if target:
   assert (p.parent/target).exists(),(name,target)
   links+=1
requirements=json.loads((ROOT/'docs/submission/official_requirements.json').read_text())
assert any(r['id']=='demo_format' and r['status']=='confirmed' for r in requirements['requirements'])
assert not any(r['id']=='team_actual_submission' and r['status']=='confirmed' for r in requirements['requirements'])
print(json.dumps({'references':len(rows),'NASA_resources':sum(r['category']=='NASA_data_or_resource' for r in rows),'entrypoint_documents':len(files),'local_links_checked':links,'url_syntax_and_unique_ids':True,'provider_live_availability':'not_rechecked_for_all_links','account_submission':'not_verified'},indent=2))
