"""Locate published Oytag samples in the existing Gale Earth candidate window."""

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from shapely.geometry import Point, Polygon

from analog import evidence_status as es
from analog.provenance import write_json
from analog.screening import EARTH_RADIUS_M

CANDIDATE_ID = "gale-01"


def main():
    root = Path(__file__).resolve().parents[1]
    inputs = [
        root / "outputs/analysis/results_with_context.json",
        root / "outputs/research/oytag_literature_points.csv",
    ]
    candidate = next(
        c
        for c in json.loads(inputs[0].read_text())["candidates"]["gale"]
        if c["candidate_id"] == CANDIDATE_ID
    )
    assert (candidate["lat"], candidate["lon"]) == (39, 75)
    polygon = Polygon(candidate["footprint"])
    supplement = root / "outputs/research/oytag_supplement_coordinates.csv"
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
                "latitude_deg": lat,
                "longitude_deg": lon,
                "east_km": float(east),
                "north_km": float(north),
                "inside_local_100km_square": in_square,
                "inside_stored_polygon": in_polygon,
                "nearest_square_boundary_km": float(50 - max(abs(east), abs(north))),
            }
        )
        print(row["sample_id"], f"east={east:.3f} km north={north:.3f} km inside={in_square}")
    # The two published point sets come from different tables; keep them apart.
    supplement_ids = {r["parent_sample_id"] for r in csv.DictReader(supplement.open())}
    shared = sorted(supplement_ids & {r["sample_id"] for r in records})
    assert not shared, f"Point sets share sample IDs: {shared}"
    write_json(
        root / "outputs/research/oytag_overlap.json",
        {
            "schema_version": es.SCHEMA_VERSION,
            "generated_utc": es.generated_utc(),
            "candidate_id": candidate["candidate_id"],
            "center": {"lat": float(candidate["lat"]), "lon": float(candidate["lon"])},
            "local_axes": "east_km/north_km from the window centre (azimuthal equidistant)",
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
            "claims": [
                es.claim(
                    "samples_inside_window",
                    "All 3 published sample coordinates fall inside the 100x100 km window",
                    es.VERIFIED,
                    "Recomputed here; table datum unstated, so approximate overlap only",
                ),
                es.claim(
                    "reported_lithology",
                    "Samples are mudstone, limestone and sandstone",
                    es.EXTERNAL,
                    "Rock types as reported by the publication; not re-measured",
                    source="doi:10.1016/j.jseaes.2011.04.020 Table 1",
                ),
            ],
            "related_point_sets": [
                {
                    "path": str(supplement.relative_to(root)),
                    "sha256": hashlib.sha256(supplement.read_bytes()).hexdigest(),
                    "id_field": "parent_sample_id",
                    "role": "Table DR1 zircon U-Pb parent-rock coordinates; not lithology samples",
                    "shared_sample_ids": shared,
                }
            ],
        },
    )
    assert len(records) == 3 and all(r["inside_local_100km_square"] for r in records)
    print("Three sample containment checks passed; no mineral scores or rankings changed")


if __name__ == "__main__":
    main()
