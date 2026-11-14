#!/usr/bin/env python3
"""Writes manifest.json for MS-02 local_validation (run last, after verify_local_validation.py)."""
import hashlib, json, pathlib, platform, sys, csv
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
NOTES = ROOT/"docs/research/MS-02/local_validation/research_notes.md"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files = sorted(p for p in list(HERE.iterdir())+[NOTES] if p.is_file() and p.name != "manifest.json" and p.suffix != ".pyc")
log = list(csv.DictReader(open(HERE/"search_log.csv", encoding="utf-8-sig")))
ver = json.loads((HERE/"verification.json").read_text())
try:
    import numpy; npv = numpy.__version__
except Exception: npv = None
try:
    import matplotlib; mv = matplotlib.__version__
except Exception: mv = None
m = {
 "purpose": "MS-02 local validation: research gap, local Mars material/ice evidence, Earth analog validation level. Data/notes only; no report prose, no slides.",
 "date_taipei": "2026-11-15",
 "pinned": {
   "PR6_head_at_start": "38b8fa0dea527b1cc47aeb02dc260e039da37122",
   "PR6_base": "handoff/verified-data-20261114 @ f7076c9fdc77e00244ed5d6863aad2bf78cfa28f",
   "main_read": "3cc8488577535e2fa4d146021fde51f8ff6cc667",
   "PR9_head_read": "c206553fc681328d214cbbcd508d3c5b1391e200",
   "PR10_head_read": "0260c511d9fce6be12d3460a69e474f333160cbf"},
 "environment": {"python": sys.version.split()[0], "platform": platform.platform(), "numpy": npv, "matplotlib": mv},
 "inputs_from_repo": ["outputs/research/mars_reselection_20261114/final_candidates.csv", "outputs/research/mars_reselection_20261114/known_ice_points_morgan2025.csv", "outputs/research/mars_reselection_20261114/bounded_prior_site_audit.json (inherited statements, not re-read)"],
 "search_log_rows": len(log),
 "verification": ver["summary"],
 "data_products_not_obtained": [
   {"product": "Piqueux 2019 ice-table depth map (d_m.ascii)", "reason": "no download URL found; host unreachable from shell"},
   {"product": "SHARAD tracks/radargrams in 52.50-53.00N,168.00-168.50E", "reason": "PDS Geosciences index fetch client_error; shell CONNECT 403"},
   {"product": "HiRISE/CTX footprints (ODE REST; RDRCUMINDEX.TAB 168,675,271 B)", "reason": "ODE refused by robots; TAB cannot be parsed via fetch; shell CONNECT 403"},
   {"product": "CRISM/OMEGA detections", "reason": "title-level search only; no product retrieved"},
   {"product": "Tanaka 2014 SIM 3292 GIS (unit at coordinate)", "reason": "astrogeology/pubs.usgs CONNECT 403; pamphlet read to p.14 only"},
   {"product": "MONS WEH value at the cell", "reason": "map not retrieved; paper text gives no cell value"},
   {"product": "Wendt 2026 Zenodo core data (10.5281/zenodo.11187359)", "reason": "not downloaded (zenodo unreachable from shell)"},
   {"product": "HAL insu-03914738 (GPR field tests on Svalbard)", "reason": "Access Denied by Anubis bot protection; not bypassed"}],
 "inherited_not_reread": ["Dundas 2014/2021 point tables", "EZMars/SWIM4MIM/MCOA/Phlegra proposals", "Morgan 2025 Table 2 (points read from the repo CSV)"],
 "unresolved_source_discrepancies": ["Piqueux pixel size 2 ppd (data-file page) vs 3 ppd (abstract page)", "Morgan 2021 study-region longitude wording '290E to 225E'", "Ramsdale 2019 strip longitude limits not stated (edges are this-study estimates)"],
 "files": [{"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)} for p in files],
}
(HERE/"manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print("manifest", len(files), "files")
