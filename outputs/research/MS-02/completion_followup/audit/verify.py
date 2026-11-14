"""Verify current structured-data integrity; never equate this with ice proof."""
from pathlib import Path
import csv
import hashlib
import json

HERE=Path(__file__).resolve().parent
SITE=HERE.parents[1]
REPO=SITE.parents[2]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):
    with (SITE/name).open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        rows=list(reader)
        assert reader.fieldnames and len(reader.fieldnames)==len(set(reader.fieldnames))
        assert all(None not in r and None not in r.values() for r in rows), name
        return reader.fieldnames,rows

checks=[]
def check(name,condition,detail):
    checks.append(dict(name=name,passed=bool(condition),detail=detail))

log=json.loads((HERE/'reconciliation_log.json').read_text())
tables={}
keys={'candidates.csv':'candidate_id','evidence.csv':'evidence_id',
      'claims.csv':'claim_id','footprint.csv':'footprint_id',
      'prior_work.csv':'prior_id','local_validation/mars_ice_evidence.csv':'evidence_id'}
for name,key in keys.items():
    fields,rows=read(name)
    ids=[r[key] for r in rows]
    check(name+' IDs',len(ids)==len(set(ids)),{'rows':len(rows),'key':key})
    tables[name]={r[key]:r for r in rows}
    state=log['files'][name]
    check(name+' schema preserved',fields==state['fields'],fields)
    inserted=sum(x['file']==name for x in log.get('inserted_rows',[]))
    check(name+' identities retained',len(rows)==state['row_count']+inserted,
          {'before':state['row_count'],'inserted':inserted,'after':len(rows)})
    check(name+' output hash',sha(SITE/name)==state['sha256_after'],sha(SITE/name))

for c in log['changes']:
    row=tables[c['file']][c['record_id']]
    # Some fields may have more than one intentionally logged revision; require
    # the final logged value while retaining all prior text in the history.
    later=[x for x in log['changes'] if (x['file'],x['record_id'],x['field']) ==
           (c['file'],c['record_id'],c['field'])]
    expected=later[-1]['new']
    check('reconciled '+c['record_id']+'.'+c['field'],row[c['field']]==expected,
          {'authority':c['authority'],'locator':c['locator']})
for x in log.get('inserted_rows',[]):
    key=keys[x['file']]
    check('new record '+x['row'][key],tables[x['file']][x['row'][key]]==x['row'],
          {'authority':x['authority'],'locator':x['locator']})

candidates=tables['candidates.csv']
expected_ids={'MS-02-E01','MS-02-E02','MS-02-E03','MS-02-E04'}
check('fixed Earth candidate IDs',set(candidates)==expected_ids,sorted(candidates))
ev=list(tables['evidence.csv'].values())
facets={}
for cid in expected_ids:
    facets[cid]=sorted({r['facet'] for r in ev if r['candidate_id']==cid})
    check(cid+' four facets',set(facets[cid])=={'地形','熱性質','水/冰','大氣/沙塵'},facets[cid])
    c=candidates[cid]
    check(cid+' disposition and limitation',all(c[k].strip() for k in
          ['research_extent','boundary_basis','disposition','disposition_reason','cannot_extrapolate','next_verification_step']),
          {'disposition':c['disposition']})
    if c['lat_deg'] or c['lon_deg_east']:
        check(cid+' coordinate pair',bool(c['lat_deg']) and bool(c['lon_deg_east']),
              [c['lat_deg'],c['lon_deg_east']])
        check(cid+' numeric coordinate bounds',-90<=float(c['lat_deg'])<=90 and
              -180<=float(c['lon_deg_east'])<=360,[c['lat_deg'],c['lon_deg_east']])

check('E02 quantitative terrain stays unknown','unknown' in tables['evidence.csv']['EV-062']['value'],
      'No invented slope/relief or zero fill')
check('CS1 core date resolved','September2019' in tables['claims.csv']['C1']['site_year_depth_of_direct_evidence'] and
      'September2019' in tables['footprint.csv']['FP-01']['survey_or_sample_year'],
      'Separate September2019 cores and August2022 exposure')
check('WISDOM chain remains unproven','不成立' in tables['claims.csv']['C7']['status'] and
      '證據不足' in tables['claims.csv']['C9']['status'],'No same-valley truth join')
check('EV018 measurement/calculation separation','不是兩變量直接量測' in tables['evidence.csv']['EV-018']['evidence_type'],
      'Recorded T; calculated aw; no energy-model annual hours')
check('0.45m remains conditional','Conditional' in tables['evidence.csv']['EV-063']['evidence_type'] and
      'Not observed ice table' in tables['evidence.csv']['EV-063']['limitation_or_comparability'],
      'No independent local ice/interface confirmation')
check('Haughton excavation boundary','excavat' in tables['prior_work.csv']['PW-22']['difference_in_data'] and
      'no intact-cover' in tables['prior_work.csv']['PW-22']['difference_in_method'],
      'Earth method precedent cannot be advertised as intact-cover or orbital validation')
