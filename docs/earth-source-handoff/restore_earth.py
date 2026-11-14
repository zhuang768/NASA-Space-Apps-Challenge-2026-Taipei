#!/usr/bin/env python3
import csv, hashlib, shutil, sys
from pathlib import Path

def ok(f, r):
    if not f.is_file() or f.stat().st_size != int(r["bytes"]):
        return False
    h = hashlib.sha256()
    with f.open("rb") as s:
        for chunk in iter(lambda: s.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest() == r["sha256"]

if len(sys.argv) != 3:
    raise SystemExit("usage: python3 restore_earth.py ASSET_DIR RAW_EARTH_DIR")
src, out = map(Path, sys.argv[1:])
with (src / "earth_inventory.csv").open(newline="") as f:
    manifest = list(csv.DictReader(f))
n = 0
errors = []
for r in manifest:
    name = r["file"]
    target = out / r["folder"] / name
    item = src / name
    if target.exists():
        if not ok(target, r):
            errors.append(f"existing destination differs, kept unchanged: {target}")
            continue
    elif not ok(item, r):
        errors.append(f"missing or checksum mismatch: {name}")
        continue
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        with item.open("rb") as inp, target.open("xb") as dest:
            shutil.copyfileobj(inp,dest,4*1024*1024)
    n += 1
for e in errors: print(e, file=sys.stderr)
print(f"Verified and available: {n}/{len(manifest)}")
raise SystemExit(bool(errors))
