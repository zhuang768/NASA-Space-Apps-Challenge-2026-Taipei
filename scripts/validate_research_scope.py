"""Check terrain interpretation using a known analog region and a terrain contrast.

Does not alter candidate rankings or validate mineralogy/mission suitability.
"""

import hashlib
import json
from pathlib import Path

import numpy as np
from shapely import contains_xy

from analog import earth, mars
from analog.matching import FEATURES, TOLERANCES, WEIGHTS, terrain_distance
from analog.provenance import write_json
from analog.screening import EARTH_RADIUS_M, land_geometry, patch_features, sample_patch

ROOT = Path(__file__).resolve().parents[1]


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    stored = json.loads((ROOT / "outputs/analysis/results.json").read_text())
    raw_paths = [
        earth.RAW_DIR / earth.ETOPO_URL.rsplit("/", 1)[1],
        earth.RAW_DIR / "ne_110m_land.zip",
        mars.RAW_DIR / mars.PRODUCTS["mola_topography"].rsplit("/", 1)[1],
    ]
    raw_inputs = [{"path": str(p.relative_to(ROOT)), "sha256": file_hash(p)} for p in raw_paths]
    grid = earth.load_terrain()
    mola = mars.load("mola_topography").astype("float32")
    land = land_geometry(earth.RAW_DIR / "ne_110m_land.zip")
    targets = {}
    for name, target in stored["targets"].items():
        patch, _, _ = sample_patch(mola, target["lat"], target["lon"], mars.MARS_RADIUS_M)
        vector = patch_features(patch)
        assert np.allclose(vector, [target[f] for f in FEATURES], rtol=1e-6, atol=1e-5)
        targets[name] = vector
    records = []
    # Centers are project analysis choices, not paper sampling coordinates.
    for name, lat, lon, role in [
        (
            "Death Valley regional reference",
            36.25,
            -116.82,
            "known analog region; chosen regional center",
        ),
        (
            "Amazon terrain contrast",
            -3.0,
            -61.0,
            "project-designed low-relief contrast; not a universal non-analog",
        ),
    ]:
        patch, qlat, qlon = sample_patch(grid, lat, lon, EARTH_RADIUS_M)
        vector = patch_features(patch)
        land_fraction = float(contains_xy(land, qlon, qlat).mean())
        assert np.isfinite(vector).all()
        comparisons = {}
        for target, tv in targets.items():
            terms = WEIGHTS / WEIGHTS.sum() * np.abs(vector - tv) / TOLERANCES
            distance = float(terrain_distance(vector, tv))
            assert np.isclose(terms.sum(), distance, atol=1e-12)
            comparisons[target] = {
                "distance": distance,
                "contributions": dict(zip(FEATURES, terms.tolist())),
            }
        records.append(
            {
                "name": name,
                "lat": lat,
                "lon": lon,
                "role": role,
                "features": dict(zip(FEATURES, vector.tolist())),
                "sampled_land_fraction": land_fraction,
                "eligible_by_land_rule": land_fraction >= 0.95,
                "comparisons": comparisons,
            }
        )
    inputs = [ROOT / "outputs/analysis/results.json", ROOT / "data/raw/earth/public_sources.json"]
    write_json(
        ROOT / "outputs/research/reference_terrain_check.json",
        {
            "analysis_type": "limited_reference_interpretation_check",
            "raw_inputs": raw_inputs,
            "code_sha256": file_hash(Path(__file__)),
            "source_metadata": "outputs/analysis/results.json sources and docs/earth_pipeline.md",
            "parameters": {
                "window_km": 100,
                "spacing_km": 4,
                "slope_stencil_km": 8,
                "weights": WEIGHTS.tolist(),
                "tolerances": TOLERANCES.tolist(),
            },
            "inputs": [
                {
                    "path": str(p.relative_to(ROOT)),
                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                }
                for p in inputs
            ],
            "target_features_recomputed_match_stored": True,
            "records": records,
            "reference_source": "https://science.nasa.gov/earth/earth-observatory/mars-rover-curiosity-on-a-familiar-landscape-78860/",
            "limitations": [
                "Not a classification accuracy test",
                "No calibration or new candidate ranking",
                "Regional center is a design choice, not a located mineral sample",
                "Terrain-only distance cannot establish geology or environment",
                "Only two reference windows tested",
            ],
        },
    )
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
