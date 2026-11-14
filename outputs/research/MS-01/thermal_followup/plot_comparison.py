"""Plot the bounded University Valley thermal comparison from saved row exports.

Run from the repository root after analyze.py:
  .venv/bin/python outputs/research/MS-01/thermal_followup/plot_comparison.py

Only the two comparison_figure images in this directory are written. No raw
download, time correction, cross-instrument join, or thermal inversion occurs.
"""
from pathlib import Path
import csv
from datetime import datetime
import gzip
import json
import os
import tempfile

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'ms01_followup_matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import NullFormatter

HERE = Path(__file__).resolve().parent


def main():
    comparison = json.loads((HERE/'comparison.json').read_text())
    with gzip.open(HERE/'primary_temperature_records.csv.gz', 'rt') as stream:
        rows = list(csv.DictReader(stream))
    stations = ['S8', 'M22', 'D36', 'W42_Campbell']
    expected = {'S8': 264, 'M22': 264, 'D36': 264, 'W42_Campbell': 528}
    for station in stations:
        assert comparison['qa'][station]['common_valid_rows'] == expected[station]
        assert comparison['qa'][station]['common_valid_rows'] == comparison['qa'][station]['expected_primary_rows']
    colors = {'upper':'#cf6546', 'middle':'#d5a539', 'ice':'#187e8c', 'below':'#49638a'}
    plt.rcParams.update({
        'font.family':'DejaVu Sans', 'font.size':10.5,
        'axes.spines.top':False, 'axes.spines.right':False,
        'axes.labelcolor':'#2b3b4b', 'text.color':'#2b3b4b',
        'xtick.color':'#4d6174', 'ytick.color':'#4d6174',
        'svg.fonttype':'none', 'savefig.facecolor':'white'})
    fig = plt.figure(figsize=(17.6, 10.6))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.25, 1.25, 1],
                          left=.06, right=.975, top=.75, bottom=.18,
                          hspace=.46, wspace=.28)
    fig.suptitle('Known ice interfaces: thermal response needs more than one explanation',
                 x=.06, y=.965, ha='left', fontsize=21, fontweight='bold')
    fig.text(.06, .915,
             'University Valley  |  Author-calibrated field records  |  Printed-date window: 7-17 Nov 2010',
             ha='left', fontsize=13, color='#52697c')
    fig.text(.06, .878,
             'Each panel uses its own common-valid records. Shared printed dates do not establish identical forcing or verified cross-site timing.',
             ha='left', fontsize=11, color='#52697c')
    legend = [Line2D([0],[0], color=colors[r], lw=2,
                      linestyle='--' if r=='below' else '-',
                      label=l) for r,l in [('upper','Upper probe'),('middle','Intermediate dry-soil probe'),
                                          ('ice','Known ice interface'),('below','Nominal below-interface probe')]]
    fig.legend(handles=legend, loc='upper left', bbox_to_anchor=(.055,.85),
               ncol=4, frameon=False, fontsize=10.5, handlelength=2.0, columnspacing=2.0)
    positions = [(0,0),(0,1),(1,0),(1,1)]
    descriptions = {
        'S8': ('S8 export label: 8 cm interface', 'U12 1122968  |  264 hourly records'),
        'M22': ('M22 export label: 22 cm interface', 'U12 2432937  |  Upper probe is 1 cm, not 0 cm'),
        'D36': ('D36 export label: 36 cm interface', 'U12 2432936  |  264 hourly records'),
        'W42_Campbell': ('W42: 42 cm interface', 'Campbell CR1000  |  528 half-hourly records')}
    start = datetime.fromisoformat(comparison['start_inclusive'])
    end = datetime.fromisoformat(comparison['end_exclusive'])
    for station, pos in zip(stations, positions):
        ax = fig.add_subplot(gs[pos])
        for sensor in comparison['results'][station]:
            selection = [row for row in rows if row['station']==station and row['column']==sensor['column']]
            assert len(selection) == expected[station]
            times = [datetime.fromisoformat(row['printed_timestamp']) for row in selection]
            values = [float(row['temperature_C']) for row in selection]
            ax.plot(times, values, color=colors[sensor['role']], lw=1.25,
                    linestyle='--' if sensor['role']=='below' else '-',
                    alpha=.88 if sensor['role']=='below' else 1)
        title, subtitle = descriptions[station]
        ax.set_title(title, fontsize=12, fontweight='bold', loc='left', pad=22)
        ax.text(0, 1.025, subtitle, transform=ax.transAxes, fontsize=9.3, color='#607487')
        ax.set_xlim(start, end); ax.set_ylim(-27, 10)
        ax.axhline(0, color='#a1adb9', lw=.8, linestyle=':')
        ax.grid(axis='y', color='#e2e8ed', lw=.8); ax.set_axisbelow(True)
        ax.set_yticks([-20,-10,0,10])
        ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[7,10,13,16,18]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d Nov'))
        if pos[1]==0: ax.set_ylabel('Probe temperature (deg C)', labelpad=9)
        if pos[0]==1: ax.set_xlabel('Author printed timestamp', labelpad=8)
        ice = next(r for r in comparison['results'][station] if r['role']=='ice')
        upper = next(r for r in comparison['results'][station] if r['role']=='upper')
        ax.text(.98,.04,
                f'24 h half-amplitude: upper {upper["amplitude_K"]:.2f} K; ice {ice["amplitude_K"]:.3f} K',
                transform=ax.transAxes, ha='right', va='bottom', fontsize=9.2,
                bbox={'boxstyle':'round,pad=.28','facecolor':'white','edgecolor':'none','alpha':.9})
    ratios = fig.add_subplot(gs[0,2])
    ratio_stations = stations + ['W42_HOBO']
    labels = ['S8\n0-8 cm', 'M22\n1-22 cm', 'D36\n0-36 cm',
              'W42 Campbell\n0-42 cm', 'W42 HOBO*\n0-42 cm']
    for y, station in enumerate(ratio_stations):
        r = next(v for v in comparison['results'][station] if v['role']=='ice')
        x = r['amplitude_to_upper_ratio']
        lower = r['leave_one_day_ratio_min']; upper = r['leave_one_day_ratio_max']
        color = '#187e8c' if station!='W42_HOBO' else '#8b97a3'
        ratios.errorbar(x, y, xerr=[[x-lower],[upper-x]], fmt='o', ms=6.8,
                        mfc='white' if station=='W42_HOBO' else color, mec=color,
                        ecolor=color, capsize=3, elinewidth=1.3)
        ratios.annotate(f'{x:.4f}', (x,y), xytext=(0,-13), textcoords='offset points',
                        ha='center', va='top', fontsize=9.4, color=color)
    ratios.set_xscale('log'); ratios.set_xlim(.012,.65); ratios.set_ylim(4.65,-.65)
    ratios.set_xticks([.02,.05,.1,.2,.5]); ratios.set_xticklabels(['0.02','0.05','0.10','0.20','0.50'])
    ratios.xaxis.set_minor_formatter(NullFormatter())
    ratios.set_yticks(range(5)); ratios.set_yticklabels(labels, fontsize=9)
    ratios.set_xlabel('Ice / upper 24 h half-amplitude (unitless)', fontsize=10, labelpad=9)
    ratios.set_title('Within-profile attenuation', fontsize=12, fontweight='bold', loc='left', pad=21)
    ratios.grid(axis='x', color='#e2e8ed', lw=.8); ratios.set_axisbelow(True)
    ratios.text(0,1.025,'Whiskers: leave-one-day-out range, not a CI', transform=ratios.transAxes,
                fontsize=9.0, color='#607487')
    note = fig.add_subplot(gs[1,2]); note.axis('off')
    note.set_title('What these data can establish', fontsize=12, fontweight='bold', loc='left', pad=22)
    paragraphs = [
        ('Observed', 'The fitted daily component is smaller at the\nknown ice interface than at the upper probe.'),
        ('Still confounded', 'Depth, material, shading, surface forcing and\nprobe contact vary; all profiles already contain ice.'),
        ('Location and clock limits', 'The 2009 notes and 2022 paper swap S/D\ncoordinates. No cross-site absolute phase is shown.'),
        ('* W HOBO', 'Separate U23 loggers: descriptive amplitudes only.\nNo Campbell-HOBO join or clock correction.')]
    ypos=.98
    for heading, body in paragraphs:
        note.text(0,ypos,heading,fontsize=10.5,fontweight='bold',va='top',transform=note.transAxes)
        note.text(0,ypos-.075,body,fontsize=10.2,va='top',linespacing=1.4,
                  transform=note.transAxes,color='#52697c')
        ypos-=.25
    fig.text(.06,.104,
             'Source: Marinova, Zenodo 10.5281/zenodo.10553882 (v1). Source MD5s checked; no missing primary-window values filled.',
             fontsize=10.2,color='#607487')
    fig.text(.06,.073,
             'Fits: intercept + linear trend + 24 h sine/cosine. Half-amplitude is not peak-to-peak. Whiskers show fit stability, not sensor uncertainty.',
             fontsize=10.2,color='#607487')
    fig.text(.06,.042,
             'These Earth profiles constrain heat-transfer interpretation; they do not uniquely identify ice, invert MS-01 ice depth, or establish a new mechanism.',
             fontsize=10.2,color='#607487')
    for extension in ['png','svg']:
        path = HERE/f'comparison_figure.{extension}'
        fig.savefig(path,dpi=180)
        print(path)
    plt.close(fig)


if __name__=='__main__': main()
