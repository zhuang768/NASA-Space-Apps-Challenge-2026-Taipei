#!/usr/bin/env python3
"""Independent recompute for MS-01 scale-gap table; exits 1 on any FAIL."""
import csv, json, pathlib, sys, math
import numpy as np, pandas as pd
R = pathlib.Path(__file__).resolve().parents[4]; L = R/"outputs/research/MS-01/local_validation"; M = R/"outputs/research/mars_reselection_20261114"
res = []
def chk(n, ok, d=""): res.append((n, bool(ok), d))
sg = list(csv.DictReader(open(L/"scale_gap_resolution.csv", encoding="utf-8")))
chk("8 rows SG-01..08", [r["id"] for r in sg] == [f"SG-0{i}" for i in range(1, 9)])
chk("no empty cells", all(v.strip() for r in sg for v in r.values()))
chk("3 CANNOT rows (material, cover, morphology)", [r["id"] for r in sg if "CANNOT" in r["status"]] == ["SG-05", "SG-06", "SG-07"])
t = " ".join(r["cell_value"] for r in sg)
fc = next(r for r in csv.DictReader(open(M/"final_candidates.csv", encoding="utf-8-sig")) if r["candidate_id"] == "MS-01")
for key, txt in [("TES_TI_mean", f'{float(fc["TES_TI_mean"]):.1f}'), ("mola_elevation_m_mean", f'{float(fc["mola_elevation_m_mean"]):.1f}'), ("SWIM_0_1m_mean", f'{float(fc["SWIM_0_1m_mean"]):.4f}'), ("SWIM_1_5m_mean", f'{float(fc["SWIM_1_5m_mean"]):.4f}'), ("dust_my34_mean_cdodtot", f'{float(fc["dust_my34_mean_cdodtot"]):.4f}')]:
    chk(f"{key} value in table", txt in t, txt)
d = pd.read_csv(M/"screened_pool.csv.gz")
n = d[(d.lat >= 54.75) & (d.lat <= 58.75) & (d.lon >= 70.75) & (d.lon <= 74.75)]
nj = json.load(open(L/"neighbourhood_context.json"))
chk("neighbour cell count", nj["cells"] == len(n), (nj["cells"], len(n)))
chk("neighbour TI mean", abs(nj["stats_mean_min_max"]["thermal_inertia"][0]-n.thermal_inertia.mean()) < 5e-4)
chk("TI CV text", f'{100*float(fc["TES_TI_std_population"])/float(fc["TES_TI_mean"]):.1f}%' in " ".join(r["cell_value"] for r in sg))
rs = f'{math.hypot(0,0)}'
bad = [x for x in res if not x[1]]
for x in res: print("PASS" if x[1] else "FAIL", x[0], x[2])
sys.exit(1 if bad else 0)
