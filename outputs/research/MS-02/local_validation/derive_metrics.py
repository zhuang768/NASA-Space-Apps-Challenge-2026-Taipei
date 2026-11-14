#!/usr/bin/env python3
"""MS-02 local_validation: derived numbers + context figure. Inputs: main hand-off table (final_candidates.csv),
known_ice_points_morgan2025.csv. Study extents are the bounds quoted in each source (see local_prior_work.csv).
Run from repo root: python3 outputs/research/MS-02/local_validation/derive_metrics.py"""
import csv, json, math, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent
RM = 3396.0   # km, same radius as the hand-off cell sizes
LAT, LON = 52.75, 168.25
def hav(a, b, c, d, R=RM):
    a, b, c, d = map(math.radians, (a, b, c, d))
    x = math.sin((c-a)/2)**2 + math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 2*R*math.asin(math.sqrt(x))
def dist_to_box(lat, lon, s, n, w, e):
    """great-circle distance (km) from a point to the nearest point of a lat/lon box; 0 if inside.
    nearest point approximated by clamping lat/lon (adequate for boxes tens of degrees wide)."""
    la = min(max(lat, s), n); lo = min(max(lon, w), e)
    return hav(lat, lon, la, lo)
rows = list(csv.DictReader(open(ROOT/"outputs/research/mars_reselection_20261114/final_candidates.csv", encoding="utf-8-sig")))
r = next(x for x in rows if x["candidate_id"] == "MS-02")
f = lambda k: float(r[k])
half = 150.0
strip_half_deg = half/(2*math.pi*RM/360*math.cos(math.radians(LAT)))
boxes = {   # name: (south, north, west, east, basis)
 "Bramson2015_CTX_search": (38, 50, 180, 225, "Sec.2 p.3 'between 180-225E and 38-50N' (one tabulated crater at 53.17N)"),
 "Viola2015_region":       (35, 65, 180, 240, "Sec.4 Fig.4 '35-65N, 180-240E'"),
 "Ramsdale2019_strip":     (30, 80, 190-strip_half_deg, 190+strip_half_deg, "300 km strip centred on 170W (=190E); exact longitude limits not stated -> 150 km half-width at 52.75N, this-study calc"),
 "Sejourne2019_strip":     (30, 80, 90-strip_half_deg, 90+strip_half_deg, "~300 km strip centred ~90E (Sec.1); this-study calc of edge"),
 "Pathare_Arcadia_box":    (36, 56, 184, 228, "arXiv:1705.05556 Sec.4.2.3 Fig.17 '36-56N, 132-176W'"),
}
dist = {k: round(dist_to_box(LAT, LON, *v[:4]), 1) for k, v in boxes.items()}
gaz = (33.9, 64.2, 165.9, 210.4)
mc7 = (30, 65, 120, 180)
out = {
 "cell_centre": [LAT, LON],
 "cell_size_km": [round(2*math.pi*RM/360*0.5*math.cos(math.radians(LAT)), 3), round(2*math.pi*RM/360*0.5, 3)],
 "distance_cell_centre_to_study_extent_km": dist,
 "strip_half_width_deg_at_52.75N": round(strip_half_deg, 3),
 "inside_Arcadia_Planitia_bbox_wikipedia_secondary": gaz[0] <= LAT <= gaz[1] and gaz[2] <= LON <= gaz[3],
 "km_to_west_edge_of_that_bbox_along_parallel": round((LON-gaz[2])*2*math.pi*RM/360*math.cos(math.radians(LAT)), 1),
 "inside_MC7_Cebrenia_quadrangle": mc7[0] <= LAT <= mc7[1] and mc7[2] <= LON <= mc7[3],
 "km_to_MC7_east_edge_180E_along_parallel": round((180-LON)*2*math.pi*RM/360*math.cos(math.radians(LAT)), 1),
}
ice = list(csv.DictReader(open(ROOT/"outputs/research/mars_reselection_20261114/known_ice_points_morgan2025.csv")))
nn = sorted((hav(LAT, LON, float(x["lat"]), float(x["lonE"])), x["site"]) for x in ice)[:3]
out["morgan2025_nearest_3_km"] = [[round(d, 1), s] for d, s in nn]
# footprint ratios
cell_area = out["cell_size_km"][0]*out["cell_size_km"][1]
mons_area = math.pi*(550/2)**2
out["cell_area_km2"] = round(cell_area, 1)
out["MONS_550km_FWHM_circle_area_km2"] = round(mons_area)
out["cell_fraction_of_MONS_FWHM_circle"] = round(cell_area/mons_area, 5)
out["Piqueux2019_pixel_deg"] = 0.5
# SWIM discreteness (assumption flagged)
m15 = f("SWIM_1_5m_mean")
out["SWIM_1_5m"] = {"min": f("SWIM_1_5m_min"), "median": f("SWIM_1_5m_median"), "max": f("SWIM_1_5m_max"), "mean": m15,
  "share_at_max_if_only_two_values_0.5_and_1.0": round((m15-0.5)/0.5, 4),
  "cells_at_1.0_if_only_two_values_of_100": round((m15-0.5)/0.5*100, 1),
  "assumption": "only two distinct values (0.5, 1.0); NOT verified, per-cell grid not available locally"}
out["SWIM_0_1m"] = {"min": f("SWIM_0_1m_min"), "median": f("SWIM_0_1m_median"), "max": f("SWIM_0_1m_max"), "mean": f("SWIM_0_1m_mean"),
  "note": "median == min -> at least half of the 100 cells share the minimum value"}
