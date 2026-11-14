"""Attach real NASA Earth climate context to a bounded terrain shortlist; never re-rank."""

import argparse
import json
from pathlib import Path

from analog.climate import NETWORK_ERRORS, fetch_context
from analog.earth import RAW_DIR
from analog.provenance import write_json


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--analysis", type=Path, default=Path("outputs/analysis"))
    p.add_argument("--top", type=int, default=2)
    args = p.parse_args()
    data = json.loads((args.analysis / "results.json").read_text())
    for candidates in data["candidates"].values():
        for candidate in candidates[: args.top]:
            try:
                candidate["earth_climate_context"] = fetch_context(
                    candidate["lat"], candidate["lon"], RAW_DIR / "power"
                )
                print(candidate["candidate_id"], "NASA POWER context retrieved", flush=True)
            except NETWORK_ERRORS as exc:
                candidate["earth_climate_context"] = {
                    "status": "unavailable",
                    "error_type": type(exc).__name__,
                }
                print(
                    candidate["candidate_id"],
                    "context unavailable:",
                    type(exc).__name__,
                    flush=True,
                )
    write_json(args.analysis / "results_with_context.json", data)


if __name__ == "__main__":
    main()
