#!/usr/bin/env python3
"""MS-01 scale-gap table, neighbourhood context and statistics. Reads shared hand-off files and MS-01's own receipts; no new retrieval. Run from anywhere."""
import csv, json, pathlib, gzip
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[4]; L = R/"outputs/research/MS-01/local_validation"; M = R/"outputs/research/mars_reselection_20261114"
fc = next(r for r in csv.DictReader(open(M/"final_candidates.csv", encoding="utf-8-sig")) if r["candidate_id"] == "MS-01")
f = lambda k: float(fc[k])
cat = {r["dataset"]: r for r in csv.DictReader(open(L/"catalogue_summary.csv", encoding="utf-8-sig"))}
pool = pd.read_csv(M/"screened_pool.csv.gz")
la, lo = 56.75, 72.75
nb = pool[pool.lat.between(la-2, la+2) & pool.lon.between(lo-2, lo+2)]
nbs = {c: (round(float(nb[c].mean()), 3), round(float(nb[c].min()), 3), round(float(nb[c].max()), 3)) for c in ["thermal_inertia", "relief", "ice_shallow", "dust_my34_mean", "slope"]}
pq = next(r for r in csv.DictReader(open(L/"mars_ice_evidence.csv", encoding="utf-8-sig")) if r["id"] == "MI01")
dm = float(pq["value"])
sg = [
 ("SG-01","terrain","MOLA 64 native cells (~3.7 km baseline)",f'mean {f("mola_elevation_m_mean"):.1f} m; relief {f("mola_relief_m"):.0f} m; slope mean {f("mola_slope_deg_mean"):.3f} deg, max {f("mola_slope_deg_max"):.3f} deg',"Smooth at >=3.7 km baseline; no information below 3.7 km (small slopes, craters, boulders, polygons)","Answered at 3.7 km only","CTX/HiRISE DTM or images of the fixed range"),
 ("SG-02","thermal","TES TI 100 native cells, 73 valid (27 mask-zero excluded)",f'mean {f("TES_TI_mean"):.1f}; median {f("TES_TI_median"):.0f}; range {f("TES_TI_min"):.0f}-{f("TES_TI_max"):.0f}; sd {f("TES_TI_std_population"):.1f} (CV {100*f("TES_TI_std_population")/f("TES_TI_mean"):.1f}%)',"Apparent bulk TI of top ~cm-dm; not temperature, hardness, material type, grain size, cover thickness or ice; 27% of native cells excluded","Answered as cell-scale descriptor; local material unknown","THEMIS night TI at ~100 m; projection offset convention (themis_qc) unresolved"),
 ("SG-03","water-ice","SWIM2 0-1 m and 1-5 m (consistency -1..1); Piqueux 2019 conditional model; MONS ~550 km",f'SWIM 0-1 m mean {f("SWIM_0_1m_mean"):.4f} ({f("SWIM_0_1m_min"):.3f}-{f("SWIM_0_1m_max"):.3f}); 1-5 m mean {f("SWIM_1_5m_mean"):.4f} (min {f("SWIM_1_5m_min"):.1f}, median {f("SWIM_1_5m_median"):.1f}, max {f("SWIM_1_5m_max"):.1f}); Piqueux conditional model depth {dm:.3f} m',"SWIM is a composite consistency, not abundance/depth/probability; Piqueux depth assumes a frozen H2O lower layer, not an observed interface; SWIM and thermal inputs may share sources","Existence = evidence insufficient; depth = model only; content unknown","Independent local ice truth: calibrated, co-located seasonal observation or radar echo with clutter control"),
 ("SG-04","atmosphere-dust","Montabone CDOD 3 deg grid; MCS 5 deg bins",f'MY34 mean {f("dust_my34_mean_cdodtot"):.4f} (p95 {f("dust_my34_p95_cdodtot"):.4f}); MY35 mean {f("dust_my35_mean_cdodtot"):.4f} (p95 {f("dust_my35_p95_cdodtot"):.4f})',"9.3 um column absorption; not surface deposition rate or cover thickness; MCS model time-adjusted, no QA","Answered as column context only; cover unknown","Repeat imaging change detection or in-situ record"),
 ("SG-05","local material","none at <3.7 km",f'CRISM TRDR {cat["CRISM_TRDR"]["query_count"]} products in {cat["CRISM_TRDR"]["grouped_observations"]} observation groups (footprints only); TOD sample 21747/336384 finite, 48 spectra all missing',"No usable spectrum; geologic unit not determined (SIM 3292 GIS not downloaded)","CANNOT be answered","CRISM spectra with wavelength CDR/DDR QC; SIM 3292 vector intersected with the fixed range"),
 ("SG-06","cover (overburden)","Piqueux conditional model only",f'conditional model dry-layer {dm:.3f} m; SHARAD {cat["SHARAD_RDR"]["query_count"]} nominal tracks, 1 actual geometry (64 columns in range)',"Model depth is an assumption-bound output; no echo picking, clutter simulation or dielectric inversion; not validated","CANNOT be answered","SHARAD echoes with clutter simulation; co-located seasonal thermal revisit"),
 ("SG-07","morphology","CTX nominal footprints only",f'CTX EDR {cat["CTX_EDR"]["query_count"]} footprints intersecting the range (coverage {float(cat["CTX_EDR"]["nominal_roi_coverage_fraction"]):.2f} nominal); HiRISE {cat["HIRISE_RDR"]["query_count"]}',"Footprint union is not valid pixel coverage; images not downloaded or classified","CANNOT be answered","Map-projected CTX images of the range (ISIS/SPICE or projected mosaic) and quantitative classification"),
 ("SG-08","neighbourhood representativeness",f"screened_pool 0.5 deg cells, {len(nb)} cells within +/-2 deg of MS-01",f'neighbour TI mean {nbs["thermal_inertia"][0]} ({nbs["thermal_inertia"][1]}-{nbs["thermal_inertia"][2]}) vs MS-01 {f("TES_TI_mean"):.1f}; relief mean {nbs["relief"][0]} m (max {nbs["relief"][2]}); SWIM shallow mean {nbs["ice_shallow"][0]} ({nbs["ice_shallow"][1]}-{nbs["ice_shallow"][2]}); MY34 CDOD mean {nbs["dust_my34_mean"][0]}',"Same coarse products around the cell; shows regional spread, not local material","Answered as regional context; does not resolve SG-05-07","Same as SG-05-07"),
]
with open(L/"scale_gap_resolution.csv","w",newline="",encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["id","theme","finest_data","cell_value","limit","status","minimum_data_needed"]); w.writerows(sg)
json.dump({"centre":[la,lo],"window_deg":2,"cells":len(nb),"stats_mean_min_max":nbs},open(L/"neighbourhood_context.json","w"),indent=1)
cnt = lambda n: len(list(csv.DictReader(open(L/n, encoding="utf-8-sig"))))
lines = ["# MS-01 統計彙整（僅計數與數值；非報告正文）\n", "目標：MS-01，56.75°N、72.75°E（56.50–57.00°N、72.50–73.00°E，約 29.6 × 16.2 km）\n",
 "## 檔案列數\n","| 檔案 | 資料列 |","|---|---|"]+[f"| {n} | {cnt(n)} |" for n in ["mars_ice_evidence.csv","local_prior_work.csv","analog_validation.csv","search_log.csv","product_inventory.csv","catalogue_summary.csv","scale_gap_resolution.csv"]]
lines += ["\n## ODE 目錄（nominal 足跡；不是有效像元）\n","| 資料集 | 查詢數 | 面相交 | 線相交 | 觀測組 |","|---|---|---|---|---|"]+[f'| {k} | {v["query_count"]} | {v["positive_area_intersections"]} | {v["positive_line_intersections"]} | {v["grouped_observations"]} |' for k,v in cat.items()]
lines += ["\n## 尺度缺口判定\n","| id | 主題 | 狀態 |","|---|---|---|"]+[f"| {r[0]} | {r[1]} | {r[5]} |" for r in sg]
lines += ["\n## 周邊（±2°）\n",f"{len(nb)} 個 0.5° 格；"+"；".join(f"{k} 平均 {v[0]}（{v[1]}–{v[2]}）" for k,v in nbs.items())+"\n"]
(L/"statistics_summary.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print("\n".join(lines))
