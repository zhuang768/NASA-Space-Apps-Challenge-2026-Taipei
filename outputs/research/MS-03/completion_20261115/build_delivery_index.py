#!/usr/bin/env python3
"""Build an honest, offline MS-03 delivery inventory and requirement audit.

Usage: python3 build_delivery_index.py ROOT [--source-tree JSON]
       [--repository-tree JSON] [--strict] [--self-test]

The original selected Git-tree snapshot is read from ROOT/source_tree.json on
first use and retained as completion_20261115/baseline_git_tree.json. A full
repository_tree.json is optional and improves relative-link verification. The
program never downloads, changes science arrays, repairs timestamps, or labels
scientific unknowns resolved. Inherited checksums are not recomputed checksums.
"""
import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from urllib.parse import unquote, urlsplit

PREFIXES = ('docs/research/MS-03/', 'outputs/research/MS-03/', 'scripts/research/MS-03/')
OUT = 'outputs/research/MS-03/completion_20261115'
REPO = 'https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei'
EXCLUDED = {
    'outputs/research/MS-03/manifest.json': 'Parent manifest may link to this package; excluded to avoid a checksum cycle.',
    OUT + '/file_inventory.csv': 'Generated inventory cannot contain its own checksum.',
    OUT + '/manifest.json': 'Package manifest cannot contain its own checksum.',
    OUT + '/validation.json': 'Validation receipt describes generated inventories; excluded from the content hash graph.',
    OUT + '/publication_receipt.json': 'Post-publication metadata is excluded to avoid a publication checksum cycle.',
    OUT + '/delivery_receipt.json': 'Post-publication metadata is excluded to avoid a publication checksum cycle.',
}
GENERATED = {'file_inventory.csv', 'manifest.json', 'validation.json', 'publication_receipt.json', 'delivery_receipt.json'}
THEMES = {'terrain', 'temperature_thermal', 'water_ice', 'atmosphere_dust'}
ALLOWED_CHANGED = {
    'docs/research/MS-03/report.md',
    'outputs/research/MS-03/candidates.csv',
    'outputs/research/MS-03/evidence.csv',
    'outputs/research/MS-03/prior_work.csv',
    'outputs/research/MS-03/search_log.csv',
    'outputs/research/MS-03/sources.json',
}


def owned(path):
    return any(path.startswith(p) for p in PREFIXES)


def ephemeral(path):
    parts = PurePosixPath(path).parts
    return any(p in {'__pycache__', '.mplconfig', '.pytest_cache', '.downloads'} for p in parts) or path.endswith(('.pyc', '.pyo', '.DS_Store'))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load_json(path, default=None):
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def read_csv(path):
    if not path.is_file():
        return [], [], ['missing: ' + str(path)]
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    errors = []
    if not reader.fieldnames or None in reader.fieldnames:
        errors.append('invalid header: ' + str(path))
    if any(None in row for row in rows):
        errors.append('extra CSV fields: ' + str(path))
    return reader.fieldnames or [], rows, errors


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n', extrasaction='raise')
        writer.writeheader()
        writer.writerows(rows)


def tree_entries(tree):
    if not isinstance(tree, dict):
        return {}
    return {e['path']: e for e in tree.get('files', tree.get('tree', []))
            if e.get('type', 'blob') == 'blob' and 'path' in e}


def inherited_hashes(root):
    """Read checksum assertions as assertions, preserving their origin/conflicts."""
    found = {}
    for parent in ('outputs/research/MS-03', 'docs/research/MS-03'):
        for path in (root / parent).rglob('manifest.json'):
            if path == root / OUT / 'manifest.json':
                continue
            try:
                value = load_json(path, {})
            except (ValueError, OSError):
                continue
            for key in ('files', 'outputs', 'inputs', 'historical_outputs'):
                entries = value.get(key, [])
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    if not isinstance(entry, dict) or not entry.get('path') or not entry.get('sha256'):
                        continue
                    p = str(entry['path'])
                    if not p.startswith(('outputs/', 'docs/', 'scripts/')):
                        p = (path.parent.relative_to(root) / p).as_posix()
                    found.setdefault(p, []).append({
                        'manifest': path.relative_to(root).as_posix(),
                        'sha256': entry['sha256'],
                        'bytes': entry.get('bytes', entry.get('size')),
                    })
    return found


