"""Record the observed baseline, local verification and this delivery's hashes."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'outputs/research/MS-01'
BASE='3cc8488577535e2fa4d146021fde51f8ff6cc667'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def main():
    remote=json.loads((OUT/'inputs/remote_tree_baseline.json').read_text())
    paths={x['path'] for x in remote['tree']}
    local_manifest=ROOT/'outputs/handoff/bundle_manifest.json'
    availability=[]
    targets=['docs/TEAM_START.md','scripts/restore_team_data.py','outputs/handoff/bundle_manifest.json',
             'outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx',
             'outputs/research/mars_reselection_20261114/screened_pool.csv.gz']
    local=json.loads(local_manifest.read_text())
    for bundle in local['bundles']:
        targets += [bundle['target']]+[p['path'] for p in bundle['parts']]
    for rel in dict.fromkeys(targets):
        p=ROOT/rel
        availability.append(dict(path=rel,present_in_remote_baseline=rel in paths,
                                 local_exists=p.is_file(),local_bytes=p.stat().st_size if p.is_file() else None,
                                 local_sha256=sha(p) if p.is_file() else None))
    checks=[]
    for b in local['bundles']:
        # Unlike restore's already-existing-target shortcut, verify every part too.
        for entry in b['parts']+[dict(path=b['target'],size=b['size'],sha256=b['sha256'])]:
            p=ROOT/entry['path']
            checks.append(dict(path=entry['path'],expected_bytes=entry['size'],expected_sha256=entry['sha256'],
                               match=p.stat().st_size==entry['size'] and sha(p)==entry['sha256']))
    pool=local['screened_pool'];p=ROOT/pool['path']
    checks.append(dict(path=pool['path'],expected_bytes=pool['size'],expected_sha256=pool['sha256'],
                       match=p.stat().st_size==pool['size'] and sha(p)==pool['sha256']))
    observed=dict(observed_date='2026-11-14',baseline_sha=BASE,baseline_tree=remote['sha'],
                  remote_method='GitHub REST branches/main, contents GETs, complete nontruncated recursive Git tree',
                  http_results={'docs/TEAM_START.md':404,'outputs/handoff/':404},
                  entries=availability,local_bundle_and_part_checks=checks,
                  restore_command='python3 scripts/restore_team_data.py',restore_exit_code=0,
                  restore_stdout=['Already verified: outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx',
                    'Already verified: outputs/handoff/legacy_snapshot.zip',
                    'Verified screened pool and 186 historical supplement files.',
                    'Use current MS-01/MS-02/MS-03 JSON/CSV as authority; workbook and legacy files are historical context.'],
                  conclusion='Local bytes verified; these handoff paths were absent from the remote baseline. No fresh remote bundle download occurred.')
    assert all(x['match'] for x in checks)
    (OUT/'inputs/remote_availability.json').write_text(json.dumps(observed,ensure_ascii=False,indent=2)+'\n')
    files=[]
    for p in sorted(list((ROOT/'docs/research/MS-01').rglob('*'))+list(OUT.rglob('*'))):
        if not p.is_file() or '__pycache__' in p.parts or p in {OUT/'manifest.json',OUT/'validation.json'}:continue
        files.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
    manifest=dict(schema_version='MS01-EARTH-ANALOGS-v1',research_date='2026-11-14',timezone='Asia/Taipei',
                  team='zasa',mars_id='MS-01',baseline_sha=BASE,baseline_tree=remote['sha'],
                  baseline_policy='No common SHA was specified; exact origin/main at task start used. Complete handoff version not yet remote.',
                  branch='research/ms-01-earth-analogs',
                  mars_center={'latitude_planetocentric':56.75,'longitude_east':72.75},
                  nominal_bounds={'south':56.5,'north':57,'west':72.5,'east':73},
                  candidate_ids=['MS-01-E01','MS-01-E02'],
                  delivery_paths=['docs/research/MS-01/','outputs/research/MS-01/'],files=files,
                  hash_scope='Only root outputs/research/MS-01/manifest.json and validation.json excluded to avoid self-reference; nested follow-up manifests/verification and all reports are included.',
                  sources_file='outputs/research/MS-01/sources.json',
                  source_acquisition={'mars':'11 existing local raw files match remote baseline source hashes; re-extracted this task',
                    'university_valley':'Existing author-processed calibrated bytes; publisher MD5 independently checked online; this task calculated summaries and warm-window harmonic fit',
                    'beacon_valley':'Primary papers/tables read; raw time series not downloaded; no original model reproduction',
                    'shared_excel_pool':'Local restoration/check executed; remote baseline absent; not used for current matching'},
                  calculations={'mars_validation':'analysis/numerical_audit.json','earth_partial_QA':'analysis/uv_partial_summary.json',
                    'earth_signal_fit':'analysis/uv_diurnal_fit.json','classification':'Product reprocessing / published in-situ reanalysis / hypotheses explicitly separated'},
                  unresolved_gaps=[
                    {'id':'GAP-01','paths':[e['path'] for e in availability if not e['present_in_remote_baseline']],
                     'impact':'Complete handoff is not obtainable from the pinned remote; no all-data-available assertion. Mars selected products and public literature suffice for this scoped research.'},
                    {'id':'GAP-02','topic':'MS-01 ice truth/material/wind/pressure/fine terrain','impact':'No ground-truth ice depth, purity or continuity; no extraction or landing claims.'},
                    {'id':'GAP-03','topic':'Earth shared-scale DEM and same-definition dust','impact':'No quantitative terrain similarity ranking or Earth–Mars optical-depth subtraction.'},
                    {'id':'GAP-04','topic':'Earth precise footprints and coordinates','impact':'UV old-paper longitude conflict; Beacon 2015/2018 longitude conflict, minute-only anchor and unknown polygon/GPS. Do not assume station co-location.'},
                    {'id':'GAP-05','topic':'Beacon original hourly data','url':'http://gcmd.nasa.gov/r/d/[GCMD]UW_Dry_Valley_Datalogging','observed_result':'502 via source-link retrieval','impact':'No raw validation or FDM/FVM reproduction; retain literature-supported process case.'},
                    {'id':'GAP-06','topic':'Thermal retrieval uncertainty and time support','impact':'MCS no QA/count/error; Earth timestamps timezone unresolved, surface-probe exposure risk, fit confidence interval not estimated.'},
                    {'id':'GAP-07','topic':'Prior work completeness','impact':'Bounded primary-source search, not systematic WoS/Scopus review; no first-ever claim.'}],
                  scope_stop='Two evidence-supported candidates and complete bounded delivery; no main merge, deployment, further research expansion or teammate dependency.',
                  licensing='Underlying sources retain their terms. Dust-derived summaries follow Montabone CC-BY-SA-3.0; no new project-wide license.',
                  execution='Mac CPU; Python/numpy/pandas/xarray/matplotlib; no new field observations, no model training.')
    followup=OUT/'thermal_followup/manifest.json'
    if followup.is_file():
        manifest['followups']=[dict(path=followup.relative_to(ROOT).as_posix(),starting_sha='33f78ed986b0c39585dc4224b5f68bd6a7e9bed7',date_taipei='2026-11-15',report='docs/research/MS-01/thermal_followup.md',scope='Known-interface temperature comparison; original baseline acquisition statements above are historical, not current all-branch availability.')]
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'manifest_files':len(files),'local_parts_verified':len(checks),'handoff_remote_present':any(e['present_in_remote_baseline'] for e in availability)}))

if __name__=='__main__':main()
