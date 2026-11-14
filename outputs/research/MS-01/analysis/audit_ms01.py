#!/usr/bin/env python3
"""Read-only MS-01 native-grid audit and University Valley partial-series summary.

Run from a complete project checkout with: .venv/bin/python outputs/research/MS-01/analysis/audit_ms01.py
Only this script's directory is written. No download, global rescreen, or source edit.
"""
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import pandas as pd
import xarray as xr

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from analog import mars, swim, dust
from analog.terrain import slope_deg
from analog.regional_temperature import extract_context
from analog.mars_profiles import summarize_dust


def digest(path, method="sha256"):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, method).hexdigest()


def crop(grid, width=0.25):
    # A half-open box avoids double counting boundary centres; longitude is circular.
    lon_delta = (np.asarray(grid.lon) - 72.75 + 180) % 360 - 180
    return grid.isel(
        lat=np.flatnonzero((grid.lat.values >= 56.75-width) & (grid.lat.values < 56.75+width)),
        lon=np.flatnonzero((lon_delta >= -width) & (lon_delta < width)),
    )


def stats(grid):
    z = np.asarray(grid, dtype=float)
    good = np.isfinite(z)
    weights = np.repeat(np.cos(np.deg2rad(grid.lat.values)), z.shape[1]).reshape(z.shape)
    return {
        "native_cells": int(z.size), "valid_cells": int(good.sum()),
        "mean": float((z[good]*weights[good]).sum()/weights[good].sum()),
        "median": float(np.median(z[good])), "min": float(z[good].min()),
        "max": float(z[good].max()), "positive_cells": int((z[good] > 0).sum()),
    }


