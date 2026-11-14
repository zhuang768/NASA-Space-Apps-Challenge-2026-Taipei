"""Verify or explicitly download the checksum-pinned public Mars inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config/raw_inputs_manifest.json"


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_file(path: Path, item: dict) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Missing input: {item['path']}")
    if path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
        raise ValueError(f"Checksum/size mismatch: {item['path']}; existing files are not replaced")


def verify_inputs(download: bool = False) -> list[dict]:
    spec = json.loads(MANIFEST.read_text())
    verified = []
    for item in spec["files"]:
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts or relative.parts[:2] != ("data", "raw"):
            raise ValueError("Manifest input must be a relative data/raw path")
        path = ROOT / relative
        if path.exists() or path.is_symlink():
            verify_file(path, item)
        elif not download:
            raise FileNotFoundError(f"Missing {item['path']}; use --download to fetch the public inputs")
        else:
            if not item["url"].startswith("https://"):
                raise ValueError("Only HTTPS public source URLs are accepted")
            path.parent.mkdir(parents=True, exist_ok=True)
            partial = path.with_name(path.name + ".part")
            if partial.is_symlink():
                raise ValueError(f"Refusing a symlink download destination: {partial}")
            with requests.get(item["url"], stream=True, timeout=90,
                              headers={"User-Agent":"Team-zasa-Mars-repro/1.0"}) as response:
                response.raise_for_status()
                with partial.open("wb") as stream:
                    for chunk in response.iter_content(chunk_size=1 << 20):
                        stream.write(chunk)
            verify_file(partial, item)
            partial.replace(path)
        verified.append({"path": item["path"], "bytes": item["bytes"], "sha256": item["sha256"]})
    return verified


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--download", action="store_true", help="Fetch missing inputs from the manifest's public source URLs")
    mode.add_argument("--verify-only", action="store_true", help="Check local files only; this is the default")
    args = parser.parse_args()
    verified = verify_inputs(download=args.download)
    print(json.dumps({"status":"PASS","network_requested":args.download,
                      "verified_input_count":len(verified),"verified_bytes":sum(i["bytes"] for i in verified),
                      "files":verified}, indent=2))


if __name__ == "__main__":
    main()
