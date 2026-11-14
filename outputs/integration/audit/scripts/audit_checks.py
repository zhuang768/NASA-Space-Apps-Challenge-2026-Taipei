#!/usr/bin/env python3
"""Final-round evidence audit checks for Team zasa (MS-01 PR #8, MS-02 PR #6, MS-03 PR #7).

Read-only with respect to the audited trees. Writes outputs/integration/audit/checks.json.

Usage (from the audit worktree root):
  python3 outputs/integration/audit/scripts/audit_checks.py \
      --repo <git repo containing the objects> \
      --main <dir checked out at origin/main> --ms01 <dir @ PR8 head> \
      --ms02 <dir @ PR6 head> --ms03 <dir @ PR7 head>

No network access. No scoring, no weights, no similarity percentage is computed.
"""
import argparse, csv, gzip, hashlib, json, math, pathlib, platform, re, subprocess, sys

EXPECTED = {
    "main": "3cc8488577535e2fa4d146021fde51f8ff6cc667",
    "handoff": "f7076c9fdc77e00244ed5d6863aad2bf78cfa28f",
    "ms01": "b4b6929e890018668ef4faa9a74128a4ce5aa8df",
    "ms02": "38b8fa0dea527b1cc47aeb02dc260e039da37122",
    "ms03": "8fa07afac4a98096958880f6a5ece16f35abc4db",
}
MARS_R_M = 3396000.0      # radius used by the hand-off native evidence (coordinate_model)
EARTH_R_KM = 6371.0
CHECKS = []


def add(cid, desc, status, detail):
    CHECKS.append({"id": cid, "description": desc, "status": status, "detail": detail})


def sh(cwd, *args, check=True):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"{args} failed: {p.stderr[:300]}")
    return p


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def gc_km(lat1, lon1, lat2, lon2, r=EARTH_R_KM):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def utm_inverse(E, N, lon0_deg):
    """Inverse UTM (northern hemisphere), WGS84, Kruger series."""
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


def read_csv(path):
    return list(csv.DictReader(open(path, newline="", encoding="utf-8-sig")))


