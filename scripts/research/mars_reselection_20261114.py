#!/usr/bin/env python3
"""Full-data, unweighted exploratory Mars rescreen; old products are read-only.

Run from the repository root with .venv/bin/python -m scripts.research.mars_reselection_20261114.
The output is a pool for a subsequent bounded prior-site audit, not novelty clearance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

from analog import dust, mars, swim
from analog.stack import _onto_grid, _coarsen_factor
from analog.regional_temperature import validate_grid, extract_context
from analog.mars_profiles import summarize_dust
from analog.terrain import slope_deg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/research/mars_reselection_20261114"
VERSION = "MARS-RESELECT-20261114-v1-exploratory"
OBJECTIVES = {
    "ice_shallow": "maximize",
    "ice_deep": "maximize",
    "slope": "minimize",
    "relief": "minimize",
    "dust_my34_p95": "minimize",
    "dust_my35_p95": "minimize",
}


def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def source_manifest() -> list[dict]:
    paths = [ROOT / "data/processed/mars_stack_0p5deg.nc"]
    urls = {}
    for module in [mars, swim, dust]:
        for key, url in module.PRODUCTS.items():
            p = mars.RAW_DIR / url.rsplit("/", 1)[1]
            paths.append(p)
            urls[p.relative_to(ROOT).as_posix()] = url
            if module is mars:
                paths.append(p.with_suffix(".lbl"))
                urls[p.with_suffix(".lbl").relative_to(ROOT).as_posix()] = url.rsplit(".", 1)[0] + ".lbl"
    paths += [ROOT / "data/raw/mars/temperature/mcs_corrected/MCS_tsurf_corrected.nc",
              ROOT / "data/raw/mars/temperature/mcs_corrected/record.json",
              ROOT / "outputs/mars_temperature/summary.json",
              ROOT / "outputs/mars_discovery/mars_site_discovery.json"]
    urls["data/raw/mars/temperature/mcs_corrected/MCS_tsurf_corrected.nc"] = "https://zenodo.org/api/records/17947556/files/MCS_tsurf_corrected.nc/content"
    urls["data/raw/mars/temperature/mcs_corrected/record.json"] = "https://zenodo.org/api/records/17947556"
    return [{"path": p.relative_to(ROOT).as_posix(), "url": urls.get(p.relative_to(ROOT).as_posix()), "bytes": p.stat().st_size,
             "sha256": sha(p)} for p in paths]


def to_common(grid: xr.DataArray) -> xr.DataArray:
    return _onto_grid(grid, method="nearest")


def dust_layers(name: str) -> dict[str, xr.DataArray]:
    path = mars.RAW_DIR / dust.PRODUCTS[name].rsplit("/", 1)[1]
    result = {}
    with dust.open_dataset(path) as ds:
        value = ds.cdodtot.where(np.isfinite(ds.cdodtot) & (ds.cdodtot >= 0))
        native = {
            "mean": value.mean("Time"),
            "p95": value.quantile(.95, dim="Time"),
            "max": value.max("Time"),
            "valid_sols": value.count("Time"),
            "reliability_mean": ds.cdodrel.where(np.isfinite(ds.cdodrel)).mean("Time"),
            "cdod610_mean": ds.cdod610.where(np.isfinite(ds.cdod610) & (ds.cdod610 >= 0)).mean("Time"),
        }
        for a in range(0, 360, 90):
            mask = (ds.Ls >= a) & (ds.Ls < a + 90)
            native[f"Ls{a}_{a+90}_mean"] = value.where(mask).mean("Time")
        for key, grid in native.items():
            grid = grid.reset_coords(drop=True)
            grid = grid.rename(latitude="lat", longitude="lon")
            grid = grid.assign_coords(lon=((grid.lon + 180) % 360) - 180).sortby("lon")
            result[f"{name}_{key}"] = to_common(grid).load()
        # Coordinates are explicit native 3-degree nearest-cell provenance.
        for key, grid in {
            "native_lat": xr.ones_like(native["mean"]) * ds.latitude,
            "native_lon": xr.ones_like(native["mean"]) * ds.longitude,
        }.items():
            grid = grid.rename(latitude="lat", longitude="lon")
            grid = grid.assign_coords(lon=((grid.lon + 180) % 360) - 180).sortby("lon")
            result[f"{name}_{key}"] = to_common(grid).load()
    return result


def mcs_layers(stack: xr.Dataset) -> dict[str, xr.DataArray]:
    p = ROOT / "data/raw/mars/temperature/mcs_corrected/MCS_tsurf_corrected.nc"
    with xr.open_dataset(p) as ds:
        validate_grid(ds)
        value = ds.tsurf_correct.sel(MY=slice(29, 36)).load()
        value = value.where(np.isfinite(value) & (value > 0))
        night, day = value.sel(ltst=3), value.sel(ltst=15)
        paired = day.notnull() & night.notnull()
        values = {
            "mcs_day_bins": day.count(("MY", "Ls")),
            "mcs_night_bins": night.count(("MY", "Ls")),
            "mcs_paired_bins": paired.sum(("MY", "Ls")),
            "mcs_day_median_K": day.median(("MY", "Ls")),
            "mcs_night_median_K": night.median(("MY", "Ls")),
            "mcs_paired_contrast_median_K": (day-night).where(paired).median(("MY", "Ls")),
        }
        ilat = np.abs(ds.Lat.values[:, None] - stack.lat.values[None, :]).argmin(axis=0)
        dlon = (ds.Lon.values[:, None] - stack.lon.values[None, :] + 180) % 360 - 180
        ilon = np.abs(dlon).argmin(axis=0)
        result = {key: xr.DataArray(grid.values[np.ix_(ilat, ilon)], dims=("lat", "lon"),
                  coords={"lat": stack.lat, "lon": stack.lon}) for key, grid in values.items()}
        result["mcs_native_lat"] = xr.DataArray(np.broadcast_to(ds.Lat.values[ilat, None], stack.slope.shape), dims=("lat", "lon"), coords={"lat":stack.lat,"lon":stack.lon})
        result["mcs_native_lon"] = xr.DataArray(np.broadcast_to(ds.Lon.values[None, ilon], stack.slope.shape), dims=("lat", "lon"), coords={"lat":stack.lat,"lon":stack.lon})
        return result


def pareto_mask(table: pd.DataFrame) -> np.ndarray:
    """Exact non-dominated set; no weights, target values or scalar score."""
    values = np.column_stack([table[k].to_numpy() * (-1 if direction == "maximize" else 1)
                              for k, direction in OBJECTIVES.items()])
    order = np.lexsort(tuple(values[:, j] for j in range(values.shape[1]-1, -1, -1)))
    frontier: list[int] = []
    for idx in order:
        v = values[idx]
        if frontier:
            f = values[frontier]
            if np.any(np.all(f <= v, axis=1) & np.any(f < v, axis=1)):
                continue
            keep = ~(np.all(v <= f, axis=1) & np.any(v < f, axis=1))
            frontier = [j for j, yes in zip(frontier, keep) if yes]
        frontier.append(int(idx))
    result = np.zeros(len(table), dtype=bool)
    result[frontier] = True
    return result


def separated_add(chosen: list[dict], rows: pd.DataFrame, reason: str, limit: int, min_deg=5.0) -> None:
    n = 0
    for r in rows.to_dict("records"):
        # This is a presentation-diversity rule, not a physical hazard buffer.
        if any(abs(r["lat"]-s["lat"]) < min_deg and abs((r["lon"]-s["lon"]+180)%360-180) < min_deg for s in chosen):
            continue
        r["exploratory_reason"] = reason
        chosen.append(r)
        n += 1
        if n >= limit:
            break


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_manifest()
    before = {r["path"]: r["sha256"] for r in sources}
    with xr.open_dataset(ROOT / "data/processed/mars_stack_0p5deg.nc", engine="scipy") as s:
        stack = s.load()
    stack = stack.sel(lat=slice(59.75, -59.75))
    grids = {name: stack[name] for name in stack.data_vars}
    deep = swim.load("ice_consistency_deep")
    deep = deep.coarsen(lat=_coarsen_factor(deep), lon=_coarsen_factor(deep), boundary="trim").mean()
    grids["ice_deep"] = _onto_grid(deep).sel(lat=stack.lat)
    topo = mars.load("mola_topography").astype("float32")
    elev = topo.coarsen(lat=_coarsen_factor(topo), lon=_coarsen_factor(topo), boundary="trim").mean()
    grids["elevation_mean_m_areoid"] = _onto_grid(elev).sel(lat=stack.lat)
    for name in ["dust_my34", "dust_my35"]:
        for key, value in dust_layers(name).items():
            grids[key] = value.sel(lat=stack.lat)
    grids.update(mcs_layers(stack))
    frame = xr.Dataset(grids).to_dataframe().reset_index()
    # Real observations are not all contemporaneous, and repeated coarse cells are not new samples.
    frame["ice_lower_consistency"] = np.minimum(frame.ice_shallow, frame.ice_deep)
    finite_keys = list(OBJECTIVES) + ["thermal_inertia", "elevation_mean_m_areoid"]
    frame["finite_core_descriptors"] = np.isfinite(frame[finite_keys]).all(axis=1)
    frame["positive_both_ice_consistency"] = (frame.ice_shallow > 0) & (frame.ice_deep > 0)
    old = json.loads((ROOT / "outputs/mars_discovery/mars_site_discovery.json").read_text())
    old_coords = {(p["lat"], p["lon"]) for p in old["purposes"]["isru_shallow_ice"]["picks"]}
    frame["old_ice_candidate_cell"] = [(a,b) in old_coords for a,b in zip(frame.lat,frame.lon)]
    # Famous old project boxes remain exclusions, with no implication that every site outside is new.
    frame["inside_old_known_box"] = False
    for box in old["excluded_boxes"].values():
        inside = frame.lat.between(box["south"],box["north"]) & frame.lon.between(box["west"],box["east"])
        frame.loc[inside,"inside_old_known_box"] = True
    eligible = frame.finite_core_descriptors & frame.positive_both_ice_consistency & ~frame.old_ice_candidate_cell & ~frame.inside_old_known_box
    frame["exploratory_pool"] = eligible
    pool = frame.loc[eligible].copy().reset_index(drop=True)
    for key, direction in OBJECTIVES.items():
        pool[f"{key}_favourable_percentile"] = pool[key].rank(pct=True, ascending=(direction=="maximize"), method="average") * 100
    pool["pareto_front"] = pareto_mask(pool)
    front = pool.loc[pool.pareto_front].copy()
    chosen: list[dict] = []
    north = front.loc[front.lat >= 51]
    separated_add(chosen, north.sort_values(["ice_lower_consistency","slope"],ascending=[False,True]), "north>=51; stronger minimum of the two related ice descriptors", 7)
    separated_add(chosen, front.sort_values(["ice_lower_consistency","slope"],ascending=[False,True]), "stronger minimum of two related ice descriptors", 5)
    separated_add(chosen, front.sort_values(["slope","relief"],ascending=[True,True]), "lower regional slope on the full-data Pareto front", 5)
    separated_add(chosen, front.sort_values(["dust_my35_p95","dust_my34_p95"],ascending=[True,True]), "lower reconstructed dust p95 on the full-data Pareto front", 5)
    pd.DataFrame(chosen).to_csv(OUT/"exploratory_candidates.csv",index=False)
    pool.to_csv(OUT/"screened_pool.csv.gz",index=False,compression={"method":"gzip","mtime":0})
    front.to_csv(OUT/"pareto_front.csv.gz",index=False,compression={"method":"gzip","mtime":0})
    method = {
        "version": VERSION, "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "exploration_only_prior_site_audit_pending", "scope": "Mars regional ice-investigation candidates; no landing or extractability approval",
        "grid": {"step_deg": .5,"candidate_latitude_centres":[-59.75,59.75],"longitude_centres":[-179.75,179.75],"latitude_rationale":"native SWIM coverage, both hemispheres"},
        "counts": {"examined_grid_cells":len(frame),"finite_core_cells":int(frame.finite_core_descriptors.sum()),"positive_both_cells":int(frame.positive_both_ice_consistency.sum()),"exploratory_pool":len(pool),"pareto_front":len(front),"exploratory_candidates":len(chosen)},
        "pool_rule": "All six objective descriptors and TI/elevation finite, both SWIM depth-zone consistency descriptors >0, not old eight ice-candidate cells and not inside old project boxes. Sign>0 is an exploration choice, not calibrated presence/quantity or a mission threshold.",
        "objectives":OBJECTIVES,"weights":None,"scalar_score":None,"reference_population":"all exploratory-pool cells in this run, not all potential Mars landing sites",
        "selection_for_review":"union of front extremes and geographically separated examples; 5-degree rectangular display-diversity exclusion, not fixed km or engineering buffer; deliberately includes >=51N candidates, without marking prior-site audit as passed",
        "contexts_not_monotonic_objectives":["TES thermal inertia","MOLA absolute elevation","MCS adjusted temperature medians, contrast and populated-bin counts","dust seasonal profiles, maxima and reliability"],
        "full_data_accounting": {
            "terrain":"existing MOLA slope/relief plus newly extracted absolute elevation; regional means do not resolve hazards",
            "thermal":"TI kept separate from temperature; no preferred TI assumed",
            "water_ice":"both SWIM 2 depth ranges included; they share data and are not independent confirmations; cannot estimate ice content/depth",
            "dust":"MY34 and MY35 mean/p95/max/four Ls seasons/provider reliability and 610Pa-normalized context; no local wind/deposition/pressure inferred",
            "temperature":"MCS MY29–36 at native 5deg 03/15 LTST, model time-adjusted and QA/count/uncertainty absent; context only, no favourable ranking",
            "MEDA":"159418 rover-local records at already-known Jezero, no quality-qualified rows in existing report; inventoried but not transplanted to candidates",
            "unavailable":"local pressure/wind, material strength, mineralogy, independent ice truth, instrument-specific thresholds, local hazard and extraction readiness remain unknown"
        },
        "limits":["No novelty clearance: all candidates require bounded footprint and same-purpose literature audit.","The front depends on declared objectives and incomplete available products; non-dominated does not mean mission-optimal.","MOLA terrain variables and the two SWIM layers are correlated/shared-source evidence; variable count is not independent evidence count.","5deg MCS and 3deg reconstructed dust support are retained; interpolated 0.5deg columns do not increase native resolution.","Different product periods and footprints do not constitute one contemporaneous controlled experiment."],
        "sources":sources,"script_sha256":sha(Path(__file__)),
    }
    after = {r["path"]:sha(ROOT/r["path"]) for r in sources}
    if before != after:
        raise RuntimeError("Protected scientific input changed while run was active")
    method["protected_inputs_hashes_unchanged"] = True
    (OUT/"method.json").write_text(json.dumps(method,ensure_ascii=False,indent=2)+"\n")
    cols=["lat","lon","ice_shallow","ice_deep","slope","relief","thermal_inertia","elevation_mean_m_areoid","dust_my34_p95","dust_my35_p95","mcs_paired_bins","mcs_native_lat","mcs_native_lon","exploratory_reason"]
    print(json.dumps(method["counts"],indent=2))
    print(pd.DataFrame(chosen)[cols].to_string(index=False))


def native_crop(grid: xr.DataArray, lat: float, lon: float, half_width=.25) -> xr.DataArray:
    """Select native cell centres in half-open nominal lat/lon bounds, wrapping longitude."""
    delta = (grid.lon.values - lon + 180) % 360 - 180
    yi = np.flatnonzero((grid.lat.values >= lat-half_width) & (grid.lat.values < lat+half_width))
    xi = np.flatnonzero((delta >= -half_width) & (delta < half_width))
    return grid.isel(lat=yi,lon=xi)


def native_stats(grid: xr.DataArray, positive=False) -> dict:
    values = np.asarray(grid.values, dtype=float)
    good = np.isfinite(values)
    n, count = int(values.size), int(good.sum())
    if not count:
        return {"native_cells":n,"valid_cells":count,"valid_fraction":count/n if n else None,"mean":None,"min":None,"max":None}
    weights = np.broadcast_to(np.cos(np.deg2rad(grid.lat.values))[:,None], values.shape)
    result = {"native_cells":n,"valid_cells":count,"valid_fraction":count/n if n else None,
              "mean":float(np.average(values[good],weights=weights[good])),
              "median":float(np.median(values[good])),"min":float(values[good].min()),
              "max":float(values[good].max()),"std_population":float(values[good].std())}
    if positive:
        result["positive_cells"] = int((values[good]>0).sum())
        result["positive_fraction_of_valid"] = float((values[good]>0).mean())
    return result


def details(targets_path: Path | None = None) -> None:
    """Native-support checks for fixed review targets; no rescreen or novelty claim."""
    candidates = pd.read_csv(OUT/"exploratory_candidates.csv")
    if targets_path is not None:
        target_spec=json.loads(targets_path.read_text())
        targets=pd.DataFrame([{"review_id":key,**v} for key,v in target_spec.items()])
        candidates=targets.merge(candidates,on=["lat","lon"],how="left",validate="one_to_one")
        if candidates.ice_shallow.isna().any():raise ValueError("Fixed target must match a reviewed exploratory cell")
    else:
        candidates.insert(0,"review_id",[f"REVIEW-{i+1:02d}" for i in range(len(candidates))])
    protected=source_manifest()
    if targets_path is not None:
        protected.append({"path":targets_path.resolve().relative_to(ROOT).as_posix(),"bytes":targets_path.stat().st_size,"sha256":sha(targets_path)})
    dem = mars.load("mola_topography").astype("float32")
    ti_all = mars.load_thermal_inertia(keep_interpolated=True)
    ti = mars.load_thermal_inertia(keep_interpolated=False)
    ti_mask = mars.load("tes_thermal_inertia_night_mask")
    s0,s1 = swim.load("ice_consistency_shallow"),swim.load("ice_consistency_deep")
    source_path=ROOT/"data/raw/mars/temperature/mcs_corrected/MCS_tsurf_corrected.nc"
    result=[];dust_tables=[];mcs_tables=[];metrics=[]
    with xr.open_dataset(source_path) as mcs:
        for i,r in candidates.iterrows():
            lat,lon=float(r.lat),float(r.lon)
            identifier=str(r.review_id)
            # A halo makes the central finite differences independent of this crop's outer edge.
            halo=native_crop(dem,lat,lon,half_width=1.0)
            slope=native_crop(slope_deg(halo,mars.MARS_RADIUS_M),lat,lon)
            topo=native_crop(dem,lat,lon)
            record={"review_id":identifier,"center":{"lat":lat,"lon":lon},
              "review_role":str(r.get("review_role","exploratory_example")),
              "coordinate_convention":"Mars planetocentric latitude, east-positive longitude [-180,180)",
              "nominal_cell_bounds":{"south":lat-.25,"north":lat+.25,"west":lon-.25,"east":lon+.25},
              "nominal_size_km_NS_EW": [float(np.pi*mars.MARS_RADIUS_M/180*.5/1000),float(np.pi*mars.MARS_RADIUS_M/180*.5*np.cos(np.deg2rad(lat))/1000)],
              "native_support_rule":"native cell centres inside half-open bounds; longitude wraps; no inferred continuous coverage or drilling footprint",
              "mola_elevation_m_areoid":native_stats(topo),
              "mola_slope_deg_3p7km_baseline":native_stats(slope),
              "mola_relief_m":float(topo.max()-topo.min()),
              "tes_TI_native_excluding_infill":native_stats(native_crop(ti,lat,lon)),
              "tes_TI_native_including_infill":native_stats(native_crop(ti_all,lat,lon)),
              "tes_mask_zero_native_cells":int((native_crop(ti_mask,lat,lon)==0).sum()),
              "swim_0_1m_native":native_stats(native_crop(s0,lat,lon),positive=True),
              "swim_1_5m_native":native_stats(native_crop(s1,lat,lon),positive=True),
              "stack_descriptors":{key:float(r[key]) for key in ["slope","relief","thermal_inertia","ice_shallow","ice_deep","elevation_mean_m_areoid"]},
              "dust":{},"MCS_context":None,"novelty_status":"pending_bounded_prior_site_audit",
              "engineering_requirement_status":"not_validated; local ice truth, wind/pressure, material, hazards and equipment limits unknown"}
            record["stack_minus_native"]={
                "slope_deg":float(r.slope)-record["mola_slope_deg_3p7km_baseline"]["mean"],
                "relief_m":float(r.relief)-record["mola_relief_m"],
                "thermal_inertia":float(r.thermal_inertia)-record["tes_TI_native_excluding_infill"]["mean"],
                "ice_shallow":float(r.ice_shallow)-record["swim_0_1m_native"]["mean"],
                "ice_deep":float(r.ice_deep)-record["swim_1_5m_native"]["mean"],
                "interpretation":"Stack MOLA/TES coarsening and SWIM coarsened-then-interpolated descriptors differ from cosine-weighted native grid centres in the nominal cell; use the native evidence for final cards, not silent substitution."}
            for year in ["dust_my34","dust_my35"]:
                site=dust.load_site_series(lat,lon,year)
                record["dust"][year]=summarize_dust(site)
                table=pd.DataFrame({key:site[key].values for key in ["Time","SOY","Ls","cdodtot","cdod610","cdodrel"]})
                table.insert(0,"year",year);table.insert(0,"review_id",identifier)
                dust_tables.append(table)
            context=extract_context(mcs,lat,lon)
            series=context.pop("series")
            record["MCS_context"]=context
            table=pd.DataFrame(series);table.insert(0,"review_id",identifier);mcs_tables.append(table)
            result.append(record)
            flat={"candidate_id":identifier,"review_role":record["review_role"],"lat":lat,"lon_east_minus180_180":lon,"lon_east_0_360":lon%360,
                  "status":"detailed_data_review_only_novelty_audit_pending",
                  "north_south_km":record["nominal_size_km_NS_EW"][0],"east_west_km":record["nominal_size_km_NS_EW"][1],
                  "mola_relief_m":record["mola_relief_m"],"tes_mask_zero_cells":record["tes_mask_zero_native_cells"]}
            for key,group in [("mola_elevation_m",record["mola_elevation_m_areoid"]),("mola_slope_deg",record["mola_slope_deg_3p7km_baseline"]),("TES_TI",record["tes_TI_native_excluding_infill"]),("SWIM_0_1m",record["swim_0_1m_native"]),("SWIM_1_5m",record["swim_1_5m_native"])]:
                for k,v in group.items():flat[f"{key}_{k}"]=v
            for key,value in record["stack_descriptors"].items():flat[f"stack_{key}"]=value
            for year,group in record["dust"].items():
                for k in ["mean_cdodtot","p95_cdodtot","max_cdodtot","peak_sol_of_year","peak_Ls_deg","valid_reconstructed_sols","expected_reconstructed_sols","native_cell_lat","native_cell_lon","reliability_mean"]:flat[f"{year}_{k}"]=group[k]
                for season,values in group["seasons_by_Ls"].items():flat[f"{year}_Ls{season}_mean"]=values["mean_cdodtot"]
                # Same native selection as global dust screening; finite year support must agree.
                assert np.isclose(group["p95_cdodtot"],r[f"{year}_p95"],atol=1e-7)
            for k in ["valid_day_bins","valid_night_bins","paired_bins","expected_year_season_pairs","paired_contrast_median_K"]:flat[f"MCS_{k}"]=context[k]
            for k in ["lat","lon"]:flat[f"MCS_native_{k}"]=context["selected_grid_coordinate"][k]
            night=[x["night_03_K"] for x in series if x["night_03_K"] is not None]
            day=[x["day_15_K"] for x in series if x["day_15_K"] is not None]
            flat["MCS_populated_night_median_K"]=float(np.median(night)) if night else None
            flat["MCS_populated_day_median_K"]=float(np.median(day)) if day else None
            assert context["paired_bins"]==int(r.mcs_paired_bins)
            metrics.append(flat)
    changed=[s["path"] for s in protected if sha(ROOT/s["path"])!=s["sha256"]]
    if changed:raise RuntimeError(f"Protected inputs changed: {changed}")
    package={"version":VERSION,"scope":"Fixed detailed-review targets; review roles in each record, not novelty clearance",
             "units_periods_and_support":{
                 "MOLA":{"elevation":"m relative to areoid","slope":"degrees at about 3.7 km baseline","relief":"m within nominal 0.5 degree native-grid-centre footprint","period":"MGS mapping; exact source dates in PDS labels"},
                 "TES":{"thermal_inertia":"J m-2 K-1 s-0.5","period":"input PDS label has no observation start/end; 2007 is product creation, not observation year","mask":"original mask==0 infill pixels excluded from primary result"},
                 "SWIM":{"both_zones":"dimensionless ice consistency -1..1; not fraction/probability/depth truth","version":"SWIM2 2021 products; composite multi-instrument/time support","dependence":"two depth-zone maps share sources and are not independent evidence"},
                 "dust":{"years":["MY34","MY35"],"period":"669 reconstructed equally spaced sols per year","quantity":"local-column 9.3 micron absorption optical depth; dimensionless","native_grid_deg":[3,3],"cdod610":"610 Pa-normalized optical depth is not local pressure"},
                 "MCS":{"years":[29,36],"MY_Ls_possible_pairs":288,"nominal_times_LTST":[3,15],"grid_deg":[5,5],"temperature":"K from paper/author code, absent NetCDF units attribute","status":"context-only model-time-adjusted; QA, counts, uncertainties absent; populated-bin medians not full-year mean or daily amplitude"},
                 "coordinate_model":{"Mars_radius_m":mars.MARS_RADIUS_M,"cell":"0.5 degree nominal lat/lon cell, not landing ellipse/drill site","native_summary":"cos(latitude)-weighted mean over included native grid centres; no interpolation for primary native checks"}},
             "protected_inputs_hashes_unchanged":True,"sources":protected,"script_sha256":sha(Path(__file__)),"records":result}
    (OUT/"candidate_native_evidence.json").write_text(json.dumps(package,ensure_ascii=False,indent=2)+"\n")
    pd.DataFrame(metrics).to_csv(OUT/"candidate_metrics.csv",index=False)
    pd.concat(dust_tables,ignore_index=True).to_csv(OUT/"candidate_dust_series.csv.gz",index=False,compression={"method":"gzip","mtime":0})
    pd.concat(mcs_tables,ignore_index=True).to_csv(OUT/"candidate_mcs_bins.csv.gz",index=False,compression={"method":"gzip","mtime":0})
    print(json.dumps({"native_candidates":len(result),"dust_rows":sum(map(len,dust_tables)),"MCS_bins":sum(map(len,mcs_tables)),"protected_inputs_unchanged":True},indent=2))
    print(pd.DataFrame(metrics)[["candidate_id","lat","lon_east_0_360","mola_slope_deg_mean","mola_relief_m","TES_TI_valid_fraction","TES_TI_mean","SWIM_0_1m_mean","SWIM_1_5m_mean","MCS_paired_bins"]].to_string(index=False))


def validate_outputs() -> None:
    """Independent output/provenance checks, including brute-force front dominance."""
    method=json.loads((OUT/"method.json").read_text())
    evidence=json.loads((OUT/"candidate_native_evidence.json").read_text())
    metrics=pd.read_csv(OUT/"candidate_metrics.csv")
    pool=pd.read_csv(OUT/"screened_pool.csv.gz")
    front=pd.read_csv(OUT/"pareto_front.csv.gz")
    ds=pd.read_csv(OUT/"candidate_dust_series.csv.gz")
    ms=pd.read_csv(OUT/"candidate_mcs_bins.csv.gz")
    checks={
        "final_script_hash_chain_matches":method["script_sha256"]==evidence["script_sha256"]==sha(Path(__file__)),
        "all_protected_input_hashes_match":all(sha(ROOT/r["path"])==r["sha256"] for r in evidence["sources"]),
        "global_candidate_coordinates_unique":not pool.duplicated(["lat","lon"]).any(),
        "native_fixed_IDs_and_coordinates_match":set(metrics.candidate_id)=={r["review_id"] for r in evidence["records"]} and len(metrics)==len(evidence["records"]),
        "native_full_ice_data_support":all(r["swim_0_1m_native"]["valid_cells"]==100 and r["swim_1_5m_native"]["valid_cells"]==100 for r in evidence["records"]),
        "TES_excludes_infilled_cells":all(r["tes_TI_native_excluding_infill"]["valid_cells"]+r["tes_mask_zero_native_cells"]==100 for r in evidence["records"]),
        "dust_669_sols_per_candidate_year":len(ds)==len(metrics)*2*669 and ds.groupby(["review_id","year"]).size().eq(669).all(),
        "dust_unique_candidate_year_time":not ds.duplicated(["review_id","year","Time"]).any(),
        "MCS_288_bins_per_candidate":len(ms)==len(metrics)*288 and ms.groupby("review_id").size().eq(288).all(),
        "MCS_unique_candidate_MY_Ls":not ms.duplicated(["review_id","mars_year","Ls_coordinate_deg"]).any(),
        "MCS_pair_contrast_exact_same_bin":np.allclose((ms.day_15_K-ms.night_03_K).dropna(),ms.sampled_contrast_K.dropna(),atol=1e-10),
        "native_summary_and_series_agree":True,
    }
    for r in evidence["records"]:
        subset=ms[ms.review_id==r["review_id"]];context=r["MCS_context"]
        checks["native_summary_and_series_agree"] &= (int(subset.day_15_K.notna().sum())==context["valid_day_bins"] and int(subset.night_03_K.notna().sum())==context["valid_night_bins"] and int(subset.sampled_contrast_K.notna().sum())==context["paired_bins"] and np.isclose(subset.sampled_contrast_K.median(),context["paired_contrast_median_K"]))
        for year in ["dust_my34","dust_my35"]:
            subset=ds[(ds.review_id==r["review_id"])&(ds.year==year)];s=r["dust"][year]
            checks["native_summary_and_series_agree"] &= np.isclose(subset.cdodtot.mean(),s["mean_cdodtot"]) and np.isclose(subset.cdodtot.quantile(.95),s["p95_cdodtot"]) and np.isclose(subset.cdodtot.max(),s["max_cdodtot"])
    keys=list(OBJECTIVES);sign=np.array([-1 if OBJECTIVES[k]=="maximize" else 1 for k in keys]);values=pool[keys].to_numpy()*sign
    nondominated=True
    for row in front[keys].to_numpy()*sign:
        if np.any(np.all(values<=row,axis=1)&np.any(values<row,axis=1)):
            nondominated=False
            break
    checks["all_front_points_bruteforce_nondominated"]=nondominated
    checks={k:bool(v) for k,v in checks.items()}
    validation={"scope":"File, provenance, geometry, finite support and numerical reproduction; not science validity, originality, ice truth or mission approval","checks":checks,"status":"PASS" if all(checks.values()) else "FAIL","counts":{"pool":len(pool),"front":len(front),"native_targets":len(metrics),"dust_rows":len(ds),"MCS_rows":len(ms)},"script_sha256":sha(Path(__file__)),"protected_input_hashes_unchanged":checks["all_protected_input_hashes_match"]}
    (OUT/"numerical_validation.json").write_text(json.dumps(validation,indent=2)+"\n")
    print(json.dumps(validation,indent=2))
    if not all(checks.values()):raise RuntimeError("Numerical output validation failed")


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--details",action="store_true",help="Only extract native support for the existing exploratory-candidate table")
    p.add_argument("--finalize-targets",type=Path,help="JSON mapping fixed review IDs to lat/lon; name does not imply novelty clearance")
    p.add_argument("--validate",action="store_true",help="Read back all produced outputs and validate provenance, support, series and Pareto front")
    args=p.parse_args()
    if args.validate:validate_outputs()
    elif args.finalize_targets:details(args.finalize_targets)
    elif args.details:details()
    else:build()
