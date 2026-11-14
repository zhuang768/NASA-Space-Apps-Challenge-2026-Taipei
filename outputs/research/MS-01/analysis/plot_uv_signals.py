"""Plot the measured Earth-site window and descriptive harmonic amplitudes.

Requires numpy and matplotlib. Run after uv_diurnal_fit.py. No Mars overlay.
"""
import csv
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import tempfile
import numpy as np

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'ms01_matplotlib_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def main():
    summary = json.loads((HERE / 'uv_diurnal_fit.json').read_text())
    source = ROOT / summary['source_file']
    if not source.exists():
        source = ROOT / 'outputs/handoff/legacy_snapshot' / summary['source_file']
    raw = source.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == summary['source_sha256']
    start = datetime.fromisoformat(summary['start_inclusive'])
    end = datetime.fromisoformat(summary['end_exclusive'])
    lines = raw.decode().splitlines()
    header = [s.strip() for s in next(csv.reader([lines[1]]))]
    indices = [header.index(c) for c in summary['source_columns']]
    times, values = [], []
    for row in csv.reader(lines[4:]):
        try:
            time = datetime.fromisoformat(row[0])
        except ValueError:
            time = datetime.strptime(row[0], '%m/%d/%Y %H:%M')
        if start <= time < end:
            observation = np.array([float(row[j]) for j in indices])
            if np.isfinite(observation).all():
                times.append(time)
                values.append(observation)
    assert len(times) == summary['common_valid_samples'] == 528
    values = np.array(values)
    colors = ['#cd5d37', '#d6a335', '#258c9b', '#3c527d']
    labels = ['Surface (0 cm)', 'Dry soil (10 cm)', 'Ice table (42 cm)', 'Below ice table (49 cm)']
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.labelcolor': '#243445', 'text.color': '#243445',
                         'xtick.color': '#405568', 'ytick.color': '#405568',
                         'svg.fonttype': 'none'})
    fig, (left, right) = plt.subplots(1, 2, figsize=(12.5, 5.8),
                                      gridspec_kw={'width_ratios': [2.15, 1]})
    fig.subplots_adjust(left=.075, right=.97, bottom=.25, top=.77, wspace=.34)
    fig.suptitle('University Valley: measured thermal signals',
                 x=.075, y=.955, ha='left', fontsize=18, fontweight='bold')
    fig.text(.075, .88, 'Partial Earth-site process demonstration  |  528 common-valid 30 min samples  |  7-17 Nov 2010',
             ha='left', fontsize=10.4, color='#4d6275')
    for i, (color, label) in enumerate(zip(colors, labels)):
        left.plot(times, values[:, i], color=color, label=label, lw=1.35)
    left.set_title('Observed temperatures at one soil column', loc='left', fontsize=11, pad=13)
    left.set_ylabel('Temperature (deg C)')
    left.set_xlabel('File timestamp (timezone not established)', labelpad=9)
    left.set_xlim(start, end)
    left.set_ylim(-27, 12)
    left.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    left.xaxis.set_major_formatter(mdates.DateFormatter('%d Nov'))
    left.grid(axis='y', color='#dbe2e8', lw=.8)
    left.set_axisbelow(True)
    left.axhline(0, color='#8999a7', linestyle='--', lw=.8)
    left.legend(loc='upper right', ncol=2, frameon=False, fontsize=8.5,
                handlelength=1.6, columnspacing=1.5)
    amplitudes = [v['diurnal_amplitude_K'] for v in summary['values']]
    depths = [100*v['depth_m'] for v in summary['values']]
    right.plot(amplitudes, depths, color='#b2bec9', lw=1.2, zorder=1)
    for amp, depth, color in zip(amplitudes, depths, colors):
        right.scatter([amp], [depth], s=60, color=color, edgecolor='white', linewidth=.8, zorder=3)
        right.annotate(f'{amp:.3g} K', (amp, depth), xytext=(8, -4),
                       textcoords='offset points', va='center', fontsize=9.5, color=color)
    right.set_title('Fitted daily component', loc='left', fontsize=11, pad=13)
    right.set_xlabel('24 h harmonic half-amplitude (K)', labelpad=9)
    right.set_ylabel('Depth below surface (cm)')
    right.set_xlim(-.25, 10.5)
    right.set_ylim(55, -6)
    right.set_yticks([0, 10, 20, 30, 40, 49])
    right.set_xticks([0, 2, 4, 6, 8, 10])
    right.grid(color='#e1e7ed', lw=.8)
    right.set_axisbelow(True)
    fig.text(.075, .117,
             'Source: Marinova dataset, Zenodo 10.5281/zenodo.10553882 (v1); calibrated/good-only Campbell measurements.',
             fontsize=8.8, color='#53697a')
    fig.text(.075, .075,
             'Right: least squares with intercept + linear trend + 24 h sine/cosine. Amplitude is not peak-to-peak; uncertainty not estimated.',
             fontsize=8.8, color='#53697a')
    fig.text(.075, .035,
             'Local Earth observations illustrate depth-dependent attenuation. They do not identify MS-01 ice depth or thermal inertia.',
             fontsize=8.8, color='#53697a')
    for extension in ('png', 'svg'):
        path = HERE / f'uv_thermal_signals.{extension}'
        fig.savefig(path, dpi=180, facecolor='white')
        print(path)
    plt.close(fig)


if __name__ == '__main__':
    main()
