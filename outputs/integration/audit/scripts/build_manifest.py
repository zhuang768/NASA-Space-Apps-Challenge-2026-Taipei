#!/usr/bin/env python3
"""Writes outputs/integration/audit/manifest.json: pinned SHAs, SHA-256 of every deliverable, reruns with exit codes, gaps."""
import hashlib, json, pathlib, re, sys, datetime
root = pathlib.Path(".")
A = root / "outputs/integration/audit"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files = sorted([p for p in list(A.rglob("*")) + list((root / "docs/integration/audit").rglob("*"))
                if p.is_file() and p.name != "manifest.json" and "__pycache__" not in p.parts])
checks = json.loads((A / "checks.json").read_text())
reruns = {}
for p in sorted((A / "reruns").glob("*.txt")):
    last = p.read_text(errors="replace").strip().splitlines()[-1]
    m = re.fullmatch(r"exit=(\d+)", last)
    reruns[p.name] = {"exit_code": int(m.group(1)) if m else None}
reruns["ms01_thermal_validate_noraw.txt"]["status"] = "NOT_RERUN: Zenodo raw HOBO/Campbell files unavailable (FileNotFoundError); not a PASS"
for k in reruns:
    reruns[k].setdefault("status", "ran; exit 0 = that team's own structural/reproduction checks passed" if reruns[k]["exit_code"] == 0 else "failed")
out = {
  "purpose": "Final-round evidence and claim audit, Team zasa, NASA Space Apps 2026",
  "audit_date_taipei": "2026-11-15",
  "pinned": checks["pinned_shas"],
  "task_listed_ms03_head_superseded": {"listed": "3321765dc0cd24316e7e12d30b4ade803fa67fcd", "audited_latest": "8fa07afac4a98096958880f6a5ece16f35abc4db"},
  "environment": checks["environment"],
  "automated_checks_summary": checks["summary"],
  "reruns_of_existing_validators": reruns,
  "not_verified": [
    "MS-01 thermal_followup/validate.py against Zenodo raw files (raw unavailable)",
    "MS-03 149 PDS labels not re-downloaded (CSV-internal recompute only)",
    "literature contents beyond what each team's report states it read",
    "root cause of HiRISE duplicate index rows (unknown by MS-03's own report)",
    "Workers Builds failure cause (fails on main and handoff as well)",
    "legal licence status of third-party files"],
  "claim_ledger_rows": sum(1 for _ in open(A / "claim_ledger.csv", encoding="utf-8-sig")) - 1,
  "files": [{"path": str(p), "sha256": sha(p), "bytes": p.stat().st_size} for p in files],
}
(A / "manifest.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("manifest files:", len(files))
