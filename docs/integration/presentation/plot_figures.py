"""Presentation-only redraw of delivered statistics; no fitting or time alignment."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'outputs/integration/presentation'
j=json.loads((OUT/'assets/MS01_comparison.json').read_text())
fig,ax=plt.subplots(figsize=(9.1,4.8),dpi=200)
keys=['S8','M22','D36','W42_Campbell']
labels=['S8  |  0 → 8 cm','M22  |  1 → 22 cm','D36  |  0 → 36 cm','W42 Campbell  |  0 → 42 cm']
for i,key in enumerate(keys):
 r=next(r for r in j['results'][key] if r['role']=='ice')
 y=3-i; v=r['amplitude_to_upper_ratio']; lo=r['leave_one_day_ratio_min']; hi=r['leave_one_day_ratio_max']
 ax.hlines(y,lo,hi,color='#117F83',linewidth=3)
 ax.plot(v,y,'o',color='#117F83',markersize=8)
 ax.text(v+.022,y+.05,f'{v:.3f}',fontsize=13,color='#12283E')
ax.set_yticks([3,2,1,0],labels,fontsize=13)
ax.set_xlim(0,.54); ax.set_ylim(-.6,3.6)
ax.set_xlabel('Interface / upper-sensor 24 h half-amplitude (dimensionless)',fontsize=12,labelpad=13)
ax.tick_params(axis='x',labelsize=12); ax.tick_params(axis='y',length=0,pad=12)
ax.grid(axis='x',color='#DCE4EA',linewidth=.7); ax.set_axisbelow(True)
for spine in ['top','right','left']: ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#9AAAB8')
fig.subplots_adjust(left=.38,bottom=.2,right=.98,top=.96)
fig.savefig(OUT/'assets/F01_UV_amplitude_ratios.png',facecolor='white')
plt.close(fig)
print('Redrew four delivered ratios and leave-one-day-out ranges; no new statistics.')
# Re-layout existing catalogue footprints; do not recompute intersections or assess pixels.
fps=json.loads((OUT/'assets/MS03_CTX_footprints.json').read_text())
from matplotlib.patches import Polygon,Rectangle
fig,ax=plt.subplots(figsize=(4.8,4.2),dpi=200)
colors=['#117F83','#C67B33','#637B99']
for ft,col in zip(fps['features'],colors):
 xy=ft['geometry']['coordinates'][0]
 ax.add_patch(Polygon(xy,facecolor=col,edgecolor=col,alpha=.22,label=ft['properties']['product_id'].split('_')[0]))
ax.add_patch(Rectangle((242,57.5),.5,.5,fill=False,edgecolor='#12283E',linewidth=2,label='MS-03 cell'))
ax.set(xlim=(241.6,242.8),ylim=(57.3,58.1),xlabel='Mars east longitude (deg)',ylabel='Planetocentric latitude (deg)')
ax.tick_params(labelsize=11);ax.xaxis.label.set_size(12);ax.yaxis.label.set_size(12)
ax.legend(fontsize=10,loc='lower left',framealpha=.92,ncol=2)
ax.grid(color='#DCE4EA',lw=.5);fig.tight_layout()
fig.savefig(OUT/'assets/F03_CTX_coverage.png',facecolor='white');plt.close(fig)