def source_registry(root):
    base = root / 'outputs/research/MS-03'
    registry = {}
    for path in (base / 'manifest.json', base / 'sources.json'):
        value = load_json(path, {})
        if path.name == 'manifest.json':
            value = value.get('sources', {})
        if isinstance(value, dict):
            for key, item in value.items():
                if isinstance(item, dict) and item.get('url'):
                    registry[key] = item
    # A source crosswalk is an explicit registry, not an inferred citation.
    for name in ('source_crosswalk.csv', 'source_catalog.csv'):
        path = root / OUT / name
        if path.is_file():
            _, rows, _ = read_csv(path)
            for row in rows:
                source_id = row.get('source_id')
                url = row.get('source_url', row.get('url'))
                if source_id and url:
                    registry[source_id] = {'url': url, 'locator': row.get('source_locator', row.get('locator', ''))}
    return registry


def parse_links(root, remote_paths):
    links = []
    pattern = re.compile(r'!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)')
    for base in ('docs/research/MS-03', 'outputs/research/MS-03'):
        for path in sorted((root / base).rglob('*.md')):
            text = path.read_text(encoding='utf-8')
            for line_no, line in enumerate(text.splitlines(), 1):
                for match in pattern.finditer(line):
                    target = match.group(1).strip('<>')
                    parsed = urlsplit(target)
                    if parsed.scheme or parsed.netloc or target.startswith('#'):
                        continue
                    clean = unquote(parsed.path).replace('\\', '/')
                    if not clean:
                        continue
                    # Normalize lexically; resolve() would follow a local symlink.
                    candidate = Path(os.path.normpath(str(path.parent / clean)))
                    try:
                        rel = candidate.relative_to(root).as_posix()
                    except ValueError:
                        status = 'outside_repository_unverified'
                        rel = str(candidate)
                    else:
                        if candidate.exists():
                            status = 'local_exists'
                        elif rel in remote_paths:
                            status = 'remote_tree_reference_only'
                        else:
                            status = 'missing_or_not_in_supplied_tree'
                    links.append({'from_path': path.relative_to(root).as_posix(),
                                  'line': line_no, 'target': target,
                                  'resolved_path': rel, 'status': status,
                                  'limit': 'Existence/path check only; anchors, external URLs, scientific content and historical URLs are not validated here.'})
    return links


