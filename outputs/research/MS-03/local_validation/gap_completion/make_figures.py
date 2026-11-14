"""Evidence figures only; no enhancement, tracing, classifier or performance metrics."""
from pathlib import Path
import os,json
O=Path(__file__).resolve().parent;os.environ.setdefault('MPLCONFIGDIR',str(O/'.mplconfig'))
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from shapely import wkt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def save(fig,name):
 fig.savefig(O/(name+'.png'),dpi=180,facecolor='white');plt.close(fig)
# MOC: official camera footprint and three fixed native-DN detail windows.
m=json.loads((O/'moc_summary.json').read_text());r=json.loads((O/'sources/moc_NASDP.json').read_text())['ODEResults']['Products']['Product']
geo=r['Footprint_geometry']  # Explicit 0–360 east field; C0 uses negative longitudes.
poly=wkt.loads(geo)
fig,axs=plt.subplots(1,4,figsize=(16,5.1),gridspec_kw={'width_ratios':[1,1.3,1.3,1.3]})
ax=axs[0];xx,yy=poly.exterior.xy;ax.fill(xx,yy,color='#9ad0d4',alpha=.65,label='ODE footprint (not QA mask)');ax.plot([242,242.5,242.5,242,242],[57.5,57.5,58,58,57.5],color='#c76c2c',lw=2,label='Fixed MS-03 cell');ax.scatter([t['longitude_deg_E'] for t in m['tiles']],[t['latitude_deg_N'] for t in m['tiles']],c='#172d48',s=24)
for t in m['tiles']:ax.annotate(str(t['id']),(t['longitude_deg_E'],t['latitude_deg_N']),xytext=(-12,0),textcoords='offset points')
ax.set(xlim=(241.97,242.56),ylim=(57.47,58.15),xlabel='Longitude (deg E)',ylabel='Planetocentric latitude (deg N)',title='A  Footprint and review windows');ax.set_aspect(1/np.cos(np.radians(57.75)));fig.legend(*ax.get_legend_handles_labels(),loc='lower left',bbox_to_anchor=(.33,.115),fontsize=8,frameon=False,ncol=2)
for ax,t in zip(axs[1:],m['tiles']):
 im=np.asarray(Image.open(O/f'MOC_detail_{t["id"]}_native_DN.png'));ax.imshow(np.ma.masked_equal(im,0),cmap='gray',vmin=1,vmax=255,interpolation='nearest');ax.plot([35,135],[470,470],lw=3,color='white');ax.text(35,450,'100 map pixels',color='white',fontsize=9);ax.set_title(f'{chr(65+t["id"])}  Window {t["id"]}\n{t["latitude_deg_N"]:.4f} N, {t["longitude_deg_E"]:.4f} E',fontsize=10);ax.set_xticks([]);ax.set_yticks([])
