"""Rebuild the unchanged 0.5-degree Mars stack from verified public originals."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from analog import stack as stack_mod
from scripts.download_mars import verify_inputs

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    verify_inputs(download=False)
    stack = stack_mod.build_mars_stack()
    destination = ROOT / "data/processed/mars_stack_0p5deg.nc"
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".part")
    if temporary.is_symlink():
        raise ValueError("Refusing a symlink temporary output")
    # Atomic replacement replaces a verification symlink itself, never its source file.
    stack.to_netcdf(temporary, engine="scipy", format="NETCDF3_64BIT")
    temporary.replace(destination)
    with destination.open("rb") as stream:
        checksum = hashlib.file_digest(stream,"sha256").hexdigest()
    print(json.dumps({"path":destination.relative_to(ROOT).as_posix(),"bytes":destination.stat().st_size,
                      "sha256":checksum,"variables":list(stack.data_vars),
                      "scope":"unchanged stack algorithm, no new score or Earth comparison"},indent=2))


if __name__ == "__main__":
    main()
