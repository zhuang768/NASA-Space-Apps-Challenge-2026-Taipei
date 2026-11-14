"""MS-02 value cross-check and simple geometry/unit calculations.

Reads only committed hand-off files, writes outputs/research/MS-02/verification.json.
No scoring, no weights, no "similarity percentage" is computed.
Run from the repo root:  python3 -I scripts/research/ms02_earth_analogs/verify_ms02.py
"""
import csv, gzip, json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
RES = ROOT / "outputs/research/mars_reselection_20261114"
OUT = ROOT / "outputs/research/MS-02"
OUT.mkdir(parents=True, exist_ok=True)

MARS_R_M = 3396000.0  # radius used by the hand-off evidence file (coordinate_model)
EARTH_R_M = 6371000.0


def gc_km(lat1, lon1, lat2, lon2, r):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a)) / 1000.0


def dms(d, m, hemi):
    v = d + m / 60.0
    return -v if hemi in "SW" else v


# --- 1. read MS-02 from three hand-off sources -------------------------------
with open(RES / "final_candidates.csv", newline="", encoding="utf-8") as f:
    final = next(r for r in csv.DictReader(f) if r["candidate_id"] == "MS-02")

with gzip.open(RES / "screened_pool.csv.gz", "rt") as f:
    rdr = csv.DictReader(f)
    pool_n = 0
    pool = None
    for r in rdr:
        pool_n += 1
        if abs(float(r["lat"]) - 52.75) < 1e-9 and abs(float(r["lon"]) - 168.25) < 1e-9:
            pool = r

native = next(r for r in json.load(open(RES / "candidate_native_evidence.json"))["records"]
              if r["review_id"] == "D")

checks = []


def chk(name, a, b, tol, note=""):
    a, b = float(a), float(b)
    checks.append({"item": name, "source_a": a, "source_b": b, "abs_diff": abs(a - b),
                   "tolerance": tol, "pass": abs(a - b) <= tol, "note": note})


# same quantity, different sources (coarse stack vs native-cell stats are different
# quantities by design; those are reported as "expected_difference" not as failures)
chk("lat", final["lat"], native["center"]["lat"], 0)
chk("lon_east", final["lon_east_0_360"], native["center"]["lon"], 0)
chk("mola_relief_m final_vs_pool", final["mola_relief_m"], pool["relief"], 0)
chk("SWIM_0_1m stack final_vs_pool", final["stack_ice_shallow"], pool["ice_shallow"], 1e-9)
chk("SWIM_1_5m stack final_vs_pool", final["stack_ice_deep"], pool["ice_deep"], 1e-9)
chk("dust_my34_p95 final_vs_pool", final["dust_my34_p95_cdodtot"], pool["dust_my34_p95"], 1e-9)
chk("dust_my35_p95 final_vs_pool", final["dust_my35_p95_cdodtot"], pool["dust_my35_p95"], 1e-9)
chk("dust_my34_mean final_vs_pool", final["dust_my34_mean_cdodtot"], pool["dust_my34_mean"], 1e-6,
    "pool stores float32")
chk("dust_my35_mean final_vs_pool", final["dust_my35_mean_cdodtot"], pool["dust_my35_mean"], 1e-6,
    "pool stores float32")
chk("MCS night median K final_vs_pool", final["MCS_populated_night_median_K"], pool["mcs_night_median_K"], 1e-9)
chk("MCS day median K final_vs_pool", final["MCS_populated_day_median_K"], pool["mcs_day_median_K"], 1e-9)
chk("MCS paired contrast K final_vs_pool", final["MCS_paired_contrast_median_K"], pool["mcs_paired_contrast_median_K"], 1e-9)
chk("TES TI native-vs-final", final["TES_TI_mean"], native["tes_TI_native_excluding_infill"]["mean"], 1e-9)
chk("MOLA slope native-vs-final", final["mola_slope_deg_mean"], native["mola_slope_deg_3p7km_baseline"]["mean"], 1e-9)

