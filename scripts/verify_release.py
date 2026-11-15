#!/usr/bin/env python3
"""Check the current named evidence inventory; no scientific/eligibility approval.

The preceding historical manifest is retained separately. This checks only the
explicitly listed current files and active entry-point links, not every old
source note, deleted report, or every path in the full repository history.
"""
from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/research/mars_reselection_20261114'


def main():
    manifest = json.loads((ROOT / 'release_manifest.json').read_text())
    checked = set()
    for entry in manifest['files']:
        assert entry['path'] not in checked, entry['path']
        checked.add(entry['path'])
        path = ROOT / entry['path']
        content = path.read_bytes()
        assert len(content) == entry['bytes'], entry['path']
        assert hashlib.sha256(content).hexdigest() == entry['sha256'], entry['path']
    rows = list(csv.DictReader((OUT / 'final_candidates.csv').open()))
    assert [r['candidate_id'] for r in rows] == ['MS-01', 'MS-02', 'MS-03']
    assert [r['input_review_id'] for r in rows] == ['A', 'D', 'C']
    assert all('not_globally_novelty_cleared' in r['final_selection_status'] for r in rows)
    sites = json.loads((OUT / 'selected_targets.json').read_text())['sites']
    assert [(s['center']['lat'], s['center']['lon']) for s in sites] == [(56.75, 72.75), (52.75, 168.25), (57.75, -117.75)]
    assert (OUT / 'candidate_map.png').read_bytes().startswith(bytes([137, 80, 78, 71]))
    active_docs = ['README.md', 'DATA_LICENSES.md', 'docs/REPORT.md', 'docs/CHALLENGE_ALIGNMENT.md', 'docs/ARCHIVE.md', 'docs/REPRODUCE.md']
    for name in active_docs:
        path = ROOT / name
        for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            if '://' in link or link.startswith(('#', 'mailto:')):
                continue
            target = link.split('#', 1)[0]
            if target:
                assert (path.parent / target).exists(), (name, target)
    print(f"PASS: {len(checked)} named file hashes; fixed target identities; current entry-point links. No ice, novelty, eligibility or deployment validation.")


if __name__ == '__main__':
    main()