fig.suptitle('MS-03 | MOC S1700607_NA: actual in-cell image samples',fontsize=16,x=.06,ha='left')
fig.text(.06,.07,'2006-04-08 00:22:40–00:22:50 UTC | PDS MGS-M-MOC-NA/WA-4-RDR-L1B-V1.0 | 3.00034 m projected map grid; effective resolution not established.',fontsize=9)
fig.text(.06,.035,'Source: official PDS IMG/LBL and ODE footprint. Original 8-bit RDR DN; no sharpening/interpolation. Three 512 × 512 samples do not establish closed polygons or ice.',fontsize=9)
fig.subplots_adjust(left=.06,right=.99,top=.83,bottom=.22,wspace=.2);save(fig,'F-GAP01_MOC_in_cell_review')
# Parameter implementation residual; limits explicitly not a detection threshold.
a=np.load(O/'spectral_diagnostic_arrays.npz');mask=a['strict'];res=np.where(mask,a['residual'],np.nan)
fig,axs=plt.subplots(1,3,figsize=(13,4.8));lim=np.nanmax(abs(res));im=axs[0].imshow(res,cmap='RdBu_r',vmin=-lim,vmax=lim,interpolation='nearest',aspect='auto');fig.colorbar(im,ax=axs[0],label='Calculated minus official (dimensionless)');axs[0].set(title='A  BD1500_2 residual',xlabel='ROI map-grid column',ylabel='ROI map-grid row')
axs[1].scatter(a['official'][mask],a['calculated'][mask],s=2,alpha=.15,color='#1a7888',rasterized=True);lo=min(a['official'][mask].min(),a['calculated'][mask].min());hi=max(a['official'][mask].max(),a['calculated'][mask].max());axs[1].plot([lo,hi],[lo,hi],color='#c76c2c',lw=1);axs[1].set(title='B  Formula check, not detection',xlabel='Original official parameter',ylabel='CAT-reference calculation')
from matplotlib.ticker import MaxNLocator
axs[2].xaxis.set_major_locator(MaxNLocator(5));axs[2].hist(a['residual'][mask],bins=70,color='#287f8e');axs[2].set(title='C  Strict source-centre subset',xlabel='Residual (dimensionless)',ylabel='Map-grid centres')
fig.suptitle('MS-03 | MRDR v4 T1811 implementation diagnostics',fontsize=15,x=.06,ha='left')
fig.text(.06,.07,'13,169 source DDR centres inside fixed cell | Source observations 2006–2014; mosaic produced 2023-07-18. Official PDS MRDR albedo/summary + CAT 7.4 reference.',fontsize=9)
fig.text(.06,.035,'This precision variant: difference ≤1.27e−7 cannot by itself explain residual up to 0.01935. Producer execution, clouds/frost and detection limits remain unvalidated; no ice inference.',fontsize=9)
fig.subplots_adjust(left=.07,right=.97,top=.83,bottom=.24,wspace=.5);save(fig,'F-GAP02_spectral_implementation_QA')
# Same-observation radar and clutter. Display panels independently scaled, never subtracted.
a=np.load(O/'radar_local_arrays.npz');cols=a['column_1based'];rows=a['row_0based'];fig,axs=plt.subplots(1,2,figsize=(12.5,6.5),sharex=True,sharey=True)
for ax,key,title in zip(axs,['observed','simulated'],['A  Observed US radargram','B  Official surface-clutter simulation']):
 z=a[key];db=np.where(z>0,10*np.log10(np.maximum(z,np.finfo('float32').tiny)/z.max()),np.nan)
 im=ax.imshow(db,origin='upper',aspect='auto',extent=(cols[0]-.5,cols[-1]+.5,rows[-1]+.5,rows[0]-.5),vmin=-45,vmax=0,cmap='gray',interpolation='nearest');ax.plot(cols,a['nadir'],color='#12bbc0',lw=1,label='Model nadir row');ax.plot(cols,a['first'],color='#df8700',lw=.8,label='Model first return');ax.set_title(title);ax.set_xlabel('Official radargram column (one-based)');fig.colorbar(im,ax=ax,label='Display dB relative to this panel maximum')
axs[0].set_ylabel('Official range row (zero-based; not ice depth)');axs[0].legend(loc='lower left',fontsize=8)
fig.suptitle('MS-03 | S_04624502_RGRAM + same-track clutter',fontsize=15,x=.07,ha='left')
fig.text(.07,.115,'65 planetocentric GEOM centres inside MS-03 | 2016-06-07 22:23:51.611–22:24:01.059 UTC | rows 2182–2450; columns 2185–2249.',fontsize=9)
fig.text(.07,.08,'Source: PDS USRDR v2 and UA SHARAD surface-clutter archive. Native sample spacing 0.0375 µs; not vertical resolving power.',fontsize=9)
fig.text(.07,.045,'Independent panel display scaling; no power subtraction. Model amplitude is not calibrated; missing model clutter remains possible.',fontsize=9)
fig.text(.07,.02,'No validated subsurface reflector, ice depth or content. Off-nadir scattering may originate outside the fixed cell.',fontsize=9)
fig.subplots_adjust(left=.07,right=.96,top=.88,bottom=.22,wspace=.3);save(fig,'F-GAP03_same_track_radar_clutter')
print('Rendered three evidence figures.')
