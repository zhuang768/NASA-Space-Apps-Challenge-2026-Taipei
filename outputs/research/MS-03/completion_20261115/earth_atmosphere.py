#!/usr/bin/env python3
"""Describe one pinned author-processed W Campbell export; never align clocks.

Usage: python3 earth_atmosphere.py [source_path] [out_dir]
Defaults to retained earth_raw/*.txt.gz, then the original data/raw path if absent.
An explicit uncompressed source path remains supported; requires only stdlib.
"""
import calendar
import collections
import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import sys

SOURCE_URL = "https://zenodo.org/records/10553882/files/UniversityV_09_10_Campbell_data_good_only_calibrated.txt?download=1"
SHA256 = "c46d93e3dd07c6c91d700a814214716f00caa0d5cc3a520f8969ce0af63ecafd"
MD5 = "ae2133eac5c92c695c5f6ef93bcbbd25"
RAW_NAME = "UniversityV_09_10_Campbell_data_good_only_calibrated.txt"
GZIP_SHA256 = "f2ab00f49fdfa9f64cb2e6fe15df3d32599f382292ba7b2e4b916f75c5f311f1"
START, STOP = dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 1)
FIELDS = [
    ("air_temperature", "T107_air", "Deg C", "degC", "Campbell 207 per paper; export column named T107_air", 1.2),
    ("air_RH_water_basis", "RH_wrt_water", "%", "%", "Campbell 207; author corrected export basis retained", 1.2),
    ("air_RH_ice_basis", "RH_wrt_WaterIce", "%", "%", "Campbell 207; author corrected export basis retained", 1.2),
    ("solar_irradiance", "SlrW", "W/m^2", "W m-2", "LI-COR LI200X; 400-1100 nm response", 1.27),
    ("wind_speed", "WS_ms", "meters/second", "m s-1", "RM Young 05103 in paper Methods; paper accuracy paragraph says 05013", 1.08),
]

