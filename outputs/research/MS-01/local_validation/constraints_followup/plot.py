"""Plot actual same-column received power and corresponding surface simulation."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent;d=np.load(p/'radar_clutter_roi.npz')
fig,ax=plt.subplots(1,2,figsize=(11,5),sharey=True)
for a,k,title in zip(ax,['radar_power','combined_simulation'],['Received SHARAD power','Surface-clutter simulation']):
 z=d[k];mask=(d['row0']>=2420)&(d['row0']<=2530);z=z[mask];db=10*np.log10(np.maximum(z,1e-30)/np.max(z))
 im=a.imshow(db,extent=[1663.5,1727.5,2530.5,2419.5],aspect='auto',cmap='gray',vmin=-35,vmax=0,interpolation='nearest');a.set_title(title);a.set_xlabel('Radargram column (label, 1-based)')
 fig.colorbar(im,ax=a,label='dB relative to this panel maximum')
ax[0].set_ylabel('Original radargram row (0-based; increasing delay)')
fig.suptitle('MS-01: orbit 19588, columns located inside the fixed ROI',fontsize=13)
fig.text(.07,.045,'Source: PDS USRDR V2 S_01958801_RGRAM + SIM combined array; 2010-09-30 UTC.\nSeparate power scales; qualitative comparison only. No clutter subtraction, ice pick or depth inversion.',fontsize=9)
fig.subplots_adjust(bottom=.22,top=.83,wspace=.23)
fig.savefig(p/'radar_clutter_comparison.png',dpi=160);fig.savefig(p/'radar_clutter_comparison.svg');plt.close(fig)