def open_questions():
    # Deliberately separates scientific inference from delivery/test status.
    return [
        {'question_id': 'SCI-01', 'topic': 'MS-03 independent ice confirmation', 'status': 'unresolved',
         'current_evidence': 'Regional SWIM/thermal products and acquired local optical/spectral/radar evidence do not independently establish local subsurface ice.',
         'decisive_next_step': 'Acquire QA-qualified co-located evidence with a justified sensitivity model; validate alternative material/atmospheric/surface explanations.',
         'blocked_claim': 'Confirmed ice presence or validated resource/base feasibility.'},
        {'question_id': 'SCI-02', 'topic': 'Actual ice depth and fraction', 'status': 'unresolved',
         'current_evidence': 'The conditional thermal-model interface is not a measured depth; unvalidated radar maxima are not subsurface picks.',
         'decisive_next_step': 'Validate surface/clutter/artefacts and a physical reflector interpretation with independent dielectric/depth constraints; do not infer a shallow interface from delay sampling alone.',
         'blocked_claim': 'Measured ice depth, ice abundance, extraction yield or energy.'},
        {'question_id': 'SCI-03', 'topic': 'Mars polygons and specific AD1 pairing', 'status': 'unresolved',
         'current_evidence': 'No reliable closed Mars-boundary sample has been established in the fixed cell; AD1 remains a general-method reference.',
         'decisive_next_step': 'Obtain registered, adequately resolved in-cell imagery; define reproducible tracing/reviewer agreement and common sampling before comparing Earth/Mars distributions.',
         'blocked_claim': 'Absent Mars polygons, an AD1-matched distribution, common genesis or an ice-wedge identification.'},
        {'question_id': 'SCI-04', 'topic': 'T1811 numerical production attribution', 'status': 'unresolved',
         'current_evidence': 'Documented summary-stage adjustment explains non-equivalence of delivered AL/SU in principle; actual build/settings/intermediates are not recovered.',
         'decisive_next_step': 'Obtain versioned executable/source/dependencies, exact options, masks, optimization coefficients and paired before/after arrays; replay rather than fit away the residual.',
         'blocked_claim': 'An identified producer bug, a corrected official parameter or a calibrated ice index.'},
        {'question_id': 'SCI-05', 'topic': 'Spectral scientific QA and detection limits', 'status': 'unresolved',
         'current_evidence': 'Numeric/calibration masks and formula diagnostics do not resolve local cloud, frost, aerosol or instrument residuals.',
         'decisive_next_step': 'Use mode-appropriate corrections and independently justified quality/seasonal/control masks; derive detection limits from justified controls and uncertainty.',
         'blocked_claim': 'An ice detection/absence result based only on an index sign or numeric-valid pixel count.'},
        {'question_id': 'SCI-06', 'topic': 'University Valley independent clock alignment', 'status': 'unresolved',
         'current_evidence': 'Author-processed files are available, but unprocessed logger, calibration code and deployment/clock logs are missing; the documented discontinuity does not identify a correct shift.',
         'decisive_next_step': 'Recover original logger bytes, calibration/dependency versions and independent clock-operation records for each instrument; verify alignment before cross-logger thermal analysis.',
         'blocked_claim': 'An inferred four-hour correction, synchronized Campbell-HOBO lag/diffusivity or an Earth-to-Mars ice-depth transfer.'},
        {'question_id': 'SCI-07', 'topic': 'AD1 exact thermal/GPR spatial crosswalk', 'status': 'unresolved',
         'current_evidence': 'Published polygon GIS and regional permafrost monitoring do not establish co-location of every later sensor or radar profile with the AD1 polygons.',
         'decisive_next_step': 'Acquire original sensor/profile coordinates, datum and deployment geometry; intersect footprints explicitly and preserve observations from different places separately.',
         'blocked_claim': 'A measured thermal/ice truth series for every mapped AD1 polygon.'},
        {'question_id': 'SCI-08', 'topic': 'Historical completeness and novelty', 'status': 'unresolved',
         'current_evidence': 'Direct Earth-use precedents and bounded Mars catalogue checks are recorded; point membership and failed acquisitions do not exhaust all observations, footprints or literature.',
         'decisive_next_step': 'Continue source-specific original-table membership/footprint checks and an explicitly bounded primary-literature search; retain inclusion rules and reading scope.',
         'blocked_claim': 'A first site/analogue, a globally unstudied location or exhaustive novelty clearance.'},
    ]