def parse_time(value):
    for fmt in ("%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return dt.datetime.strptime(value.strip(), fmt)
        except ValueError:
            pass
    raise ValueError("Unexpected printed timestamp format: " + value)

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def main():
    here = Path(__file__).resolve().parent
    retained = here/"earth_raw"/(RAW_NAME+".gz")
    fallback = here.parents[3]/"data/raw/earth/university_valley"/RAW_NAME
    src = Path(sys.argv[1]) if len(sys.argv)>1 else retained if retained.is_file() else fallback
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else here
    out.mkdir(parents=True, exist_ok=True)
    packed = src.read_bytes()
    if src.suffix==".gz":
        assert hashlib.sha256(packed).hexdigest()==GZIP_SHA256, "retained gzip SHA256 mismatch"
        raw = gzip.decompress(packed)
        input_mode="retained_lossless_gzip"
    else:
        raw = packed
        input_mode="explicit_or_fallback_uncompressed_original"
    assert hashlib.sha256(raw).hexdigest() == SHA256, "wrong source version"
    assert hashlib.md5(raw).hexdigest() == MD5, "provider MD5 mismatch"
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8"))))
    header, units, body = [x.strip() for x in rows[1]], [x.strip() for x in rows[2]], rows[4:]
    assert len(body) == 17705 and all(len(r) == 20 for r in body)
    times = [parse_time(r[0]) for r in body]
    assert len(set(times)) == len(times)
    assert all((b-a).total_seconds() == 1800 for a,b in zip(times, times[1:]))
    selected = [(t,r) for t,r in zip(times,body) if START <= t < STOP]
    assert len(selected) == 16032
    assert selected[0][0] == START and selected[-1][0] == STOP-dt.timedelta(minutes=30)
    metadata = {}
    for metric, column, rawunit, unit, instrument, height in FIELDS:
        pos = header.index(column)
        assert units[pos] == rawunit
        metadata[metric] = dict(column=column, position_0based=pos, unit=unit, instrument=instrument, height_m=height)
    summary, monthly = [], []
    for metric, md in metadata.items():
        values = [float(r[md["position_0based"]]) for _,r in selected]
        finite = [v for v in values if math.isfinite(v)]
        assert len(finite) == 16032
        common = dict(candidate_id="MS-03-E01", metric=metric, unit=md["unit"],
                      printed_start_inclusive=START.isoformat(), printed_stop_exclusive=STOP.isoformat(),
                      printed_time_basis="unresolved; no UTC conversion", cadence_minutes=30,
                      support="W point; author-processed short09_10 file only", height_m=md["height_m"],
                      source_column=md["column"], source_url=SOURCE_URL,
                      source_locator="second header row column="+md["column"], evidence_type="descriptive_calculation_of_author_processed_export")
        summary.append(dict(common, expected_n=len(selected), valid_n=len(finite), missing_n=len(values)-len(finite),
                            mean=statistics.fmean(finite), min=min(finite), max=max(finite)))
        for month in range(1,12):
            vals=[float(r[md["position_0based"]]) for t,r in selected if t.month==month]
            good=[v for v in vals if math.isfinite(v)]
            expected=calendar.monthrange(2010,month)[1]*48
            assert len(vals)==expected
            monthly.append(dict(candidate_id="MS-03-E01",metric=metric,month=f"2010-{month:02}",unit=md["unit"],
                                expected_n=expected,valid_n=len(good),missing_n=len(vals)-len(good),
                                mean=statistics.fmean(good),min=min(good),max=max(good)))
    write_csv(out/"earth_atmosphere_summary.csv",summary)
    write_csv(out/"earth_atmosphere_monthly.csv",monthly)
    receipt=dict(source_url=SOURCE_URL,dataset_doi="10.5281/zenodo.10553882",source_bytes=len(raw),
        sha256=SHA256,md5=MD5,provider_md5_observed_again_taipei="2026-11-15",
        retained_source="earth_raw/"+RAW_NAME+".gz",retained_gzip_sha256=GZIP_SHA256,input_mode=input_mode,
        retention="Lossless gzip;mtime0;empty stored filename. Decompressed original bytes, line endings and timestamps unchanged. Attribution/license/full provenance in earth_raw/provenance.json.",
        original_acquisition="Existing local bytes; prior provenance says browser download 2026-11-14; this task independently rehashed and rechecked online provider MD5",
        input_rows=len(body),input_printed_first=times[0].isoformat(),input_printed_last=times[-1].isoformat(),
        selected_rows=len(selected),selected_start_inclusive=START.isoformat(),selected_stop_exclusive=STOP.isoformat(),
        source_timestamp_formats=sorted(set("ISO8601-like" if "-" in r[0] else "month/day/year" for r in body)),
        input_printed_cadence_minutes=30,duplicate_printed_timestamps=0,header_mapping=metadata,
        checks="Pinned source SHA256 and provider MD5; all row widths; header+unit positions; mixed time-format parse; unique ordered 30-minute source cadence; complete 11 calendar months; per-month sample counts; all five fields finite",
        limitations=["11 calendar months, not an annual climatology", "Unresolved clock basis retained; no UTC conversion, Campbell-HOBO join, lag or diffusivity calculation", "Processed/calibrated author file, not logger bytes; missing per-row intervention flags", "Separate short export, not asserted identical to long09_13 export", "0 wind values may be below the anemometer threshold; no calibration or dust proxy", "Source sensor-model spelling differs within paper; do not silently resolve 05103 versus 05013", "RH basis kept as supplied, no water activity or vapour correction", "Solar channel response differs from TES and is not a Mars radiation estimate", "Sample counts do not reduce systematic instrument errors", "Point records, not gridded terrain or whole-valley climate"])
    (out/"earth_input_receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(dict(status="passed",input_rows=len(body),selected_rows=len(selected),summary_rows=len(summary),monthly_rows=len(monthly))))

if __name__ == "__main__":
    main()
