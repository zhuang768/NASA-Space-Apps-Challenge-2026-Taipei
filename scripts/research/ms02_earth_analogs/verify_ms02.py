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
    "E04_Haughton_structure_center_p6": {"lat": dms(75, 22, "N"), "lon": dms(89, 41, "W"), "src": "Andres 2020 sec.1.2.2 p.6 (impact structure)"},
    "E04_HRV_study_area_fig1.8": {"lat": 75.37, "lon": -89.53, "src": "Andres 2020 Fig 1.8 p.20 / p.1 (Haughton River Valley study area)"},
}
d1, d2 = earth["E04_Haughton_structure_center_p6"], earth["E04_HRV_study_area_fig1.8"]
earth["E04_structure_center_to_HRV_study_area_km"] = gc_km(d1["lat"], d1["lon"], d2["lat"], d2["lon"], EARTH_R_M)


def utm_inverse(E, N, lon0_deg):
    """Inverse UTM (northern hemisphere), WGS84, Kruger series. This-study calculation."""
    a_, f_, k0, E0 = 6378137.0, 1 / 298.257223563, 0.9996, 500000.0
    n = f_ / (2 - f_)
    A = a_ / (1 + n) * (1 + n**2 / 4 + n**4 / 64)
    b = [n/2 - 2*n**2/3 + 37*n**3/96 - n**4/360, n**2/48 + n**3/15 - 437*n**4/1440,
         17*n**3/480 - 37*n**4/840, 4397*n**4/161280]
    dd = [2*n - 2*n**2/3 - 2*n**3, 7*n**2/3 - 8*n**3/5, 56*n**3/15]
    xi, eta = N / (k0 * A), (E - E0) / (k0 * A)
    xi_p = xi - sum(b[j] * math.sin(2*(j+1)*xi) * math.cosh(2*(j+1)*eta) for j in range(4))
    eta_p = eta - sum(b[j] * math.cos(2*(j+1)*xi) * math.sinh(2*(j+1)*eta) for j in range(4))
    chi = math.asin(math.sin(xi_p) / math.cosh(eta_p))
    lat = chi + sum(dd[j] * math.sin(2*(j+1)*chi) for j in range(3))
    lon = math.radians(lon0_deg) + math.atan2(math.sinh(eta_p), math.cos(xi_p))
    return math.degrees(lat), math.degrees(lon)


# Andres 2020 Table 3.1: LiDAR grids, UTM zone 16N (central meridian -87), "Lat"=northing, "Long"=easting
HAUGHTON_GRIDS = {"16A": (428554, 8367099), "16C": (428529, 8367504), "16D": (428565, 8367644),
                  "16K": (428257, 8365195), "16L": (428525, 8365174), "16N": (428803, 8366051),
                  "16AD": (427651, 8369103), "StoneStripes": (425145, 8365883),
                  "EastCampPolygons": (429239, 8366440)}
conv = {k: dict(zip(("lat", "lon"), utm_inverse(E, N, -87))) for k, (E, N) in HAUGHTON_GRIDS.items()}
lats = [v["lat"] for v in conv.values()]
lons = [v["lon"] for v in conv.values()]
earth["E04_LiDAR_grids_latlon_from_UTM16N_Table3.1"] = {
    "grids": conv,
    "lat_range": [min(lats), max(lats)], "lon_range": [min(lons), max(lons)],
    "ns_extent_km": gc_km(min(lats), lons[0], max(lats), lons[0], EARTH_R_M),
    "ew_extent_km_at_mean_lat": gc_km(sum(lats)/len(lats), min(lons), sum(lats)/len(lats), max(lons), EARTH_R_M),
    "note": "grids agree with Fig 1.8 (75.37N, -89.53) to ~0.01-0.1 deg; the p.6 coordinate is the impact-structure centre, a different anchor"}
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
print(json.dumps({k: v for k, v in earth.items() if k.startswith("E04_structure") or k.startswith("E04_LiDAR") or k == "unit_conversions_K"}, indent=1))
