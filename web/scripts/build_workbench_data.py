"""Build a typed JSON bundle for TerraMatch Mission Lab from existing repo outputs.

Reads only existing outputs under outputs/ without modifying any scientific
results or re-running rankings.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT_JSON = pathlib.Path(__file__).resolve().parents[1] / "src" / "data" / "workbenchData.json"
PUB_FIGURES = pathlib.Path(__file__).resolve().parents[1] / "public" / "figures"


def load_json(rel: str) -> dict:
    with open(ROOT / rel, encoding="utf-8") as f:
        return json.load(f)


def file_ref(rel: str) -> dict:
    return {"path": rel, "sha256": hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()}


def build_research() -> dict:
    """Featured deep-dive candidates and the Oytag literature overlay (gale-01)."""
    evidence_rel = "outputs/research/three_candidate_evidence.json"
    overlap_rel = "outputs/research/oytag_overlap.json"
    transect_rel = "outputs/research/oytag_transect_check.json"
    evidence = load_json(evidence_rel)
    overlap = load_json(overlap_rel)
    transect = load_json(transect_rel)
    assert evidence.get("schema_version") == "1.0", "Regenerate research outputs first"

    featured = {}
    for r in evidence["records"]:
        featured[r["candidate_id"]] = {
            "candidate_id": r["candidate_id"],
            "mars_target": r["mars_target"],
            "top2_in_tested_configurations": r["top2_in_tested_configurations"],
            "top2_count": r["top2_count"],
            "configurations_count": r["configurations_count"],
            "scale10km_rank": r["scale10km_rank"],
            "prior_analog_literature": r["prior_analog_literature"],
            "interpretation": r["interpretation"],
        }

    overlays = {
        overlap["candidate_id"]: {
            "candidate_id": overlap["candidate_id"],
            "center": overlap["center"],
            "window_km": overlap["window_km"],
            "local_axes": overlap["local_axes"],
            "coordinate_caveat": overlap["coordinate_caveat"],
            "evidence_scope": overlap["evidence_scope"],
            "samples": [
                {
                    k: s[k]
                    for k in (
                        "sample_id",
                        "latitude_deg",
                        "longitude_deg",
                        "reported_rock_type",
                        "source_doi",
                        "source_locator",
                        "coordinate_datum",
                        "east_km",
                        "north_km",
                        "inside_local_100km_square",
                    )
                }
                for s in overlap["samples"]
            ],
            "transect": {
                "source_doi": transect["source_doi"],
                "source_figures": transect["source_figures"],
                "source_url": transect["source_url"],
                "source_pdf_sha256": transect["source_pdf_sha256"],
                "source_transport": transect["source_transport"],
                "sensitivity": transect["sensitivity"],
                "endpoints": [
                    {
                        k: e[k]
                        for k in (
                            "label",
                            "approx_lat_deg",
                            "approx_lon_deg",
                            "east_km",
                            "north_km",
                            "inside",
                        )
                    }
                    for e in transect["endpoints"]
                ],
            },
            "claims": overlap["claims"] + transect["claims"],
        }
    }
    assert set(overlays) <= set(featured), "Overlay candidate missing from featured records"
    return {
        "schema_version": evidence["schema_version"],
        "source_commit": evidence["source_commit"],
        "files": [file_ref(evidence_rel), file_ref(overlap_rel), file_ref(transect_rel)],
        "featured": featured,
        "oytag_overlays": overlays,
    }


def build_mars_discovery() -> dict:
    """Package GPT handoff cards with layer values from the discovery JSON (no rerank)."""
    discovery_rel = "outputs/mars_discovery/mars_site_discovery.json"
    cards_rel = "outputs/mars_discovery/reporting_cards.json"
    discovery = load_json(discovery_rel)
    cards_doc = load_json(cards_rel)

    by_coord = {}
    for purpose_key, purpose in discovery.get("purposes", {}).items():
        for order, pick in enumerate(purpose.get("picks", []), start=1):
            by_coord[(round(pick["lat"], 2), round(pick["lon"], 2))] = {
                "purpose_key": purpose_key,
                "json_order": order,
                "score": pick["score"],
                "layers": pick["layers"],
                "excluded_known_sites": pick.get("excluded_known_sites", []),
            }

    enriched = []
    for card in cards_doc["cards"]:
        key = (round(card["lat"], 2), round(card["lon"], 2))
        match = by_coord.get(key)
        if match is None:
            raise SystemExit(f"Reporting card {card['id']} missing from discovery JSON")
        enriched.append(
            {
                **card,
                "descriptor_score": match["score"],
                "json_order": match["json_order"],
                "layers": match["layers"],
                "excluded_known_sites": match["excluded_known_sites"],
                "earth_analog": {
                    "status": "unknown",
                    "note": "Earth analog pairing is not completed for these Mars references; do not reuse old Earth terrain rankings.",
                },
                "themes": {
                    "terrain": {
                        "status": "displayed",
                        "slope_deg": match["layers"]["slope"],
                        "relief_m": match["layers"]["relief"],
                    },
                    "temperature": {
                        "status": "partial",
                        "thermal_inertia": match["layers"]["thermal_inertia"],
                        "regional_surface_temperature": "unknown",
                    },
                    "water_ice": {
                        "status": "displayed",
                        "ice_shallow": match["layers"]["ice_shallow"],
                    },
                    "atmosphere_dust": {
                        "status": "displayed",
                        "dust_cdod_my35": match["layers"]["dust_cdod"],
                    },
                },
            }
        )

    return {
        "schema_version": cards_doc["schema_version"],
        "earth_analog_pairing": cards_doc["earth_analog_pairing"],
        "novelty_policy": cards_doc["novelty_policy"],
        "firm_rocky_status": cards_doc["firm_rocky_status"],
        "limitations": discovery.get("limitations", []),
        "excluded_boxes": discovery.get("excluded_boxes", {}),
        "source_index": cards_doc.get("source_index", {}),
        "files": [file_ref(discovery_rel), file_ref(cards_rel)],
        "cards": enriched,
    }


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
        "research": build_research(),
        "mars_discovery": build_mars_discovery(),
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

    discovery_fig_dir = ROOT / "outputs" / "mars_discovery" / "figures"
    if discovery_fig_dir.exists():
        for png in discovery_fig_dir.glob("*.png"):
            shutil.copy2(png, PUB_FIGURES / png.name)

    print(f"Wrote {OUT_JSON} ({OUT_JSON.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
