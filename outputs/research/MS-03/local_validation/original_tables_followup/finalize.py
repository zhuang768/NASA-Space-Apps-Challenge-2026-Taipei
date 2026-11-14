"""Finalize this local supplement, without network access, commit, or push."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
LOCAL = HERE.parent
ROOT = HERE.parents[4]

for script in [HERE/'integrate_tables.py', LOCAL/'validate.py', HERE/'validate_followup.py']:
    subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)

path = LOCAL/'manifest.json'
manifest = json.loads(path.read_text())
manifest['original_tables_followup'] = {
    'date_taipei': '2026-11-15',
    'starting_sha': '778af696c654a191fe2a720f24d9f30ebd7d247b',
    'delivery_state': 'prepared for user-authorized follow-up PR and merge; actual status recorded by GitHub',
    'integration_base_sha': 'fbfa780cf587a0787739200898e80b4d27fea8d1',
    'branch': 'codex/ms03-original-tables-followup',
    'prior_delivery_state': 'initial local-only checkpoint superseded by later push-and-merge authorization',
    'public_requests_recorded': 29,
    'original_target_tables_acquired': 0,
    'fixed_cell_membership_computed': False,
    'new_scientific_disposition': 'unchanged; unknown morphology, independent local ice/depth/content unconfirmed',
    'validation': 'original_tables_followup/validation.json',
    'timestamp_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
}
manifest['known_acquisition_limits'] = list(dict.fromkeys(manifest['known_acquisition_limits'] + [
    'Cohen-Zada exact file identities confirmed by DataCite; original table/header bytes not acquired',
    'Levy Data Set S1 TXT/XLS and Dundas TableS4 CSV not acquired; table membership remains unknown',
    'USGS AIS is the same existing FGDC metadata, not an independent observation table',
    'A speculative historical lab alias returned an HTTP200 sign-in page, not readable public research',
]))
paths = {row['path'] for row in manifest['files']}
paths.add('docs/research/MS-03/local_validation/research_notes.md')
for f in HERE.rglob('*'):
    if f.is_file() and not any(part in {'responses','__pycache__'} for part in f.relative_to(HERE).parts):
        paths.add(str(f.relative_to(ROOT)))
entries = []
for name in sorted(paths):
    file = ROOT/name
    assert file.exists(), name
    assert name.startswith(('docs/research/MS-03/local_validation/','outputs/research/MS-03/local_validation/'))
    assert file != path
    raw = file.read_bytes()
    entries.append({'path':name, 'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()})
manifest['files'] = entries
path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for row in json.loads(path.read_text())['files']:
    raw = (ROOT/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
print('Manifest verified:',len(entries),'files; no commit, push, PR edit, or merge performed.')
