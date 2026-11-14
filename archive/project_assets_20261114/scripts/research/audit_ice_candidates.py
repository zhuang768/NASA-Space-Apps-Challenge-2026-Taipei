"""Audit the two retained ice candidates, without scoring or changing the Mars stack.

Run: .venv/bin/python scripts/research/audit_ice_candidates.py
Reads existing native products; writes only outputs/research/ice_candidate_followup/.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.patches import Rectangle

from analog import mars, swim
from analog.terrain import slope_deg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/research/ice_candidate_followup"
CATALOG = ROOT / "outputs/mars_discovery/mars_site_discovery.json"
STACK = ROOT / "data/processed/mars_stack_0p5deg.nc"


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def crop(grid: xr.DataArray, lat: float, lon: float, half_width: float) -> xr.DataArray:
    return grid.sel(
        lat=slice(lat + half_width, lat - half_width),
        lon=slice(lon - half_width, lon + half_width),
    )


def stats(grid: xr.DataArray) -> dict:
    values = np.asarray(grid.values, dtype="float64")
    valid = values[np.isfinite(values)]
    return {
        "shape": list(values.shape),
        "total_pixels": int(values.size),
        "valid_pixels": int(valid.size),
        "mean": float(valid.mean()) if valid.size else None,
        "min": float(valid.min()) if valid.size else None,
        "max": float(valid.max()) if valid.size else None,
        "std_population": float(valid.std()) if valid.size else None,
    }


def bracket(values: np.ndarray, target: float) -> list[tuple[int, float]]:
    order = np.argsort(values)
    coordinates = values[order]
    pos = int(np.searchsorted(coordinates, target))
    if pos < len(coordinates) and abs(coordinates[pos] - target) < 1e-10:
        return [(int(order[pos]), 1.0)]
    if pos == 0 or pos == len(coordinates):
        raise ValueError("Candidate lies outside the native coarse grid")
    weight = (target - coordinates[pos - 1]) / (coordinates[pos] - coordinates[pos - 1])
    return [(int(order[pos - 1]), float(1 - weight)), (int(order[pos]), float(weight))]


def great_circle_km(lat: float, lon: float, other_lat: float, other_lon: float) -> float:
    a, b = np.deg2rad([lat, other_lat])
    dlon = np.deg2rad(other_lon - lon)
    haversine = np.sin((b - a) / 2) ** 2 + np.cos(a) * np.cos(b) * np.sin(dlon / 2) ** 2
    return float(2 * mars.MARS_RADIUS_M / 1000 * np.arcsin(np.sqrt(np.clip(haversine, 0, 1))))


def swim_evidence(grid: xr.DataArray, lat: float, lon: float) -> dict:
    # Follow the existing loader's coordinates, then the stack's 10x10 mean + interpolation.
    coarse = grid.coarsen(lat=10, lon=10, boundary="trim").mean()
    contributors = []
    for row, wy in bracket(coarse.lat.values, lat):
        for col, wx in bracket(coarse.lon.values, lon):
            block = grid.isel(lat=slice(row * 10, (row + 1) * 10),
                              lon=slice(col * 10, (col + 1) * 10))
            contributors.append({
                "coarse_center": [float(coarse.lat[row]), float(coarse.lon[col])],
                "weight": wy * wx,
                "coarse_mean_float32": float(coarse[row, col]),
                "native_block_stats": stats(block),
            })
    interpolated = float(coarse.interp(lat=lat, lon=lon))
    reconstructed = sum(c["weight"] * c["coarse_mean_float32"] for c in contributors)
    assert abs(reconstructed - interpolated) < 1e-10
    assert abs(sum(c["weight"] for c in contributors) - 1) < 1e-12
    return {
        "nominal_cell_native_stats": stats(crop(grid, lat, lon, 0.25)),
        "coarsened_then_interpolated": interpolated,
        "contributing_blocks": contributors,
        "note": "Grid samples are not independent observations. Positive values are not ice fractions.",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    protected = [CATALOG, STACK, ROOT / "scripts/discover_mars_sites.py"]
    protected += sorted((ROOT / "analog").glob("*.py"))
    protected += sorted((ROOT / "outputs/mars_discovery/figures").glob("*.png"))
    before = {p.relative_to(ROOT).as_posix(): sha256(p) for p in protected}

    catalog = json.loads(CATALOG.read_text())
    picks = catalog["purposes"]["isru_shallow_ice"]["picks"][:2]
    assert [(p["lat"], p["lon"]) for p in picks] == [(54.25, 1.25), (53.75, 42.25)]
    dem = mars.load("mola_topography").astype("float32")
    ti = mars.load("tes_thermal_inertia_night").astype("float32")
    mask = mars.load("tes_thermal_inertia_night_mask")
    shallow = swim.load("ice_consistency_shallow")
    deep = swim.load("ice_consistency_deep")
    fig, axes = plt.subplots(2, 3, figsize=(12, 7.4), layout="constrained")
    candidates = []

    with xr.open_dataset(STACK, engine="scipy") as stack:
        for index, pick in enumerate(picks):
            lat, lon = pick["lat"], pick["lon"]
            source_ti = crop(ti, lat, lon, 0.25)
            source_mask = crop(mask, lat, lon, 0.25)
            valid_ti = source_ti.where(
                (source_ti >= 5) & (source_ti <= 5000) & (source_mask != 0)
            )
            terrain_region = crop(dem, lat, lon, 1)
            terrain_cell = crop(terrain_region, lat, lon, 0.25)
            slopes = crop(slope_deg(terrain_region, mars.MARS_RADIUS_M), lat, lon, 0.25)
            s0, s1 = swim_evidence(shallow, lat, lon), swim_evidence(deep, lat, lon)
            stored = {k: float(v) for k, v in stack.sel(lat=lat, lon=lon).data_vars.items()}
            assert stored == pick["layers"]
            recomputed = {
                "slope": float(slopes.mean()),
                "relief": float(terrain_cell.max() - terrain_cell.min()),
                "thermal_inertia": float(valid_ti.mean()),
                "ice_shallow": s0["coarsened_then_interpolated"],
            }
            errors = {k: recomputed[k] - stored[k] for k in recomputed}
            for key, error in errors.items():
                assert abs(error) < (5e-5 if key == "thermal_inertia" else 1e-8), (key, error)
            meridian_km = np.pi * mars.MARS_RADIUS_M / 180 / 1000
            record = {
                "id": f"I-{index + 1:02d}",
                "center_lat_lon": [lat, lon],
                "stored_score_unchanged": pick["score"],
                "stored_layers": stored,
                "nominal_cell_bounds": {
                    "south": lat - 0.25, "north": lat + 0.25,
                    "west": lon - 0.25, "east": lon + 0.25,
                },
                "nominal_size_km_NS_EW_at_center": [
                    meridian_km * 0.5, meridian_km * 0.5 * np.cos(np.deg2rad(lat)),
                ],
                "mola_native_cell": stats(terrain_cell),
                "mola_native_cell_slopes": stats(slopes),
                "tes_native_unmasked_cell": stats(source_ti),
                "tes_native_non_infilled_cell": stats(valid_ti),
                "tes_mask_zero_pixels_excluded": int((source_mask == 0).sum()),
                "swim_0_1m": s0,
                "swim_1_5m_context_only": s1,
                "native_recomputed_minus_stored": errors,
                "nominal_2015_EZ_screen": {
                    "assumption": "All centers at <=50N, circular radius 100 km, not actual polygons",
                    "minimum_cell_distance_to_50N_km": (lat - 0.25 - 50) * meridian_km,
                    "clearance_beyond_nominal_100km_radius_km":
                        (lat - 0.25 - 50) * meridian_km - 100,
                    "interpretation": "Outside this nominal envelope only; not novelty clearance",
                },
                "published_comparator_center_distances_km": {
                    "Protonilus_2015_EZ_42.187N_48.062E":
                        great_circle_km(lat, lon, 42.187, 48.062),
                    "AP1_Luzzi2025_39.8N_202.1E": great_circle_km(lat, lon, 39.8, 202.1),
                    "AP8_Luzzi2025_40.75N_201.3E": great_circle_km(lat, lon, 40.75, 201.3),
                    "AP9_Luzzi2025_40.02N_203.35E": great_circle_km(lat, lon, 40.02, 203.35),
                    "Dundas2021_Fig14a_crater_41.4N_48.8E":
                        great_circle_km(lat, lon, 41.4, 48.8),
                    "Dundas2021_Fig14b_crater_41.9N_36.4E":
                        great_circle_km(lat, lon, 41.9, 36.4),
                },
            }
            candidates.append(record)
            for column, (grid, title) in enumerate([
                (shallow, "SWIM 2.0: 0-1 m"), (deep, "SWIM 2.0: 1-5 m"),
                (dem, "MOLA elevation (m)"),
            ]):
                region = crop(grid, lat, lon, 1)
                ax = axes[index, column]
                plot_options = {"cmap": "coolwarm", "vmin": -1, "vmax": 1} if column < 2 else {
                    "cmap": "terrain",
                }
                mesh = ax.pcolormesh(region.lon, region.lat, region, shading="nearest", **plot_options)
                fig.colorbar(mesh, ax=ax, shrink=0.82, label="consistency" if column < 2 else "m")
                ax.add_patch(Rectangle((lon - 0.25, lat - 0.25), 0.5, 0.5, fill=False,
                                       edgecolor="black", linewidth=1.5))
                ax.plot(lon, lat, marker="+", color="black", markersize=7)
                ax.set(title=f"{record['id']} | {title}", xlabel="East longitude (deg)",
                       ylabel="Planetocentric latitude (deg)")
                ax.set_aspect(1 / np.cos(np.deg2rad(lat)))
    fig.suptitle("Native raster context | black box: nominal 0.5-degree cell\n"
                 "Shared SWIM inputs; no independent ice confirmation or landing assessment", fontsize=12)
    fig.savefig(OUT / "native_context.png", dpi=150)
    plt.close(fig)

    manifest = json.loads((ROOT / "outputs/mars_profiles/profiles.json").read_text())
    raw_sources = []
    for source in manifest["sources"]:
        if source["file"] in {
            "megt90n000eb.img", "megt90n000eb.lbl", "global_ti_night_2007.img",
            "global_ti_night_2007.lbl", "global_ti_msk_night_2007.img",
            "global_ti_msk_night_2007.lbl", "SWIM2_c0_1.tif", "SWIM2_c1_5.tif",
        }:
            actual = sha256(ROOT / "data/raw/mars" / source["file"])
            assert actual == source["sha256"], source["file"]
            raw_sources.append({"file": source["file"], "url": source["url"], "sha256": actual})
    assert len(raw_sources) == 8
    after = {p.relative_to(ROOT).as_posix(): sha256(p) for p in protected}
    assert before == after, "A protected input changed while auditing"
    result = {
        "generated_utc": datetime.now(UTC).isoformat(),
        "scope": "Source QA for original I-01 and I-02 only. No rescoring or reranking.",
        "candidates": candidates,
        "raw_sources_verified_against_profiles_manifest": raw_sources,
        "protected_inputs_sha256": before,
        "protected_inputs_unchanged": True,
        "dust_note": "Matched JSON to stack only; no native dust reprocessing in this follow-up.",
        "deep_ice_note": "Not part of the original score; context only and shares shallow-product inputs.",
        "novelty_status": "unchecked_exact_site; nominal 2015 envelope screen is a bounded subcheck",
    }
    (OUT / "native_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: two candidates, all five JSON/stack layers, four native reconstructions each,")
    print("eight native source hashes and protected inputs; no scores changed.")
    for c in candidates:
        print(c["id"], "TES valid", c["tes_native_non_infilled_cell"]["valid_pixels"],
              "/100; SWIM nominal", c["swim_0_1m"]["nominal_cell_native_stats"])
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
