"""Rerun current MS-02 handoff consistency checks without historical writes.

Uses only the standard library. Exact Git blob identities pin all four inputs
to base main 5217401. No original Mars-grid reprocessing is claimed.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import csv
import gzip
import hashlib
import json
import math
import shutil
import xml.etree.ElementTree as ET
import zipfile

HERE=Path(__file__).resolve().parent
SITE=HERE.parents[1]
REPO=SITE.parents[2]
RES=REPO/'outputs/research/mars_reselection_20261114'
BASE='521740108050ba16e406f8becb67a786179ff8bd'
EXPECTED={
    'final_candidates.csv':'2371ade1c27087efaa165acb98b7541266eaa606',
    'candidate_native_evidence.json':'faf4421c57da38852972efe36623c603c29eda4c',
    'screened_pool.csv.gz':'f1563c4094487fe844d4e9beed0d806d1f7ad3c0',
    'NASA_Space_Apps_2026_All_Data.xlsx':'3cad1ffc711dbddeef6def24447e1bd1ff3fb5ba'}

def digest(p):
    data=p.read_bytes()
    return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                git_blob_sha1=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest())

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pool-source',type=Path,
                    help='Optional local copy; verified before copying into the isolated handoff path')
    ap.add_argument('--workbook-source',type=Path,
                    default=REPO/'outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx',
                    help='Read-only exact workbook copy; no table inference is made')
    args=ap.parse_args()
    historical_paths=[SITE/'verification.json',SITE/'local_validation/verification.json',
                      SITE/'local_validation/revision_verification.json',
                      SITE/'local_validation/repair_verification.json']
    before={str(p.relative_to(REPO)):digest(p)['sha256'] for p in historical_paths if p.exists()}
    acquisition={}
    pool_path=RES/'screened_pool.csv.gz'
    if args.pool_source:
        incoming=digest(args.pool_source)
        assert incoming['git_blob_sha1']==EXPECTED[pool_path.name], 'Pool source is not base-commit blob'
        assert incoming['bytes']==7702846
        if pool_path.exists():
            assert digest(pool_path)==incoming, 'Refusing to replace a different pool file'
            copied=False
        else:
            pool_path.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(args.pool_source,pool_path)
            assert digest(pool_path)==incoming
            copied=True
        acquisition={'pool_source_read_only':str(args.pool_source),
                     'isolated_copy_created_this_run':copied,
                     'copy_git_blob_verified':True,
                     'upload_change_required':False}

    paths={'final_candidates.csv':RES/'final_candidates.csv',
           'candidate_native_evidence.json':RES/'candidate_native_evidence.json',
           'screened_pool.csv.gz':pool_path,
           'NASA_Space_Apps_2026_All_Data.xlsx':args.workbook_source}
    inputs={}
    for name,path in paths.items():
        got=digest(path)
        assert got['git_blob_sha1']==EXPECTED[name], name+' does not match base-commit blob'
        inputs[name]={'path_used':str(path),'expected_git_blob':EXPECTED[name],
                      'matches_base_commit':True,**got}

    with paths['final_candidates.csv'].open(encoding='utf-8-sig',newline='') as f:
        final_rows=[r for r in csv.DictReader(f) if r['candidate_id']=='MS-02']
    assert len(final_rows)==1
    final=final_rows[0]
    target_rows=[]
    pool_n=0
    with gzip.open(pool_path,'rt',encoding='utf-8',newline='') as f:
        reader=csv.DictReader(f)
        fields=reader.fieldnames
        for row in reader:
            pool_n+=1
            if abs(float(row['lat'])-52.75)<1e-9 and abs(float(row['lon'])-168.25)<1e-9:
                target_rows.append(row)
    assert pool_n==58238
    assert len(fields)==54
    assert len(target_rows)==1
    pool=target_rows[0]
    native_json=json.loads(paths['candidate_native_evidence.json'].read_text())
    natives=[r for r in native_json['records'] if r['review_id']=='D']
    assert len(natives)==1
    native=natives[0]

    checks=[]
    def chk(name,a,b,tol,note=''):
        a,b=float(a),float(b)
        assert math.isfinite(a) and math.isfinite(b), name
        checks.append(dict(item=name,source_a=a,source_b=b,abs_diff=abs(a-b),
                           tolerance=tol,passed=abs(a-b)<=tol,note=note))
    # Independently transcribed same-quantity comparisons from section1 of the
    # historical verifier. Do not import/execute that file: it overwrites history.
    chk('lat final_vs_native',final['lat'],native['center']['lat'],0)
    chk('lon_east final_vs_native',final['lon_east_0_360'],native['center']['lon'],0)
    chk('mola_relief_m final_vs_pool',final['mola_relief_m'],pool['relief'],0)
    chk('SWIM_0_1m stack final_vs_pool',final['stack_ice_shallow'],pool['ice_shallow'],1e-9)
    chk('SWIM_1_5m stack final_vs_pool',final['stack_ice_deep'],pool['ice_deep'],1e-9)
    chk('dust_my34_p95 final_vs_pool',final['dust_my34_p95_cdodtot'],pool['dust_my34_p95'],1e-9)
    chk('dust_my35_p95 final_vs_pool',final['dust_my35_p95_cdodtot'],pool['dust_my35_p95'],1e-9)
    chk('dust_my34_mean final_vs_pool',final['dust_my34_mean_cdodtot'],pool['dust_my34_mean'],1e-6,'pool stores float32')
    chk('dust_my35_mean final_vs_pool',final['dust_my35_mean_cdodtot'],pool['dust_my35_mean'],1e-6,'pool stores float32')
    chk('MCS night median K final_vs_pool',final['MCS_populated_night_median_K'],pool['mcs_night_median_K'],1e-9)
    chk('MCS day median K final_vs_pool',final['MCS_populated_day_median_K'],pool['mcs_day_median_K'],1e-9)
    chk('MCS paired contrast K final_vs_pool',final['MCS_paired_contrast_median_K'],pool['mcs_paired_contrast_median_K'],1e-9)
    chk('TES TI native_vs_final',final['TES_TI_mean'],native['tes_TI_native_excluding_infill']['mean'],1e-9)
    chk('MOLA slope native_vs_final',final['mola_slope_deg_mean'],native['mola_slope_deg_3p7km_baseline']['mean'],1e-9)
    assert len(checks)==14
    expected_differences=[]
    for label,stack_col,native_col,why in [
        ('TES TI','stack_thermal_inertia','TES_TI_mean','0.5degree coarse stack versus mean of93 non-infill native cells'),
        ('MOLA slope','stack_slope','mola_slope_deg_mean','different aggregation scales'),
        ('SWIM1-5m','stack_ice_deep','SWIM_1_5m_mean','different aggregation scales')]:
        a,b=float(final[stack_col]),float(final[native_col])
        expected_differences.append(dict(quantity=label,stack=a,native_mean=b,
                                        signed_difference=a-b,disposition='expected_difference_not_failure',reason=why))

    workbook=paths['NASA_Space_Apps_2026_All_Data.xlsx']
    assert inputs[workbook.name]['bytes']==23035176
    with zipfile.ZipFile(workbook) as z:
        bad=z.testzip()
        assert bad is None, bad
        tree=ET.fromstring(z.read('xl/workbook.xml'))
        ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        sheets=[s.attrib['name'] for s in tree.findall('s:sheets/s:sheet',ns)]
    after={str(p.relative_to(REPO)):digest(p)['sha256'] for p in historical_paths if p.exists()}
    assert before==after, 'Historical verification artifact modified'
    result=dict(base_commit=BASE,run_utc=datetime.now(timezone.utc).isoformat(),
                scope='Current exact-blob handoff consistency and workbook container integrity; no original-grid reanalysis or new ice proof',
                reference_method='scripts/research/ms02_earth_analogs/verify_ms02.py section1 read, not executed',
                inputs=inputs,acquisition=acquisition,
                screened_pool_rows=pool_n,screened_pool_columns=len(fields),
                ms02_rows_in_final=len(final_rows),ms02_rows_in_pool=len(target_rows),
                review_D_rows_in_native=len(natives),same_quantity_checks=checks,
                same_quantity_check_count=len(checks),same_quantity_passed=sum(x['passed'] for x in checks),
                expected_aggregation_differences=expected_differences,
                workbook_zip_integrity={'all_members_crc_pass':True,'bad_member':None,
                                        'sheet_count':len(sheets),'sheet_names':sheets,
                                        'content_scope':'Historic workbook; not a replacement MS-02 native source or fresh Earth/Mars match'},
                historical_verifications_unchanged=before==after,
                historical_verification_sha256=after,
                all_handoff_checks_passed=all(x['passed'] for x in checks),
                all_scientific_questions_resolved=False)
    (HERE/'current_handoff_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['screened_pool_rows','ms02_rows_in_pool','same_quantity_check_count','same_quantity_passed','historical_verifications_unchanged','all_handoff_checks_passed']}))
    print(json.dumps({'workbook_bytes':inputs[workbook.name]['bytes'],'workbook_sheets':len(sheets),'zip_crc_ok':True}))
    assert result['all_handoff_checks_passed']

if __name__=='__main__': main()
