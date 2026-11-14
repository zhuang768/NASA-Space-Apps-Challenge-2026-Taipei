"""Export existing matching results and explanatory figures; never rerank candidates."""

import hashlib
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analog.matching import FEATURES, terrain_distance

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/matching_handoff"


def main():
    OUT.mkdir(exist_ok=True)
    paths = [
        "outputs/analysis/results_with_context.json",
        "outputs/analysis/sensitivity.json",
        "outputs/mars_profiles/profiles.json",
        "outputs/analysis/candidates.geojson",
    ]
    base, sensitivity, mars, geo = [json.loads((ROOT / p).read_text()) for p in paths]
    identifiers = set()
    records = []
    for target, candidates in base["candidates"].items():
        tv = np.array([base["targets"][target][f] for f in FEATURES])
        for candidate in candidates:
            cid = candidate["candidate_id"]
            assert cid not in identifiers
            identifiers.add(cid)
            values = np.array([candidate[f] for f in FEATURES])
            terms = (
                np.abs(values - tv)
                / np.array(base["parameters"]["distance_tolerances"])
                * np.array(base["parameters"]["within_terrain_weights"])
            )
            distance = float(terrain_distance(values, tv))
            assert np.isclose(distance, candidate["terrain_distance"], atol=1e-6)
            assert np.isclose(terms.sum(), distance)
            context = candidate.get("earth_climate_context")
            records.append(
                {
                    **candidate,
                    "terrain_distance_components": dict(zip(FEATURES, terms.tolist())),
                    "themes": {
                        "terrain": "scored",
                        "temperature": "not_scored",
                        "water_ice": "not_scored",
                        "atmosphere_dust": "not_scored",
                    },
                    "has_power_context": context is not None,
                }
            )
    assert len(records) == sum(map(len, base["candidates"].values()))
    assert len(geo["features"]) == len(records)
    captions = {
        "terrain_distance_components": "Top two stored candidates per target. Stacked terms sum to the terrain distance; lower is closer in three regional statistics only. No environmental score or confidence is implied. ETOPO 2022 / MGS MOLA; 100 km windows, 4 km sampling, 8 km slope stencil. Weights and tolerances are uncalibrated design assumptions.",
        "top2_sensitivity": "Number of baseline top-two candidates retained under each setting, out of two. Weight variants use the same candidate set. The 10 km sampling run changes the eligible set, so it is a pipeline sensitivity check, not an isolated precision test or confidence estimate.",
    }
    manifest = {
        "schema_version": "1.0",
        "analysis_type": base["analysis_type"],
        "input_analysis_generated_utc": base["generated_utc"],
        "input_analysis_base_commit": base["base_commit"],
        "inputs": [
            {"path": p, "sha256": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()}
            for p in paths
        ],
        "parameters": base["parameters"],
        "counts": base["counts"],
        "targets": base["targets"],
        "candidates": records,
        "mars_profiles": mars["profiles"],
        "earth_sources": base["sources"],
        "mars_sources": mars["sources"],
        "sensitivity": sensitivity,
        "missing_requirements": mars["missing_requirements"],
        "footprints_path": "outputs/analysis/candidates.geojson",
        "captions": captions,
        "checks": {
            "unique_candidate_ids": True,
            "all_stored_distances_recomputed": True,
            "distance_components_sum": True,
            "footprint_count_matches": True,
        },
        "limitations": base["limitations"],
        "dust_license_path": "outputs/mars_profiles/LICENSE-data.md",
    }
    (OUT / "matching_data.json").write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n")
    plt.rcParams.update(
        {
            "figure.facecolor": "#101923",
            "axes.facecolor": "#152331",
            "text.color": "#e4ebef",
            "axes.labelcolor": "#b9cbd5",
            "xtick.color": "#b9cbd5",
            "ytick.color": "#b9cbd5",
            "axes.edgecolor": "#486171",
            "font.size": 10,
        }
    )
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.subplots_adjust(bottom=0.25, top=0.78, wspace=0.5)
    for ax, (target, candidates) in zip(axes, base["candidates"].items()):
        subset = [
            next(r for r in records if r["candidate_id"] == c["candidate_id"])
            for c in candidates[:2]
        ]
        left = np.zeros(len(subset))
        for feature, color, label in zip(
            FEATURES, ["#45c7c3", "#90a9bc", "#efa25d"], ["Median slope", "Slope P90", "Relief"]
        ):
            values = np.array([r["terrain_distance_components"][feature] for r in subset])
            ax.barh(
                [r["candidate_id"] for r in subset], values, left=left, color=color, label=label
            )
            left += values
        ax.invert_yaxis()
        ax.set_title(target.title(), color="#e4ebef")
        ax.set_xlabel("Terrain distance (lower is closer)")
        ax.set_xlim(0, max(left) * 1.15)
    handles, legend_labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        legend_labels,
        loc="center",
        bbox_to_anchor=(0.5, 0.87),
        ncol=3,
        facecolor="#152331",
        labelcolor="#e4ebef",
    )
    fig.suptitle("What contributes to each terrain match?", fontsize=17, y=0.98)
    fig.text(
        0.5,
        0.055,
        "Top two per target | Independent panel scales | 100 km windows; 4 km samples\nTerrain only; not confidence, geology, climate, ice or landing safety",
        ha="center",
        fontsize=10,
    )
    for suffix in ["png", "svg"]:
        fig.savefig(OUT / f"terrain_distance_components.{suffix}", dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(11, 5.4))
    fig.subplots_adjust(bottom=0.23, top=0.82)
    labels = list(sensitivity)
    names = ["alternative_10km", "slope_emphasis", "relief_emphasis"]
    for j, (name, color) in enumerate(zip(names, ["#efa25d", "#45c7c3", "#90a9bc"])):
        vals = [
            sensitivity[t]["top2_overlap_count"]
            if name == "alternative_10km"
            else sensitivity[t]["weight_variants"][name]["top2_overlap_count"]
            for t in labels
        ]
        ax.bar(np.arange(len(labels)) + (j - 1) * 0.23, vals, width=0.23, label=name, color=color)
    ax.set(
        xticks=np.arange(len(labels)),
        xticklabels=[t.title() for t in labels],
        yticks=[0, 1, 2],
        ylim=(0, 2.65),
        ylabel="Baseline top-two retained (out of 2)",
    )
    ax.legend(facecolor="#152331", labelcolor="#e4ebef", loc="upper center", ncol=3)
    ax.set_title(
        "Recommendation changes across tested settings", fontsize=16, color="#e4ebef", pad=18
    )
    fig.text(
        0.5,
        0.05,
        "10 km run changes eligible windows; weight variants keep the candidate set fixed.\nRetention is not confidence. Source: outputs/analysis/sensitivity.json",
        ha="center",
        fontsize=10,
    )
    for suffix in ["png", "svg"]:
        fig.savefig(OUT / f"top2_sensitivity.{suffix}", dpi=180)
    plt.close(fig)
    print(
        f"Exported {len(records)} candidates; {sum(r['has_power_context'] for r in records)} with POWER context. All export checks passed."
    )


if __name__ == "__main__":
    main()