expected_diff = {
    "TES_TI coarse stack vs native-cell mean (excl. infill)": {
        "stack": float(final["stack_thermal_inertia"]), "native_mean": float(final["TES_TI_mean"]),
        "diff": float(final["stack_thermal_inertia"]) - float(final["TES_TI_mean"]),
        "why": "stack is a 0.5-degree coarsened product; native value averages 93 non-infill cells (hand-off README discloses this)"},
    "MOLA slope coarse stack vs native-cell mean": {
        "stack": float(final["stack_slope"]), "native_mean": float(final["mola_slope_deg_mean"]),
        "diff": float(final["stack_slope"]) - float(final["mola_slope_deg_mean"]),
        "why": "different aggregation scale"},
    "SWIM_1_5m stack vs native-cell mean": {
        "stack": float(final["stack_ice_deep"]), "native_mean": float(final["SWIM_1_5m_mean"]),
        "diff": float(final["stack_ice_deep"]) - float(final["SWIM_1_5m_mean"]),
        "why": "different aggregation scale"},
}

# --- 2. geometry (this-study calculations) ------------------------------------
c_lat, c_lon = 52.75, 168.25
deg_km_mars = math.pi * MARS_R_M / 180 / 1000
geom = {
    "mars_km_per_degree": deg_km_mars,
    "nominal_NS_km_from_bounds": 0.5 * deg_km_mars,
    "nominal_EW_km_at_center_lat": 0.5 * deg_km_mars * math.cos(math.radians(c_lat)),
    "dust_cell_center_(52.5,168.0)_distance_km": gc_km(c_lat, c_lon, 52.5, 168.0, MARS_R_M),
    "mcs_bin_center_(55.0,170.0)_distance_km": gc_km(c_lat, c_lon, 55.0, 170.0, MARS_R_M),
    "mcs_bin_note": "5-degree MCS bin center is ~2.25 deg north of MS-02: a regional background, not a site value",
}

earth = {
    "E01_UniversityValley": {"lat": dms(77, 52, "S"), "lon": dms(160, 45, "E"), "src": "Marinova 2022 p.145 (valley); met station 77deg51.729'S 160deg42.606'E p.146"},
    "E03_Adventdalen_ADE": {"lat": 78.1722, "lon": 16.0613, "src": "Rotem 2023 (valley terrace site ADE)"},
    "E04_Haughton_p6_DMS": {"lat": dms(75, 22, "N"), "lon": dms(89, 41, "W"), "src": "Andres 2020 sec.1.2.2 p.6"},
    "E04_Haughton_fig1.8": {"lat": 75.37, "lon": -89.53, "src": "Andres 2020 Fig 1.8 p.20"},
}
d = earth["E04_Haughton_p6_DMS"], earth["E04_Haughton_fig1.8"]
earth["E04_coordinate_discrepancy_km"] = gc_km(d[0]["lat"], d[0]["lon"], d[1]["lat"], d[1]["lon"], EARTH_R_M)
# unit conversions used in the report (this-study calculation, Kelvin = Celsius + 273.15)
earth["unit_conversions_K"] = {
    "UV_MAAT_-23.4C": -23.4 + 273.15, "UV_42cm_-24.1C": -24.1 + 273.15,
    "Svalbard_Polygons_MAAT_-5.8C": -5.8 + 273.15, "Devon_MAAT_-16C": -16 + 273.15,
    "UV_SpecialRegion_threshold_255K_as_C": 255 - 273.15,
    "UV_2560h_fraction_of_year": 2560 / 8760,
}
for name, v in earth.items():
    if isinstance(v, dict) and "lat" in v:
        v["lat_abs_deg"] = abs(v["lat"])

result = {
    "script": "scripts/research/ms02_earth_analogs/verify_ms02.py",
    "inputs": [str((RES / "final_candidates.csv").relative_to(ROOT)),
               str((RES / "screened_pool.csv.gz").relative_to(ROOT)),
               str((RES / "candidate_native_evidence.json").relative_to(ROOT))],
    "screened_pool_rows": pool_n,
    "all_consistency_checks_pass": all(c["pass"] for c in checks),
    "checks": checks,
    "expected_scale_differences_not_errors": expected_diff,
    "geometry": geom,
    "earth_coordinates_and_conversions": earth,
    "not_computed": "no weights, no composite score, no 'most Mars-like' percentage",
}
(OUT / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("pool rows", pool_n, "| all pass:", result["all_consistency_checks_pass"])
for c in checks:
    print(("OK  " if c["pass"] else "FAIL"), c["item"], c["abs_diff"])
print(json.dumps(geom, indent=1))
print(json.dumps({k: v for k, v in earth.items() if k.startswith("E04_coord") or k == "unit_conversions_K"}, indent=1))
