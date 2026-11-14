"""Download/check a version-pinned MCS derivative and export unscored context."""

import argparse
import hashlib
import json
from pathlib import Path

import requests
import xarray as xr

from analog.provenance import write_json
from analog.regional_temperature import extract_context
from analog.screening import TARGETS

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/mars/temperature/mcs_corrected"
RECORD = "https://zenodo.org/api/records/17947556"
URL = RECORD + "/files/MCS_tsurf_corrected.nc/content"
EXPECTED_MD5 = "921ebf89ba5f1ac35d89d62f83369c27"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / "MCS_tsurf_corrected.nc"
    if args.download:
        meta = requests.get(RECORD, timeout=45)
        meta.raise_for_status()
        if meta.json()["id"] != 17947556:
            raise ValueError("Unexpected record version")
        (RAW / "record.json").write_text(json.dumps(meta.json(), indent=2) + "\n")
        if not path.exists():
            response = requests.get(URL, timeout=90)
            response.raise_for_status()
            partial = path.with_suffix(".part")
            partial.write_bytes(response.content)
            if hashlib.md5(response.content).hexdigest() != EXPECTED_MD5:
                raise ValueError("Downloaded checksum mismatch")
            partial.replace(path)
    data = path.read_bytes()
    if hashlib.md5(data).hexdigest() != EXPECTED_MD5:
        raise ValueError("MCS checksum mismatch")
    metadata = json.loads((RAW / "record.json").read_text())
    if metadata["metadata"]["license"]["id"] != "cc-by-4.0":
        raise ValueError("Review changed source terms")
    with xr.open_dataset(path) as ds:
        profiles = {name: extract_context(ds, t["lat"], t["lon"]) for name, t in TARGETS.items()}
        attrs = {v: dict(ds[v].attrs) for v in ds.variables}
    write_json(
        ROOT / "outputs/mars_regional_temperature/context.json",
        {
            "schema_version": "1.0",
            "analysis_type": "unscored_regional_temperature_context",
            "source": {
                "doi": "10.5281/zenodo.17947556",
                "concept_doi": "10.5281/zenodo.17947555",
                "url": URL,
                "record_url": RECORD,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "md5": EXPECTED_MD5,
                "version_record": 17947556,
                "license": "CC-BY-4.0",
                "authors": "Yu Wang; Shuanggen Jin",
                "publication_date": "2025-12-16",
                "paper": "https://doi.org/10.1029/2025JE009381",
                "author_code": "https://github.com/YuleWork/Mars-surface-temperature-JGR2025",
                "netcdf_attributes": attrs,
            },
            "profiles": profiles,
            "formal_surface_temperature_status": "missing comparable QA-qualified 100 km observation product",
            "ranking_changed": False,
        },
    )
    for name, p in profiles.items():
        print(
            name,
            p["selected_grid_coordinate"],
            p["valid_day_bins"],
            p["valid_night_bins"],
            p["paired_bins"],
        )


if __name__ == "__main__":
    main()
