"""Check exact replay inputs without extracting archives or fetching anything."""
import argparse
import hashlib
import json
from pathlib import Path

def sha256(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path.cwd(), help="repository checkout")
    p.add_argument("--archives", type=Path, help="optional directory of team-provided ZIPs")
    args = p.parse_args()
    manifest = json.loads(Path(__file__).with_name("inputs.json").read_text())
    checks = [(args.repo / x["path"], x) for x in manifest["repository_inputs"]]
    if args.archives:
        checks += [(args.archives / x["file"], x) for x in manifest["team_archives"]]
    failures = 0
    for path, expected in checks:
        if not path.is_file():
            print(f"MISSING  {path}")
            failures += 1
            continue
        good = path.stat().st_size == expected["bytes"] and sha256(path) == expected["sha256"]
        print(f"{'OK' if good else 'MISMATCH':8} {expected.get('path', expected.get('file'))}")
        failures += not good
    if not args.archives:
        print("External ZIPs not checked; repository-only workflows can still run.")
    return int(bool(failures))

if __name__ == "__main__":
    raise SystemExit(main())
