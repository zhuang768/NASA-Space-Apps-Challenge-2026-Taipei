"""Actual pixel centres and uncorrected per-channel distributions; no detection map."""
from pathlib import Path
import json,csv,gzip
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).resolve().parent
q=json.loads((O/'qa.json').read_text());products=q['products'];r=list(csv.DictReader(gzip.open(O/'roi_pixels.csv.gz','rt')));ch=list(csv.DictReader((O/'channel_qa.csv').open(encoding='utf-8-sig')))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig,axs=plt.subplots(2,2,figsize=(14,10),dpi=180);fig.subplots_adjust(left=.08,right=.97,top=.86,bottom=.22,hspace=.55,wspace=.28)
for i,p in enumerate(products):
 pid=p['product_id'];a=[x for x in r if x['product_id']==pid];x=np.array([float(z['longitude_east_0_360_deg']) for z in a]);y=np.array([float(z['latitude_planetocentric_deg']) for z in a]);valid=np.array([z['positive_1300_2200_nm']=='True' for z in a]);ax=axs[0,i]
 ax.scatter(x[~valid],y[~valid],s=5,color='#b2b6bd',label='Calibration/non-scene or numeric failure');ax.scatter(x[valid],y[valid],s=5,color='#007f8b',label='Basic numeric/calibration checks pass')
 ax.set(xlim=(242,242.5),ylim=(57.5,58),xlabel='Mars east longitude (deg)',ylabel='Planetocentric latitude (deg)',title=pid.upper()+'\n'+p['UTC_start'][:10]+f" | {valid.sum():,}/{len(a):,} centres pass")
 ax.grid(alpha=.2);ax.legend(fontsize=8,loc='lower right',markerscale=1.2)
 ax=axs[1,i];a=[z for z in ch if z['product_id']==pid and z['wavelength_nm_median'] and z['IF_median'] and 1250<=float(z['wavelength_nm_median'])<=2400];w=np.array([float(z['wavelength_nm_median']) for z in a]);z=np.array([float(z['IF_median']) for z in a]);lo=np.array([float(v['IF_p05']) for v in a]);hi=np.array([float(v['IF_p95']) for v in a]);ax.vlines(w,lo,hi,color='#99bcc1',lw=1,label='Spatial 5th–95th percentiles');ax.scatter(w,z,s=10,color='#007f8b',label='Median of numeric/calibration-valid samples');ax.axvline(1525,color='#bd7945',ls=':',lw=1);ax.text(1525,.97,'1525 nm reference',rotation=90,ha='right',va='top',fontsize=8,transform=ax.get_xaxis_transform());ax.set(xlabel='Per-channel median wavelength (nm; no spectral resampling)',ylabel='Uncorrected I/F (dimensionless)',title=f"{p['all_1300_2200_positive_pixels']:,} centres pass across sampled 1300–2200 nm channels");ax.grid(alpha=.2);ax.legend(fontsize=8,loc='lower left')
fig.suptitle('MS-03 CRISM: acquired local spectra and basic pixel QA\nIce presence remains unknown; these are not ice-detection maps',fontsize=17,y=.97)
fig.text(.08,.14,'Sources: NASA/MRO CRISM PDS TRR3 + matching DDR1 + exact WA CDR3; product URLs and byte ranges in retrievals.json.\nMaps show DDR pixel centres (IR reference near2300 nm), not validated footprints or whole-cell quality coverage.\n10x spatial binning; median adjacent cross-track centre spacing ~188 m (not a measured PSF or crack resolution).\nAtmospheric, thermal and photometric correction flags are OFF. Cloud/frost and instrument residual QA remain incomplete.\nDots retain the transmitted channels; gaps are not filled. Spatial percentiles are not confidence intervals or a detection threshold.',ha='left',va='top',fontsize=10)
fig.savefig(O/'F-CRISM01_pixel_QA_spectra.png',facecolor='white');plt.close(fig)
