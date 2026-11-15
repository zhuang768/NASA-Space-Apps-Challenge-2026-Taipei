"""Verify the UI refinement preserves the existing scientific numeric arrays.

Run from any directory. This is a value-preservation check, not scientific validation.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = '25b0744ac3d2230803505e1679109c2c35b6204d'
WEB = 'outputs/integration/zasa-acceptance-20261115/web/app.js'
previous = subprocess.check_output(['git', 'show', f'{BASE}:{WEB}'], cwd=ROOT).decode()
current = (ROOT / WEB).read_text()
checks = []
for name in ['SITES', 'UV_MONTHLY_C', 'UV_DAMP', 'UV_MIN_C', 'UV_MAX_C']:
    pattern = r'var SITES = (\[.*?\n\]);' if name == 'SITES' else rf'var {name} = (.*?);'
    old = re.search(pattern, previous, re.S).group(1)
    new = re.search(pattern, current, re.S).group(1)
    assert old == new, f'{name}: source array changed'
    checks.append({'array': name, 'unchanged': True, 'sha256': hashlib.sha256(new.encode()).hexdigest()})
protected = ['outputs/research/mars_reselection_20261114/final_candidates.csv',
             'outputs/research/mars_reselection_20261114/candidate_native_evidence.json',
             'outputs/research/MS-01/candidates.csv', 'outputs/research/MS-02/candidates.csv',
             'outputs/research/MS-03/candidates.csv']
for path in protected:
    assert subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT) == (ROOT / path).read_bytes(), path
print(json.dumps({'base_commit': BASE, 'numeric_arrays': checks, 'protected_data_files': len(protected),
                  'scope': 'UI source preservation only; no new ice, analogy or novelty validation'}, indent=2))
