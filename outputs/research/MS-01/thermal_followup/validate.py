"""Verify source bytes, row provenance, independent fits and scoped deliverables."""
from pathlib import Path
from datetime import datetime
import argparse,ast,csv,gzip,hashlib,io,json,math,re
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
STARTING_SHA='33f78ed986b0c39585dc4224b5f68bd6a7e9bed7'

def read_json(name):return json.loads((HERE/name).read_text())
def rows(name):return list(csv.DictReader((HERE/name).open(newline='',encoding='utf-8')))
def close(a,b):assert math.isclose(float(a),float(b),rel_tol=1e-10,abs_tol=1e-10),(a,b)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--raw-dir',type=Path,required=True);args=parser.parse_args()
    sources=read_json('source_manifest.json');comparison=read_json('comparison.json');audit=read_json('independent_audit.json')
    assert comparison['starting_sha']==sources['starting_sha']==STARTING_SHA
    raw={}
    for asset in sources['assets']:
        path=args.raw_dir/asset['filename']
        if not path.exists() and asset['filename'].startswith('UniversityV_09_10_Campbell'):
            path=ROOT/'data/raw/earth/university_valley'/asset['filename']
        b=path.read_bytes()
        assert len(b)==asset['bytes'] and hashlib.md5(b).hexdigest()==asset['expected_md5']
        assert hashlib.sha256(b).hexdigest()==asset['sha256']
        if path.suffix=='.txt':raw[path.name]=list(csv.reader(b.decode('utf-8-sig').splitlines()))
    table=rows('amplitudes.csv');assert len(table)==18
    independent_map={'S8':'S','M22':'M','D36':'D','W42_HOBO':'W_HOBO'}
    old=json.loads((HERE.parent/'analysis/uv_diurnal_fit.json').read_text())
    fit_count=0
    for station,results in comparison['results'].items():
        qa=comparison['qa'][station];expected=528 if station=='W42_Campbell' else 264
        assert qa['common_valid_rows']==qa['primary_rows']==qa['expected_primary_rows']==expected
        assert not qa['non_nominal_intervals'] and qa['duplicate_times']==0
        for result in results:
            row=next(r for r in table if r['station']==station and r['column']==result['column'])
            for field in ['amplitude_K','residual_rmse_K','amplitude_to_upper_ratio']:close(row[field],result[field])
            if station in independent_map:
                channel=next(c for c in audit['stations'][independent_map[station]]['channels'] if c['header']==result['column'])
                close(result['amplitude_K'],channel['half_amplitude_K']);close(result['residual_rmse_K'],channel['residual_RMSE_K'])
            else:
                channel=next(c for c in old['values'] if c['column']==result['column'])
                close(result['amplitude_K'],channel['diurnal_amplitude_K']);close(result['residual_rmse_K'],channel['residual_rmse_K'])
            if station=='W42_HOBO':assert result['relative_lag_to_upper_h'] is None
            assert result['leave_one_day_amplitude_min_K']<=result['leave_one_day_amplitude_max_K']
            fit_count+=1
    with gzip.open(HERE/'primary_temperature_records.csv.gz','rt',newline='',encoding='utf-8') as f:export=list(csv.DictReader(f))
    assert len(export)==5808
    seen=set();groups={}
    for row in export:
        key=(row['station'],row['column'],row['printed_timestamp']);assert key not in seen;seen.add(key)
        source=raw[row['source_filename']];line=int(row['source_line_1based']);source_row=source[line-1]
        qa=comparison['qa'][row['station']];sensor=next(c for c in qa['sensors'] if c['column']==row['column'])
        assert source_row[sensor['source_index_0_based']].strip()==row['source_numeric_string']
        close(row['temperature_C'],row['source_numeric_string']);close(row['depth_m'],sensor['depth_m'])
        assert row['unit']=='degree_C' and source_row[0].strip()==row['source_timestamp']
        t=datetime.fromisoformat(row['printed_timestamp'])
        assert datetime(2010,11,7)<=t<datetime(2010,11,18)
        groups.setdefault((row['station'],row['column']),[]).append(row)
    # Refit the durable export independently of the main script and compare all18.
    for (station,column),group in groups.items():
        h=np.array([(datetime.fromisoformat(r['printed_timestamp'])-datetime(2010,11,7)).total_seconds()/3600 for r in group])
        temp=np.array([float(r['temperature_C']) for r in group]);X=np.column_stack([np.ones(len(h)),h,np.sin(2*np.pi*h/24),np.cos(2*np.pi*h/24)])
        c=np.linalg.lstsq(X,temp,rcond=None)[0];result=next(r for r in comparison['results'][station] if r['column']==column)
        close(math.hypot(c[2],c[3]),result['amplitude_K']);close(np.sqrt(np.mean((temp-X@c)**2)),result['residual_rmse_K'])
    stations={r['station']:r for r in rows('station_metadata.csv')}
    assert stations['S8']['paper_latitude']==stations['D36']['deployment2009_latitude']
    assert stations['D36']['paper_latitude']==stations['S8']['deployment2009_latitude']
    assert len(rows('channel_metadata.csv'))==18 and len(rows('interpretation_table.csv'))==8 and len(rows('dispositions.csv'))==2
    assert next(r for r in rows('channel_metadata.csv') if r['station']=='M22' and r['role']=='upper')['nominal_depth_m']=='0.01'
    paragraphs=read_json('deployment_paragraphs.json')
    assert len(paragraphs)==2 and all(p['paragraphs'] for p in paragraphs.values())
    report=ROOT/'docs/research/MS-01/thermal_followup.md';text=report.read_text();assert STARTING_SHA in text
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if not target.startswith('https://'):assert (report.parent/target).is_file(),target
    for path in HERE.glob('*.py'):ast.parse(path.read_text())
    assert (HERE/'comparison_figure.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    assert '<svg' in (HERE/'comparison_figure.svg').read_text()
    result=dict(status='PASS',starting_sha=STARTING_SHA,counts=dict(source_assets=len(sources['assets']),verified_profiles=5,independently_matched_channels=fit_count,source_row_column_values=len(export),interpretation_rows=8),checks=['All7 source sizes/MD5/SHA256','Primary common-valid counts and no duplicate/gapped printed grids','Independent HOBO OLS and previous W Campbell match','All5808 export values trace to exact source line/column/string','All18 export fits independently match','S/D coordinate conflict preserved; M upper1cm; no W HOBO phase','Two source DOCX paragraph extractions retained','Report links, code syntax and figure signatures'],limits='Deliverable consistency, not true historical clock synchronization, geolocation resolution, instrument calibration, unique ice detection or Mars ground truth.')
    (HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
