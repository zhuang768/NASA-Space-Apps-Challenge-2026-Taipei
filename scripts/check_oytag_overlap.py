"""Locate published Oytag samples in the existing Gale Earth candidate window."""

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from shapely.geometry import Point, Polygon

from analog.provenance import write_json
from analog.screening import EARTH_RADIUS_M


def main():
    root = Path(__file__).resolve().parents[1]
    inputs = [
        root / "outputs/analysis/results_with_context.json",
        root / "outputs/research/oytag_literature_points.csv",
    ]
    candidate = next(
        c
        for c in json.loads(inputs[0].read_text())["candidates"]["gale"]
        if c["lat"] == 39 and c["lon"] == 75
    )
    polygon = Polygon(candidate["footprint"])
    records = []
    for row in csv.DictReader(inputs[1].open()):
        lat, lon = float(row["latitude_deg"]), float(row["longitude_deg"])
        p0, p, dl = np.deg2rad([39, lat, lon - 75])
        angle = np.arccos(
            np.clip(np.sin(p0) * np.sin(p) + np.cos(p0) * np.cos(p) * np.cos(dl), -1, 1)
        )
        k = angle / np.sin(angle) if angle else 1.0
        east = EARTH_RADIUS_M * k * np.cos(p) * np.sin(dl) / 1000
        north = (
            EARTH_RADIUS_M
            * k
            * (np.cos(p0) * np.sin(p) - np.sin(p0) * np.cos(p) * np.cos(dl))
            / 1000
        )
        in_square = bool(abs(east) <= 50 and abs(north) <= 50)
        in_polygon = polygon.covers(Point(lon, lat))
        assert in_square == in_polygon
        records.append(
            {
                **row,
                "east_km": float(east),
                "north_km": float(north),
                "inside_local_100km_square": in_square,
                "inside_stored_polygon": in_polygon,
                "nearest_square_boundary_km": float(50 - max(abs(east), abs(north))),
            }
        )
        print(row["sample_id"], f"east={east:.3f} km north={north:.3f} km inside={in_square}")
    write_json(
        root / "outputs/research/oytag_overlap.json",
        {
            "candidate_id": candidate["candidate_id"],
            "center": {"lat": 39, "lon": 75},
            "sphere_radius_m": EARTH_RADIUS_M,
            "window_km": 100,
            "method": "spherical azimuthal equidistant coordinates and independent stored-polygon containment",
            "coordinate_caveat": "Published table does not specify datum; approximate overlap only, not survey navigation",
            "evidence_scope": "Selected published rock samples only; no mineral polygons or gypsum sample coordinates",
            "inputs": [
                {
                    "path": str(p.relative_to(root)),
                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                }
                for p in inputs
            ],
            "samples": records,
        },
    )
    assert len(records) == 3 and all(r["inside_local_100km_square"] for r in records)
    print("Three sample containment checks passed; no mineral scores or rankings changed")


if __name__ == "__main__":
    main()
