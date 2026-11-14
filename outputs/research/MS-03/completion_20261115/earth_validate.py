#!/usr/bin/env python3
"""Independent Decimal arithmetic and consistency check of the W summaries."""
import csv
import datetime as dt
import gzip
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sys

out=Path(__file__).resolve().parent
name='UniversityV_09_10_Campbell_data_good_only_calibrated.txt'
retained=out/'earth_raw'/(name+'.gz')
fallback=out.parents[3]/'data/raw/earth/university_valley'/name
src=Path(sys.argv[1]) if len(sys.argv)>1 else retained if retained.is_file() else fallback
packed=src.read_bytes()
if src.suffix=='.gz':
    assert hashlib.sha256(packed).hexdigest()=='f2ab00f49fdfa9f64cb2e6fe15df3d32599f382292ba7b2e4b916f75c5f311f1'
    raw=gzip.decompress(packed)
else:
    raw=packed
assert hashlib.md5(raw).hexdigest()=='ae2133eac5c92c695c5f6ef93bcbbd25'
assert hashlib.sha256(raw).hexdigest()=='c46d93e3dd07c6c91d700a814214716f00caa0d5cc3a520f8969ce0af63ecafd'
lines=list(csv.reader(raw.decode().splitlines()))
selected=[]
for row in lines[4:]:
    stamp=row[0].strip()
    t=dt.datetime.fromisoformat(stamp) if '-' in stamp else dt.datetime.strptime(stamp,'%m/%d/%Y %H:%M')
    if dt.datetime(2010,1,1)<=t<dt.datetime(2010,12,1):selected.append((t,row))
assert len(selected)==334*48
with (out/'earth_atmosphere_summary.csv').open() as f:summary={r['metric']:r for r in csv.DictReader(f)}
with (out/'earth_atmosphere_monthly.csv').open() as f:monthly=list(csv.DictReader(f))
checks=[]
for name,pos in [('air_temperature',4),('air_RH_water_basis',5),('air_RH_ice_basis',6),('solar_irradiance',7),('wind_speed',8)]:
    values=[Decimal(row[pos].strip()) for t,row in selected]
    exact=sum(values)/Decimal(len(values)); got=Decimal(summary[name]['mean'])
    assert abs(exact-got)<Decimal('1e-12')
    assert Decimal(summary[name]['min'])==min(values) and Decimal(summary[name]['max'])==max(values)
    pieces=[r for r in monthly if r['metric']==name]
    assert len(pieces)==11 and sum(int(r['valid_n']) for r in pieces)==len(values)
    aggregate=sum(Decimal(r['mean'])*Decimal(r['valid_n']) for r in pieces)/Decimal(len(values))
    assert abs(aggregate-got)<Decimal('1e-12')
    checks.append(dict(metric=name,decimal_mean=str(exact),output_mean=str(got),absolute_difference=str(abs(exact-got)),valid_n=len(values),monthly_reaggregation_passed=True,extrema_passed=True))
with (out/'earth_comparability.csv').open() as f:comparison=list(csv.DictReader(f))
for cid in ['MS-03-E01','MS-03-E02']:
    assert {r['theme'] for r in comparison if r['candidate_id']==cid}=={'terrain','temperature_thermal','water_ice','atmosphere_dust'}
for name in ['earth_evidence.csv','earth_prior_work.csv','earth_source_read_log.csv','earth_search_log.csv']:
    with (out/name).open() as f:
        rows=list(csv.DictReader(f)); assert rows and all(None not in r for r in rows)
result=dict(status='passed',checks=checks,source_md5_passed=True,selected_n=16032,expected_days=334,
    source_sha256_passed=True,retained_gzip_sha256_passed=True if src.suffix=='.gz' else None,
    selected_period='[2010-01-01,2010-12-01) printed time; no UTC claim',
    four_themes_per_candidate_passed=True,all_csv_rows_match_headers=True,
    scope='Independent Decimal arithmetic from fixed original columns; monthly weighted identity; extrema; four-theme coverage and CSV schema. This does not validate sensors, physical simultaneity or Mars transfer.')
(out/'earth_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status='passed',metrics=len(checks),sample_n=16032)))