check('Beacon raw availability boundary','not acquired' in tables['prior_work.csv']['PW-21']['read_scope'],
      'Literature review is not a new raw-data rerun')
fp=tables['footprint.csv']
for fid,lat,lon,doi in [
    ('FP-10',-(77+51.729/60),160+42.606/60,'10.1017/S0954102022000025'),
    ('FP-11',-(77+49/60),160+39/60,'10.1029/2017JF004535'),
    ('FP-12',75+22/60+6/3600,-(89+31/60+33/3600),'10.1029/2012JE004053')]:
    row=fp[fid]
    check(fid+' DMS conversion',abs(float(row['lat_deg'])-lat)<1e-8 and
          abs(float(row['lon_deg_east'])-lon)<1e-8,
          {'published_anchor_decimal':[lat,lon],'stored':[row['lat_deg'],row['lon_deg_east']]})
    check(fid+' primary footprint source',doi in row['source'] and bool(row['locator']),row['source'])
check('historical valley anchors not repointed',
      candidates['MS-02-E02']['lat_deg']=='' and candidates['MS-02-E02']['lon_deg_east']=='' and
      candidates['MS-02-E03']['lat_deg']=='78.1722' and candidates['MS-02-E03']['lon_deg_east']=='16.0613' and
      candidates['MS-02-E04']['lat_deg']=='75.37' and candidates['MS-02-E04']['lon_deg_east']=='-89.53',
      'Located subcases get separate footprint IDs; original scalar anchors retain their declared scopes')
check('E03 retained CS1 distinguished from ADE',
      'FP-03' in candidates['MS-02-E03']['research_extent'] and
      'FP-01' in candidates['MS-02-E03']['research_extent'] and
      '5.97km' in candidates['MS-02-E03']['research_extent'],
      'Same valley grouping does not imply a shared observation footprint')
check('E04 boundary cites actual Thomson source',
      '10.1029/2012JE004053' in candidates['MS-02-E04']['boundary_basis'] and
      'FP-12' in candidates['MS-02-E04']['boundary_basis'],
      'Independent source for plateau line; Andres boundary retained separately')
check('FP12 excavation and unresolved line geometry',
      'excavated' in fp['FP-12']['stated_extent'] and
      'endpoints/azimuth not encoded' in fp['FP-12']['geometry_type'] and
      'not exhaustive line truth' in fp['FP-12']['measured_quantity'],
      'Point anchor and one core do not create a surveyed line polygon or intact-cover validation')
handoff=json.loads((HERE/'current_handoff_check.json').read_text())
check('current handoff pinned base',handoff['base_commit']==log['base_commit'] and
      all(x['matches_base_commit'] and x['git_blob_sha1']==x['expected_git_blob'] for x in handoff['inputs'].values()),
      'Four inputs match independently checked base-commit Git blobs')
check('screened pool target support',handoff['screened_pool_rows']==58238 and
      handoff['screened_pool_columns']==54 and handoff['ms02_rows_in_pool']==1 and
      handoff['ms02_rows_in_final']==1 and handoff['review_D_rows_in_native']==1,
      'Exactly one fixed MS-02 target, without confusing other candidate IDs')
check('current handoff same-quantity checks',handoff['same_quantity_check_count']==14 and
      handoff['same_quantity_passed']==14 and all(x['passed'] for x in handoff['same_quantity_checks']),
      'Actual new run; historical script not executed or relabelled')
check('aggregation differences preserved',len(handoff['expected_aggregation_differences'])==3 and
      all(x['disposition']=='expected_difference_not_failure' for x in handoff['expected_aggregation_differences']),
      'Native and coarse-scale statistics are distinct quantities')
check('workbook current container check',handoff['workbook_zip_integrity']['all_members_crc_pass'] and
      handoff['workbook_zip_integrity']['sheet_count']==32 and
      handoff['inputs']['NASA_Space_Apps_2026_All_Data.xlsx']['bytes']==23035176,
      'Exact 23,035,176-byte Git blob contains32 sheets; historical33-sheet report statement is superseded')
check('historical verification files preserved',handoff['historical_verifications_unchanged'],
      'Current handoff QA writes a separate JSON and does not overwrite historical science-verification files')
check('formal report unchanged',sha(REPO/'docs/research/MS-02/report.md')==log['formal_report_sha256'],
      log['formal_report_sha256'])

result={'base_commit':log['base_commit'],'scope':'current structured records and correction provenance only',
        'checks':checks,'check_count':len(checks),'passed_count':sum(c['passed'] for c in checks),
        'all_integrity_checks_passed':all(c['passed'] for c in checks),
        'all_scientific_questions_resolved':False,
        'reason':'Independent MS-02 ice truth/local uncertainty, original calibration/field records and undisturbed material controls remain absent; see current gap ledger.',
        'candidate_facets':facets}
(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['check_count','passed_count','all_integrity_checks_passed','all_scientific_questions_resolved']}))
assert result['all_integrity_checks_passed']
