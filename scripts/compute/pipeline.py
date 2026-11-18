"""Candidate-bound station extraction. Descriptive observations, never suitability scores."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import gzip
import io
import json
import math
from pathlib import Path
import statistics
import sys
import time

from inventory import inventory


def digest(path, algorithm="sha256"):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, algorithm).hexdigest()


def read_candidate(path, candidate_id):
    """Keep Team 1 columns unchanged; aliases are additions, never renames."""
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    ids = [r["earth_candidate_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate Earth candidate ID")
    matches = [r for r in rows if r["earth_candidate_id"] == candidate_id]
    if len(matches) != 1:
        raise ValueError(f"Candidate not uniquely found: {candidate_id}")
    row = matches[0].copy()
    aliases = {"site_name": "earth_site_name", "latitude_deg": "earth_lat_deg",
               "longitude_east_deg": "earth_lon_east_deg", "anchor_description": "coordinate_basis",
               "intended_test": "test_purpose", "evidence_sources": "source_urls"}
    for normalized, original in aliases.items():
        value = row[normalized] if normalized in row else row.get(original)
        if not value:
            raise ValueError(f"Missing input contract field: {normalized} / {original}")
        row.setdefault(normalized, value)
    lat, lon = float(row["latitude_deg"]), float(row["longitude_east_deg"])
    if not math.isfinite(lat) or not math.isfinite(lon) or not (-90 <= lat <= 90 and -180 <= lon <= 360):
        raise ValueError("Invalid N/E-positive candidate coordinates")
    if not row.get("mars_candidate_id") or not (row.get("requirements_version") or row.get("review_date")):
        raise ValueError("Mars ID and requirement version/date required")
    return row


def bind_source(candidate, source):
    for key in ["earth_candidate_id", "mars_candidate_id"]:
        if candidate[key] != source[key]:
            raise ValueError(f"Candidate/source {key} mismatch")
    for key in ["latitude_deg", "longitude_east_deg"]:
        if not math.isclose(float(candidate[key]), float(source[key]), abs_tol=1e-8, rel_tol=0):
            raise ValueError(f"Source station does not support candidate {key}")
    if source["adapter"] not in ["campbell_toa5", "elephant_head_pdf"]:
        raise ValueError("Adapter not implemented; unsupported products remain missing")


def parse_timestamp(value, formats):
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(f"Unrecognized station-clock timestamp: {value}")


def decode_value(token, variable, missing_tokens):
    """Explicit token mask, then declared scaling once, then instrument-range mask."""
    if token in missing_tokens:
        return None, "missing_token"
    try:
        raw = float(token)
    except ValueError as exc:
        raise ValueError(f"Unrecognized numeric token: {token}") from exc
    if not math.isfinite(raw):
        return None, "nonfinite"
    if raw in variable.get("fill_values", []):
        return None, "fill_value"
    value = raw * variable["scale_factor"] + variable["add_offset"]
    if not math.isfinite(value):
        return None, "nonfinite_scaled"
    if "valid_range" in variable and not variable["valid_range"][0] <= value <= variable["valid_range"][1]:
        return None, "outside_instrument_range"
    return value, "valid"


def read_station(path, source):
    """Reject ambiguous structure/time; preserve source row numbers and missing observations."""
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.reader(stream, skipinitialspace=True))
    if len(rows) < 5 or rows[0][0].strip() != "TOA5":
        raise ValueError("Not a supported TOA5 archive")
    header = [x.strip() for x in rows[1]]
    units = [x.strip() for x in rows[2]]
    if len(set(header)) != len(header) or len(units) != len(header):
        raise ValueError("Ambiguous column headers/units")
    for variable in source["variables"]:
        if units[header.index(variable["column"]) ] != variable["unit"]:
            raise ValueError(f"Unexpected unit for {variable['column']}")
    expected_md5 = source["expected_md5"]
    if digest(path, "md5") != expected_md5:
        raise ValueError("Input checksum differs from publisher record")
    epoch = datetime.fromisoformat(source["decimal_day_epoch"])
    interval = timedelta(minutes=source["sample_interval_minutes"])
    formats = source["timestamp_formats"]
    seen, records = {}, []
    identical_duplicates, backwards = 0, 0
    last_time = None
    statuses = {v["column"]: Counter() for v in source["variables"]}
    for line, cells in enumerate(rows[4:], start=5):
        cells = [x.strip() for x in cells]
        if len(cells) != len(header):
            raise ValueError(f"Column count mismatch at source line {line}")
        raw = dict(zip(header, cells))
        stamp = parse_timestamp(raw["TIMESTAMP"], formats)
        decimal = float(raw["decimalDaySinceJan1_2009"])
        if not math.isfinite(decimal) or abs((stamp - epoch).total_seconds()/86400 - decimal) > source["decimal_day_tolerance_days"]:
            raise ValueError(f"Date encoding disagreement at source line {line}")
        if (stamp - epoch).total_seconds() % interval.total_seconds() != 0:
            raise ValueError(f"Timestamp off sampling grid at source line {line}")
        if stamp in seen:
            if seen[stamp] != cells:
                raise ValueError(f"Conflicting duplicate timestamp at source line {line}")
            identical_duplicates += 1
            continue
        if last_time is not None and stamp < last_time:
            backwards += 1
        last_time = stamp
        seen[stamp] = cells
        values, flags = {}, {}
        for variable in source["variables"]:
            column = variable["column"]
            values[column], flags[column] = decode_value(raw[column], variable, source["missing_tokens"])
            statuses[column][flags[column]] += 1
        records.append({"timestamp": stamp, "source_line": line, "raw_timestamp": raw["TIMESTAMP"],
                        "raw_decimal_day": raw["decimalDaySinceJan1_2009"], "values": values, "flags": flags})
    records.sort(key=lambda r: r["timestamp"])
    if not records:
        raise ValueError("No records")
    gaps = []
    for previous, current in zip(records, records[1:]):
        steps = (current["timestamp"] - previous["timestamp"]) / interval
        if steps > 1:
            gaps.append({"after": previous["timestamp"].isoformat(), "before": current["timestamp"].isoformat(),
                         "missing_slots": int(steps)-1})
    qa = {"header": header, "units": dict(zip(header, units)), "logger_header": rows[0],
          "source_data_rows": len(rows)-4, "unique_timestamp_rows": len(records),
          "identical_duplicate_rows_removed": identical_duplicates, "conflicting_duplicates": 0,
          "source_order_backward_steps": backwards, "records_sorted_for_output": True,
          "first_timestamp": records[0]["timestamp"].isoformat(), "last_timestamp": records[-1]["timestamp"].isoformat(),
          "raw_timestamp_formats": formats, "decimal_day_epoch": source["decimal_day_epoch"],
          "decimal_day_max_tolerance_seconds": source["decimal_day_tolerance_days"]*86400,
          "time_standard": source["time_standard"], "timestamp_gaps": gaps,
          "all_file_variable_counts": {k: dict(v) for k,v in statuses.items()},
          "qa_flag_column": None, "original_calibration_coefficients": None,
          "prior_QA": "Author good-only calibrated file; independent audit cannot recover removed samples or original QA bits.",
          "scale_offset_policy": "Already calibrated degC; declared identity scale/offset applied once. No re-calibration.",
          "range_policy": "Declared probe operating range; outside values masked and counted, never silently clipped."}
    return records, qa


def months(start, end):
    if start.day != 1 or end.day != 1 or start.time() != datetime.min.time() or end.time() != datetime.min.time():
        raise ValueError("Monthly analysis window requires month boundaries")
    stamp = start
    while stamp < end:
        nxt = datetime(stamp.year + (stamp.month == 12), stamp.month % 12 + 1, 1)
        yield stamp, nxt
        stamp = nxt


def percentile(values, probability):
    values = sorted(values)
    index = (len(values)-1)*probability
    lower = math.floor(index)
    upper = math.ceil(index)
    return values[lower] + (values[upper]-values[lower])*(index-lower)


def summarize(records, source, candidate, file_hash, requirement_version):
    """Observed monthly statistics with explicit support. No annual aggregation or pass threshold."""
    start, end = datetime.fromisoformat(source["period_start"]), datetime.fromisoformat(source["period_end_exclusive"])
    interval_seconds = source["sample_interval_minutes"]*60
    metrics = [dict(v, metric_id=v["column"], columns=[v["column"]], operation="identity") for v in source["variables"]]
    metrics += [{"metric_id": p["metric_id"], "quantity": "paired_temperature_difference", "unit": "Deg C",
                 "columns": p["columns"], "operation": "subtract", "height_above_surface_m": "",
                 "scale_factor": 1.0, "add_offset": 0.0} for p in source.get("paired_differences", [])]
    output = []
    for month_start, month_end in months(start, end):
        samples = [r for r in records if month_start <= r["timestamp"] < month_end]
        expected = int((month_end-month_start).total_seconds()/interval_seconds)
        if len(samples) > expected:
            raise ValueError("More unique records than expected sampling slots")
        for metric in metrics:
            valid = []
            for record in samples:
                values = [record["values"][c] for c in metric["columns"]]
                if all(v is not None for v in values):
                    val = values[0] if metric["operation"] == "identity" else values[0]-values[1]
                    valid.append((record, val))
            values = [v for _,v in valid]
            row = {"earth_candidate_id": candidate["earth_candidate_id"], "mars_candidate_id": candidate["mars_candidate_id"],
                   "site_name": candidate["site_name"], "latitude_deg": candidate["latitude_deg"],
                   "longitude_east_deg": candidate["longitude_east_deg"], "spatial_support": source["spatial_support"],
                   "horizontal_datum": source["horizontal_datum"], "requirement_version": requirement_version,
                   "candidate_purpose_version": candidate.get("requirements_version", candidate.get("review_date")),
                   "source_id": source["source_id"], "source_path": source["path"], "source_sha256": file_hash,
                   "source_columns": ";".join(metric["columns"]), "metric_id": metric["metric_id"], "operation": metric["operation"],
                   "quantity": metric["quantity"], "unit": metric["unit"], "height_above_surface_m": metric["height_above_surface_m"],
                   "period_start": month_start.isoformat(), "period_end_exclusive": month_end.isoformat(),
                   "time_standard": source["time_standard"], "native_interval_minutes": source["sample_interval_minutes"],
                   "output_interval": "calendar month; observed samples only", "sampling_method": "station point; no spatial interpolation",
                   "scale_factor": metric["scale_factor"], "add_offset": metric["add_offset"],
                   "expected_n": expected, "timestamp_n": len(samples), "absent_timestamp_n": expected-len(samples),
                   "valid_n": len(values), "present_but_invalid_n": len(samples)-len(values),
                   "missing_n": expected-len(values), "coverage_fraction": len(values)/expected,
                   "coverage_status": "complete_calendar_support" if len(values)==expected else ("partial_calendar_support" if values else "no_valid_data"),
                   "suitability_threshold_status": "not_defined", "annual_statistic": "not_computed",
                   "first_valid_source_line": valid[0][0]["source_line"] if valid else "",
                   "last_valid_source_line": valid[-1][0]["source_line"] if valid else "",
                   "observed_mean": statistics.fmean(values) if values else "",
                   "observed_median": statistics.median(values) if values else "",
                   "observed_min": min(values) if values else "", "observed_max": max(values) if values else "",
                   "observed_p05": percentile(values, .05) if values else "", "observed_p95": percentile(values, .95) if values else "",
                   "dataset_doi": source["dataset_doi"], "method_url": source["method_url"]}
            output.append(row)
    return output


def write_csv(path, rows):
    if not rows:
        raise ValueError("Empty CSV result")
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = list(dict.fromkeys(k for r in rows for k in r))
    if path.suffix == ".gz":
        binary = gzip.GzipFile(filename=str(path), mode="wb", mtime=0)
        stream_context = io.TextIOWrapper(binary, encoding="utf-8", newline="")
    else:
        stream_context = path.open("w", encoding="utf-8", newline="")
    with stream_context as stream:
        writer = csv.DictWriter(stream, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def plot(rows, source, candidate, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    variables = source["variables"]
    figure, axes = plt.subplots(2, 1, figsize=(12, 8.3), gridspec_kw={"height_ratios": [2.1,1]}, constrained_layout=True)
    coverage = []
    chosen_periods = [r["period_start"] for r in rows if r["metric_id"] == variables[0]["column"]]
    count = len(chosen_periods)
    labels = [p[:7] for p in chosen_periods]
    for var in variables:
        chosen = [r for r in rows if r["metric_id"] == var["column"]]
        y = [float(r["observed_mean"]) if r["observed_mean"] != "" and r["coverage_status"] == "complete_calendar_support" else float("nan") for r in chosen]
        line, = axes[0].plot(range(count), y, "o-", label=var["plot_label"], linewidth=1.4, markersize=4)
        partial = [(i,float(r["observed_mean"])) for i,r in enumerate(chosen) if r["observed_mean"] != "" and r["coverage_status"] != "complete_calendar_support"]
        if partial:
            axes[0].scatter([i for i,_ in partial], [v for _,v in partial], marker="x", color=line.get_color(), s=40)
        coverage.append([100*r["coverage_fraction"] for r in chosen])
    axes[0].set(ylabel="Observed monthly mean (degC)", xticks=range(count), xticklabels=labels)
    axes[0].tick_params(axis="x", rotation=35)
    axes[0].grid(alpha=.25)
    axes[0].legend(ncol=2, fontsize=9)
    axes[0].set_title("Means describe available samples; x = incomplete calendar month, shown separately", fontsize=10)
    hm = axes[1].imshow(np.asarray(coverage), aspect="auto", vmin=0, vmax=100, cmap="YlGnBu")
    axes[1].set(yticks=range(len(variables)), yticklabels=[v["plot_label"] for v in variables],
                xticks=range(count), xticklabels=labels)
    axes[1].tick_params(axis="x", rotation=35)
    for j, line in enumerate(coverage):
        for i, value in enumerate(line):
            axes[1].text(i,j,f"{value:.1f}",ha="center",va="center",fontsize=8,color="white" if value>70 else "black")
    figure.colorbar(hm, ax=axes[1], label="Valid / expected native samples (%)")
    figure.suptitle(f"{candidate['earth_candidate_id']} / {candidate['mars_candidate_id']} | {candidate['site_name']}\n"
                    f"{float(candidate['latitude_deg']):.5f} deg N, {float(candidate['longitude_east_deg']):.4f} deg E | Station clock (UTC offset unknown)\n"
                    "Point probes; sensor heights/depths in legend; no area interpolation", fontsize=11)
    figure.supxlabel(f"Source DOI {source['dataset_doi']}; author-calibrated archive.\n"
                       f"{source['sample_interval_minutes']} min native records -> calendar-month summaries; no filling, annual mean, ice-depth inference or suitability threshold.", fontsize=9)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=160)
    plt.close(figure)


def run(root, candidate_path, profiles_path, candidate_id, output):
    total_start = time.perf_counter()
    config = json.loads(profiles_path.read_text())
    candidate = read_candidate(candidate_path, candidate_id)
    sources = [s for s in config["sources"] if s["earth_candidate_id"] == candidate_id]
    if len(sources) != 1:
        raise ValueError("Exactly one supported station source per candidate is required in v1")
    source = sources[0]
    bind_source(candidate, source)
    if source["adapter"] == "elephant_head_pdf":
        from eh_adapter import run_eh
        return run_eh(root, candidate_path, profiles_path, candidate, source, config, output)
    output.mkdir(parents=True, exist_ok=True)
    path = root / source["path"]
    manifest = [{"source_id": source["source_id"], "candidate_id": candidate_id,
                 "filename_or_product": path.name, "relative_path": source["path"], "source_url": source["url"],
                 "dataset_doi": source["dataset_doi"], "period": "actual file dates in QA report; analysis 2010",
                 "variables": ";".join(v["column"] for v in source["variables"]), "units": "degC; already author-calibrated",
                 "coordinates_grid": "W station point; no projected raster grid; datum unstated", "native_interval": "30 minutes",
                 "file_status": "present" if path.is_file() else "missing", "bytes": path.stat().st_size if path.is_file() else "",
                 "sha256": digest(path) if path.is_file() else "", "expected_md5": source["expected_md5"],
                 "source_level": source["source_level"], "archive_publication_date": source["archive_published"],
                 "acquisition_date": "2026-11-14; original browser download; see provenance sidecar"}]
    for pending in config.get("pending_inputs", []):
        manifest.append({"source_id": pending["product"], "candidate_id": candidate_id,
                         "filename_or_product": pending["filename_pattern"], "source_url": pending["source"],
                         "period": pending["period"], "variables": pending["variables"], "units": pending["units"],
                         "coordinates_grid": pending["grid"], "file_status": "not_supplied_to_this_case",
                         "expected_files": pending["expected_files"], "missing_reason": pending["reason"]})
    write_csv(output/"inputs_manifest.csv", manifest)
    if not path.is_file():
        raise FileNotFoundError(f"Real input absent; manifest written without numeric output: {path}")
    reading_start = time.perf_counter()
    records, qa = read_station(path, source)
    reading_seconds = time.perf_counter()-reading_start
    manifest[0]["observation_start"] = qa["first_timestamp"]
    manifest[0]["observation_end"] = qa["last_timestamp"]
    manifest[0]["analysis_start"] = source["period_start"]
    manifest[0]["analysis_end_exclusive"] = source["period_end_exclusive"]
    provenance_path = path.with_suffix(path.suffix+".provenance.json")
    acquisition = json.loads(provenance_path.read_text()) if provenance_path.is_file() else {"status":"acquisition_details_not_supplied"}
    manifest[0]["acquisition_date"] = acquisition.get("retrieval_date", acquisition.get("retrieved_utc", "unknown"))
    write_csv(output/"inputs_manifest.csv", manifest)
    calc_start = time.perf_counter()
    features = summarize(records, source, candidate, digest(path), config["requirement_version"])
    calculation_seconds = time.perf_counter()-calc_start
    write_csv(output/"earth_candidate_features.csv", features)
    tidy = []
    for record in records:
        tidy.append({"earth_candidate_id": candidate_id, "mars_candidate_id": candidate["mars_candidate_id"],
                     "source_id": source["source_id"], "source_line": record["source_line"],
                     "raw_timestamp": record["raw_timestamp"], "station_clock": record["timestamp"].isoformat(),
                     "raw_decimal_day_since_2009_01_01": record["raw_decimal_day"],
                     **{k: "" if v is None else v for k,v in record["values"].items()},
                     **{k+"__status": v for k,v in record["flags"].items()}})
    write_csv(output/"station_observations.csv.gz", tidy)
    figure_start = time.perf_counter()
    plot(features, source, candidate, output/"figures"/f"{candidate_id}_temperature_coverage.png")
    figure_seconds = time.perf_counter()-figure_start
    env = inventory(root, include_files=False)
    report = {"schema_version": "1.0", "generated_utc": datetime.now(timezone.utc).isoformat(),
              "requirement_version": config["requirement_version"], "candidate_contract": candidate,
              "source_profile": source, "candidate_csv_sha256": digest(candidate_path),
              "acquisition": acquisition,
              "profiles_sha256": digest(profiles_path), "source_sha256": digest(path),
              "processing_code_sha256": {p.name: digest(p) for p in sorted((root/"scripts/compute").glob("*.py"))},
              "source_md5_verified": digest(path,"md5") == source["expected_md5"],
              "qa": qa, "monthly_support": [{k:r[k] for k in ["metric_id","period_start","valid_n","expected_n","missing_n","coverage_fraction","coverage_status"]} for r in features],
              "policy": {"annual_statistics": "not_computed", "interpolation": "none", "unknown_UTC_offset": "no conversion",
                         "suitability_threshold": None, "threshold_status": "not_defined",
                         "observed_statistics": "Descriptive only, retain all actual valid N and calendar coverage; no automatic acceptance cutoff",
                         "independent_truth": "Historical published interface is contextual metadata, not held-out truth or current ice depth",
                         "unimplemented_products": "MERRA-2, MODIS and DEM remain missing, no fabricated extraction"},
              "environment": env, "execution": {"backend": "CPU", "numeric_precision": "Python binary64 / float64",
              "gpu_used": False, "speedup": None, "read_parse_qa_seconds": reading_seconds,
              "monthly_calculation_seconds": calculation_seconds, "figure_seconds": figure_seconds,
              "data_transfer_seconds": None, "timing_note": "Single local descriptive run; no GPU or performance comparison; download not included",
              "total_seconds": time.perf_counter()-total_start}}
    (output/"qa_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"candidate": candidate_id, "rows_read": len(records), "monthly_rows": len(features),
                      "backend": "CPU", "output": str(output), "seconds": report["execution"]["total_seconds"]}))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--candidates", type=Path)
    parser.add_argument("--profiles", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    run(root, args.candidates or root/"outputs/compute/inputs/team1_earth_analog_candidates.csv",
        args.profiles or root/"scripts/compute/source_profiles.json", args.candidate_id,
        args.output or root/"outputs/compute"/args.candidate_id)


if __name__ == "__main__":
    main()
