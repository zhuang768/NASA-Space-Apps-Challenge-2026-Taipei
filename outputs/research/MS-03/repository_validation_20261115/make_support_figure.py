from pathlib import Path
import argparse,json,math,re,csv
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(exist_ok=True)
g=a.repo/'outputs/research/MS-03/local_validation/gap_completion';lv=g.parent
q=json.load(open(g/'moc_summary.json'));im=np.array(Image.open(g/'MOC_S1700607_roi_native_DN.png'));r0,r1,c0,c1=q['roi_crop_0based_inclusive'];R=q['radius_m'];s=q['map_grid_m']
l=(g/'sources/s1700607_na.lbl').read_text();f=lambda k:float(re.search(r'^'+k+r'\s*=\s*([-\d.]+)',l,re.M)[1]);so=f('SAMPLE_PROJECTION_OFFSET');lo=f('LINE_PROJECTION_OFFSET');l0=f('CENTER_LONGITUDE')
fig=plt.figure(figsize=(9,7));ax=fig.add_axes([.10,.25,.48,.58]);ax.set_anchor('W')
# For display only: every16th retained nonzero sample is plotted at its source position. No outline detection.
stride=16;rr,cc=np.meshgrid(np.arange(0,im.shape[0],stride),np.arange(0,im.shape[1],stride),indexing='ij');v=im[rr,cc]>0
x=(cc+c0-so)*s;y=(lo-(rr+r0))*s
lat=90-np.degrees(2*np.arctan(np.hypot(x,y)/(2*R)));
lon=(l0+np.degrees(np.arctan2(x,-y)))%360
ax.scatter(lon[v],lat[v],s=1.8,c='#d5e3ed',marker='s',linewidth=0,zorder=1)
win=list(csv.DictReader(open(a.out/'windows.csv')))
for w in win[:8]:
 x,y=float(w['west_E']),float(w['south_N']);width=float(w['east_E'])-x;height=float(w['north_N'])-y;color='#007986' if w['window_id'].startswith('CTX') else '#a44f15'
 ax.add_patch(Rectangle((x,y),width,height,fill=False,ec=color,lw=1.5,zorder=3));ax.text(x,y+height+.004,w['window_id'],color=color,fontsize=9,zorder=4)
ax.add_patch(Rectangle((242,57.5),.5,.5,fill=False,ec='#14283e',lw=1.6,zorder=2))
ax.set(xlim=(241.985,242.515),ylim=(57.485,58.015),xlabel='East-positive longitude (degrees)',ylabel='Planetocentric latitude (degrees)')
ax.set_aspect(1/math.cos(math.radians(57.75)));ax.grid(alpha=.2)
fig.text(.10,.955,'MS-03: retained image support',fontsize=16,color='#14283e')
fig.text(.10,.915,'Fixed review windows; no accepted polygon measurements.',fontsize=11,color='#4b5563')
handles=[Line2D([0],[0],color='#d5e3ed',lw=7,label='MOC nonzero support\n(display subset)'),Line2D([0],[0],color='#007986',lw=2,label='Five CTX display windows'),Line2D([0],[0],color='#a44f15',lw=2,label='Three MOC windows')]
fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.57,.81),frameon=False,fontsize=9,handlelength=1.5)
fig.text(.59,.63,'Retained MOC support: 15.18% of ROI\nThree MOC windows reviewed: 1.29%\nFive CTX windows reviewed: 2.06%\n\nSupport can overlap.\nNonzero / opaque is not feature QA.\nMap spacing is not optical resolution.',fontsize=10,color='#4b5563',linespacing=1.6,va='top')
fig.text(.10,.055,'MOC: S1700607_NA, 2006-04-08. CTX: retained mixed-date KML derivatives.\nAreas and full coordinates: windows.csv / summary.json. Source main: 07dbe2920350.\nMask shown every 16th sample for layout only; calculations use every retained pixel. No Mars contours accepted.',fontsize=8,color='#4b5563')
fig.savefig(a.out/'MS03_support_and_review_windows.png',dpi=180);fig.savefig(a.out/'MS03_support_and_review_windows.pdf');plt.close(fig)
