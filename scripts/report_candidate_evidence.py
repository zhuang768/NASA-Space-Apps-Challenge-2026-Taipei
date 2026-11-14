"""Reproduce three existing terrain candidate evidence records without reranking."""

import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

from analog.matching import FEATURES, terrain_distance
from analog.provenance import write_json


def main():
    root = Path(__file__).resolve().parents[1]
    paths = [
        "outputs/analysis/results_with_context.json",
        "outputs/analysis/sensitivity.json",
        "outputs/analysis_scale10km/results.json",
        "outputs/mars_profiles/profiles.json",
    ]
    base, sensitivity, coarse, profiles = [json.loads((root / p).read_text()) for p in paths]
    records = []
    for target, lat, lon in [("gale", 39, 75), ("arcadia", 29, -105), ("arcadia", 35, 57)]:
        item = next(i for i in base["candidates"][target] if (i["lat"], i["lon"]) == (lat, lon))
        calculated = float(
            terrain_distance(
                [item[f] for f in FEATURES],
                np.array([base["targets"][target][f] for f in FEATURES]),
            )
        )
        assert np.isclose(calculated, item["terrain_distance"], atol=1e-6)
        configurations = {
            "base_4km": (lat, lon) in [tuple(x) for x in sensitivity[target]["base_4km_top2"]],
            "alternative_10km": (lat, lon)
            in [tuple(x) for x in sensitivity[target]["alternative_10km_top2"]],
        }
        for name, scenario in sensitivity[target]["weight_variants"].items():
            configurations[name] = (lat, lon) in [tuple(x) for x in scenario["separated_top2"]]
        raw = next(
            (i for i in coarse["candidates"][target] if (i["lat"], i["lon"]) == (lat, lon)), None
        )
        records.append(
            {
                "candidate": item,
                "mars_profile": profiles["profiles"][target],
                "recalculated_distance": calculated,
                "top2_in_tested_configurations": configurations,
                "top2_count": sum(configurations.values()),
                "configurations_count": len(configurations),
                "coarse_shortlist_rank": raw["rank"] if raw else None,
                "interpretation": "existing terrain shortlist; not calibrated confidence or a new ranking",
            }
        )
    write_json(
        root / "outputs/research/three_candidate_evidence.json",
        {
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip(),
            "inputs": [
                {"path": p, "sha256": hashlib.sha256((root / p).read_bytes()).hexdigest()}
                for p in paths
            ],
            "parameters": base["parameters"],
            "search_counts": base["counts"],
            "records": records,
        },
    )
    for r in records:
        i = r["candidate"]
        print(
            i["candidate_id"],
            {f: i[f] for f in FEATURES},
            r["top2_count"],
            "/",
            r["configurations_count"],
        )
    print("Three stored terrain distances independently recomputed from stored features: passed")


if __name__ == "__main__":
    main()
