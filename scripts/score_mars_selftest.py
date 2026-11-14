"""Behaviour check using the same Mars data for reference and scoring.

High descriptor similarity near Arcadia is expected. This is not independent
scientific validation or an Earth analog recommendation.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from analog import sites
from analog import stack as stack_mod
from analog.score import similarity, top_cells

FIGURE = stack_mod.PROCESSED_DIR.parent.parent / "outputs" / "figures" / "mars_selftest_arcadia.png"


def main() -> None:
    stack = stack_mod.load_stack()
    box = sites.SITES["arcadia_planitia"]
    sig = sites.signature(stack, box)
    print("Arcadia signature (median / IQR):")
    for layer in sig.layer.values:
        median = float(sig["median"].sel(layer=layer))
        iqr = float(sig["iqr"].sel(layer=layer))
        print(f"  {layer!s:16s} {median:10.2f} / {iqr:.2f}")

    score = similarity(stack, sig)
    print("\nTop matches (should start inside or near Arcadia, lat 38..48, lon -180..-160):")
    for pick in top_cells(score, n=8, separation_deg=10):
        inside = box.south <= pick["lat"] <= box.north and box.west <= pick["lon"] <= box.east
        print(
            f"  lat {pick['lat']:7.2f}  lon {pick['lon']:8.2f}  score {pick['score']:.3f}"
            f"  {'<- inside target box' if inside else ''}"
        )

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.subplots_adjust(bottom=0.17, top=0.90, left=0.08, right=0.94)
    cmap = plt.colormaps["magma"].copy()
    cmap.set_bad("#d9dde2")
    image = ax.imshow(score.values, extent=[-180, 180, -90, 90], cmap=cmap, vmin=0, vmax=1)
    ax.add_patch(
        plt.Rectangle(
            (box.west, box.south),
            box.east - box.west,
            box.north - box.south,
            fill=False,
            edgecolor="cyan",
        )
    )
    ax.set_title("Within-Mars check against Arcadia (cyan box); all 5 layers required")
    ax.set_xlabel("East longitude (deg)")
    ax.set_ylabel("Latitude (deg)")
    ax.legend(
        handles=[Patch(color="#d9dde2", label="Insufficient layer coverage")],
        loc="lower left",
        fontsize=8,
    )
    fig.colorbar(image, ax=ax, label="Descriptor similarity, not probability")
    fig.text(
        0.5,
        0.02,
        "Dust native grid: 3 deg; no Earth analog validation. Dust: Montabone et al. (2020), CC BY-SA 3.0",
        ha="center",
        fontsize=8,
    )
    FIGURE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE, dpi=110)
    print(f"\nsaved {FIGURE}")


if __name__ == "__main__":
    main()
