import pathlib,json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
P=pathlib.Path(__file__).parent;O=P/'derived';S=P/'sources'
rows=list(csv.DictReader(open(O/'thermal_epoch_qc.csv')));fig,axs=plt.subplots(3,3,figsize=(11,10),layout='constrained')
for ax,r in zip(axs.flat,rows):
 a=np.load(O/(r['product']+'.npy'));im=ax.imshow(a,origin='lower',extent=[168,168.5,52.5,53],vmin=155,vmax=245,cmap='inferno',aspect='auto');ax.set_title(f"{r['product']}\nLs {r['Ls_deg']}, LT {r['local_time_h']}",fontsize=9);ax.set_xlabel('East longitude');ax.set_ylabel('Planetocentric latitude')
fig.colorbar(im,ax=axs,label='Band 9 brightness temperature (K)',shrink=.7);fig.suptitle('MS-02: projected PDS THEMIS pixels; white = no valid sample\nDifferent Ls/local time; temperatures do not establish ice',fontsize=12);fig.savefig(O/'F01_thermal_epochs.png',dpi=140);plt.close(fig)
fig,axs=plt.subplots(3,2,figsize=(11,10),layout='constrained')
for k,id in enumerate(['00464501','01983502','02004601']):
 a=np.load((S/f's_{id}.npz') if (S/f's_{id}.npz').exists() else P.parent/'radar_roi'/f's_{id}.npz');b=np.load(O/f's_{id}_numeric_clutter_roi.npz');pick=list(csv.DictReader(open(O/f's_{id}_surface_picks.csv')));rr=np.array([int(x['observed_peak_row_0based'])for x in pick]);lo,hi=rr.min()-100,rr.max()+300
 for ax,x,title in [(axs[k,0],a['power'],'Observed'),(axs[k,1],b['power'],'Numerical surface clutter')]:
  db=10*np.log10(np.maximum(x[lo:hi],1e-30));ax.imshow(db,aspect='auto',cmap='gray',vmin=np.percentile(db,5),vmax=np.percentile(db,99),extent=[a['source_columns_1based'][0],a['source_columns_1based'][-1],hi,lo]);ax.plot(a['source_columns_1based'],rr,color='cyan',lw=.7);ax.set_title(f'{id}: {title}');ax.set_ylabel('Native delay row (not depth)');ax.set_xlabel('Source column (1-based)')
fig.suptitle('Independent display stretches: amplitudes cannot be compared\nCyan = provisional observed surface peak; no accepted ice reflector',fontsize=12);fig.savefig(O/'F02_radar_numeric_clutter.png',dpi=140);plt.close(fig)
a=np.load(O/'mrdr4_roi.npz');g=np.load(O/'mrdr4_geometry_roi.npz')['geometry'];r=list(csv.DictReader(open(O/'mrdr4_filtered_spectrum.csv')));fig,ax=plt.subplots(1,2,figsize=(11,4),layout='constrained');ax[0].plot([float(x['wavelength_nm'])/1000 for x in r],[float(x['median_albedo'])if x['median_albedo']else np.nan for x in r],'.-');ax[0].set(xlabel='Wavelength (micrometres)',ylabel='Median delivered Lambert albedo',title='Geometry-filtered PDS MRDR4 spectrum');im=ax[1].imshow(np.isfinite(a['albedo']).mean(0),extent=[a['longitude'][0],a['longitude'][-1],a['latitude'][-1],a['latitude'][0]],vmin=0,vmax=1);ax[1].set(title='Fraction of 72 numerically valid bands',xlabel='East longitude',ylabel='Planetocentric latitude');fig.colorbar(im,ax=ax[1]);fig.suptitle('No unique mineral or water-ice identification; residual atmospheric and mosaic effects remain');fig.savefig(O/'F03_crism_mrdr4.png',dpi=140);plt.close(fig)
meta=json.load(open(O/'ctx_sample_metadata.json'));fig,axs=plt.subplots(1,5,figsize=(15,4),layout='constrained')
for ax,r in zip(axs,meta):
 ax.imshow(Image.open(S/f"ctx_{r['sample']}_L12.png"),cmap='gray');ax.set_title(f"{r['sample']}\n{r['anchor_lon']}, {r['anchor_lat']}");ax.axis('off')
fig.suptitle('Five fixed MS-02 samples: Esri beta01 uncontrolled CTX rendering\nNative source ~5-6 m; geographic rendering is not absolute co-registration or ice truth');fig.savefig(O/'F04_ctx_samples.png',dpi=140);plt.close(fig)
r=list(csv.DictReader(open(O/'uniscalm_by_date.csv')));fig,ax=plt.subplots(figsize=(9,4),layout='constrained');y=np.array([float(x['mean_cm'])for x in r]);mn=np.array([float(x['min_cm'])for x in r]);mx=np.array([float(x['max_cm'])for x in r]);ax.errorbar([x['date']for x in r],y,yerr=[y-mn,mx-y],fmt='o-',capsize=4);ax.tick_params(axis='x',rotation=30);ax.set(ylabel='Measured thaw depth (cm)',title='UNISCALM: 121 probing nodes per observation date\nBars = spatial min/max, not uncertainty; dates differ across years');fig.savefig(O/'F05_uniscalm.png',dpi=140);plt.close(fig)
print('five figures written')
