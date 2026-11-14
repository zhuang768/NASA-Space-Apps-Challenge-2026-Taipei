"""Render sourced locators and pinned compute exports; never parse raw PDFs or recompute statistics."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'outputs/research/final_figures'
INK='#172B40';GRAY='#52616E';GRID='#DCE3E8';TEAL='#007F8B';ORANGE='#C16A16'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'text.color':INK,'axes.labelcolor':INK,'xtick.color':GRAY,'ytick.color':GRAY,'pdf.fonttype':42,'savefig.facecolor':'white'})
def base(fid,title,subtitle):
 f=plt.figure(figsize=(14,8),facecolor='white')
 f.text(.055,.946,f'{fid}  /  TEAM ZASA',fontsize=11,weight='bold',color=TEAL)
 f.text(.055,.887,title,fontsize=25,weight='bold')
 f.text(.055,.842,subtitle,fontsize=12,color=GRAY)
 return f
def save(f,name,folder=OUT):
 folder.mkdir(parents=True,exist_ok=True)
 for ext in ['png','pdf']:f.savefig(folder/f'{name}.{ext}',dpi=220)
 plt.close(f)
f=base('F01','Case context: I-02 and Elephant Head','I-02 is a conditional Mars research candidate; Elephant Head provides a historical method reference.')
a=f.add_axes([.07,.36,.39,.39]);a.set_facecolor('#F7F9FA')
a.set_xlim(40.75,43.75);a.set_ylim(52.75,54.75)
a.set_aspect(1/np.cos(np.deg2rad(53.75)))
a.set_xticks([41,42,43]);a.set_xticklabels(['41°E','42°E','43°E'])
a.set_yticks([53,53.5,54,54.5]);a.set_yticklabels(['53°N','53.5°N','54°N','54.5°N'])
a.grid(color=GRID,lw=.7);a.add_patch(Rectangle((42,53.5),.5,.5,facecolor=ORANGE,alpha=.22,edgecolor=ORANGE,lw=2))
a.plot(42.25,53.75,'+',color=ORANGE,ms=11,mew=2)
a.annotate('I-02',xy=(42.25,53.75),xytext=(42.8,54.18),arrowprops={'arrowstyle':'-','color':ORANGE},weight='bold',color=ORANGE)
a.set_title('MARS  /  nominal screening cell',loc='left',fontsize=14,pad=14,weight='bold')
a.set_xlabel('East-positive longitude');a.set_ylabel('Planetocentric latitude')
# South-polar coordinate locator, not a terrestrial metric survey projection.
b=f.add_axes([.58,.37,.31,.38],projection='polar')
b.set_theta_zero_location('N');b.set_theta_direction(-1)
b.set_ylim(0,30);b.set_yticks([10,20,30]);b.set_yticklabels(['80°S','70°S','60°S'],fontsize=10)
b.set_xticks(np.deg2rad([0,90,180,270]));b.set_xticklabels(['0°','90°E','180°','90°W'],fontsize=10)
b.grid(color=GRID,lw=.8);b.set_facecolor('#F7F9FA')
b.plot(np.deg2rad(-83.314333333),90-79.820216667,marker='o',color=TEAL,ms=8)
b.annotate('EARTH-002',xy=(np.deg2rad(-83.314333333),10.179783333),xytext=(np.deg2rad(-60),24),color=TEAL,weight='bold',fontsize=11,arrowprops={'arrowstyle':'-','color':TEAL})
b.set_title('EARTH  /  station anchor',fontsize=14,pad=24,weight='bold',loc='center')
f.text(.07,.257,'53.75°N, 42.25°E',fontsize=15,weight='bold')
f.text(.07,.225,'Cell: 53.5–54°N × 42–42.5°E\nScreening support, not a borehole or landing ellipse.',fontsize=11,linespacing=1.6,va='top')
f.text(.56,.257,'Elephant Head · Ellsworth Land, Antarctica',fontsize=14,weight='bold')
f.text(.56,.225,'79.820216667°S, 83.314333333°W\nPoint anchor only. Datum and positioning error unstated.\nMarker is symbolic; no test-area radius is assigned.',fontsize=11,linespacing=1.6,va='top')
f.text(.055,.105,'Research-purpose pairing does not establish environmental equivalence, local Mars ice or extraction suitability.',fontsize=11,weight='bold')
f.text(.055,.064,'Sources: MR-20261114-v2 I-02 card; McKay et al. (2019), Methods / Fig. 1, doi:10.1017/S0954102019000269.\nCoordinate locators only: no imagery, terrain, inferred footprint or common Earth–Mars distance scale.',fontsize=9,color=GRAY,linespacing=1.5)
save(f,'F01_case_context')

# User-selected compute delivery. Same summer mask and per-row subtraction as
# upstream eh_adapter.plot_eh; published means are read, never recomputed.
import csv, gzip, json, hashlib
from datetime import datetime
import matplotlib.dates as mdates
plt.rcParams['path.simplify'] = False
inputs=OUT/'inputs/14f6550'
lock=json.loads((OUT/'input_lock.json').read_text())
for item in lock['files']:
    assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']
with gzip.open(inputs/'station_observations.csv.gz','rt',newline='') as fh:
    all_rows=list(csv.DictReader(fh))
with (inputs/'window_summaries.csv').open(newline='') as fh:
    summary={r['metric_id']:r for r in csv.DictReader(fh) if r['window']=='summer'}
reference=summary['T_3cm_minus_49cm_C']
start=datetime.fromisoformat(reference['period_start'])
end=datetime.fromisoformat(reference['period_end_exclusive'])
# This selects the identical plotting window, without aggregation or resampling.
rows=[r for r in all_rows if start<=datetime.fromisoformat(r['time_1_naive'])<end
      and r['T_3cm_C'] and r['T_49cm_C']]
assert len(rows)==int(reference['valid_n'])==2160
assert all(r['earth_candidate_id']=='EARTH-002' and r['mars_candidate_id']=='I-02' for r in rows)
times=[datetime.fromisoformat(r['time_1_naive']) for r in rows]
t3=[float(r['T_3cm_C']) for r in rows]
t49=[float(r['T_49cm_C']) for r in rows]
difference=[a-b for a,b in zip(t3,t49)] # Same expression as original plot_eh.
mean_from_export=float(reference['observed_mean'])

def result_frame(fid,title):
    fig=base(fid,title,'EARTH-002 · historical station observations · 2,160 same-row hourly pairs')
    ax=fig.add_axes([.095,.29,.85,.45])
    ax.spines[['top','right']].set_visible(False)
    for sp in ['left','bottom']:ax.spines[sp].set_color('#B8C3CC')
    ax.grid(axis='y',color=GRID,lw=.65);ax.set_axisbelow(True)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))
    ax.set_xlim(start,end)
    ax.set_xlabel('First printed time · label “GMT-07:00” · no UTC / solar-time conversion',labelpad=13)
    ax.set_ylabel('Temperature (°C)',labelpad=10)
    fig.text(.095,.785,'Window: 01 Dec 2017 inclusive → 01 Mar 2018 exclusive',fontsize=12,color=GRAY)
    fig.text(.055,.13,'Source: McKay et al. (2019), published EH2 supplement · doi:10.1017/S0954102019000269',fontsize=10)
    fig.text(.055,.095,'Compute export 14f6550 · unchanged hourly values; no smoothing, filling or resampling.',fontsize=10,color=GRAY)
    fig.text(.055,.055,'DISPLAY EDITION · mainline final acceptance pending · station temperature is not Mars thermal inertia.',fontsize=10,color=GRAY)
    return fig,ax
f,a=result_frame('F02','Elephant Head: temperatures by depth')
l3,=a.plot(times,t3,color=TEAL,lw=.8,label='3 cm · subsurface soil')
l49,=a.plot(times,t49,color=ORANGE,lw=1.6,label='49 cm · historical ice-table probe')
a.legend(loc='upper left',bbox_to_anchor=(0,1.035),frameon=False,ncol=2,fontsize=11)
f.text(.095,.185,'Nominal sensor depths at one published station; the 3 cm series is not surface skin temperature.',fontsize=11)
save(f,'F02_EH_temperatures')
f,a=result_frame('F03','Elephant Head: paired temperature difference')
a.set_ylabel('3 cm − 49 cm (°C)',labelpad=10)
ld,=a.plot(times,difference,color='#725799',lw=.8,label='Same-row difference')
a.axhline(0,color='#9BA7B0',lw=.75)
a.axhline(mean_from_export,color=INK,lw=1.3,ls='--',label=f'Descriptive mean: {mean_from_export:+.4f}°C')
a.legend(loc='upper left',bbox_to_anchor=(0,1.035),frameon=False,ncol=2,fontsize=11)
f.text(.095,.185,'Difference describes two observed depths; it does not estimate ice depth, ice quantity or equipment performance.',fontsize=11)
save(f,'F03_EH_temperature_difference')
# Rendering checks compare plotted vertices to the selected exported values.
assert list(l3.get_ydata())==t3 and list(l49.get_ydata())==t49
assert list(ld.get_ydata())==difference
checks={'input_commit':lock['input_commit'],'input_hashes_match':True,
        'selected_pair_count':len(rows),'first_selected_printed_time':times[0].isoformat(),
        'last_selected_printed_time':times[-1].isoformat(),
        'mean_source':'window_summaries.csv / summer / T_3cm_minus_49cm_C / observed_mean',
        'mean_from_export_C':mean_from_export,'mean_recomputed':False,
        'statistics_recomputed':False,'raw_pdf_parsed':False,
        'curve_vertex_checks':'all 2160 y values per plotted series match export/original plotting expression',
        'transformations':['same original summer selection','same-row subtraction copied from upstream plot_eh','new typography/colours/layout','source mean annotation'],
        'mainline_acceptance':'pending','team2_consolidated_review':'pending'}
(OUT/'render_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('F01/F02/F03 exported; pinned compute data only; no PDF parsing or statistical recomputation.')
# Refresh output provenance after every render (PDF metadata can change by run).
context_commit='ab1da697ad2093ca8185d29932e3fc5b85e7f80b'
context_paths=['docs/research/main_mars_research_cards.md','docs/research/main_project_synthesis.md','docs/research/team1_earth_analog_matching.md','outputs/research/team1_earth_analog_candidates.csv','docs/research/team2_novelty_audit.md']
# Pin context hashes already recorded at the initial figure handoff.
manifest_path=OUT/'figure_manifest.csv'
old_manifest=list(csv.DictReader(manifest_path.open())) if manifest_path.exists() else []
context_hashes=json.loads(old_manifest[0]['input_sha256_json']) if old_manifest else {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in context_paths}
records=[]
for fid,name in [('F01','F01_case_context'),('F02','F02_EH_temperatures'),('F03','F03_EH_temperature_difference')]:
    context=fid=='F01'
    input_paths=context_paths if context else [item['path'] for item in lock['files']]
    input_hashes=context_hashes if context else {item['path']:item['sha256'] for item in lock['files']}
    for ext in ['png','pdf']:
        file=OUT/f'{name}.{ext}'
        records.append(dict(figure_id=fid,format=ext,status='display_edition_pending_main_and_Team2_review',
            output_path=str(file.relative_to(ROOT)),output_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
            input_commit=context_commit if context else lock['input_commit'],input_files=';'.join(input_paths),
            input_sha256_json=json.dumps(input_hashes,separators=(',',':')),
            source_url='https://doi.org/10.1017/S0954102019000269',
            source_locator='Methods/Fig1;main I-02 card' if context else 'EH2 publication supplement;compute export;summer window_summaries.csv',
            data_period_or_image_date='Historical station coordinate;imagery not included' if context else 'First printed time [2017-12-01T00:00:00,2018-03-01T00:00:00);2160same-row pairs',
            image_use='No photograph/orbital imagery included;acquisition metadata and per-image reuse pending',
            use_conditions='Original display layout;underlying measurements attributed to McKay etal2019;article CC-BY4.0 per existing source record;project code license pending team decision',
            necessary_limitations='Earth datum/error unstated;no shared physical scale/no test-area radius' if context else 'Unresolved printed time semantics;nominal sensor depths;descriptive only;no ice-depth/quantity/causal/Mars-performance inference',
            science_review='pending_Team2_consolidated_review',
            transform='Coordinate illustration only' if context else 'Same original summer mask/row subtraction;separate panels;new colour/type/layout;mean read from export,not recomputed'))
with manifest_path.open('w',newline='') as fh:
    writer=csv.DictWriter(fh,fieldnames=list(records[0]),lineterminator='\n');writer.writeheader();writer.writerows(records)
