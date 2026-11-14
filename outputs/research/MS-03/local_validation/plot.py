"""Evidence figures only. No inferred cracks, reflectors, unknown point fills or smoothing."""
from pathlib import Path
import json,csv,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator,FormatStrFormatter
from PIL import Image
O=Path(__file__).resolve().parent
q=json.loads((O/'ctx_observability.json').read_text());R=3396190
fig,axs=plt.subplots(2,3,figsize=(14,9),dpi=170)
ax=axs.flat[0];ax.set(xlim=(242,242.5),ylim=(57.5,58),xlabel='Mars east longitude (deg)',ylabel='Planetocentric latitude (deg)');ax.set_title('Fixed ROI and five acquired display patches',fontsize=12)
for s in q['samples']:
 b=s['bounds_mars_east180_lat'];x=b['west']+360;y=b['south'];ax.add_patch(Rectangle((x,y),b['east']-b['west'],b['north']-b['south'],fill=False,edgecolor='#087F8C',lw=1.5));ax.text(x+.006,y+.025,s['sample_id'],fontsize=11,color='#12283E')
ax.grid(alpha=.2)
for ax,s in zip(list(axs.flat)[1:],q['samples']):
 b=s['bounds_mars_east180_lat'];arr=np.asarray(Image.open(O/s['image_file']))[:,:,0]
 ax.imshow(arr,cmap='gray',vmin=0,vmax=255,interpolation='nearest',extent=[b['west']+360,b['east']+360,b['south'],b['north']],aspect='auto')
 ax.set_title(f"{s['sample_id']} | " + '+'.join(p.split('_')[0] for p in s['source_product_ids'])+'\n'+' / '.join(d[:10] for d in s['source_dates']),fontsize=10)
 ax.set_xlabel('Mars east longitude (deg)',fontsize=10);ax.set_ylabel('Planetocentric latitude (deg)',fontsize=10);ax.tick_params(labelsize=8);ax.xaxis.set_major_locator(MaxNLocator(3));ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
fig.suptitle('MS-03: five local CTX mosaic display samples; morphology remains unknown',fontsize=16,y=.99)
fig.subplots_adjust(left=.07,right=.98,top=.88,bottom=.25,wspace=.33,hspace=.55)
fig.text(.06,.12,'Source: Caltech Murray Lab CTX V01 KML + E-120_N56 seam map; NASA/JPL/MSSS/Caltech.\nDisplay grid ~5.4 m/pixel; original CTX ~6.08–6.09 m/pixel. Resampling does not add detail.\n256 x 256 pixels per patch; not whole-cell quality coverage. No reliable closed boundaries traced; absence is not established.',fontsize=11,va='top')
fig.savefig(O/'F-LV01_CTX_samples.png',facecolor='white');plt.close(fig)
# The line data are actual acquired catalogue geometries, not drawn hypothetical flight lines.
tracks=json.loads((O/'sharad_tracks.geojson').read_text())['features'];fig,ax=plt.subplots(figsize=(9,8),dpi=170)
ax.add_patch(Rectangle((242,57.5),.5,.5,facecolor='#F4F1E7',edgecolor='#12283E',lw=1.6,label='Fixed cell / one deposited thermal-model bin'))
for i,f in enumerate(tracks):
 coords=np.asarray(f['geometry']['coordinates']);ax.plot(coords[:,0],coords[:,1],color='#AF7844',alpha=.7,ls='--',lw=1.3,label='6 ODE sampled sub-spacecraft tracks' if i==0 else None)
r=list(csv.DictReader((O/'sharad_local_geometry.csv').open(encoding='utf-8-sig')));x=[float(a['longitude_east_deg']) for a in r];y=[float(a['latitude_planetocentric_deg']) for a in r]
ax.plot(x,y,color='#087F8C',lw=3,label='One acquired RDR segment (256 records)')
ax.set(xlim=(241.98,242.52),ylim=(57.48,58.02),xlabel='Mars east longitude (deg)',ylabel='Planetocentric latitude (deg)');ax.grid(alpha=.2)
ax.set_title('MS-03 geometry validation only; echoes not interpreted',fontsize=15,pad=16);ax.legend(loc='lower left',fontsize=10)
fig.subplots_adjust(bottom=.32,left=.12,right=.96,top=.90)
fig.text(.10,.19,'Thermal model: Piqueux et al. 2019 / CaltechDATA D1.1316, v1.0.\nOne 0.5-degree cell: conditional d_model ~0.10 m; actual local ice depth unknown.\nRDR: R_1768301_001_SS19_700_A, 2010-05-05; rows 57227–57482 (zero-based).\nLines are sub-spacecraft coordinates, NOT beam footprints or ice detections.\nOriginal USGS SIM3292: regional AHv polygon covers the nominal cell; 1:20M map.\nNo waveform QA, clutter simulation or dielectric/depth inversion performed.',fontsize=10,va='top')
fig.savefig(O/'F-LV02_observation_support.png',facecolor='white');plt.close(fig)
print('Two sourced evidence figures generated; unknown Mars geometry remains blank.')
