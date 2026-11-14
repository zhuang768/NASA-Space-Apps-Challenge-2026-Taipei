"""Local source manifests. Never record authentication material."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


def source_record(path, url, **metadata):
    path = Path(path)
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return {
        "file": path.name,
        "url": url,
        "bytes": path.stat().st_size,
        "sha256": digest.hexdigest(),
        "recorded_utc": datetime.now(UTC).isoformat(),
        **metadata,
    }


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
