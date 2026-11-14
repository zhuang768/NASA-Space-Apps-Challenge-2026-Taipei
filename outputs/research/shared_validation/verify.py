"""Delivery checks. Passing these does not close any physical evidence gap."""
import csv
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def verify():
    results=[]
    for p in sorted(HERE.glob('*.csv')):
        with p.open(newline='',encoding='utf-8') as f:
            rows=list(csv.reader(f))
        assert len(rows)>1 and len(rows[0])==len(set(rows[0])),p.name
        assert all(len(row)==len(rows[0]) for row in rows),p.name
        results.append({'check':'CSV:'+p.name,'pass':True,'data_rows':len(rows)-1})
    with (HERE/'native_model_cells.csv').open() as f:cells=list(csv.DictReader(f))
    assert [r['site'] for r in cells]==['MS-01','MS-02','MS-03']
    for r in cells:
        assert float(r['south_deg_N'])<float(r['latitude_deg_N'])<float(r['north_deg_N'])
        assert float(r['west_deg_E'])<float(r['longitude_deg_E'])<float(r['east_deg_E'])
        assert not r['local_RMS_K'] and not r['local_depth_CI_m'] and not r['local_obs_count']
    assert float(cells[0]['conditional_depth_m'])==0.426995635
    assert float(cells[1]['conditional_depth_m'])==0.4499824941
    assert float(cells[2]['conditional_depth_m'])==0.103161566
    results.append({'check':'fixed_native_cells_missing_qa_not_filled','pass':True})
    a=json.loads((HERE/'analysis_checks.json').read_text())
    assert all(x['pass'] for x in a['checks'])
    assert not a['raw_UV_time_series_recomputed'] and not a['new_Mars_model_fit']
    assert not a['new_laboratory_measurements'] and not a['scientific_gaps_solved_by_passing_checks']
    results.append({'check':'no_old_window_recompute_or_new_fit_claim','pass':True})
    for r in json.loads((HERE/'http_attempts.json').read_text()):
        if r.get('receipt_file'):
            p=HERE/r['receipt_file']
            assert p.name.endswith('.error.html')
            assert hashlib.sha256(p.read_bytes()).hexdigest()==r['body_sha256']
            assert r.get('status')!=200
    results.append({'check':'failed_downloads_not_mislabeled_data','pass':True})
    doc=ROOT/'docs/research/shared_validation/research_notes.md'
    assert doc.exists()
    for rel in ['../../../outputs/research/shared_validation/','../../../outputs/research/shared_validation/laboratory_control.png']:
        assert (doc.parent/rel).exists(),rel
    results.append({'check':'local_note_links','pass':True})
    manifest_path=HERE/'manifest.json'
    if manifest_path.exists():
        m=json.loads(manifest_path.read_text())
        for r in m['files']:
            p=ROOT/r['path']
            assert p.stat().st_size==r['bytes'],r['path']
            assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],r['path']
        results.append({'check':'manifest_payload_hashes','pass':True,'files':len(m['files'])})
    print(json.dumps({'all_passed':True,'checks':results},ensure_ascii=False,indent=2))


if __name__=='__main__':
    verify()
