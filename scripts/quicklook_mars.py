"""Plot the Mars grids on a 1-degree grid to check that they load correctly."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from analog import mars
from analog.terrain import block_stats, slope_deg

FIGURE = Path(__file__).resolve().parent.parent / "outputs" / "figures" / "mars_quicklook.png"


def main() -> None:
    topo = mars.load("mola_topography")  # 16 pixels/degree
    slope = slope_deg(topo, mars.MARS_RADIUS_M)
    inertia = mars.load_thermal_inertia()  # 20 pixels/degree

    highest = topo.where(topo == topo.max(), drop=True)
    lowest = topo.where(topo == topo.min(), drop=True)
    print(f"topography: {topo.shape}, {int(topo.min())} to {int(topo.max())} m")
    print(f"  highest at lat {float(highest.lat[0]):.2f}, lon {float(highest.lon[0]):.2f}")
    print(f"  lowest  at lat {float(lowest.lat[0]):.2f}, lon {float(lowest.lon[0]):.2f}")
    print(f"slope: median {float(slope.median()):.2f} deg, max {float(slope.max()):.1f} deg")
    print(
        f"thermal inertia: {inertia.shape}, {float(inertia.min()):.0f} to "
        f"{float(inertia.max()):.0f}, median {float(inertia.median()):.0f}, "
        f"{float(inertia.isnull().mean()) * 100:.1f}% missing"
    )

    panels = [
        (block_stats(topo, 16)["mean"], "MOLA topography (m)", "terrain", None),
        (block_stats(slope, 16)["mean"], "Mean slope at 3.7 km baseline (deg)", "viridis", None),
        (
            block_stats(inertia, 20)["mean"],
            "TES nightside thermal inertia (J m$^{-2}$ K$^{-1}$ s$^{-1/2}$)",
            "inferno",
            LogNorm(vmin=30, vmax=1000),
        ),
    ]
    fig, axes = plt.subplots(len(panels), 1, figsize=(10, 14), constrained_layout=True)
    for ax, (grid, title, cmap, norm) in zip(axes, panels):
        extent = [-180, 180, -90, 90]
        image = ax.imshow(grid.values, extent=extent, cmap=cmap, norm=norm, interpolation="nearest")
        ax.set_title(f"Mars: {title}, 1-degree cells")
        ax.set_xlabel("East longitude (deg)")
        ax.set_ylabel("Latitude (deg)")
        fig.colorbar(image, ax=ax, shrink=0.8)

    FIGURE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE, dpi=110)
    print(f"saved {FIGURE}")


if __name__ == "__main__":
    main()
