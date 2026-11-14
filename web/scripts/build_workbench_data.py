"""Build a typed JSON bundle for TerraMatch Mission Lab from existing repo outputs.

Reads only existing outputs under outputs/ without modifying any scientific
results or re-running rankings.
"""

from __future__ import annotations

import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT_JSON = pathlib.Path(__file__).resolve().parents[1] / "src" / "data" / "workbenchData.json"
PUB_FIGURES = pathlib.Path(__file__).resolve().parents[1] / "public" / "figures"


def load_json(rel: str) -> dict:
    with open(ROOT / rel, encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    results = load_json("outputs/analysis/results_with_context.json")
    results_10km = load_json("outputs/analysis_scale10km/results.json")
    sensitivity = load_json("outputs/analysis/sensitivity.json")
    mars_profiles = load_json("outputs/mars_profiles/profiles.json")
    mars_temp = load_json("outputs/mars_temperature/summary.json")

    bundle = {
        "meta": {
            "app_name": "TerraMatch Mission Lab",
            "analysis_type": results.get("analysis_type"),
            "generated_utc": results.get("generated_utc"),
            "base_commit": results.get("base_commit"),
            "parameters": results.get("parameters"),
            "counts": results.get("counts"),
            "limitations": results.get("limitations", []),
        },
        "earth_sources": results.get("sources", []),
        "mars_sources": mars_profiles.get("sources", []),
        "mars_missing_requirements": mars_profiles.get("missing_requirements", []),
        "mars_dust_license": mars_profiles.get("dust_data_license"),
        "targets": {},
        "sensitivity": sensitivity,
        "scale10km_counts": results_10km.get("counts"),
        "rover_temperature_context": mars_temp,
    }

    for tid, tdata in results.get("targets", {}).items():
        mprof = mars_profiles.get("profiles", {}).get(tid, {})
        cands_4km = results.get("candidates", {}).get(tid, [])
        cands_10km = results_10km.get("candidates", {}).get(tid, [])
        bundle["targets"][tid] = {
            "id": tid,
            "summary": tdata,
            "mars_profile": mprof,
            "candidates": cands_4km,
            "candidates_10km_top2": [
                {"candidate_id": c.get("candidate_id"), "lat": c.get("lat"), "lon": c.get("lon"), "rank": c.get("rank"), "terrain_distance": c.get("terrain_distance")}
                for c in cands_10km[:2]
            ],
        }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)

    PUB_FIGURES.mkdir(parents=True, exist_ok=True)
    fig_dir = ROOT / "outputs" / "analysis" / "figures"
    if fig_dir.exists():
        for png in fig_dir.glob("*.png"):
            shutil.copy2(png, PUB_FIGURES / png.name)

    print(f"Wrote {OUT_JSON} ({OUT_JSON.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
