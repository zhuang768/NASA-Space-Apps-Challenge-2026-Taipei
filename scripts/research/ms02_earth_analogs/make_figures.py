"""Two context figures for MS-02. No scores, no weights, no rankings.

fig1: native-cell values of MS-01 / MS-02 / MS-03 side by side (hand-off final_candidates.csv).
fig2: absolute latitude of MS-02 and the Earth candidates whose coordinates were obtained.
Run from repo root: python3 -I scripts/research/ms02_earth_analogs/make_figures.py
"""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs/research/MS-02/figures"
OUT.mkdir(parents=True, exist_ok=True)

# validated categorical slots 1-3 (light mode, surface #fcfcfb), assigned per entity, fixed order
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
COL = {"MS-01": "#2a78d6", "MS-02": "#eb6834", "MS-03": "#1baf7a"}

with open(ROOT / "outputs/research/mars_reselection_20261114/final_candidates.csv", newline="", encoding="utf-8") as f:
    rows = {r["candidate_id"]: r for r in csv.DictReader(f)}

panels = [  # (column, title, unit/note)
    ("mola_slope_deg_mean", "MOLA slope, mean", "degrees, ~3.7 km baseline"),
    ("mola_relief_m", "MOLA relief in cell", "m"),
    ("TES_TI_mean", "TES thermal inertia, mean", "J m$^{-2}$ K$^{-1}$ s$^{-0.5}$ (not temperature)"),
    ("SWIM_0_1m_mean", "SWIM 0-1 m consistency", "dimensionless (not ice amount)"),
    ("SWIM_1_5m_mean", "SWIM 1-5 m consistency", "dimensionless (not ice amount)"),
    ("dust_my34_p95_cdodtot", "MY34 dust opacity, p95", "9.3 µm column (not wind)"),
    ("dust_my35_p95_cdodtot", "MY35 dust opacity, p95", "9.3 µm column (not wind)"),
]

plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "text.color": INK})
fig, axes = plt.subplots(2, 4, figsize=(12.5, 6.2), facecolor=SURFACE)
for ax, (col, title, note) in zip(axes.flat, panels):
    ids = ["MS-01", "MS-02", "MS-03"]
    vals = [float(rows[i][col]) for i in ids]
    bars = ax.bar(ids, vals, color=[COL[i] for i in ids], width=0.55, edgecolor=SURFACE, linewidth=2)
    ax.set_facecolor(SURFACE)
    ax.set_title(title, fontsize=10, loc="left", color=INK)
    ax.set_xlabel(note, fontsize=7.5, color=INK2, labelpad=6)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    top = max(vals) * 1.0
    ax.set_ylim(0, top * 1.18)
    for b, v in zip(bars, vals):  # visible value labels (relief for the low-contrast aqua slot)
        txt = f"{v:.0f}" if col in ("mola_relief_m", "TES_TI_mean") else f"{v:.3f}"
        ax.text(b.get_x() + b.get_width() / 2, v + top * 0.02, txt, ha="center", va="bottom", fontsize=8.5, color=INK)
axes.flat[-1].axis("off")
axes.flat[-1].text(0.0, 0.95,
                   "Each panel has its own axis;\nbars are NOT summed or ranked.\n\n"
                   "Native-cell values from the\nhand-off final_candidates.csv.\n"
                   "MS-02 = orange.\n\nSWIM = consistency, not abundance.\nThermal inertia is not temperature.\n"
                   "Dust opacity is not wind speed.",
                   va="top", ha="left", fontsize=8.5, color=INK2, transform=axes.flat[-1].transAxes)
fig.suptitle("MS-02 beside the other two team targets (context only; no score)", x=0.01, ha="left", fontsize=12, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(OUT / "fig1_team_targets_context.png", dpi=170, facecolor=SURFACE)
plt.close(fig)

# ---- fig2: absolute latitude of MS-02 and Earth candidates with known coordinates
pts = [("MS-02 (Mars)", 52.75, "N", "#eb6834"),
       ("E04 Haughton R. valley", 75.37, "N", INK2),
       ("E01 University Valley", 77.8667, "S", INK2),
       ("E03 Adventdalen", 78.1722, "N", INK2)]
fig, ax = plt.subplots(figsize=(8.5, 3.6), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
for i, (name, lat, hemi, c) in enumerate(pts):
    y = len(pts) - 1 - i
    ax.hlines(y, 0, lat, color=GRID, linewidth=2)
    ax.plot(lat, y, "o", color=c, markersize=10, markeredgecolor=SURFACE, markeredgewidth=2)
    ax.text(lat + 1.0, y, f"{lat:.2f}°{hemi}", va="center", fontsize=9, color=INK)
ax.set_yticks(range(len(pts))); ax.set_yticklabels([p[0] for p in pts][::-1], fontsize=9)
ax.set_xlim(0, 95); ax.set_xlabel("Absolute latitude (degrees); hemisphere ignored", color=INK2)
ax.xaxis.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.set_title("Earth candidates sit 22-25° poleward of MS-02 (latitude only; insolation and obliquity not compared)",
             loc="left", fontsize=10, color=INK)
fig.text(0.01, 0.01, "E02 Beacon Valley omitted: coordinates not obtained from the sources read.", fontsize=8, color=INK2)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(OUT / "fig2_latitude_context.png", dpi=170, facecolor=SURFACE)
plt.close(fig)
print("wrote", sorted(p.name for p in OUT.iterdir()))
