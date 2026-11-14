"""Produce a source-labelled terrain screening map and equal-scale terrain panels."""

import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from analog import earth, mars
from analog.screening import EARTH_RADIUS_M, land_geometry, sample_patch


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--analysis", type=Path, default=Path("outputs/analysis"))
    args = p.parse_args()
    result = json.loads((args.analysis / "results.json").read_text())
    earth_grid = earth.load_terrain()
    mars_grid = mars.load("mola_topography").astype("float32")
    land = land_geometry(earth.RAW_DIR / "ne_110m_land.zip")
    plt.rcParams.update(
        {
            "figure.facecolor": "#101923",
            "axes.facecolor": "#152331",
            "text.color": "#e4ebef",
            "axes.labelcolor": "#b9cbd5",
            "xtick.color": "#a9bfca",
            "ytick.color": "#a9bfca",
            "axes.titlecolor": "#e4ebef",
            "axes.edgecolor": "#37505f",
            "font.size": 10,
        }
    )
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.subplots_adjust(bottom=0.20, top=0.90, left=0.08, right=0.98)
    for polygon in land.geoms:
        ax.add_patch(
            Polygon(
                np.asarray(polygon.exterior.coords),
                facecolor="#29404b",
                edgecolor="#4b6470",
                linewidth=0.3,
            )
        )
    palette = ["#48d5ce", "#f3ad65", "#baacff"]
    for color, (name, items) in zip(palette, result["candidates"].items()):
        ax.scatter(
            [i["lon"] for i in items], [i["lat"] for i in items], color=color, s=20, label=name
        )
        for item in items[:2]:
            ax.annotate(
                item["candidate_id"],
                (item["lon"], item["lat"]),
                xytext=(4, 5),
                textcoords="offset points",
                fontsize=8,
                color=color,
            )
    ax.set(
        xlim=(-180, 180),
        ylim=(-60, 60),
        xlabel="Earth east longitude (degrees)",
        ylabel="Earth latitude (degrees)",
        title="Mars Analog Finder | Regional terrain screening",
    )
    ax.grid(alpha=0.15)
    ax.legend(labelcolor="#101923", facecolor="#e4ebef", loc="lower left")
    fig.text(
        0.5,
        0.01,
        "ETOPO 2022 + MGS MOLA | 100 km windows | 4 km samples | Terrain only; candidates unvalidated",
        ha="center",
        fontsize=9,
    )
    folder = args.analysis / "figures"
    folder.mkdir(exist_ok=True)
    fig.savefig(folder / "candidate_map.png", dpi=160)
    plt.close(fig)
    for name, items in result["candidates"].items():
        if not items:
            continue
        target = result["targets"][name]
        settings = result["parameters"]
        spacing, window = settings["sample_spacing_km"], settings["window_km"]
        target_patch, _, _ = sample_patch(
            mars_grid, target["lat"], target["lon"], mars.MARS_RADIUS_M, spacing, window
        )
        patches = [target_patch]
        titles = [f"Mars: {name} ({target['lat']:.2f}, {target['lon']:.2f})"]
        for item in items[:2]:
            patch, _, _ = sample_patch(
                earth_grid, item["lat"], item["lon"], EARTH_RADIUS_M, spacing, window
            )
            patches.append(patch)
            titles.append(f"Earth: {item['candidate_id']} ({item['lat']:.1f}, {item['lon']:.1f})")
        relative = [v - np.median(v) for v in patches]
        limit = max(float(np.abs(v).max()) for v in relative)
        fig, axes = plt.subplots(1, len(relative), figsize=(13, 4.8), layout="constrained")
        for axis, values, title in zip(np.atleast_1d(axes), relative, titles):
            image = axis.imshow(
                values,
                extent=[
                    -window / 2 - spacing / 2,
                    window / 2 + spacing / 2,
                    -window / 2 - spacing / 2,
                    window / 2 + spacing / 2,
                ],
                origin="lower",
                cmap="terrain",
                vmin=-limit,
                vmax=limit,
                interpolation="nearest",
            )
            axis.set(
                title=title,
                xlabel="Local east (km)",
                ylabel="Local north (km)",
                xlim=(-window / 2, window / 2),
                ylim=(-window / 2, window / 2),
            )
        fig.colorbar(
            image, ax=axes, label="Elevation relative to each window median (m)", shrink=0.7
        )
        fig.suptitle(
            f"{name.title()} | Same physical extent and colour scale | Elevation shown by colour"
        )
        fig.text(
            0.5,
            0.01,
            "Regional sampled terrain; not landing safety, geology, climate, ice or rover-scale validation",
            ha="center",
            fontsize=9,
        )
        fig.savefig(folder / f"{name}_terrain_comparison.png", dpi=160)
        plt.close(fig)
    print(folder)


if __name__ == "__main__":
    main()
