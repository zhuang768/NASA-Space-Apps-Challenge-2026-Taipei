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


# ---- fig3: Adventdalen evidence footprint (coordinates exactly as stated in sources; unknown geometry is NOT plotted)
import math
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

# measurement-type roles (palette slots reused as roles in this figure only, not as MS-01/02/03 entities)
C_SAMPLE, C_RADAR, C_MON = "#2a78d6", "#eb6834", "#1baf7a"
ADE = (78.1722, 16.0613)
def xy(lat, lon):  # km east / north of ADE, local equirectangular
    k = math.pi * 6371.0 / 180
    return (lon - ADE[1]) * k * math.cos(math.radians(ADE[0])), (lat - ADE[0]) * k

fig, (ax, bx) = plt.subplots(1, 2, figsize=(13, 6.4), facecolor=SURFACE, gridspec_kw={"width_ratios": [1.35, 1]})
ax.set_facecolor(SURFACE)
x0, y0 = xy(78.182, 15.79); x1, y1 = xy(78.206, 16.559)
ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=GRID, edgecolor=INK2, linestyle="--", linewidth=1, alpha=0.7))
ax.text(x1, y0 - 0.35, "HRSC-AX polygon-site bounding box (8 sites, 2008-09; outlines not obtained)", ha="right", va="top", fontsize=8.5, color=INK2)
cs = xy(78.201, 15.840); ad = xy(*ADE); vc = xy(78.110, 16.180)
ax.plot(*cs, "o", color=C_SAMPLE, markersize=11, markeredgecolor=SURFACE, markeredgewidth=2)
ax.text(cs[0] + 0.5, cs[1] + 1.0, "CS-1 loess core + met station\n78.201°N 15.840°E (Rasmussen 2023)\ncore date not extracted", fontsize=8.5, color=INK, va="bottom")
ax.plot(*ad, "s", color=C_SAMPLE, markersize=10, markeredgecolor=SURFACE, markeredgewidth=2)
ax.text(ad[0] + 0.5, ad[1] - 0.2, "ADE boreholes 78.1722°N 16.0613°E\nMarch 2017 (Rotem 2023)", fontsize=8.5, color=INK, va="top")
ax.plot(*vc, "D", markerfacecolor=SURFACE, markeredgecolor=INK2, markersize=8, markeredgewidth=1.5)
ax.text(vc[0] + 0.6, vc[1] + 0.3, "valley-centre reference point only\n(no measurement)", fontsize=8.5, color=INK2, va="center")
ax.plot([cs[0], ad[0]], [cs[1], ad[1]], color=INK2, linewidth=1.2)
mx, my = (cs[0] + ad[0]) / 2, (cs[1] + ad[1]) / 2
ax.text(mx + 0.25, my, "5.97 km", fontsize=9.5, color=INK, ha="left", va="center", fontweight="bold")
ax.set_aspect("equal"); ax.set_xlim(-12, 14); ax.set_ylim(-11.5, 8)
ax.set_xlabel("km east of ADE (local scale; positions from stated coordinates)", color=INK2)
ax.set_ylabel("km north of ADE", color=INK2)
ax.grid(color=GRID, linewidth=0.8); ax.set_axisbelow(True)
for s_ in ("top", "right"):
    ax.spines[s_].set_visible(False)
ax.text(-11.8, -11.2,
        "NOT plotted (no coordinates in the sources read): WISDOM polygon-trough lines (Mar 2022), UNISCALM CALM grid,\n"
        "'Polygons' MAAT site, Longyearbreen ice cave (ground truth for a different terrain).",
        fontsize=8.3, color=C_RADAR, va="bottom", ha="left",
        bbox=dict(boxstyle="round,pad=0.35", facecolor=SURFACE, edgecolor=C_RADAR, linestyle="--"))
ax.set_title("Where each measurement was made", loc="left", fontsize=10.5, color=INK)

# depth panel
bx.set_facecolor(SURFACE)
cats = ["CS-1 loess core\n(coring date n/a)", "ADE cores\n(Mar 2017)", "WISDOM polygon\ntroughs (Mar 2022)", "CALM probing\n(2000-16)"]
bx.axhspan(0, 3.2, color=GRID, alpha=0.6, zorder=0)
bx.text(3.55, 3.45, "shaded band 0-3.2 m: the only depth\nrange shared by core and radar", fontsize=8, color=INK2, ha="right", va="top")
bx.bar(0, 3.22, width=0.5, color=C_SAMPLE, edgecolor=SURFACE, linewidth=2, zorder=2)
bx.bar(1, 13, width=0.5, color=C_SAMPLE, edgecolor=SURFACE, linewidth=2, zorder=2)
bx.bar(3, 1.0, width=0.5, color=C_MON, edgecolor=SURFACE, linewidth=2, zorder=2)
bx.plot([2 - 0.25, 2 + 0.25], [1.5, 1.5], color=C_RADAR, linewidth=4, zorder=3)
bx.text(2, 1.9, "3 reflections ~1.5 m\npenetration 'a few m'\n(not quantified)", fontsize=8, color=INK, ha="center", va="top")
bx.text(0, 3.5, "0-3.22 m\nAL 98 cm; ice 20-250%", fontsize=8, color=INK, ha="center", va="top")
bx.text(1.3, 6.5, "0-13 m\n(permafrost ~20 m)", fontsize=8, color=INK, ha="left", va="center")
bx.text(3, 1.15, "AL 0.74 m (2005)\n>=1 m since 2006", fontsize=7.5, color=INK, ha="center", va="top")
bx.set_ylim(14.2, 0); bx.set_xlim(-0.6, 3.6)
bx.set_xticks(range(4)); bx.set_xticklabels(cats, fontsize=8.3)
bx.set_ylabel("depth (m)", color=INK2); bx.yaxis.grid(True, color=GRID, linewidth=0.8); bx.set_axisbelow(True)
for s_ in ("top", "right"):
    bx.spines[s_].set_visible(False)
bx.set_title("How deep each looked", loc="left", fontsize=10.5, color=INK)
leg = [Line2D([0], [0], color=C_SAMPLE, linewidth=8, label="sampled directly"),
       Line2D([0], [0], color=C_RADAR, linewidth=4, label="radar inference (unlocated)"),
       Line2D([0], [0], color=C_MON, linewidth=8, label="monitoring (location unknown)")]
bx.legend(handles=leg, loc="lower right", bbox_to_anchor=(1.0, 0.08), fontsize=8, frameon=False, handlelength=1.3)
fig.suptitle("Adventdalen: the loess core, the borehole and the radar survey are three different places",
             x=0.01, ha="left", fontsize=12, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(OUT / "fig3_adventdalen_evidence_footprint.png", dpi=170, facecolor=SURFACE)
plt.close(fig)
print("wrote", sorted(p.name for p in OUT.iterdir()))
