#!/usr/bin/env python3
"""Loop-verify scale_gap_resolution.csv against derived_metrics.json; 3 passes must agree."""
import csv, json, pathlib, sys
H=pathlib.Path(__file__).resolve().parent
D=json.load(open(H/"derived_metrics.json")); R=list(csv.DictReader(open(H/"scale_gap_resolution.csv",encoding="utf-8")))
def once():
    t=" ".join(r["cell_value"]+r["limit"] for r in R); out=[]
    cv=D["TES_TI"]["std"]/D["TES_TI"]["mean"]
    for k,ok in [("217.3",abs(D["TES_TI"]["mean"]-217.3)<.05),("8.4%",abs(cv*100-8.4)<.05),("-3898.7",abs(D["MOLA"]["mean_m"]+3898.7)<.05),
      ("0.925",abs(D["MOLA"]["slope_max_deg"]-.925)<.001),("0.6225",abs(D["SWIM_1_5m"]["mean"]-.6225)<5e-5),("0.693",abs(D["SWIM_0_1m"]["mean"]-.693)<5e-4),
      ("0.22%",abs(D["cell_fraction_of_MONS_FWHM_circle"]*100-.22)<.005),("389",abs(D["morgan2025_nearest_3_km"][0][0]-389)<.5),("0.125",abs(D["CDOD"]["MY34_mean"]-.125)<.001)]:
        out.append((k,ok and k in t))
    out.append(("unanswerable rows flagged",sum("CANNOT" in r["status"] for r in R)==3))
    out.append(("no empty cells",all(v.strip() for r in R for v in r.values())))
    return out
runs=[once() for _ in range(3)]
bad=[x for r in runs for x in r if not x[1]]
print(json.dumps({"passes":3,"fail":bad},ensure_ascii=False)); sys.exit(1 if bad or runs[0]!=runs[1]!=runs[2] else 0)
