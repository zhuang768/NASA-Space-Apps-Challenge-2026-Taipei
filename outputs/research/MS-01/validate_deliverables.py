"""Validate MS-01 delivery schema, hashes, IDs and reported calculation values.

This checks the saved research evidence. It does not download or rerun unavailable inputs.
"""
from pathlib import Path
import csv,hashlib,json,math

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'outputs/research/MS-01'

def read(name):
    with (OUT/name).open(newline='') as f:return list(csv.DictReader(f))

def digest(path,kind='sha256'):
    h=hashlib.new(kind)
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def main():
    manifest=json.loads((OUT/'manifest.json').read_text())
    sources=json.loads((OUT/'sources.json').read_text())
    c,e,p,s=[read(n) for n in ['candidates.csv','evidence.csv','prior_work.csv','search_log.csv']]
    ids={'MS-01-E01','MS-01-E02'}
    assert len(c)==2 and {v['candidate_id'] for v in c}==ids
    for row in c:
        assert -90<=float(row['latitude'])<=90 and -180<=float(row['longitude'])<=180
        assert all(row[k] for k in ['scope','boundary_basis','purpose','disposition','rationale','next_step','limits'])
    assert len({v['evidence_id'] for v in e})==len(e)
    for row in e:
        assert row['candidate_id'] in ids|{'MS-01'}
        assert row['source_id'] in sources and row['source_url'].startswith('https://')
        assert all(row[k] for k in ['value','unit','locator','observation_period','depth_height','spatial_resolution','temporal_resolution','data_kind','comparability_and_limit'])
    dimensions={'terrain','thermal','water_ice','atmosphere_dust'}
    assert all({v['dimension'] for v in e if v['candidate_id']==cid}==dimensions for cid in ids|{'MS-01'})
    assert len(p)==8 and all(v['source_id'] in sources for v in p)
    assert all(any(v['classification']=='直接先例' for v in p if v['candidate_id']==cid) for cid in ids)
    assert len({v['search_id'] for v in s})==len(s) and len(s)>=20
    assert all(v['date']=='2026-11-14' and v['platform'] and v['query'] for v in s)
    audit=json.loads((OUT/'analysis/numerical_audit.json').read_text())
    assert audit['status']=='PASS' and audit['required_raw_files_match']
    assert len(audit['comparisons'])==48 and all(x['matches'] for x in audit['comparisons'])
    assert audit['reference_csv']=='outputs/research/MS-01/inputs/final_candidates.baseline.csv'
    uv=json.loads((OUT/'analysis/uv_diurnal_fit.json').read_text())
    assert uv['common_valid_samples']==uv['expected_half_hour_samples']==528
    for value in uv['values']:
        row=next(x for x in e if x['quantity']=='24h_harmonic_half_amplitude_'+value['column'])
        assert math.isclose(float(row['value']),value['diurnal_amplitude_K'],rel_tol=1e-12)
    tree=json.loads((OUT/'inputs/remote_tree_baseline.json').read_text())
    for rel in ['candidate_native_evidence','final_candidates']:
        local=OUT/('inputs/'+rel+'.baseline.'+('json' if rel.startswith('candidate_') else 'csv'))
        data=local.read_bytes();blob=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        canonical='outputs/research/mars_reselection_20261114/'+rel+local.suffix
        expected=next(x['sha'] for x in tree['tree'] if x['path']==canonical)
        assert blob==expected,(canonical,blob,expected)
    availability=json.loads((OUT/'inputs/remote_availability.json').read_text())
    assert all(x['match'] for x in availability['local_bundle_and_part_checks'])
    assert not any(x['present_in_remote_baseline'] for x in availability['entries'])
    for f in manifest['files']:
        path=ROOT/f['path'];assert path.stat().st_size==f['bytes'] and digest(path)==f['sha256'],f['path']
        assert f['path'].startswith(('docs/research/MS-01/','outputs/research/MS-01/'))
    report=(ROOT/'docs/research/MS-01/report.md').read_text()
    assert (ROOT/'docs/research/MS-01'/'../../../outputs/research/MS-01/analysis/uv_thermal_signals.png').is_file()
    assert manifest['baseline_sha'] in report
    result=dict(status='PASS',checks=['candidate coordinates/scopes','all four evidence dimensions','source metadata and URLs','8 bounded prior-work records','search log integrity','48 native numerical checks','UV 528-sample values','baseline Git blobs','local parts vs remote absence','all delivery SHA-256 hashes','report figure path'],counts=dict(candidates=len(c),evidence=len(e),prior_work=len(p),searches=len(s),hashed_files=len(manifest['files'])),limits='Validation of deliverable consistency, not ground-truth science, global novelty or full clean-checkout data availability.')
    (OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