def build(root, source_tree=None, repository_tree=None, strict=False):
    root = root.resolve()
    package = root / OUT
    package.mkdir(parents=True, exist_ok=True)
    origin = source_tree or (root / 'source_tree.json')
    if not origin.is_file():
        origin = package / 'baseline_git_tree.json'
    baseline = load_json(origin)
    if not isinstance(baseline, dict) or not tree_entries(baseline):
        raise ValueError('A real baseline Git-tree JSON is required; no baseline is invented.')
    all_baseline = tree_entries(baseline)
    expected = {p: e for p, e in all_baseline.items() if owned(p) and not ephemeral(p)}
    # Persist the selected original tree as a small, reproducible input, not a
    # claim that remote-only payload bytes were downloaded or read.
    frozen = {'sha': baseline.get('sha'), 'tree': baseline.get('tree'),
              'scope': 'MS-03-owned paths from the supplied selected Git tree',
              'files': [expected[p] for p in sorted(expected)]}
    write_json(package / 'baseline_git_tree.json', frozen)
    full_tree_path = repository_tree or (root / 'repository_tree.json')
    full_tree = load_json(full_tree_path, {})
    remote_paths = set(all_baseline) | set(tree_entries(full_tree))
    remote_paths |= set(expected)

    base = root / 'outputs/research/MS-03'
    tables = {}
    errors = []
    for filename in ('candidates.csv', 'evidence.csv', 'prior_work.csv', 'search_log.csv'):
        _, rows, csv_errors = read_csv(base / filename)
        tables[filename] = rows
        errors.extend(csv_errors)
    candidates, evidence = tables['candidates.csv'], tables['evidence.csv']
    priors, searches = tables['prior_work.csv'], tables['search_log.csv']
    checks = []

    def check(name, passed, detail):
        checks.append({'check': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            errors.append(name + ': ' + detail)

    for filename, key in (('candidates.csv', 'candidate_id'), ('evidence.csv', 'evidence_id'),
                          ('prior_work.csv', 'prior_id'), ('search_log.csv', 'search_id')):
        rows = tables[filename]
        ids = [r.get(key, '') for r in rows]
        check('unique_nonempty_ids:' + filename, bool(ids) and all(ids) and len(ids) == len(set(ids)), 'Unique nonempty ' + key + '; rows=' + str(len(rows)))
    ids = {r.get('candidate_id') for r in candidates}
    check('at_least_two_candidates', len(ids) >= 2 and {'MS-03-E01', 'MS-03-E02'} <= ids, repr(sorted(str(x) for x in ids)))
    for row in candidates:
        cid = row.get('candidate_id', '')
        try:
            lat, lon = float(row['latitude_deg']), float(row['longitude_east_deg'])
            coordinate_ok = math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180
            json.loads(row['bounds_json'])
        except (KeyError, ValueError, TypeError):
            coordinate_ok = False
        check('candidate_coordinates_extent:' + cid, coordinate_ok and row.get('mars_id') == 'MS-03', 'Coordinate range, finite values, extent JSON and Mars ID; no invented Earth-Mars equivalence.')
        anchors = {'MS-03-E01': (-(77 + 51.729 / 60), 160 + 42.606 / 60), 'MS-03-E02': (78.184, 15.913)}
        if cid in anchors:
            target_lat, target_lon = anchors[cid]
            exact_anchor = coordinate_ok and abs(lat - target_lat) < 1e-9 and abs(lon - target_lon) < 1e-9
            check('published_candidate_anchor:' + cid, exact_anchor, 'W deployment anchor or AD1 metadata event anchor; neither is silently relabelled a sensor/area centroid.')
        actual = {r.get('theme') for r in evidence if r.get('candidate_id') == cid}
        check('four_dimensions:' + cid, THEMES <= actual, ','.join(sorted(actual)))
        check('candidate_scope_and_disposition:' + cid,
              all(row.get(k, '').strip() for k in ('name', 'coordinate_source', 'extent_basis', 'test_purpose', 'disposition', 'next_step', 'cannot_infer')),
              'Nonempty identity, extent basis, purpose, disposition, next step and inference limits.')
        direct = [p for p in priors if p.get('candidate_id') == cid]
        check('prior_use_review:' + cid, bool(direct), 'Recorded prior-use rows=' + str(len(direct)))
    reference = load_json(base / 'mars_reference.json', {})
    record = reference.get('record', {})
    center, bounds = record.get('center', {}), record.get('nominal_cell_bounds', {})
    roi_ok = center == {'lat': 57.75, 'lon': -117.75} and bounds == {'south': 57.5, 'north': 58.0, 'west': -118.0, 'east': -117.5}
    check('fixed_mars_roi', roi_ok, 'MS-03 center57.75N,242.25E; fixed57.50–58.00N,242.00–242.50E; -117.75E representation changes no geometry.')
    registry = source_registry(root)
    crossrefs = []
    for name, rows, key in (('evidence.csv', evidence, 'evidence_id'), ('prior_work.csv', priors, 'prior_id')):
        for row in rows:
            sid, url = row.get('source_id', ''), row.get('source_url', '')
            item = registry.get(sid, {})
            good = bool(sid and url and item.get('url') == url)
            crossrefs.append({'table': name, 'row_id': row.get(key, ''), 'source_id': sid,
                              'source_url': url, 'registry_url': item.get('url', ''),
                              'status': 'exact_match' if good else 'missing_or_mismatched_registry',
                              'limit': 'Registry identity and locator presence do not prove the primary source was fully read.'})
    check('source_id_url_cross_references', all(r['status'] == 'exact_match' for r in crossrefs) and bool(crossrefs), str(sum(r['status'] != 'exact_match' for r in crossrefs)) + ' unresolved source cross-reference rows.')
    check('evidence_metadata', all(all(r.get(k, '').strip() for k in ('theme', 'metric', 'value', 'unit', 'period', 'spatial_support', 'evidence_type', 'source_url', 'source_locator', 'read_scope', 'status', 'limitations')) for r in evidence), 'Unknown is an explicit permitted value; blank provenance/support/limits are not permitted.')
    check('prior_classification', all(r.get('classification') in {'direct_precedent', 'partial_overlap', 'different_use', 'insufficient_evidence'} and r.get('source_locator') and r.get('read_scope') for r in priors), 'Classification, locator and actual reading scope.')
    check('search_metadata', all(all(r.get(k, '').strip() for k in ('date_taipei', 'platform', 'query', 'outcome', 'limitation')) for r in searches), 'Dates, platform, exact query, result and bounded limitation.')
    report = root / 'docs/research/MS-03/report.md'
    check('report_exists', report.is_file() and report.stat().st_size > 0, 'Current report present; correctness of scientific prose needs explicit reviewer inspection.')
    check('required_delivery_files', all((base / name).is_file() for name in ('candidates.csv', 'evidence.csv', 'prior_work.csv', 'search_log.csv', 'manifest.json')), 'Required machine-readable files and original parent manifest present.')

    links = parse_links(root, remote_paths)
    missing_links = [r for r in links if r['status'] in {'missing_or_not_in_supplied_tree', 'outside_repository_unverified'}]
    check('relative_link_paths', not missing_links, str(len(links)) + ' local relative links checked; ' + str(len(missing_links)) + ' unresolved; tree-only targets are explicitly not downloaded bytes.')
    write_csv(package / 'link_inventory.csv', links, ['from_path', 'line', 'target', 'resolved_path', 'status', 'limit'])
    write_csv(package / 'source_cross_reference_checks.csv', crossrefs, ['table', 'row_id', 'source_id', 'source_url', 'registry_url', 'status', 'limit'])
    questions = open_questions()
    write_csv(package / 'open_questions.csv', questions, ['question_id', 'topic', 'status', 'current_evidence', 'decisive_next_step', 'blocked_claim'])
    by_check = {r['check']: r['passed'] for r in checks}

    def all_prefix(prefix):
        chosen = [r['passed'] for r in checks if r['check'].startswith(prefix)]
        return bool(chosen) and all(chosen)

    requirement_rows = [
        ('REQ-01', 'Fixed MS-03 position and cell; preserve Earth coordinate/extent definitions', by_check.get('fixed_mars_roi', False) and all_prefix('candidate_coordinates_extent:'), 'mars_reference.json; candidates.csv', 'No landing ellipse, sensor location or trial-area radius is invented.'),
        ('REQ-02', 'At least two evidence-based Earth candidates with purpose, extent and disposition', by_check.get('at_least_two_candidates', False) and all_prefix('candidate_scope_and_disposition:'), 'candidates.csv', 'Candidates may be retained as method references or downgraded; two successful matches are not proved.'),
        ('REQ-03', 'Four dimensions per Earth candidate; explicit units, support and missingness', all_prefix('four_dimensions:') and by_check.get('evidence_metadata', False), 'evidence.csv; completion_20261115/earth_four_dimensions.csv when present', 'Original instructions permit unknown when comparable observations are unavailable; no forced cross-body subtraction.'),
        ('REQ-04', 'Same-place/same-use precedents, classifications and bounded searches', all_prefix('prior_use_review:') and by_check.get('prior_classification', False) and by_check.get('search_metadata', False), 'prior_work.csv; search_log.csv', 'Presence of direct precedents is recorded; this does not clear global novelty.'),
        ('REQ-05', 'Source IDs, URLs, locators, IDs and source relationships are traceable', by_check.get('source_id_url_cross_references', False) and all_prefix('unique_nonempty_ids:'), 'sources.json; source_cross_reference_checks.csv', 'An identity check is not a substitute for primary-source scientific reading.'),
        ('REQ-06', 'Report and required structured deliverables exist', by_check.get('report_exists', False) and by_check.get('required_delivery_files', False), 'docs/research/MS-03/report.md; required CSVs; parent manifest', 'Scientific interpretation, quotations, units and uncertainty require the recorded human/agent review in addition to structural checks.'),
        ('REQ-07', 'Every owned baseline/new artifact is indexed with honest byte-acquisition status', True, 'file_inventory.csv; baseline_git_tree.json', 'Remote-only references retain original Git hashes; inherited SHA256 values are labelled not recomputed.'),
        ('REQ-08', 'Relative document links resolve locally or to an actual supplied Git-tree entry', by_check.get('relative_link_paths', False), 'link_inventory.csv', 'External URLs, historical URLs and fragment anchors are outside this offline existence check.'),
    ]
    audits = [{'requirement_id': rid, 'requirement': text, 'delivery_status': 'supported_by_current_files' if passed else 'incomplete_or_unverified',
               'evidence': proof, 'scientific_resolution': 'not_established_by_delivery_check', 'limit': limit}
              for rid, text, passed, proof, limit in requirement_rows]
    audits.extend([
        {'requirement_id': 'REQ-09', 'requirement': 'Dedicated branch, commit and PR published without merging main', 'delivery_status': 'requires_remote_readback', 'evidence': 'GitHub commit/PR and post-publication receipt, outside this offline builder', 'scientific_resolution': 'not_a_scientific_result', 'limit': 'This program performs no Git/network mutation and cannot prove publication from a local file.'},
        {'requirement_id': 'USER-ALL', 'requirement': 'All MS-03 scientific problems solved', 'delivery_status': 'not_achieved', 'evidence': 'open_questions.csv', 'scientific_resolution': 'unresolved', 'limit': 'Structural tests, exhaustive file listing and completed literature delivery do not resolve missing physical truth or unrecovered producer/logger records.'},
    ])
    write_csv(package / 'requirement_audit.csv', audits, ['requirement_id', 'requirement', 'delivery_status', 'evidence', 'scientific_resolution', 'limit'])

    historical = inherited_hashes(root)
    local_paths = {p.relative_to(root).as_posix() for prefix in PREFIXES for p in (root / prefix).rglob('*') if p.is_file() and not ephemeral(p.relative_to(root).as_posix())}
    all_paths = (set(expected) | local_paths) - set(EXCLUDED)
    inventory = []
    for path in sorted(all_paths):
        entry, file = expected.get(path, {}), root / path
        inherited = historical.get(path, [])
        if file.is_file():
            data = file.read_bytes()
            observed_blob = blob_sha(data)
            status = ('acquired_verified_against_baseline_git' if observed_blob == entry.get('sha') else
                      'locally_modified_from_baseline' if entry else 'new_local_delivery')
            actual_sha, actual_bytes = sha256(data), len(data)
            sha_origin = 'recomputed_from_local_bytes'
        else:
            observed_blob, actual_sha, actual_bytes = '', '', ''
            status, sha_origin = 'remote_tree_reference_only', 'not_recomputed_no_local_bytes'
            compatible = [v for v in inherited if v.get('bytes') in (None, entry.get('size'))]
            unique = {v['sha256'] for v in compatible}
            if len(unique) == 1:
                actual_sha = next(iter(unique))
                sha_origin = 'inherited_not_recomputed'
            elif len(unique) > 1:
                sha_origin = 'conflicting_inherited_assertions_not_recomputed'
        inventory.append({'path': path, 'baseline_commit': baseline.get('sha', '') if entry else '',
                          'baseline_git_blob_sha1': entry.get('sha', ''), 'baseline_bytes': entry.get('size', ''),
                          'local_git_blob_sha1': observed_blob, 'local_bytes': actual_bytes,
                          'sha256': actual_sha, 'sha256_origin': sha_origin, 'acquisition_status': status,
                          'inherited_hash_assertions_json': json.dumps(inherited, ensure_ascii=False, separators=(',', ':')),
                          'remote_url': REPO + '/blob/' + baseline.get('sha', '') + '/' + path if entry else '',
                          'limit': 'Checksums identify artifact bytes; neither document integrity nor a successful download establishes observation quality or physical truth.'})
    fields = ['path', 'baseline_commit', 'baseline_git_blob_sha1', 'baseline_bytes', 'local_git_blob_sha1', 'local_bytes', 'sha256', 'sha256_origin', 'acquisition_status', 'inherited_hash_assertions_json', 'remote_url', 'limit']
    write_csv(package / 'file_inventory.csv', inventory, fields)
    counts = {}
    for row in inventory:
        counts[row['acquisition_status']] = counts.get(row['acquisition_status'], 0) + 1
    check('inventory_covers_owned_baseline', set(expected) <= ({r['path'] for r in inventory} | set(EXCLUDED)), 'All supplied baseline MS-03-owned paths represented or explicitly excluded from the checksum graph.')
    unexpected_changes = [r['path'] for r in inventory if r['acquisition_status'] == 'locally_modified_from_baseline' and r['path'] not in ALLOWED_CHANGED]
    check('preserved_baseline_payloads', not unexpected_changes, 'Only explicitly allowed report/candidate/evidence/prior/search/source-registry updates may differ from baseline; unexpected changes=' + json.dumps(unexpected_changes, ensure_ascii=False))
    check('no_false_scientific_completion', bool(questions) and all(q['status'] == 'unresolved' for q in questions), 'Research handoff verification is explicitly separate from all scientific questions being solved.')
    # Completion-specific file hashes avoid a cycle with parent manifest/index.
    package_files = []
    for file in sorted(package.rglob('*')):
        rel = file.relative_to(root).as_posix()
        if file.is_file() and rel not in EXCLUDED and not ephemeral(rel):
            data = file.read_bytes()
            package_files.append({'path': rel, 'bytes': len(data), 'sha256': sha256(data), 'git_blob_sha1': blob_sha(data)})
    manifest = {
        'schema': 'MS03-delivery-completion-index-v1', 'research_date_taipei': '2026-11-15',
        'baseline_commit': baseline.get('sha'), 'baseline_tree': baseline.get('tree'),
        'scope': 'MS-03 owned documents, evidence and dedicated scripts; full baseline references plus current local additions.',
        'roi': {'latitude_convention': 'planetocentric', 'longitude_convention': 'east_positive_0_360', 'center': [57.75, 242.25], 'bounds': [57.5, 58.0, 242.0, 242.5]},
        'baseline_owned_files': len(expected), 'inventory_rows': len(inventory), 'inventory_acquisition_counts': counts,
        'inventory_sha256': sha256((package / 'file_inventory.csv').read_bytes()),
        'hash_interpretation': 'Local bytes are independently hashed. Remote-only SHA256 assertions are explicitly inherited, not recomputed. Git hashes identify committed artifact bytes, not scientific observation validity.',
        'scientific_completion': False, 'all_scientific_problems_solved': False,
        'publication_status': 'not_verified_by_offline_builder',
        'open_scientific_questions': [q['question_id'] for q in questions],
        'excluded_from_inventory_hash_graph': EXCLUDED,
        'explicitly_allowed_changed_baseline_paths': sorted(ALLOWED_CHANGED),
        'external_url_and_historical_anchor_checks': 'not_performed_by_this_offline_builder',
        'files': package_files,
    }
    write_json(package / 'manifest.json', manifest)
    validation = {'schema': 'MS03-delivery-offline-validation-v1', 'baseline_commit': baseline.get('sha'),
                  'checks': checks, 'failed_checks': [c['check'] for c in checks if not c['passed']],
                  'errors': errors, 'handoff_structural_checks_passed': not errors,
                  'all_scientific_problems_solved': False, 'goal_complete': False,
                  'publication_verified': False,
                  'limit': 'Offline structure, provenance identity, paths and manifest coverage only. Scientific unknowns and remote publication require different evidence.'}
    write_json(package / 'validation.json', validation)
    summary = {'checks': len(checks), 'failed_checks': validation['failed_checks'], 'inventory_rows': len(inventory),
               'acquisition_counts': counts, 'open_scientific_questions': len(questions),
               'all_scientific_problems_solved': False}
    if strict and errors:
        raise ValueError(json.dumps(summary, ensure_ascii=False) + '\n' + '\n'.join(errors))
    return summary


def self_test():
    """Exercise failure cases without touching the actual research snapshot."""
    with tempfile.TemporaryDirectory(prefix='ms03-index-test-') as directory:
        root = Path(directory)
        base = root / 'outputs/research/MS-03'
        base.mkdir(parents=True)
        candidates = []
        for n, lat, lon in ((1, -77.86215, 160.7101), (2, 78.184, 15.913)):
            candidates.append({'candidate_id': 'MS-03-E0' + str(n), 'mars_id': 'MS-03', 'latitude_deg': lat, 'longitude_east_deg': lon, 'bounds_json': 'null', 'name': 'fixture', 'coordinate_source': 'fixture', 'extent_basis': 'fixture', 'test_purpose': 'fixture', 'disposition': 'method_reference', 'next_step': 'get observation', 'cannot_infer': 'ice'})
        write_csv(base / 'candidates.csv', candidates, list(candidates[0]))
        evidence = []
        for c in candidates:
            for theme in sorted(THEMES):
                evidence.append({'evidence_id': c['candidate_id'] + theme, 'candidate_id': c['candidate_id'], 'theme': theme, 'metric': 'fixture', 'value': 'unknown', 'unit': 'unknown', 'period': 'unknown', 'spatial_support': 'point', 'evidence_type': 'missing', 'source_id': 'FIX', 'source_url': 'https://example.invalid/source', 'source_locator': 'fixture', 'read_scope': 'fixture only', 'status': 'unknown', 'limitations': 'fixture'})
        write_csv(base / 'evidence.csv', evidence, list(evidence[0]))
        priors = [{'prior_id': c['candidate_id'], 'candidate_id': c['candidate_id'], 'classification': 'direct_precedent', 'source_id': 'FIX', 'source_url': 'https://example.invalid/source', 'source_locator': 'fixture', 'read_scope': 'fixture'} for c in candidates]
        write_csv(base / 'prior_work.csv', priors, list(priors[0]))
        searches = [{'search_id': 'FIX1', 'date_taipei': '2026-11-15', 'platform': 'fixture', 'query': 'fixture', 'outcome': 'fixture', 'limitation': 'fixture'}]
        write_csv(base / 'search_log.csv', searches, list(searches[0]))
        write_json(base / 'sources.json', {'FIX': {'url': 'https://example.invalid/source'}})
        write_json(base / 'manifest.json', {})
        write_json(base / 'mars_reference.json', {'record': {'center': {'lat': 57.75, 'lon': -117.75}, 'nominal_cell_bounds': {'south': 57.5, 'north': 58.0, 'west': -118.0, 'east': -117.5}}})
        report = root / 'docs/research/MS-03/report.md'
        report.parent.mkdir(parents=True)
        report.write_text('Fixture only: [remote retained file](../../../outputs/research/MS-03/remote.bin)\n', encoding='utf-8')
        blob = b'\xff\x00\x80\x01'
        entries = []
        for path in root.rglob('*'):
            if path.is_file():
                data = path.read_bytes()
                entries.append({'path': path.relative_to(root).as_posix(), 'type': 'blob', 'sha': blob_sha(data), 'size': len(data)})
        entries.append({'path': 'outputs/research/MS-03/remote.bin', 'type': 'blob', 'sha': blob_sha(blob), 'size': len(blob)})
        write_json(root / 'source_tree.json', {'sha': '0' * 40, 'tree': '1' * 40, 'files': entries})
        first = build(root, strict=True)
        assert first['acquisition_counts']['remote_tree_reference_only'] == 1
        assert first['all_scientific_problems_solved'] is False
        manifest = load_json(root / OUT / 'manifest.json')
        assert not manifest['scientific_completion'] and 'outputs/research/MS-03/manifest.json' in manifest['excluded_from_inventory_hash_graph']
        evidence.append(dict(evidence[0]))
        write_csv(base / 'evidence.csv', evidence, list(evidence[0]))
        bad = build(root)
        assert 'unique_nonempty_ids:evidence.csv' in bad['failed_checks']
        evidence.pop()
        evidence[0]['source_url'] = 'https://example.invalid/wrong'
        write_csv(base / 'evidence.csv', evidence, list(evidence[0]))
        bad = build(root)
        assert 'source_id_url_cross_references' in bad['failed_checks']
        write_json(base / 'mars_reference.json', {'record': {'center': {'lat': 58, 'lon': -117.75}, 'nominal_cell_bounds': {'south': 57.5, 'north': 58.0, 'west': -118.0, 'east': -117.5}}})
        bad = build(root)
        assert 'fixed_mars_roi' in bad['failed_checks']
        return {'self_test': 'passed', 'cases': ['remote-only versus acquired bytes', 'cycle exclusions', 'false-scientific-completion guard', 'duplicate IDs rejected', 'source-URL mismatch rejected', 'ROI change rejected']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, nargs='?')
    parser.add_argument('--source-tree', type=Path)
    parser.add_argument('--repository-tree', type=Path)
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False))
        return
    if args.root is None:
        parser.error('ROOT is required unless --self-test is used')
    print(json.dumps(build(args.root, args.source_tree, args.repository_tree, args.strict), ensure_ascii=False))


if __name__ == '__main__':
    main()
