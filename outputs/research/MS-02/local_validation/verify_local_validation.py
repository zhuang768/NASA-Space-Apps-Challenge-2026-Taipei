#!/usr/bin/env python3
"""Checks for MS-02 local_validation. Run from repo root. Exit 1 on any FAIL."""
import csv, glob, json, math, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent
NOTES = ROOT/"docs/research/MS-02/local_validation/research_notes.md"
res = []
def chk(name, ok, detail=""):
    res.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
rd = lambda n: list(csv.DictReader(open(HERE/n, encoding="utf-8-sig")))
tabs = {n: rd(n) for n in ("local_prior_work.csv", "mars_ice_evidence.csv", "analog_validation.csv", "search_log.csv")}
chk("tables non-empty", all(len(v) > 0 for v in tabs.values()), {k: len(v) for k, v in tabs.items()})
empty = [(n, r[list(r)[0]], k) for n, rows in tabs.items() for r in rows for k, v in r.items() if v is None or v.strip() == ""]
chk("no empty cells (use 'n/a' or 'not obtained' for missing)", not empty, empty[:5])
ids = {r["search_id"] for r in tabs["search_log.csv"]}
refs = set(re.findall(r"LV-S\d+", "".join(open(HERE/n, encoding="utf-8-sig").read() for n in tabs if n != "search_log.csv") + NOTES.read_text(encoding="utf-8")))
chk("every LV-S reference resolves", refs <= ids, sorted(refs-ids))
dup = [i for i in ids if sum(1 for r in tabs["search_log.csv"] if r["search_id"] == i) > 1]
chk("search ids unique", not dup, dup)
# independent recompute of distances / cell size
D = json.loads((HERE/"derived_metrics.json").read_text())
R = 3396.0
def hav(a, b, c, d):
    a, b, c, d = map(math.radians, (a, b, c, d)); x = math.sin((c-a)/2)**2 + math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 2*R*math.asin(math.sqrt(x))
ew = 2*math.pi*R/360*0.5*math.cos(math.radians(52.75)); ns = 2*math.pi*R/360*0.5
chk("cell size recompute (29.64 x 17.94 km)", abs(D["cell_size_km"][0]-ew) < 1e-3 and abs(D["cell_size_km"][1]-ns) < 1e-3, [round(ew, 3), round(ns, 3)])
ice = list(csv.DictReader(open(ROOT/"outputs/research/mars_reselection_20261114/known_ice_points_morgan2025.csv")))
nn = min(hav(52.75, 168.25, float(x["lat"]), float(x["lonE"])) for x in ice)
chk("nearest Morgan 2025 point 389.0 km", abs(nn-D["morgan2025_nearest_3_km"][0][0]) < 0.06, round(nn, 3))
chk("Bramson box distance (point to 50N,180E)", abs(hav(52.75, 168.25, 50, 180)-D["distance_cell_centre_to_study_extent_km"]["Bramson2015_CTX_search"]) < 25, "clamped-box distance vs corner; tolerance 25 km")
chk("SWIM two-value share arithmetic", abs((D["SWIM_1_5m"]["mean"]-0.5)/0.5-0.245) < 5e-4, D["SWIM_1_5m"]["share_at_max_if_only_two_values_0.5_and_1.0"])
# shared values vs main table
fc = next(r for r in csv.DictReader(open(ROOT/"outputs/research/mars_reselection_20261114/final_candidates.csv", encoding="utf-8-sig")) if r["candidate_id"] == "MS-02")
ev = {r["evidence_id"]: r for r in tabs["mars_ice_evidence.csv"]}
def num(s): return [float(x) for x in re.findall(r"-?\d+\.?\d*", s)]
pairs = [("ME-03", "TES_TI_mean", 0), ("ME-04", "SWIM_0_1m_mean", 0), ("ME-05", "SWIM_1_5m_mean", 0), ("ME-01", "mola_elevation_m_mean", 0), ("ME-02", "mola_slope_deg_mean", 0)]
bad = []
for eid, col, i in pairs:
    v = num(ev[eid]["value"])[i]; t = float(fc[col])
    if abs(v-t) > 5e-4*max(1, abs(t)): bad.append((eid, v, t))
chk("evidence values equal main final_candidates (4-digit rounding)", not bad, bad)
# wording: forbidden unnegated claims
txt = NOTES.read_text(encoding="utf-8") + "".join(open(HERE/n, encoding="utf-8-sig").read() for n in tabs)
neg = re.compile(r"(不|非|無法|不得|不等於|not|no |without|cannot|未)")
hits = []
for pat in ("無冰", "最像", "已證實有冰", "證明有冰", "含冰量為", "冰機率"):
    for m in re.finditer(pat, txt):
        ctx = txt[max(0, m.start()-14):m.start()]
        if not neg.search(ctx): hits.append((pat, txt[max(0, m.start()-20):m.end()+10].replace("\n", " ")))
chk("no unnegated forbidden claim phrases (heuristic)", not hits, hits[:5])
chk("figure exists", (HERE/"fig_local_prior_work_extents.png").stat().st_size > 20000)
# scope: only local_validation paths changed vs PR head
try:
    st = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
    outside = [l for l in st if "local_validation" not in l]
    chk("changes only under local_validation dirs", not outside, outside[:5])
except Exception as e:
    chk("changes only under local_validation dirs", False, str(e))
(HERE/"verification.json").write_text(json.dumps({"checks": res, "summary": {s: sum(1 for c in res if c["status"] == s) for s in ("PASS", "FAIL")}}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
for c in res: print(c["status"], c["check"], "" if c["status"] == "PASS" else c["detail"])
sys.exit(1 if any(c["status"] == "FAIL" for c in res) else 0)