def norm(t):
    return t.replace("−", "-").replace("．", ".")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--main", required=True)
    ap.add_argument("--ms01", required=True)
    ap.add_argument("--ms02", required=True)
    ap.add_argument("--ms03", required=True)
    ap.add_argument("--out", default="outputs/integration/audit/checks.json")
    a = ap.parse_args()
    D = {k: pathlib.Path(getattr(a, k)) for k in ("main", "ms01", "ms02", "ms03")}

    env = {"python": platform.python_version(), "platform": platform.platform(),
           "numpy": None}
    try:
        import numpy as np
        env["numpy"] = np.__version__
    except Exception:
        np = None

    # ---------------------------------------------------------------- A. pinned heads
    for k, d in D.items():
        head = sh(d, "git", "rev-parse", "HEAD").stdout.strip()
        add(f"A-head-{k}", f"worktree {k} is at the pinned SHA", "PASS" if head == EXPECTED[k] else "FAIL",
            {"expected": EXPECTED[k], "actual": head})

    # ---------------------------------------------------------------- B. Mars values vs shared hand-off files on main
    mr = D["main"] / "outputs/research/mars_reselection_20261114"
    fc = {r["candidate_id"]: r for r in read_csv(mr / "final_candidates.csv")}
    nat = {r["review_id"]: r for r in json.load(open(mr / "candidate_native_evidence.json"))["records"]}
    MAP = {"MS-01": "A", "MS-02": "D", "MS-03": "C"}
    PTS = {"MS-01": (56.75, 72.75), "MS-02": (52.75, 168.25), "MS-03": (57.75, 242.25)}
    REPORT = {"MS-01": D["ms01"] / "docs/research/MS-01/report.md",
              "MS-02": D["ms02"] / "docs/research/MS-02/report.md",
              "MS-03": D["ms03"] / "docs/research/MS-03/report.md"}

    def g(rec, path):
        for p in path.split("."):
            rec = rec[p]
        return rec

    def fcv(pt, col):
        return float(fc[pt][col])

    # (point, quantity, value-from-main, token as printed in that team's report)
    TOK = []
    r1, r2, r3 = nat["A"], nat["D"], nat["C"]
    TOK += [("MS-01", "MOLA mean elevation m", g(r1, "mola_elevation_m_areoid.mean"), "-3700.914"),
            ("MS-01", "MOLA mean slope deg", g(r1, "mola_slope_deg_3p7km_baseline.mean"), "0.287207"),
            ("MS-01", "MOLA relief m", g(r1, "mola_relief_m"), "76"),
            ("MS-01", "TES TI mean (infill excluded)", g(r1, "tes_TI_native_excluding_infill.mean"), "325.1557"),
            ("MS-01", "SWIM 0-1 m mean", g(r1, "swim_0_1m_native.mean"), "0.639225"),
            ("MS-01", "SWIM 1-5 m mean", g(r1, "swim_1_5m_native.mean"), "0.647482"),
            ("MS-01", "CDOD MY34 mean", fcv("MS-01", "dust_my34_mean_cdodtot"), "0.119264"),
            ("MS-01", "CDOD MY34 p95", fcv("MS-01", "dust_my34_p95_cdodtot"), "0.222456"),
            ("MS-01", "CDOD MY35 mean", fcv("MS-01", "dust_my35_mean_cdodtot"), "0.107535"),
            ("MS-01", "CDOD MY35 p95", fcv("MS-01", "dust_my35_p95_cdodtot"), "0.180147"),
            ("MS-01", "MCS 15 LTST median K", fcv("MS-01", "MCS_populated_day_median_K"), "247.479"),
            ("MS-01", "MCS 03 LTST median K", fcv("MS-01", "MCS_populated_night_median_K"), "173.729"),
            ("MS-01", "MCS paired contrast median K", fcv("MS-01", "MCS_paired_contrast_median_K"), "63.536")]
    TOK += [("MS-02", "MOLA mean elevation m", g(r2, "mola_elevation_m_areoid.mean"), "-3898.7"),
            ("MS-02", "MOLA mean slope deg", g(r2, "mola_slope_deg_3p7km_baseline.mean"), "0.302"),
            ("MS-02", "MOLA relief m", g(r2, "mola_relief_m"), "117"),
            ("MS-02", "TES TI mean (infill excluded)", g(r2, "tes_TI_native_excluding_infill.mean"), "217.27"),
            ("MS-02", "SWIM 0-1 m mean", g(r2, "swim_0_1m_native.mean"), "0.693"),
            ("MS-02", "SWIM 1-5 m mean", g(r2, "swim_1_5m_native.mean"), "0.622"),
            ("MS-02", "CDOD MY34 p95", fcv("MS-02", "dust_my34_p95_cdodtot"), "0.240"),
            ("MS-02", "CDOD MY35 p95", fcv("MS-02", "dust_my35_p95_cdodtot"), "0.173"),
            ("MS-02", "MCS 03 LTST median K", fcv("MS-02", "MCS_populated_night_median_K"), "171.27"),
            ("MS-02", "MCS 15 LTST median K", fcv("MS-02", "MCS_populated_day_median_K"), "246.31"),
            ("MS-02", "MCS paired contrast median K", fcv("MS-02", "MCS_paired_contrast_median_K"), "66.83"),
            ("MS-02", "MCS paired bins", fcv("MS-02", "MCS_paired_bins"), "75")]
    TOK += [("MS-03", "MOLA mean slope deg", g(r3, "mola_slope_deg_3p7km_baseline.mean"), "0.1627532209"),
            ("MS-03", "MOLA relief m", g(r3, "mola_relief_m"), "76"),
            ("MS-03", "TES TI mean (infill excluded)", g(r3, "tes_TI_native_excluding_infill.mean"), "152.80772587767"),
            ("MS-03", "SWIM 0-1 m mean", g(r3, "swim_0_1m_native.mean"), "0.9109040236"),
            ("MS-03", "SWIM 1-5 m mean", g(r3, "swim_1_5m_native.mean"), "0.5099723018"),
            ("MS-03", "CDOD MY34 mean", fcv("MS-03", "dust_my34_mean_cdodtot"), "0.0982145182"),
            ("MS-03", "CDOD MY35 mean", fcv("MS-03", "dust_my35_mean_cdodtot"), "0.0886603747"),
            ("MS-03", "CDOD MY34 p95", fcv("MS-03", "dust_my34_p95_cdodtot"), "0.1733616889"),
            ("MS-03", "CDOD MY35 p95", fcv("MS-03", "dust_my35_p95_cdodtot"), "0.1409617454"),
            ("MS-03", "MCS paired contrast median K", fcv("MS-03", "MCS_paired_contrast_median_K"), "67.054737899")]
    texts = {pt: norm(open(p, encoding="utf-8").read()) for pt, p in REPORT.items()}
    tok_rows = []
    for pt, q, val, tok in TOK:
        dec = len(tok.split(".")[1]) if "." in tok else 0
        rounds_ok = abs(round(val, dec) - float(tok)) < 1e-12
        in_text = tok in texts[pt]
        tok_rows.append({"mars_point": pt, "quantity": q, "main_value": val, "printed_token": tok,
                         "rounds_to_token": rounds_ok, "token_in_report": in_text})
    bad = [r for r in tok_rows if not (r["rounds_to_token"] and r["token_in_report"])]
    add("B-mars-values", "numbers quoted in each report equal the shared native/final_candidates values (rounded to printed digits) and appear in the report",
        "PASS" if not bad else "FAIL", {"n_checked": len(tok_rows), "n_bad": len(bad), "bad": bad, "rows": tok_rows})

    # counts and grid cells quoted in the reports (support/valid-cell counts, nearest-grid coordinates)
    CNT = [("MS-01", "TES valid / mask-zero cells", f"{fc['MS-01']['TES_TI_valid_cells']}/{fc['MS-01']['tes_mask_zero_cells']}", ["73", "27"]),
           ("MS-01", "dust native cell", f"{fc['MS-01']['dust_my34_native_cell_lat']}N {fc['MS-01']['dust_my34_native_cell_lon']}E", ["55.5N72E"]),
           ("MS-01", "MCS native bin", f"{fc['MS-01']['MCS_native_lat']}N {fc['MS-01']['MCS_native_lon']}E", ["55N75E"]),
           ("MS-01", "MCS valid day/night/paired bins", f"{fc['MS-01']['MCS_valid_day_bins']}/{fc['MS-01']['MCS_valid_night_bins']}/{fc['MS-01']['MCS_paired_bins']}", ["161/288", "145/288", "69/288"]),
           ("MS-02", "TES valid / mask-zero cells", f"{fc['MS-02']['TES_TI_valid_cells']}/{fc['MS-02']['tes_mask_zero_cells']}", ["93/100", "7 格"]),
           ("MS-02", "dust native cell", f"{fc['MS-02']['dust_my34_native_cell_lat']}N {fc['MS-02']['dust_my34_native_cell_lon']}E", ["52.5\u00b0N,168.0\u00b0E"]),
           ("MS-02", "MCS native bin", f"{fc['MS-02']['MCS_native_lat']}N {fc['MS-02']['MCS_native_lon']}E", ["55.0\u00b0N,170.0\u00b0E"]),
           ("MS-02", "MCS paired bins", fc['MS-02']['MCS_paired_bins'], ["75/288"]),
           ("MS-03", "TES valid / mask-zero cells", f"{fc['MS-03']['TES_TI_valid_cells']}/{fc['MS-03']['tes_mask_zero_cells']}", ["79/100", "21個"]),
           ("MS-03", "dust native cell", f"{fc['MS-03']['dust_my34_native_cell_lat']}N {fc['MS-03']['dust_my34_native_cell_lon']}E", ["58.5\u00b0N", "117\u00b0W"]),
           ("MS-03", "MCS native bin", f"{fc['MS-03']['MCS_native_lat']}N {fc['MS-03']['MCS_native_lon']}E", ["60\u00b0N", "120\u00b0W"]),
           ("MS-03", "MCS valid day/night/paired bins", f"{fc['MS-03']['MCS_valid_day_bins']}/{fc['MS-03']['MCS_valid_night_bins']}/{fc['MS-03']['MCS_paired_bins']}", ["171", "148", "60\uff0f288"])]
    cnt_rows = []
    for pt, q, val, toks in CNT:
        cnt_rows.append({"mars_point": pt, "quantity": q, "main_value": val, "printed_tokens": toks,
                         "all_tokens_in_report": all(t in texts[pt] for t in toks)})
    badc = [r for r in cnt_rows if not r["all_tokens_in_report"]]
    # the token strings were chosen from the main values; a miss means the report states something else
    add("B-counts-and-grid-cells", "valid-cell counts, nearest dust/MCS grid cells and bin counts printed in the reports match main's final_candidates",
        "PASS" if not badc else "FAIL", {"n_checked": len(cnt_rows), "bad": badc, "rows": cnt_rows})
    mars_km = {"MS-02 MCS 5deg bin centre to MS-02 centre (km)": gc_km(52.75, 168.25, 55.0, 170.0, MARS_R_M / 1000),
               "MS-02 dust 3deg cell centre to MS-02 centre (km)": gc_km(52.75, 168.25, 52.5, 168.0, MARS_R_M / 1000)}
    add("B-bin-distances", "MS-02 report distances to the MCS and dust grid centres (146.7 km, 17.3 km) recomputed", 
        "PASS" if abs(mars_km["MS-02 MCS 5deg bin centre to MS-02 centre (km)"] - 146.7) < 0.1 and abs(mars_km["MS-02 dust 3deg cell centre to MS-02 centre (km)"] - 17.3) < 0.1 else "FAIL", mars_km)

    # native vs final_candidates internal agreement
    mism = []
    for pt, rid in MAP.items():
        rec = nat[rid]
        pairs = [("TES_TI_mean", g(rec, "tes_TI_native_excluding_infill.mean")),
                 ("mola_slope_deg_mean", g(rec, "mola_slope_deg_3p7km_baseline.mean")),
                 ("mola_relief_m", g(rec, "mola_relief_m")),
                 ("SWIM_0_1m_mean", g(rec, "swim_0_1m_native.mean")),
                 ("SWIM_1_5m_mean", g(rec, "swim_1_5m_native.mean"))]
        for col, v in pairs:
            if abs(float(fc[pt][col]) - v) > 1e-9:
                mism.append({"mars_point": pt, "col": col, "final": fc[pt][col], "native": v})
    add("B-native-vs-final", "final_candidates.csv native-cell columns agree with candidate_native_evidence.json", "PASS" if not mism else "FAIL", mism)

    # ---------------------------------------------------------------- C. geometry / coordinates
    geo = {}
    for pt, rid in MAP.items():
        rec = nat[rid]
        b = rec["nominal_cell_bounds"]
        lat0, lat1, lon0, lon1 = b["south"], b["north"], b["west"], b["east"]
        mid = ((lat0 + lat1) / 2, (lon0 + lon1) / 2)
        ns = math.radians(lat1 - lat0) * MARS_R_M / 1000
        ew = math.radians(lon1 - lon0) * MARS_R_M / 1000 * math.cos(math.radians(mid[0]))
        lon360 = PTS[pt][1] % 360
        geo[pt] = {"center_from_bounds": mid, "stated_center": [rec["center"]["lat"], rec["center"]["lon"]],
                   "NS_km": ns, "EW_km_at_center_lat": ew, "native_nominal_size_km": rec["nominal_size_km_NS_EW"],
                   "lon_east_0_360": lon360, "lon_east_signed": ((lon360 + 180) % 360) - 180}
    ok = all(abs(v["NS_km"] - v["native_nominal_size_km"][0]) < 1e-6 and abs(v["EW_km_at_center_lat"] - v["native_nominal_size_km"][1]) < 1e-6 for v in geo.values())
    add("C-cell-size", "nominal cell NS/EW km recomputed from bounds (R=3396 km) equals native evidence", "PASS" if ok else "FAIL", geo)
    quoted = {"MS-01": ("29.64", "16.25"), "MS-02": ("29.6", "17.9"), "MS-03": ("29.64", "15.81")}
    qrows = []
    for pt, (qn, qe) in quoted.items():
        qrows.append({"mars_point": pt, "NS_token": qn, "EW_token": qe,
                      "NS_in_report": qn in texts[pt], "EW_in_report": qe in texts[pt],
                      "NS_computed": geo[pt]["NS_km"], "EW_computed": geo[pt]["EW_km_at_center_lat"]})
    ok = all(r["NS_in_report"] and r["EW_in_report"] and abs(float(r["NS_token"]) - r["NS_computed"]) < 0.06 and abs(float(r["EW_token"]) - r["EW_computed"]) < 0.06 for r in qrows)
    add("C-report-sizes", "cell sizes printed in the three reports match the recomputation within rounding", "PASS" if ok else "FAIL", qrows)
    add("C-lon-convention", "MS-03 242.25 E = -117.75 (east-positive, planetocentric); MS-02 168.25 E and MS-01 72.75 E unchanged",
        "PASS" if abs(geo["MS-03"]["lon_east_signed"] + 117.75) < 1e-9 and abs(geo["MS-02"]["lon_east_signed"] - 168.25) < 1e-9 else "FAIL",
        {k: v["lon_east_signed"] for k, v in geo.items()})

    # Earth coordinates: University Valley W station DMS conversion and cross-PR use
    uv_dms = (-(77 + 51.729 / 60), 160 + 42.606 / 60)
    cand1 = {r["candidate_id"]: r for r in read_csv(D["ms01"] / "outputs/research/MS-01/candidates.csv")}
    cand2 = {r["candidate_id"]: r for r in read_csv(D["ms02"] / "outputs/research/MS-02/candidates.csv")}
    cand3 = {r["candidate_id"]: r for r in read_csv(D["ms03"] / "outputs/research/MS-03/candidates.csv")}
    uv = {"dms_77deg51.729S_160deg42.606E": uv_dms,
          "MS-01-E01": (float(cand1["MS-01-E01"]["latitude"]), float(cand1["MS-01-E01"]["longitude"])),
          "MS-03-E01": (float(cand3["MS-03-E01"]["latitude_deg"]), float(cand3["MS-03-E01"]["longitude_east_deg"])),
          "MS-02-E01_valley_anchor": (float(cand2["MS-02-E01"]["lat_deg"]), float(cand2["MS-02-E01"]["lon_deg_east"]))}
    d_station = {k: gc_km(*uv_dms, *v) for k, v in uv.items() if k != "dms_77deg51.729S_160deg42.606E"}
    ok = d_station["MS-01-E01"] < 0.01 and d_station["MS-03-E01"] < 0.01
    add("C-UV-anchor", "University Valley W-station anchor: MS-01 and MS-03 equal the published DMS; MS-02 uses a valley-level anchor",
        "PASS" if ok else "FAIL", {"coords": uv, "distance_from_DMS_station_km": d_station,
                                    "note": "MS-02-E01 anchor is the valley (77°52'S 160°45'E), not the W station; wording must not call it the station"})

    # Adventdalen anchors across PRs
    E3 = json.loads(json.dumps({}))
    bj = json.loads(cand3["MS-03-E02"]["bounds_json"])
    bb = bj["downloaded_UTM33N_bbox_m"]
    sw = utm_inverse(bb[0], bb[1], 15.0)
    ne = utm_inverse(bb[2], bb[3], 15.0)
    ad1_centre = ((sw[0] + ne[0]) / 2, (sw[1] + ne[1]) / 2)
    ADV = {"MS-02 ADE borehole (Rotem 2023)": (78.1722, 16.0613),
           "MS-02 CS-1 loess core (Rasmussen 2023)": (78.201, 15.840),
           "MS-03 AD1 event start (A1 metadata)": (bj["event_lat_start"], bj["event_lon_start"]),
           "MS-03 AD1 GIS bbox centre (UTM33N inverse, this audit)": ad1_centre}
    keys = list(ADV)
    seps = {f"{x} <-> {y}": gc_km(*ADV[x], *ADV[y]) for i, x in enumerate(keys) for y in keys[i + 1:]}
    pang = {"lat": (78.182, 78.206), "lon": (15.79, 16.559)}    # MS-02 footprint.csv FP-09 (PANGAEA 921087 site table bbox)
    inside = {k: pang["lat"][0] <= v[0] <= pang["lat"][1] and pang["lon"][0] <= v[1] <= pang["lon"][1] for k, v in ADV.items()}
    add("C-Adventdalen-anchors", "Adventdalen is not one place: ADE, CS-1 and AD1 are different anchors (distances recomputed)",
        "INFO", {"anchors": ADV, "separations_km": seps, "inside_PANGAEA_8site_bbox": inside,
                 "AD1_GIS_bbox_sw_ne_latlon": [sw, ne],
                 "note": "AD1 (Act-IWS) lies inside the PANGAEA bbox quoted in MS-02 footprint.csv; ADE lies ~1.1 km south of it"})

    # ---------------------------------------------------------------- D. dispositions (cross-PR consistency)
    disp = {"MS-01": {k: v["disposition"] for k, v in cand1.items()},
            "MS-02": {k: v["disposition"] for k, v in cand2.items()},
            "MS-03": {k: v["disposition"] for k, v in cand3.items()}}
    ms02_e03 = cand2["MS-02-E03"]["disposition"]
    ms03_e02 = cand3["MS-03-E02"]["disposition"]
    aligned = ("降為一般方法參照" in ms02_e03) and ("downgrade_general_method_reference" in ms03_e02)
    add("D-adventdalen-downgrade", "MS-02 Adventdalen (E03) and MS-03 AD1 (E02) both downgraded to general method reference",
        "PASS" if aligned else "FAIL", {"MS-02-E03": ms02_e03, "MS-03-E02": ms03_e02})
    add("D-dispositions", "candidate dispositions recorded in each PR", "INFO", disp)

    # ---------------------------------------------------------------- E. manifest hash re-verification
    def collect(obj, acc):
        if isinstance(obj, dict):
            if "path" in obj and "sha256" in obj and isinstance(obj["path"], str):
                acc.append((obj["path"], obj["sha256"], obj.get("bytes")))
            for v in obj.values():
                collect(v, acc)
        elif isinstance(obj, list):
            for v in obj:
                collect(v, acc)
    mf = {"MS-01": [D["ms01"] / "outputs/research/MS-01/manifest.json", D["ms01"] / "outputs/research/MS-01/thermal_followup/manifest.json"],
          "MS-02": [D["ms02"] / "outputs/research/MS-02/manifest.json"],
          "MS-03": [D["ms03"] / "outputs/research/MS-03/manifest.json"]}
    for pt, paths in mf.items():
        base = D[{"MS-01": "ms01", "MS-02": "ms02", "MS-03": "ms03"}[pt]]
        res = {"checked": 0, "match": 0, "mismatch": [], "not_in_repo": []}
        for mp in paths:
            acc = []
            collect(json.load(open(mp)), acc)
            for p, h, nbytes in acc:
                f = base / p
                if not f.is_file():
                    res["not_in_repo"].append({"manifest": str(mp.relative_to(base)), "path": p})
                    continue
                res["checked"] += 1
                if sha256(f) == h:
                    res["match"] += 1
                else:
                    res["mismatch"].append({"manifest": str(mp.relative_to(base)), "path": p})
        add(f"E-manifest-{pt}", f"{pt}: manifest SHA-256 values recomputed against files at the PR head",
            "PASS" if not res["mismatch"] else "FAIL", res)

    # ---------------------------------------------------------------- F. PR path sets, ownership and overlaps
    repo = a.repo
    paths = {}
    sizes = {}
    for k in ("ms01", "ms02", "ms03"):
        out = sh(repo, "git", "diff", "--name-status", EXPECTED["main"], EXPECTED[k]).stdout.strip().splitlines()
        paths[k] = [tuple(l.split("\t", 1)) for l in out if l]
    ALLOWED = {"ms01": ("docs/research/MS-01/", "outputs/research/MS-01/"),
               "ms02": ("docs/research/MS-02/", "outputs/research/MS-02/", "scripts/research/ms02_earth_analogs/"),
               "ms03": ("docs/research/MS-03/", "outputs/research/MS-03/", "scripts/research/MS-03/")}
    HANDOFF_ONLY = {"outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx",
                    "outputs/research/mars_reselection_20261114/screened_pool.csv.gz"}
    for k in ("ms01", "ms02", "ms03"):
        outside = [p for s, p in paths[k] if not p.startswith(ALLOWED[k]) and p not in HANDOFF_ONLY]
        ho = sorted(p for s, p in paths[k] if p in HANDOFF_ONLY)
        modified = [p for s, p in paths[k] if s != "A"]
        add(f"F-paths-{k}", f"{k}: diff vs main touches only its own directories (hand-off files reported separately)",
            "PASS" if not outside and not modified else "FAIL",
            {"n_files": len(paths[k]), "outside_own_dirs": outside, "non_added_status": modified, "handoff_files_in_diff_vs_main": ho})
        tot = 0
        for s, p in paths[k]:
            ls = sh(repo, "git", "ls-tree", "-l", EXPECTED[k], p, check=False).stdout.split()
            if len(ls) >= 4 and ls[3].isdigit():
                tot += int(ls[3])
        sizes[k] = tot
    sets = {k: {p for s, p in v} for k, v in paths.items()}
    ov = {f"{x}&{y}": sorted(sets[x] & sets[y]) for x, y in (("ms01", "ms02"), ("ms01", "ms03"), ("ms02", "ms03"))}
    add("F-overlap", "no file path is touched by more than one PR", "PASS" if not any(ov.values()) else "FAIL", ov)
    add("F-sizes", "added bytes per PR versus main (git blob sizes)", "INFO", sizes)
    # PR #6 base relation
    hd = sh(repo, "git", "diff", "--name-status", EXPECTED["handoff"], EXPECTED["ms02"]).stdout.strip().splitlines()
    hm = sh(repo, "git", "diff", "--name-status", EXPECTED["main"], EXPECTED["handoff"], check=False).stdout.strip().splitlines()
    add("F-PR6-base", "PR #6 base is the hand-off branch; hand-off adds only the workbook and screened pool over main",
        "PASS" if len(hm) == 2 and all(l.startswith("A") for l in hm) else "FAIL",
        {"PR6_files_vs_handoff_base": len(hd), "handoff_vs_main": hm})

    # ---------------------------------------------------------------- G. wording risk scan (candidates for manual review)
    NEG = re.compile(r"(不是|非|不能|不等於|不代表|不作|不可|不得|未|沒有|無|禁止|排除|並非|不宜|never|not |no |cannot|NOT|without)")
    RULES = [
        ("SWIM-as-amount", re.compile(r"SWIM"), re.compile(r"(含冰量|含冰率|冰量|機率|probabilit|abundance|%)")),
        ("TI-as-temperature-or-hardness", re.compile(r"(熱慣量|thermal inertia|TES)"), re.compile(r"(硬度|鬆軟|hardness|溫度計)")),
        ("attenuation-as-unique-ice", re.compile(r"(衰減|attenuat)"), re.compile(r"(唯一|證明|proves|unique)")),
        ("novelty-claim", re.compile(r"(首次|全球首|新發現|first-ever|novel)"), re.compile(r".")),
        ("absence-claim", re.compile(r"(不存在|沒有多邊形|無多邊形|absence)"), re.compile(r".")),
        ("similarity-percentage", re.compile(r"(相似|最像|Mars-like|similar)"), re.compile(r"(百分比|%|分數|score)")),
    ]
    scan = {}
    for pt, p in REPORT.items():
        sents = [s.strip() for s in re.split(r"[。\n]", open(p, encoding="utf-8").read()) if s.strip()]
        res = {}
        for name, a1, a2 in RULES:
            hits = [s for s in sents if a1.search(s) and a2.search(s)]
            unneg = [s[:240] for s in hits if not NEG.search(s)]
            res[name] = {"sentences_matching": len(hits), "without_negation_marker": len(unneg), "unnegated_examples": unneg[:8]}
        scan[pt] = res
    add("G-wording-scan", "heuristic scan of the three reports for the high-risk wording classes (candidates for manual review, not a verdict)",
        "INFO", scan)

    # ---------------------------------------------------------------- H. independent recompute: MS-01 24 h harmonic amplitudes
    h = {}
    if np is not None:
        import datetime as dt
        rows = list(csv.DictReader(gzip.open(D["ms01"] / "outputs/research/MS-01/thermal_followup/primary_temperature_records.csv.gz", "rt")))
        amp = {(r["station"], r["column"]): float(r["amplitude_K"]) for r in read_csv(D["ms01"] / "outputs/research/MS-01/thermal_followup/amplitudes.csv")}
        series = {}
        for r in rows:
            series.setdefault((r["station"], r["column"]), []).append((r["printed_timestamp"], float(r["temperature_C"])))
        diffs = []
        for key, v in series.items():
            v.sort()
            t0 = dt.datetime.fromisoformat(v[0][0])
            t = np.array([(dt.datetime.fromisoformat(x[0]) - t0).total_seconds() / 3600 for x in v])
            y = np.array([x[1] for x in v])
            X = np.column_stack([np.ones_like(t), t - t.mean(), np.sin(2 * np.pi * t / 24), np.cos(2 * np.pi * t / 24)])
            coef, *_ = np.linalg.lstsq(X, y, rcond=None)
            a_new = float(math.hypot(coef[2], coef[3]))
            if key in amp:
                diffs.append({"station": key[0], "column": key[1], "n": len(v), "amplitude_audit_K": a_new,
                              "amplitude_reported_K": amp[key], "abs_diff": abs(a_new - amp[key])})
        mx = max((d["abs_diff"] for d in diffs), default=None)
        add("H-MS01-amplitudes", "MS-01 24 h harmonic amplitudes recomputed by an independent numpy OLS from the committed analysis-window records",
            "PASS" if diffs and mx < 1e-6 else "FAIL", {"n_series": len(diffs), "max_abs_diff_K": mx, "rows": diffs})
    else:
        add("H-MS01-amplitudes", "MS-01 amplitude recompute", "NOT_RUN", "numpy unavailable")

    # ---------------------------------------------------------------- I. MS-02 numbers needing the hand-off screened pool
    sp = D["ms02"] / "outputs/research/mars_reselection_20261114/screened_pool.csv.gz"
    if sp.is_file():
        n = 0
        row = None
        with gzip.open(sp, "rt") as f:
            for r in csv.DictReader(f):
                n += 1
                if abs(float(r["lat"]) - 52.75) < 1e-9 and abs(float(r["lon"]) - 168.25) < 1e-9:
                    row = r
        ok = row is not None and abs(float(row["relief"]) - 117.0) < 1e-9 and abs(float(row["dust_my34_p95"]) - fcv("MS-02", "dust_my34_p95_cdodtot")) < 1e-9
        add("I-MS02-screened-pool", "MS-02 cell found in the hand-off screened pool (present only on the hand-off branch); relief and MY34 p95 agree with main's final_candidates",
            "PASS" if ok else "FAIL", {"rows": n, "found": row is not None})
    else:
        add("I-MS02-screened-pool", "MS-02 cell in screened pool", "NOT_RUN", "screened_pool.csv.gz absent in this checkout")

    # J: MS-03 149-label diagnostic, recomputed from the delivered comparison CSV (no network)
    import datetime as _dt
    gf = D["ms03"] / "outputs/research/MS-03/morphology/evidence_followup/generator_followup"
    rows = read_csv(gf / "duplicate_label_time_comparison.csv")
    comp = notc = over = 0
    for r in rows:
        t = _dt.datetime.fromisoformat(r["label_observation_start_time"])
        fl = t.replace(microsecond=0); ce = fl + (_dt.timedelta(seconds=1) if t.microsecond else _dt.timedelta())
        t1 = _dt.datetime.fromisoformat(r["index_time1"]); t2 = _dt.datetime.fromisoformat(r["index_time2"])
        if t1 in (fl, ce) and t2 in (fl, ce): comp += 1
        else: notc += 1
        if abs((t1 - t2).total_seconds()) > 1: over += 1
    obs = len({r["product_id"].rsplit("_", 1)[0] for r in rows})
    summ = json.loads((gf / "duplicate_label_time_summary.json").read_text())
    ok = (len(rows), comp, notc, over) == (149, 78, 71, 29) and (comp, notc, over) == (
        summ["pairs_both_floor_or_ceil_of_current_label"], summ["pairs_not_both_floor_or_ceil"], summ["pairs_over_one_second"])
    add("J-MS03-149-label-diagnostic", "independent recompute of 78/71/29 from delivered CSV (labels not re-downloaded; only internal consistency of the CSV and its rule)",
        "PASS" if ok else "FAIL", {"rows": len(rows), "compatible": comp, "not_compatible": notc, "over_1s": over, "distinct_observation_ids": obs,
        "note": "does not re-verify the labels against the network; 29 is a subset of 71 only if checked below", })
    sub = all(not (abs((_dt.datetime.fromisoformat(r["index_time1"]) - _dt.datetime.fromisoformat(r["index_time2"])).total_seconds()) > 1) or r["both_index_values_floor_or_ceil_of_label"] != "True" for r in rows)
    add("J-over1s-subset-of-incompatible", "every pair separated by >1 s is in the incompatible group (so 78/71/29 must not be summed)", "PASS" if sub else "FAIL", {})

    out = {"audit_script": "outputs/integration/audit/scripts/audit_checks.py", "environment": env,
           "pinned_shas": EXPECTED,
           "summary": {s: sum(1 for c in CHECKS if c["status"] == s) for s in ("PASS", "FAIL", "INFO", "NOT_RUN")},
           "checks": CHECKS,
           "not_computed": "no weights, no composite score, no similarity percentage; scientific truth is not re-derived"}
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out["summary"]))
    for c in CHECKS:
        print(f"{c['status']:7} {c['id']}")


if __name__ == "__main__":
    main()
