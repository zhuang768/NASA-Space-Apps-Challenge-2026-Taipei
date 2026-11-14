"""Acquire only configured public archive inputs; verify bytes before installation."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import urllib.request


def download(source, root, import_file=None):
    path = root / source["path"]
    algorithm = "sha256" if "expected_sha256" in source else "md5"
    expected = source["expected_"+algorithm]
    if path.exists():
        actual = hashlib.new(algorithm, path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Existing file checksum differs; retained without overwrite: {path}")
        return {"path": source["path"], "status": "existing_verified", algorithm: actual}
    t = time.perf_counter()
    if import_file:
        raw = Path(import_file).read_bytes()
        headers, final_url = {}, source["url"]
    else:
        request = urllib.request.Request(source["url"], headers={"User-Agent": "zasa-research-compute/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            headers = {k: response.headers.get(k) for k in ["Content-Type", "Last-Modified", "ETag"]}
            final_url = response.url
    actual = hashlib.new(algorithm, raw).hexdigest()
    if actual != expected:
        raise ValueError(f"Archive checksum mismatch: {actual} != {expected}; no data file written")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    result = {"path": source["path"], "url": source["url"], "final_url": final_url,
              "retrieved_utc": datetime.now(timezone.utc).isoformat(), "bytes": len(raw),
              "md5": hashlib.md5(raw).hexdigest(), "sha256": hashlib.sha256(raw).hexdigest(), "headers": headers,
              "acquisition_method": "import of browser-downloaded file" if import_file else "urllib HTTPS download",
              "download_seconds": None if import_file else time.perf_counter() - t,
              "verification_seconds": time.perf_counter() - t, "status": "imported_verified" if import_file else "downloaded_verified"}
    path.with_suffix(path.suffix + ".provenance.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument("--profiles", type=Path)
    p.add_argument("--source-id")
    p.add_argument("--import-file", type=Path, help="Verify and install an already downloaded original file")
    args = p.parse_args()
    profiles = args.profiles or args.root / "scripts/compute/source_profiles.json"
    data = json.loads(profiles.read_text())
    selected = [s for s in data["sources"] if not args.source_id or s["source_id"] == args.source_id]
    if not selected or (args.import_file and len(selected) != 1):
        p.error("Import requires exactly one matching source")
    for source in selected:
        print(json.dumps(download(source, args.root.resolve(), args.import_file)))


if __name__ == "__main__":
    main()
