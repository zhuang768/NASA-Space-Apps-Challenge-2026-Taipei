"""Check local artifact integrity and calculation; never certify external observations."""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "manifest.json").read_text())
for item in manifest["files"]:
    payload = (ROOT / item["path"]).read_bytes()
    assert len(payload) == item["bytes"], item["path"]
    assert hashlib.sha256(payload).hexdigest() == item["sha256"], item["path"]
with (ROOT / "source_audit.csv").open(newline="", encoding="utf-8") as f:
    sources = list(csv.DictReader(f))
assert len({row["source_id"] for row in sources}) == len(sources)
assert all(row["url"].startswith("https://") for row in sources)
assert all(row["original_data_status"] != "acquired" for row in sources)
with (ROOT / "search_log.csv").open(newline="", encoding="utf-8") as f:
    searches = list(csv.DictReader(f))
with (ROOT / "crim_identifiability.csv").open(newline="", encoding="utf-8") as f:
    scenarios = list(csv.DictReader(f))
for row in scenarios:
    fraction = float(row["algebraic_ice_fraction"])
    ki, ks = map(float, (row["ice_permittivity_assumed"], row["host_permittivity_assumed"]))
    ke = (fraction*math.sqrt(ki) + (1-fraction)*math.sqrt(ks))**2
    assert math.isclose(ke, float(row["effective_permittivity_assumed"]), abs_tol=1e-12)
    assert (0 <= fraction <= 1) == (row["physically_admissible_in_this_model"] == "True")
assert sum(row["physically_admissible_in_this_model"] == "True" for row in scenarios) == 3
# Independent checks of the source-line-linked wind derivative and withheld snow proxy.
import gzip
import statistics
from datetime import datetime
support=json.loads((ROOT/'uv_export_support.json').read_text())
assert support['source_decoded_md5']=='ae2133eac5c92c695c5f6ef93bcbbd25'
assert support['source_decoded_sha256']=='c46d93e3dd07c6c91d700a814214716f00caa0d5cc3a520f8969ce0af63ecafd'
assert support['surface_RH_available_in_this_export'] is False
assert support['snow_proxy_equivalent_days'] is None
assert support['rows_in_paper_summer_window']==4137
with gzip.open(ROOT/'uv_wind_records.csv.gz','rt',newline='') as f: windrows=list(csv.DictReader(f))
assert len(windrows)==support['data_rows']==17705
assert [int(r['source_text_line_1based']) for r in windrows]==list(range(5,17710))
wind=[float(r['wind_ms']) for r in windrows]
assert all(math.isfinite(v) for v in wind)
assert sum(v<1 for v in wind)==support['wind_below_1ms_instrument_threshold_N']==4949
assert min(wind)==support['wind_min']==0 and max(wind)==support['wind_max']==14.65
assert statistics.median(wind)==support['wind_median']==1.82
assert math.isclose(statistics.mean(wind),support['wind_mean'],abs_tol=1e-12)
sortedwind=sorted(wind);index=(len(wind)-1)*.95;lower=int(index)
p95=sortedwind[lower]+(index-lower)*(sortedwind[lower+1]-sortedwind[lower])
assert math.isclose(p95,support['wind_p95_linear'],abs_tol=1e-12)
times=[]
for r in windrows:
 t=r['printed_timestamp']
 times.append(datetime.fromisoformat(t) if r['timestamp_format']=='ISO' else datetime.strptime(t,'%m/%d/%Y %H:%M'))
assert all((b-a).total_seconds()==1800 for a,b in zip(times,times[1:]))
assert min(times).strftime('%Y-%m-%d %H:%M:%S')==support['printed_time_start']
assert max(times).strftime('%Y-%m-%d %H:%M:%S')==support['printed_time_stop']
assert sum(r['timestamp_format']=='ISO' for r in windrows)==616

# Separate hourly surface-RH checkpoint; never apply the paper's48 divisor.
surf=json.loads((ROOT/'uv_surface_RH_support.json').read_text())
assert surf['source_decoded_md5']=='0c138af0770ec15d4a4942a66507328f'
assert surf['source_decoded_sha256']=='dc85d4a15723193044c909f761f10cf8e1272912073b378300bdcf5832ccab0c'
assert surf['header'][6]=='Surf_RHIce' and surf['native_cadence_seconds']==3600
assert surf['paper_cadence_seconds']==1800 and surf['equivalent_day_divisor']==24
assert surf['full_paper_snow_days_reproduced'] is False and surf['infilled_or_resampled'] is False
assert surf['decimal_minus_printed_hours_rounded_counts']=={'1.0':8625}
with gzip.open(ROOT/'uv_surface_RH_available_summer.csv.gz','rt',newline='') as f: sr=list(csv.DictReader(f))
assert len(sr)==surf['available_hourly_samples']==1944
assert [int(r['source_text_line_1based']) for r in sr]==list(range(3,1947))
rh=[float(r['surface_RH_ice_percent']) for r in sr]
assert all(math.isfinite(v) for v in rh)
assert sum(v>=98 for v in rh)==surf['ge98_percent_sample_count']==78
assert math.isclose(sum(v>=98 for v in rh)/len(rh),surf['ge98_percent_fraction_of_finite_available_samples'])
assert sum(v>=98 for v in rh)/24==surf['nominal_hourly_sample_equivalent_days']==3.25
assert 2880-len(sr)==surf['uncovered_nominal_window_hourly_positions']==936
st=[datetime.strptime(r['printed_timestamp'],'%m/%d/%Y %H:%M') for r in sr]
assert all((b-a).total_seconds()==3600 for a,b in zip(st,st[1:]))

result = {
    "local_artifact_integrity": "pass",
    "checked_local_files": len(manifest["files"]),
    "source_records": len(sources),
    "search_records": len(searches),
    "calculation_scenarios": len(scenarios),
    "check_scope": "hashes, source schema, CRIM forward reconstruction, source-line/time-linked wind and hourly surface-RH support; full-paper snow result withheld",
    "author_calibrated_UV_export_reused": True,
    "wind_records_checked": len(windrows),
    "snow_proxy_count_reproduced": False,
    "full_paper_snow_proxy_count_reproduced": False,
    "available_hourly_surface_proxy_support_computed": True,
    "available_hourly_surface_RH_records_checked": len(sr),
    "original_earth_series_or_radar_acquired": False,
    "external_ground_truth_validated": False,
    "research_completion": "unproven; original records and independent target validation remain missing",
}
(ROOT / "verification.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
