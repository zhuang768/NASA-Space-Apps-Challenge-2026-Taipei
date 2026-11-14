"""Verify this integration's transcription, citations, dispositions and hashes.

--source-cache optionally points to the byte-verified pr6/pr7/pr8/main tree cache.
It is not a rerun of original physical models or an independent field validation.
"""
from pathlib import Path
import argparse,ast,csv,hashlib,json,math,re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def read(name):return json.loads((HERE/name).read_text())
def equal(a,b):assert math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=1e-12),(a,b)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-cache',type=Path);p.add_argument('--check-manifest',action='store_true');a=p.parse_args()
    data=read('research_cards.json');sources=read('source_index.json')['sources'];byid={s['source_id']:s for s in sources}
    assert len(sources)==len(byid)==42
    expected={6:'38b8fa0dea527b1cc47aeb02dc260e039da37122',7:'8f6d3134bc5bfef6e83a4caddb1d602872d40708',8:'b4b6929e890018668ef4faa9a74128a4ce5aa8df'}
    assert {r['pr']:r['head'] for r in data['source_prs']}==expected
    for source in sources:
        assert source['byte_exact_match'] and re.fullmatch('[0-9a-f]{40}',source['commit_sha'])
        assert re.fullmatch('[0-9a-f]{40}',source['git_blob_sha']) and re.fullmatch('[0-9a-f]{64}',source['sha256'])
        assert f"/blob/{source['commit_sha']}/{source['path']}" in source['url']
        if source['pr_number'] is not None:assert source['commit_sha']==expected[source['pr_number']]
    cards=data['cards'];assert [c['mars_id'] for c in cards]==['MS-01','MS-02','MS-03']
    with (HERE/'comparison.csv').open(encoding='utf-8-sig',newline='') as f:table=list(csv.DictReader(f))
    assert len(table)==3 and len({r['mars_id'] for r in table})==3
    candidate_ids=[];allrefs=[];metric_count=0
    for card,row in zip(cards,table):
        equal(row['latitude_deg_n'],card['center_latitude_n']);equal(row['longitude_deg_e_0_360'],card['center_longitude_e'])
        b=card['bounds'];assert b['south']<card['center_latitude_n']<b['north'] and b['west']<card['center_longitude_e']<b['east']
        equal(b['north']-b['south'],.5);equal(b['east']-b['west'],.5)
        for field in ['south','north','west','east']:equal(row[field+'_deg_'+('n' if field in ['south','north'] else 'e_0_360')],b[field])
        for key,value in card['metrics'].items():equal(row[key],value);metric_count+=1
        assert json.loads(row['earth_candidates_json'])==card['candidates']
        for field in ['research_question','validation_use','prior_work','team_contribution','limitations','disposition']:assert row[field]
        allrefs.extend(json.loads(row['source_refs_json']))
        for candidate in card['candidates']:
            assert candidate['candidate_id'].startswith(card['mars_id']+'-E')
            candidate_ids.append(candidate['candidate_id']);assert candidate['scope'] and candidate['limit'] and candidate['disposition']
    assert len(candidate_ids)==len(set(candidate_ids))==8
    dispositions={e['candidate_id']:e['disposition'] for c in cards for e in c['candidates']}
    assert '降為一般方法參照' in dispositions['MS-02-E03'] and '降為一般方法參照' in dispositions['MS-03-E02']
    assert dispositions['MS-02-E02']==dispositions['MS-02-E04']=='待補證據'
    assert cards[2]['observability']['Mars_polygon_count'] is None
    equal(cards[2]['observability']['median_diameter_pixels'],cards[2]['observability']['median_equivalent_diameter_m']/cards[2]['observability']['CTX_example_m_per_pixel'])
    assert f"{cards[2]['observability']['median_diameter_pixels']:.2f}"=='3.04'
    assert len(data['issues'])==len({i['id'] for i in data['issues']})==9
    allrefs.extend(r for issue in data['issues'] for r in issue['sources'])
    assert all(r['source_id'] in byid and r['locator'] for r in allrefs)
    report=(ROOT/'docs/integration/science/synthesis.md').read_text()
    for sha in [data['main_baseline_sha']]+list(expected.values()):assert sha in report
    definitions=dict(re.findall(r'^\[([A-Z0-9_]+)\]: (https://\S+)$',report,re.M))
    refs=set(re.findall(r'\[([A-Z0-9_]+)\](?!:)',report));assert refs<=definitions.keys()
    assert not re.search(r'\]\[[A-Z0-9_]+\]',report),'Adjacent shortcuts can mislink citations'
    for sid,url in definitions.items():assert url==byid[sid]['url']
    for target in re.findall(r'\]\(([^)]+)\)',report):
        if not target.startswith('https://'):assert (ROOT/'docs/integration/science'/target).is_file(),target
    for script in HERE.glob('*.py'):ast.parse(script.read_text())
    source_checks=0;native_checks=0;derived_checks=0
    if a.source_cache:
        loaded={}
        for source in sources:
            path=a.source_cache/('main' if source['pr_number'] is None else f"pr{source['pr_number']}")/source['path']
            b=path.read_bytes();assert len(b)==source['bytes'] and hashlib.sha256(b).hexdigest()==source['sha256'],path
            assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==source['git_blob_sha'];source_checks+=1
            loaded[source['source_id']]=b.decode('utf-8-sig')
        baseline={r['candidate_id']:r for r in csv.DictReader(loaded['MARS_CSV'].splitlines())}
        selection={s['id']:s for s in json.loads(loaded['MARS_SELECTION'])['sites']}
        for card in cards:
            orig=baseline[card['mars_id']];equal(card['center_latitude_n'],orig['lat']);equal(card['center_longitude_e'],orig['lon_east_0_360'])
            for key,value in card['metrics'].items():equal(value,orig[key]);native_checks+=1
            b=selection[card['mars_id']]['bounds'];equal(card['bounds']['south'],b['south']);equal(card['bounds']['north'],b['north'])
            for side in ['west','east']:equal(card['bounds'][side],b[side]%360)
        amps=list(csv.DictReader(loaded['MS01_AMPLITUDES'].splitlines()))
        for row in cards[0]['thermal_followup']['sites']:
            s=next(x for x in amps if x['station']==row['station'] and x['role']=='ice')
            equal(row['ice_to_upper_ratio'],s['amplitude_to_upper_ratio']);assert row['n']==int(s['common_n']);derived_checks+=1
        v=json.loads(loaded['MS02_VERIFICATION'])['earth_coordinates_and_conversions']['E03_Adventdalen_anchor_separations_km']['CS1_loess_core_Rasmussen2023__ADE_borehole_Rotem2023']
        equal(v,cards[1]['footprint_result']['CS1_ADE_distance_km']);derived_checks+=1
        g=json.loads(loaded['MS03_GEOMETRY']);assert g['n']==cards[2]['observability']['polygons'];equal(g['metrics']['equivalent_circle_diameter_m']['median'],cards[2]['observability']['median_equivalent_diameter_m']);derived_checks+=1
        d=json.loads(loaded['MS03_DUPLICATES']);diag=cards[2]['index_diagnostic']
        for field,orig in [('current_labels_read','labels_read'),('pairs_floor_ceil_compatible','pairs_both_floor_or_ceil_of_current_label'),('pairs_not_both_compatible','pairs_not_both_floor_or_ceil'),('pairs_over_one_second','pairs_over_one_second')]:assert diag[field]==d[orig];derived_checks+=1
        idx=json.loads(loaded['MS03_INDEX'])
        for field,orig in [('physical_rows','physical_rows'),('unique_products','unique_product_ids'),('duplicate_products','duplicated_product_groups'),('negative_longitude_flags','legacy_flagged_rows'),('latitude_eligible_rows','latitude_eligible_rows')]:assert diag[field]==idx[orig];derived_checks+=1
    hash_checks=0
    if a.check_manifest:
        manifest=read('manifest.json')
        for item in manifest['files']:
            path=ROOT/item['path'];assert item['path'].startswith(('docs/integration/science/','outputs/integration/science/'))
            assert path.stat().st_size==item['bytes'] and hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'];hash_checks+=1
    result=dict(status='PASS',main_baseline_sha=data['main_baseline_sha'],source_prs=expected,counts=dict(comparison_rows=3,scoped_candidates=8,issue_records=9,source_records=42,source_bytes_rechecked=source_checks,CSV_metric_values_checked=metric_count,native_source_values_checked=native_checks,derived_source_values_checked=derived_checks,output_hashes_checked=hash_checks),checks=['Coordinate ranges and0–360 representation','One row per Mars target and typed numeric transcription','Eight scoped IDs and latest downgrades','Unknown Mars morphology remains null','Source-version URLs, reference syntax and local links','Selected existing ratios,geometry,footprint/index numbers when source cache supplied','No source-branch or main mutation by this program'],limits='Integration/transcription and provenance consistency only;not new observations,raw Mars reprocessing,instrument calibration,full prior-work audit,global novelty clearance or unique ice identification.')
    if not a.check_manifest:(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
