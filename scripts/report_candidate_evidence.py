"""Reproduce three existing terrain candidate evidence records without reranking.

Run after scripts.check_oytag_overlap and scripts.check_oytag_transect, whose
claims are folded into the literature status of gale-01.
"""

import hashlib
import json
import os
import subprocess
from pathlib import Path

import numpy as np

from analog import evidence_status as es
from analog.matching import FEATURES, terrain_distance
from analog.provenance import write_json

# (candidate_id, mars_target, lat, lon); lat/lon asserted against the stored record.
FEATURED = [
    ("gale-01", "gale", 39, 75),
    ("arcadia-01", "arcadia", 29, -105),
    ("arcadia-02", "arcadia", 35, 57),
]
LITERATURE_FILES = {
    "gale-01": [
        "outputs/research/oytag_overlap.json",
        "outputs/research/oytag_transect_check.json",
    ],
}
DISTANCE_ATOL = 1e-6


def source_commit(root):
    if os.environ.get("SOURCE_COMMIT"):
        return os.environ["SOURCE_COMMIT"]
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


def literature(root, candidate_id):
    files = LITERATURE_FILES.get(candidate_id, [])
    if not files:
        return {"status": "not_checked", "evidence_files": [], "claims": []}
    claims = [c for f in files for c in json.loads((root / f).read_text())["claims"]]
    return {
        # checked_partial: literature was checked, and some claims remain UNVERIFIED.
        "status": "checked_partial"
        if any(c["level"] == es.UNVERIFIED for c in claims)
        else "checked",
        "evidence_files": files,
        "claims": claims,
    }


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
    for candidate_id, target, lat, lon in FEATURED:
        item = dict(
            next(i for i in base["candidates"][target] if i["candidate_id"] == candidate_id)
        )
        assert (item["lat"], item["lon"]) == (lat, lon), candidate_id
        calculated = float(
            terrain_distance(
                [item[f] for f in FEATURES],
                np.array([base["targets"][target][f] for f in FEATURES]),
            )
        )
        assert np.isclose(calculated, item["terrain_distance"], atol=DISTANCE_ATOL)
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
        lit = literature(root, candidate_id)
        # The copied ranking record predates the literature check; keep it consistent.
        item["prior_analog_literature_status"] = lit["status"]
        records.append(
            {
                "candidate_id": candidate_id,
                "mars_target": target,
                "candidate": item,
                "distance_check": {
                    "recomputed": calculated,
                    "stored": item["terrain_distance"],
                    "atol": DISTANCE_ATOL,
                    "matches": True,
                },
                "top2_in_tested_configurations": configurations,
                "top2_count": sum(configurations.values()),
                "configurations_count": len(configurations),
                "scale10km_rank": raw["rank"] if raw else None,
                "prior_analog_literature": lit,
                "interpretation": "existing terrain shortlist; not calibrated confidence or a new ranking",
            }
        )
    research_inputs = sorted({f for files in LITERATURE_FILES.values() for f in files})
    write_json(
        root / "outputs/research/three_candidate_evidence.json",
        {
            "schema_version": es.SCHEMA_VERSION,
            "generated_utc": es.generated_utc(),
            "source_commit": source_commit(root),
            "inputs": [
                {"path": p, "sha256": hashlib.sha256((root / p).read_bytes()).hexdigest()}
                for p in paths + research_inputs
            ],
            "field_notes": {
                "candidate_id": "Canonical key; matches outputs/analysis/results_with_context.json",
                "candidate.rank": "Rank in the base 4 km terrain run",
                "scale10km_rank": "Rank in outputs/analysis_scale10km; null = not among that run's 12 candidates",
                "candidate.footprint": "Polygon vertices as [lon, lat] pairs (EPSG:4326)",
                "top2_count": "Configurations (of configurations_count) keeping the candidate in Top-2; not probability or confidence",
                "prior_analog_literature.status": "not_checked | checked_partial (some claims UNVERIFIED) | checked",
                "claims[].level": "VERIFIED | INFERRED | EXTERNAL | UNVERIFIED; support type, not confidence",
            },
            "parameters": base["parameters"],
            "search_counts": base["counts"],
            "mars_profiles": {t: profiles["profiles"][t] for t in sorted({r[1] for r in FEATURED})},
            "records": records,
        },
    )
    for r in records:
        i = r["candidate"]
        print(
            r["candidate_id"],
            {f: i[f] for f in FEATURES},
            r["top2_count"],
            "/",
            r["configurations_count"],
            r["prior_analog_literature"]["status"],
        )
    print("Three stored terrain distances independently recomputed from stored features: passed")


if __name__ == "__main__":
    main()
