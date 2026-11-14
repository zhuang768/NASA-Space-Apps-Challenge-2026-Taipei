"""Reproducible global-band terrain screening; four-theme ranking remains pending."""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from shapely import contains_xy

from analog import earth, mars
from analog.matching import FEATURES, TOLERANCES, WEIGHTS, select_separated, terrain_distance
from analog.provenance import source_record, write_json
from analog.screening import (
    EARTH_RADIUS_M,
    EXCLUDED,
    TARGETS,
    land_geometry,
    patch_features,
    sample_patch,
    search_centres,
)

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--step", type=float, default=2.0, help="Earth candidate centre step in degrees"
    )
    parser.add_argument("--spacing-km", type=float, default=4.0)
    parser.add_argument("--window-km", type=float, default=100.0)
    parser.add_argument("--top", type=int, default=12)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/analysis")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    terrain = earth.load_terrain()
    mola = mars.load("mola_topography").astype("float32")
    land = land_geometry(earth.RAW_DIR / "ne_110m_land.zip")
    latitudes, longitudes = search_centres(land, args.step)
    rows, excluded_water = [], 0
    for lat, lon in zip(latitudes, longitudes):
        patch, qlat, qlon = sample_patch(
            terrain, lat, lon, EARTH_RADIUS_M, args.spacing_km, args.window_km
        )
        fraction = float(contains_xy(land, qlon, qlat).mean())
        if fraction < 0.95:
            excluded_water += 1
            continue
        features = patch_features(patch, args.spacing_km)
        if not np.isfinite(features).all():
            continue
        rows.append(
            {
                "lat": float(lat),
                "lon": float(lon),
                "land_fraction": fraction,
                **dict(zip(FEATURES, map(float, features))),
            }
        )
    columns = ["lat", "lon", "land_fraction", *FEATURES]
    table = pd.DataFrame(rows, columns=columns)
    table.to_csv(args.output / "earth_terrain_features.csv", index=False)
    all_results, targets = {}, {}
    for name, target in TARGETS.items():
        patch, _, _ = sample_patch(
            mola, target["lat"], target["lon"], mars.MARS_RADIUS_M, args.spacing_km, args.window_km
        )
        vector = patch_features(patch, args.spacing_km)
        targets[name] = {**target, **dict(zip(FEATURES, map(float, vector)))}
        if table.empty:
            all_results[name] = []
            continue
        distances = terrain_distance(table[list(FEATURES)].values, vector)
        table[f"{name}_terrain_distance"] = distances
        indices = select_separated(table.lat.values, table.lon.values, distances, args.top, 300)
        selected = []
        base_top = set(select_separated(table.lat.values, table.lon.values, distances, 2, 300))
        variants = {}
        for label, weights in [
            ("slope_emphasis", [0.4, 0.4, 0.2]),
            ("relief_emphasis", [0.1, 0.1, 0.8]),
        ]:
            alt = terrain_distance(table[list(FEATURES)].values, vector, weights=weights)
            order = np.argsort(alt, kind="stable")
            ranks = np.empty(len(order), dtype=int)
            ranks[order] = np.arange(1, len(order) + 1)
            variants[label] = ranks
            alt_top = set(select_separated(table.lat.values, table.lon.values, alt, 2, 300))
            print(f"{name}: {label} separated top-2 overlap {len(base_top & alt_top)}/2")
        # Full grid ranking is retained, including candidates not shown in the shortlist.
        full = table[["lat", "lon", *FEATURES, f"{name}_terrain_distance"]].copy()
        for label, ranks in variants.items():
            full[f"{label}_raw_rank"] = ranks
        full.sort_values(f"{name}_terrain_distance", kind="stable").to_csv(
            args.output / f"{name}_all_ranked.csv", index=False
        )
        for rank, index in enumerate(indices, 1):
            row = rows[index]
            _, qlat, qlon = sample_patch(
                terrain, row["lat"], row["lon"], EARTH_RADIUS_M, args.spacing_km, args.window_km
            )
            ring = [
                [float(qlon[0, 0]), float(qlat[0, 0])],
                [float(qlon[0, -1]), float(qlat[0, -1])],
                [float(qlon[-1, -1]), float(qlat[-1, -1])],
                [float(qlon[-1, 0]), float(qlat[-1, 0])],
                [float(qlon[0, 0]), float(qlat[0, 0])],
            ]
            selected.append(
                {
                    **row,
                    "candidate_id": f"{name}-{rank:02d}",
                    "rank": rank,
                    "mars_target": name,
                    "terrain_distance": float(distances[index]),
                    "sensitivity_raw_ranks": {k: int(v[index]) for k, v in variants.items()},
                    "status": "project-proposed, unvalidated regional terrain candidate",
                    "temperature_status": "unknown",
                    "water_ice_status": "unknown",
                    "air_status": "unknown",
                    "logistics_status": "unknown",
                    "prior_analog_literature_status": "not_checked",
                    "footprint": ring,
                }
            )
        all_results[name] = selected
    table.to_csv(args.output / "earth_terrain_features.csv", index=False)
    records = json.loads((earth.RAW_DIR / "public_sources.json").read_text())
    for path in [mars.RAW_DIR / "megt90n000eb.img", mars.RAW_DIR / "megt90n000eb.lbl"]:
        records.append(
            source_record(
                path,
                mars.PRODUCTS["mola_topography"].rsplit("/", 1)[0] + "/" + path.name,
                dataset="MGS MOLA MEGDR",
                dataset_id="MGS-M-MOLA-5-MEGDR-L3-V1.0",
                version="2.0",
                period="1997-09-15 to 2001-06-30 (source label)",
                units="m above Mars areoid",
                resolution="16 pixels per degree",
                crs="Mars simple cylindrical, east-positive planetocentric",
            )
        )
    result = {
        "analysis_type": "terrain_only_screening",
        "generated_utc": datetime.now(UTC).isoformat(),
        "base_commit": "330666e",
        "parameters": {
            "earth_search_latitude_bounds": [-60, 60],
            "earth_centre_step_deg": args.step,
            "window_km": args.window_km,
            "sample_spacing_km": args.spacing_km,
            "slope_stencil_km": 2 * args.spacing_km,
            "earth_spherical_radius_m": EARTH_RADIUS_M,
            "mars_spherical_radius_m": mars.MARS_RADIUS_M,
            "minimum_sampled_land_fraction": 0.95,
            "shortlist_separation_km": 300,
            "excluded_boxes": EXCLUDED,
            "feature_order": FEATURES,
            "distance_tolerances": TOLERANCES.tolist(),
            "within_terrain_weights": WEIGHTS.tolist(),
        },
        "counts": {
            "land_centres_before_window_filter": len(latitudes),
            "water_window_exclusions": excluded_water,
            "valid_windows": len(table),
        },
        "targets": targets,
        "sources": records,
        "candidates": all_results,
        "limitations": [
            "No four-theme score; no calibrated probability or mission success rate.",
            "Novelty, minerals, climate, water/ice, accessibility and permits are unverified.",
            "2-degree centre sampling is incomplete and latitude-dependent; polar regions excluded.",
            "Bilinear interpolation and nominal scale matching do not establish subpixel detail.",
            "Regional topography does not establish rover traversability or landing safety.",
            "MOLA label reports interpolated bins and profile gaps up to 12 km near equator.",
            "Natural Earth mask is coarse and does not exclude every inland water body.",
        ],
    }
    write_json(args.output / "results.json", result)
    geo = {"type": "FeatureCollection", "features": []}
    for values in all_results.values():
        for item in values:
            props = {k: v for k, v in item.items() if k != "footprint"}
            geo["features"].append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [item["footprint"]]},
                    "properties": props,
                }
            )
    write_json(args.output / "candidates.geojson", geo)
    print(f"{len(table)} valid windows; saved {args.output}")
    for name, items in all_results.items():
        print(
            name,
            [(item["lat"], item["lon"], round(item["terrain_distance"], 4)) for item in items[:2]],
        )


if __name__ == "__main__":
    main()