out["native_cell_spacing_deg_inferred"] = round(0.5/math.sqrt(100), 3)
out["TES_TI"] = {"mean": f("TES_TI_mean"), "median": f("TES_TI_median"), "min": f("TES_TI_min"), "max": f("TES_TI_max"), "std": round(f("TES_TI_std_population"), 3),
  "valid": int(f("TES_TI_valid_cells")), "native": int(f("TES_TI_native_cells")), "mask_zero_excluded": int(f("tes_mask_zero_cells"))}
out["MOLA"] = {"mean_m": round(f("mola_elevation_m_mean"), 3), "min_m": f("mola_elevation_m_min"), "max_m": f("mola_elevation_m_max"), "relief_m": f("mola_relief_m"),
  "slope_mean_deg": round(f("mola_slope_deg_mean"), 4), "slope_max_deg": round(f("mola_slope_deg_max"), 4), "cells": int(f("mola_slope_deg_native_cells"))}
out["CDOD"] = {"MY34_mean": round(f("dust_my34_mean_cdodtot"), 6), "MY34_p95": round(f("dust_my34_p95_cdodtot"), 6), "MY35_mean": round(f("dust_my35_mean_cdodtot"), 6),
  "MY35_p95": round(f("dust_my35_p95_cdodtot"), 6), "native_cell": [f("dust_my34_native_cell_lat"), f("dust_my34_native_cell_lon")],
  "note": "3 deg grid, 9.3 um absorption column; not convertible to ground cover accumulation"}
# University Valley anchors (Earth, R=6371 km)
uv_valley = (-77.8667, 160.75); uv_w = (-77.86215, 160.7101)
out["UV_valley_anchor_to_W_station_km"] = round(hav(*uv_valley, *uv_w, R=6371.0), 3)
out["CS1_to_ADE_km"] = round(hav(78.201, 15.84, 78.1722, 16.0613, R=6371.0), 3)
(HERE/"derived_metrics.json").write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1)[:2500])
# figure
try:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=160)
    C = {"b": "#1b6ca8", "o": "#c75b12", "g": "#3a7d44", "p": "#7a4fa3", "k": "#222222"}
    def rect(s, n, w, e, col, ls, label, lab_xy, fill=0.07):
        ax.add_patch(Rectangle((w, s), e-w, n-s, fill=True, facecolor=col, alpha=fill, edgecolor="none"))
        ax.add_patch(Rectangle((w, s), e-w, n-s, fill=False, edgecolor=col, linestyle=ls, linewidth=1.6))
        ax.text(*lab_xy, label, color=col, fontsize=8, va="top")
    rect(30, 65, 120, 180, C["k"], ":", "", (121, 64.3))
    rect(33.9, 64.2, 165.9, 210.4, C["g"], "--", "", (166.8, 36.2), 0.05)
    rect(35, 65, 180, 240, C["p"], "-", "", (0, 0), 0.0)
    
    rect(38, 50, 180, 225, C["o"], "-", "", (197, 49.4), 0.12)
    s_, n_, w_, e_ = boxes["Ramsdale2019_strip"][:4]
    rect(s_, n_, w_, e_, C["b"], "-", "", (w_+9, 78.5), 0.12)
    s_, n_, w_, e_ = boxes["Sejourne2019_strip"][:4]
    rect(s_, n_, w_, e_, C["b"], "-", "", (e_+1.5, 78.5), 0.12)
    ax.plot([x["lonE"] for x in []], [])
    ax.scatter([float(x["lonE"]) for x in ice if 85 <= float(x["lonE"]) <= 245 and 30 <= float(x["lat"]) <= 80],
               [float(x["lat"]) for x in ice if 85 <= float(x["lonE"]) <= 245 and 30 <= float(x["lat"]) <= 80],
               s=14, color=C["k"], marker="o", label="Morgan 2025 Table 2 ice-exposure points", zorder=5)
    ax.scatter([LON], [LAT], s=140, marker="*", color="#d11f1f", edgecolor="white", linewidth=0.8, zorder=6, label="MS-02 cell (52.75N, 168.25E)")
    ax.text(96, 56, "Sejourne 2019\nstrip (approx.)", color=C["b"], fontsize=7.5)
    ax.text(196.5, 72, "Ramsdale 2019\ngrid strip (approx.)", color=C["b"], fontsize=7.5)
    ax.annotate("MS-02", (LON, LAT), (LON-14, LAT+9), fontsize=9, color="#d11f1f", arrowprops=dict(arrowstyle="-", color="#d11f1f", lw=0.8))
    ax.set_xlim(85, 245); ax.set_ylim(30, 80)
    ax.set_xlabel("East longitude (deg, planetocentric)"); ax.set_ylabel("Latitude (deg N)")
    ax.set_title("MS-02 cell vs. extents of prior ice studies (extents as quoted by each source)", fontsize=10)
    from matplotlib.lines import Line2D
    hs, ls_ = ax.get_legend_handles_labels()
    hs += [Line2D([0],[0],color=C["k"],ls=":",lw=1.6), Line2D([0],[0],color=C["g"],ls="--",lw=1.6), Line2D([0],[0],color=C["p"],lw=1.6), Line2D([0],[0],color=C["o"],lw=1.6)]
    ls_ += ["MC-7 Cebrenia quadrangle 30-65N 120-180E", "Arcadia Planitia bbox 33.9-64.2N 165.9-210.4E (secondary source)", "Viola 2015: 35-65N 180-240E", "Bramson 2015 CTX search: 38-50N 180-225E"]
    ax.grid(alpha=0.25); ax.legend(hs, ls_, loc="upper center", bbox_to_anchor=(0.43, 0.995), fontsize=7.5, framealpha=0.95)
    fig.tight_layout(); fig.savefig(HERE/"fig_local_prior_work_extents.png"); print("figure ok")
except Exception as e:
    print("figure skipped:", e)
