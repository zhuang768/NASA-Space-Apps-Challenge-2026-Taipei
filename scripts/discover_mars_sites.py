"""Purpose-driven Mars site discovery on the 0.5° stack.

Finds cells that match a task signature while excluding well-studied boxes
(Jezero, Gale, Arcadia, Utopia). Scores are experimental descriptors only —
not probability, novelty proof, or mission approval.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from analog import stack as stack_mod
from analog.score import similarity, top_cells
from analog.sites import SITES, Box, signature

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "mars_discovery"
FIGURE = OUT / "figures"

# Well-studied / already used as project targets — keep out of "new" shortlists.
EXCLUDE = {
    **SITES,
    "gale_crater": Box(south=-6.5, north=-3.5, west=136.5, east=139.5),
}

# Purpose signatures: medians + IQRs chosen from stack quantiles, not literature optima.
PURPOSES = {
    "isru_shallow_ice": {
        "label": "Shallow-ice / ISRU screening",
        "why": "Prefer mid-latitude cells with higher SWIM shallow-ice consistency and low slope.",
        "layers": {
            "ice_shallow": (0.35, 0.20),
            "slope": (0.3, 0.25),
            "relief": (80.0, 60.0),
            "dust_cdod": (0.12, 0.04),
        },
        "weights": {"ice_shallow": 2.0, "slope": 1.5, "relief": 1.0, "dust_cdod": 0.5},
        "lat_max": 60.0,
        "lat_min": 30.0,
    },
    "dusty_flat_ops": {
        "label": "Dusty flat-ops screening",
        "why": "Prefer low-slope plains with higher reconstructed dust optical depth.",
        "layers": {
            "dust_cdod": (0.20, 0.05),
            "slope": (0.25, 0.20),
            "relief": (60.0, 50.0),
            "thermal_inertia": (180.0, 40.0),
        },
        "weights": {"dust_cdod": 2.0, "slope": 1.5, "relief": 1.0, "thermal_inertia": 0.5},
        "lat_max": 50.0,
        "lat_min": -50.0,
    },
    "firm_rocky_surface": {
        "label": "Firm / rocky surface screening",
        "why": "Prefer higher TES nightside thermal inertia with moderate relief (less dust mantle).",
        "layers": {
            "thermal_inertia": (400.0, 120.0),
            "slope": (1.0, 0.8),
            "relief": (250.0, 150.0),
            "dust_cdod": (0.10, 0.04),
        },
        "weights": {
            "thermal_inertia": 2.0,
            "slope": 1.0,
            "relief": 1.0,
            "dust_cdod": 0.5,
        },
        "lat_max": 60.0,
        "lat_min": -60.0,
    },
}


def _manual_signature(layers: dict[str, tuple[float, float]]) -> xr.Dataset:
    names = list(layers)
    median = xr.DataArray(
        [layers[n][0] for n in names], dims="layer", coords={"layer": names}, name="median"
    )
    iqr = xr.DataArray(
        [layers[n][1] for n in names], dims="layer", coords={"layer": names}, name="iqr"
    )
    return xr.Dataset({"median": median, "iqr": iqr})


def _mask_exclusions(score: xr.DataArray) -> xr.DataArray:
    masked = score.copy()
    for box in EXCLUDE.values():
        inside = (
            (masked.lat <= box.north)
            & (masked.lat >= box.south)
            & (masked.lon >= box.west)
            & (masked.lon <= box.east)
        )
        masked = masked.where(~inside)
    return masked


def _layer_snapshot(stack: xr.Dataset, lat: float, lon: float) -> dict[str, float | None]:
    cell = stack.sel(lat=lat, lon=lon, method="nearest")
    out: dict[str, float | None] = {}
    for name in stack.data_vars:
        value = cell[name].item()
        out[name] = None if value is None or np.isnan(value) else float(value)
    return out


def discover(stack: xr.Dataset, purpose: str, n: int = 8) -> dict:
    spec = PURPOSES[purpose]
    sig = _manual_signature(spec["layers"])
    score = similarity(stack, sig, weights=spec["weights"], min_valid_fraction=1.0)
    score = score.where((score.lat <= spec["lat_max"]) & (score.lat >= spec["lat_min"]))
    score = _mask_exclusions(score)
    picks = top_cells(score, n=n, separation_deg=8.0)
    for pick in picks:
        pick["layers"] = _layer_snapshot(stack, pick["lat"], pick["lon"])
        pick["excluded_known_sites"] = list(EXCLUDE)
    return {
        "purpose": purpose,
        "label": spec["label"],
        "why": spec["why"],
        "weights": spec["weights"],
        "signature": {
            name: {"median": med, "iqr": iqr} for name, (med, iqr) in spec["layers"].items()
        },
        "latitude_window": [spec["lat_min"], spec["lat_max"]],
        "picks": picks,
        "score": score,
        "interpretation": (
            "Experimental within-Mars descriptor ranking after excluding Jezero, Gale, "
            "Arcadia and Utopia boxes. Not novelty proof, landing approval, or ice quantity."
        ),
    }


def plot_purpose(result: dict, path: Path) -> None:
    score = result["score"]
    fig, ax = plt.subplots(figsize=(11, 5), constrained_layout=True)
    image = ax.imshow(
        score.values,
        extent=[-180, 180, -90, 90],
        cmap="magma",
        vmin=0,
        vmax=1,
        interpolation="nearest",
    )
    for box in EXCLUDE.values():
        ax.add_patch(
            plt.Rectangle(
                (box.west, box.south),
                box.east - box.west,
                box.north - box.south,
                fill=False,
                edgecolor="cyan",
                linewidth=1.0,
            )
        )
    for i, pick in enumerate(result["picks"][:5], start=1):
        ax.scatter(pick["lon"], pick["lat"], c="lime", s=28, zorder=3)
        ax.text(pick["lon"] + 2, pick["lat"] + 2, str(i), color="white", fontsize=9)
    ax.set_title(f"Mars discovery: {result['label']} (cyan = excluded known boxes)")
    ax.set_xlabel("East longitude (deg)")
    ax.set_ylabel("Latitude (deg)")
    fig.colorbar(image, ax=ax, label="descriptor score (not confidence)")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main() -> None:
    stack = stack_mod.load_stack()
    OUT.mkdir(parents=True, exist_ok=True)
    FIGURE.mkdir(parents=True, exist_ok=True)

    # Reference signatures of the known boxes, for the report teammate.
    known = {}
    for name, box in EXCLUDE.items():
        sig = signature(stack, box)
        known[name] = {
            "box": box.__dict__,
            "median": {str(k): float(sig["median"].sel(layer=k)) for k in sig.layer.values},
            "iqr": {str(k): float(sig["iqr"].sel(layer=k)) for k in sig.layer.values},
        }

    catalog = {
        "generated_for": "Matching / site-discovery role",
        "stack": "data/processed/mars_stack_0p5deg.nc",
        "excluded_boxes": {k: v.__dict__ for k, v in EXCLUDE.items()},
        "known_box_signatures": known,
        "purposes": {},
        "limitations": [
            "Scores are experimental within-Mars descriptor matches only.",
            "Excluding famous boxes is not proof a pick is understudied; literature checks remain required.",
            "SWIM ice_shallow covers roughly ±60°; no ice score outside support.",
            "Dust is 3° reconstructed climatology context, not local weather.",
            "Earth analogs are not ranked in this script.",
        ],
    }

    for purpose in PURPOSES:
        result = discover(stack, purpose)
        figure = FIGURE / f"{purpose}_map.png"
        plot_purpose(result, figure)
        catalog["purposes"][purpose] = {
            "label": result["label"],
            "why": result["why"],
            "weights": result["weights"],
            "signature": result["signature"],
            "latitude_window": result["latitude_window"],
            "interpretation": result["interpretation"],
            "figure": str(figure.relative_to(ROOT)),
            "picks": result["picks"],
        }
        print(f"\n{purpose}: {result['label']}")
        for i, pick in enumerate(result["picks"][:5], start=1):
            print(
                f"  {i}. lat {pick['lat']:7.2f} lon {pick['lon']:8.2f} "
                f"score {pick['score']:.3f} ice={pick['layers']['ice_shallow']} "
                f"slope={pick['layers']['slope']:.2f}"
            )

    out_json = OUT / "mars_site_discovery.json"
    out_json.write_text(json.dumps(catalog, indent=2))
    print(f"\nsaved {out_json}")
    print(f"figures in {FIGURE}")


if __name__ == "__main__":
    main()
