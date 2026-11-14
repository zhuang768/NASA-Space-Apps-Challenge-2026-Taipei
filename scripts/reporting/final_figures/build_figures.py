"""Presentation-only locators/templates; never parses or recomputes observations."""
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
for fid,title,name,definition in [('F02','Elephant Head temperatures','F02_EH_temperatures','3 cm / 49 cm temperature curves; preserve accepted observations and labels.'),('F03','Elephant Head paired temperature difference','F03_EH_temperature_difference','Same-row temperature at 3 cm minus 49 cm; mean is descriptive only.')]:
 f=base(fid,title,'LAYOUT TEMPLATE ONLY · NOT A RESULT FIGURE · DO NOT USE AS SCIENTIFIC EVIDENCE')
 ax=f.add_axes([.07,.30,.86,.45]);ax.set_axis_off()
 ax.add_patch(Rectangle((0,0),1,1,facecolor='#F7F9FA',edgecolor=GRID))
 ax.text(.5,.61,'Awaiting mainline-accepted figure package',ha='center',fontsize=20,weight='bold')
 ax.text(.5,.43,'No curves, averages or simulated data have been inserted.',ha='center',fontsize=13,color=GRAY)
 ax.text(.5,.25,definition,ha='center',fontsize=11)
 f.text(.07,.22,'Required: formal PNG + manifest + QA + acceptance/version record.',fontsize=12)
 f.text(.07,.16,'Planned encoding: 3 cm = teal (#007F8B); 49 cm = orange (#C16A16).\nReuse accepted curves unchanged; any re-export requires the approved plotting script and data.',fontsize=11,color=GRAY,linespacing=1.6)
 f.text(.07,.075,'Window to verify on receipt: first printed time [2017-12-01, 2018-03-01); 2,160 pairs.\nPrinted time semantics unresolved. No UTC conversion, smoothing, imputation or new analysis.',fontsize=10,color=GRAY,linespacing=1.6)
 save(f,name+'_TEMPLATE',OUT/'templates')
print('F01 exported; F02/F03 templates explicitly marked; no result data read.')
