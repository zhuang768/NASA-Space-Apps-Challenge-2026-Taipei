#!/usr/bin/env python3
"""Replay MS01 from the two exact, locally held 2026-11-15 archives (Python 3.9+, NumPy)."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
from zipfile import ZipFile

EARTH = "18614ed973e7d83da54ae3a32087dceecc3cb2eb1a791103380e435ec4aca347"
COMBINED = "74604bcef11df103205ddc4b6f1537aabcf9927adfd25c0183189fbce8f82937"
EARTH_MEMBERS = "MS01_validation/"
PHASE_MEMBERS = "ZASA_independent_validation_20261115/ms01/"
RESULTS = {
    "results/thermal_results.csv": 40,
    "results/daily_metrics.csv": 360,
    "results/group_differences.csv": 6,
    "results/temperature_subset.csv": 2880,
    "mars_audit/mars_native_summary.csv": 5,
    "mars_audit/mars_native_cells.csv": 428,
}
PHASE_RESULTS = {"annual_phase_consistency.csv": 8, "month_sensitivity.csv": 96}
ATOL = 1e-9


def digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def check_archive(path, expected):
    actual = digest(path)
    if actual != expected:
        raise ValueError(f"{path.name}: SHA256 {actual}, expected {expected}")


def stage(archive, prefix, relative, dest):
    # Callers choose all paths (receipt names below are taken from a pinned ZIP).
    relative = Path(relative)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Unsafe member name: {relative}")
    target = dest / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(archive.read(prefix + relative.as_posix()))
    return target


def run(script, log, *args):
    with log.open("w") as stream:
        subprocess.run(
            [sys.executable, str(script), *(str(arg) for arg in args)],
            cwd=script.parent, stdout=stream, stderr=subprocess.STDOUT, check=True,
        )


def compare(old, new, nrows):
    with old.open(newline="") as orig, new.open(newline="") as rebuilt:
        a, b = csv.DictReader(orig), csv.DictReader(rebuilt)
        if a.fieldnames != b.fieldnames:
            raise ValueError(f"Header mismatch: {new.name}")
        xs, ys = list(a), list(b)
    if not (len(xs) == len(ys) == nrows):
        raise ValueError(f"Unexpected row counts for {new.name}: {len(xs)}, {len(ys)}")
    delta = 0.0
    for row_no, (x, y) in enumerate(zip(xs, ys), 2):
        for name, a in x.items():
            b = y[name]
            if a == b:
                continue
            try:
                a, b = float(a), float(b)
            except (TypeError, ValueError) as e:
                raise ValueError(f"{new.name}:{row_no}:{name}: string mismatch") from e
            if not (math.isfinite(a) and math.isfinite(b) and abs(a-b) < ATOL):
                raise ValueError(f"{new.name}:{row_no}:{name}: {a} != {b}")
            delta = max(delta, abs(a-b))
    return {"rows": nrows, "max_abs_float_delta": delta}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ms01", required=True, type=Path)
    parser.add_argument("--combined", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path, help="A new output directory outside version control")
    args = parser.parse_args()
    check_archive(args.ms01, EARTH)
    check_archive(args.combined, COMBINED)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    earth = out / "earth_mars"
    raw, subset, expected = [out / x for x in ("phase_raw", "phase_subset", "reference")]
    with ZipFile(args.ms01) as e, ZipFile(args.combined) as c:
        receipt = stage(e, EARTH_MEMBERS, "data/download_receipts.json", earth)
        for entry in json.loads(receipt.read_text()):
            stage(e, EARTH_MEMBERS, "data/" + entry["local"], earth)
        for rel in (
            "recompute_earth.py", "mars_audit/independent_earth_numeric_check.py",
            "mars_audit/recompute_mars_subset.py", "mars_audit/mars_small_inputs.npz",
            "mars_audit/mars_subset_provenance.json",
        ):
            stage(e, EARTH_MEMBERS, rel, earth)
        for rel in RESULTS:
            stage(e, EARTH_MEMBERS, rel, expected)
        for rel in PHASE_RESULTS:
            stage(c, PHASE_MEMBERS, rel, expected / "phase")
        phase_script = stage(c, PHASE_MEMBERS, "recompute_phase_consistency.py", raw)
        subset_data = stage(c, PHASE_MEMBERS, "analysis_temperature_subset.csv.gz", subset)
        shutil.copyfile(phase_script, subset / phase_script.name)
    run(earth / "recompute_earth.py", out / "earth.log", "--root", earth)
    run(earth / "mars_audit/independent_earth_numeric_check.py", out / "earth_independent.log")
    run(earth / "mars_audit/recompute_mars_subset.py", out / "mars.log")
    run(phase_script, out / "phase_raw.log", "--data", earth / "data")
    run(subset / phase_script.name, out / "phase_subset.log", "--subset", subset_data)
    qa = json.loads((earth / "mars_audit/independent_earth_numeric_check.json").read_text())
    if qa["status"] != "PASS" or not 0 <= qa["max_abs_difference"] < 1e-10:
        raise ValueError("Independent QR check failed")
    result = {
        "absolute_tolerance": ATOL,
        "numpy": __import__("numpy").__version__,
        "python": sys.version.split()[0],
        "input_sha256": {"ms01": EARTH, "combined": COMBINED},
        "independent_QR_max_abs_delta": qa["max_abs_difference"],
        "earth_mars": {name: compare(expected/name, earth/name, n) for name, n in RESULTS.items()},
        "phase_vs_archived": {
            name: compare(expected/"phase"/name, raw/name, n) for name, n in PHASE_RESULTS.items()
        },
        "phase_raw_vs_subset": {
            name: compare(raw/name, subset/name, n) for name, n in PHASE_RESULTS.items()
        },
    }
    result["status"] = "PASS"
    (out / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