def run_mars():
    source_dir = ROOT / "outputs/research/mars_reselection_20261114"
    baseline_path = OUT.parent / "inputs/candidate_native_evidence.baseline.json"
    package = json.loads(baseline_path.read_text())
    reference = next(r for r in package["records"] if r["review_id"] == "A")
    csvpath = OUT.parent / "inputs/final_candidates.baseline.csv"
    if not csvpath.exists():
        csvpath = source_dir / "final_candidates.csv"
    csvrow = pd.read_csv(csvpath).set_index("candidate_id").loc["MS-01"]
    assert reference["center"] == {"lat": 56.75, "lon": 72.75}
    assert float(csvrow.lat) == 56.75 and float(csvrow.lon_east_0_360) == 72.75
    files = []
    for entry in package["sources"]:
        path = ROOT / entry["path"]
        actual = digest(path) if path.exists() else None
        files.append({"path": entry["path"], "source_url": entry.get("url"),
                      "required_for_this_native_recompute": entry["path"].startswith("data/raw/mars/"),
                      "bytes": path.stat().st_size if path.exists() else None,
                      "sha256": actual, "expected_sha256": entry["sha256"],
                      "matches": actual == entry["sha256"]})

    dem = mars.load("mola_topography").astype("float32")
    elevation = crop(dem)
    # Halo keeps centred finite differences independent of the box edge.
    results = {
        "mola_elevation_m_areoid": stats(elevation),
        "mola_slope_deg_3p7km_baseline": stats(crop(slope_deg(crop(dem, width=1.0), mars.MARS_RADIUS_M))),
        "tes_TI_native_excluding_infill": stats(crop(mars.load_thermal_inertia(keep_interpolated=False))),
        "swim_0_1m_native": stats(crop(swim.load("ice_consistency_shallow"))),
        "swim_1_5m_native": stats(crop(swim.load("ice_consistency_deep"))),
    }
    relief = float(elevation.max()-elevation.min())
    masked = int((crop(mars.load("tes_thermal_inertia_night_mask")) == 0).sum())
    comparisons = []
    group_columns = {
        "mola_elevation_m_areoid": "mola_elevation_m",
        "mola_slope_deg_3p7km_baseline": "mola_slope_deg",
        "tes_TI_native_excluding_infill": "TES_TI",
        "swim_0_1m_native": "SWIM_0_1m",
        "swim_1_5m_native": "SWIM_1_5m",
    }
    for group, values in results.items():
        for key in ("native_cells", "valid_cells", "mean", "median", "min", "max"):
            a, b = values[key], reference[group][key]
            c = float(csvrow[f"{group_columns[group]}_{key}"])
            comparisons.append({"quantity": f"{group}.{key}", "recomputed": a,
                                "reference_json": b, "reference_csv": c,
                                "matches": bool(np.isclose(a,b,rtol=1e-10,atol=1e-10) and np.isclose(a,c,rtol=1e-10,atol=1e-10))})
    comparisons += [
        {"quantity": "mola_relief_m", "recomputed": relief, "matches": relief == reference["mola_relief_m"] == float(csvrow.mola_relief_m)},
        {"quantity": "tes_mask_zero_cells", "recomputed": masked, "matches": masked == reference["tes_mask_zero_native_cells"] == int(csvrow.tes_mask_zero_cells)},
    ]
    dust_results = {}
    for year in ("dust_my34", "dust_my35"):
        dust_results[year] = summary = summarize_dust(dust.load_site_series(56.75,72.75,year))
        for key in ("mean_cdodtot", "p95_cdodtot", "max_cdodtot", "valid_reconstructed_sols", "reliability_mean"):
            a,b,c = summary[key], reference["dust"][year][key], float(csvrow[f"{year}_{key}"])
            comparisons.append({"quantity": f"{year}.{key}", "recomputed": a, "reference_json": b,
                                "reference_csv": c, "matches": bool(np.isclose(a,b,rtol=1e-10,atol=1e-10) and np.isclose(a,c,rtol=1e-10,atol=1e-10))})
    with xr.open_dataset(ROOT / "data/raw/mars/temperature/mcs_corrected/MCS_tsurf_corrected.nc") as ds:
        context = extract_context(ds,56.75,72.75)
    series = pd.DataFrame(context.pop("series"))
    context["populated_day_median_K"] = float(series.day_15_K.median())
    context["populated_night_median_K"] = float(series.night_03_K.median())
    for key, column in {
        "valid_day_bins":"MCS_valid_day_bins", "valid_night_bins":"MCS_valid_night_bins",
        "paired_bins":"MCS_paired_bins", "paired_contrast_median_K":"MCS_paired_contrast_median_K",
        "populated_day_median_K":"MCS_populated_day_median_K", "populated_night_median_K":"MCS_populated_night_median_K",
    }.items():
        comparisons.append({"quantity": f"MCS.{key}", "recomputed": context[key], "reference_csv": float(csvrow[column]),
                            "matches": bool(np.isclose(context[key],float(csvrow[column]),rtol=1e-10,atol=1e-10))})
    passed = all(x["matches"] for x in comparisons) and all(x["matches"] for x in files if x["required_for_this_native_recompute"])
    result = {
        "scope": "MS-01 native inputs re-read; no global rescreen, no new observations",
        "status": "PASS" if passed else "FAIL", "latitude":56.75, "longitude_east":72.75,
        "reference_native_evidence": baseline_path.relative_to(ROOT).as_posix(),
        "reference_csv": csvpath.relative_to(ROOT).as_posix(),
        "all_baseline_files_match": all(x["matches"] for x in files),
        "required_raw_files_match": all(x["matches"] for x in files if x["required_for_this_native_recompute"]),
        "bounds": {"south":56.5,"north":57,"west":72.5,"east":73},
        "aggregation": "cos(latitude) weighted native grid-centre means; [south,north),[west,east); no interpolation",
        "source_hashes":files, "comparisons":comparisons, "native":results,
        "relief_m":relief, "TES_mask_zero_cells":masked, "dust":dust_results, "MCS":context,
        "limitations":["Product reprocessing, not independent ground truth or uncertainty validation.",
                       "MOLA grid contains interpolation; finite grid cells are not all direct laser samples.",
                       "SWIM is consistency, not ice fraction/probability; both depths share evidence.",
                       "MCS 5-degree corrected bins and 3-degree dust reconstruction are regional context.",
                       "A matching local input hash does not establish current remote availability."],
    }
    (OUT / "numerical_audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    return passed


def run_uv():
    path = ROOT / "data/raw/earth/university_valley/UniversityV_09_10_Campbell_data_good_only_calibrated.txt"
    expected_md5 = "ae2133eac5c92c695c5f6ef93bcbbd25"
    actual_md5 = digest(path,"md5")
    if actual_md5 != expected_md5:
        raise ValueError("University Valley publisher MD5 mismatch")
    df = pd.read_csv(path,skiprows=[0,2,3],skipinitialspace=True)
    df.columns = df.columns.str.strip()
    # The author file mixes m/d/yyyy and ISO date strings. Never infer one format for all rows.
    df["time"] = pd.to_datetime(df.TIMESTAMP,format="mixed",dayfirst=False,errors="coerce")
    if df.time.isna().any():
        raise ValueError("Unparsed author timestamps")
    differences = df.time.diff().dt.total_seconds()/60
    columns = {
        "T107_air": ("degC","1.2 m above ground per Marinova et al.2022 methods"),
        "T107_surf": ("degC","near-surface covered probe; not remote radiometric skin temperature"),
        "T107_10cm": ("degC","0.10 m below surface"),
        "T107_ice42cm": ("degC","0.42 m ice table at weather station"),
        "T107_InIce49cm": ("degC","0.49 m below surface, in ice-cemented ground"),
        "RH_wrt_water": ("percent","1.2 m above ground; relative to water"),
        "WS_ms": ("m s-1","1.08 m above ground per 2022 methods"),
        "SlrW": ("W m-2","1.27 m above ground; 400–1100 nm pyranometer"),
    }
    rows=[]
    for column,(unit,height) in columns.items():
        z = pd.to_numeric(df[column],errors="coerce")
        z = z.where(np.isfinite(z))
        good=z.notna()
        row={"column":column,"unit":unit,"height_or_depth":height,"rows":len(df),
             "valid":int(good.sum()),"missing":int((~good).sum()),
             "first_valid_timestamp":df.loc[good,"time"].min().isoformat(),
             "last_valid_timestamp":df.loc[good,"time"].max().isoformat(),
             "mean":float(z.mean()),"min":float(z.min()),"max":float(z.max())}
        if unit=="degC":
            row.update(mean_K=row["mean"]+273.15,min_K=row["min"]+273.15,max_K=row["max"]+273.15)
        rows.append(row)
    result={
        "source_doi":"10.5281/zenodo.10553882", "source_file":path.relative_to(ROOT).as_posix(),
        "source_url":"https://zenodo.org/records/10553882/files/UniversityV_09_10_Campbell_data_good_only_calibrated.txt?download=1",
        "source_type":"author-processed calibrated field measurements; existing local bytes re-read, no new download",
        "md5":actual_md5,"publisher_expected_md5":expected_md5,"sha256":digest(path),
        "bytes":path.stat().st_size,"row_count":len(df),
        "start":df.time.min().isoformat(),"end":df.time.max().isoformat(),
        "time_zone":"not declared in this data file; not converted to LTST or UTC",
        "duplicate_timestamps":int(df.time.duplicated().sum()),
        "time_step_minute_counts":{str(k):int(v) for k,v in differences.value_counts().items()},
        "negative_time_steps":int((differences<0).sum()),
        "summaries":rows,
        "limitations":["Partial 2009–2010 file, not a full calendar-year or the complete 2009–2013 study.",
                       "Sample means are unweighted available-row means; no gap interpolation or new outlier filtering.",
                       "good_only_calibrated is author processing, not an independent instrument QA assertion.",
                       "Surface probe can lose covering grains; do not interpret extrema as exact radiometric temperature.",
                       "Not simultaneous or spatially commensurate with Mars MCS data; no direct temperature subtraction."],
    }
    (OUT / "uv_partial_summary.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    pd.DataFrame(rows).to_csv(OUT / "uv_partial_summary.csv",index=False)
    return result


if __name__ == "__main__":
    mars_pass=run_mars()
    uv=run_uv()
    print(json.dumps({"Mars_status":"PASS" if mars_pass else "FAIL", "UV_rows":uv["row_count"],
                      "UV_start":uv["start"],"UV_end":uv["end"]},indent=2))
    if not mars_pass:
        raise SystemExit(1)
