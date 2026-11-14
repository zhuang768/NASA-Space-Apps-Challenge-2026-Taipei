from pathlib import Path
import json,csv,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm,ListedColormap
O=Path(__file__).resolve().parent;q=json.loads((O/'mrdr_qa.json').read_text());p=json.loads((O/'mrdr_extraction_plan.json').read_text());z=np.load(O/'mrdr_selected_arrays.npz');m=z['source_inside'];x=z['lon'];y=z['lat'];sources=list(csv.DictReader((O/'source_observations.csv').open(encoding='utf-8-sig')))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
f,ax=plt.subplots(2,2,figsize=(15,11),dpi=180);f.subplots_adjust(left=.07,right=.94,top=.88,bottom=.24,hspace=.65,wspace=.35)
colors=['#364f6b','#e89b47','#008b8b','#7568a2','#b75e7e']
a=ax[0,0]
for i,s in enumerate(sources):
 mm=m&(z['target_id']==int(s['target_id_decimal']));a.scatter(x[mm],y[mm],s=3,color=colors[i],label=s['target_id_hex']+' | '+s['utc_start'][:10])
a.scatter(x[~m],y[~m],s=3,color='#b8b8b8',label='Source centre outside fixed cell')
a.set(title='A. Mosaic source provenance (not a single observing date)',xlabel='Mars east longitude (deg)',ylabel='Planetocentric latitude (deg)',xlim=(242,242.5),ylim=(57.5,58));a.legend(loc='upper right',fontsize=7,markerscale=2)
a=ax[0,1];data=np.ma.masked_where(~m,z['official_BD1500_2']);im=a.pcolormesh(x,y,data,cmap='RdBu_r',norm=TwoSlopeNorm(vmin=-.04,vcenter=0,vmax=.04),shading='nearest');f.colorbar(im,ax=a,label='Official BD1500_2 (dimensionless)');a.set(title='B. Official summary parameter; negative is not ice absence',xlabel='Mars east longitude (deg)',ylabel='Planetocentric latitude (deg)',xlim=(242,242.5),ylim=(57.5,58))
a=ax[1,0];w=[];med=[];lo=[];hi=[]
for req in p['requests']:
 if req['type']!='al':continue
 vals=z['AL_'+str(req['quantity'])][m];w.append(req['actual_wavelength_nm']);med.append(np.median(vals));lo.append(np.percentile(vals,5));hi.append(np.percentile(vals,95))
a.vlines(w,lo,hi,color='#9ab6c7',lw=2,label='Spatial 5th–95th percentiles');a.scatter(w,med,color='#007f8b',s=30,label='Median of selected native bands');a.set(title='C. Acquired Lambert-albedo samples (gaps not filled)',xlabel='Wavelength from official table (nm)',ylabel='Lambert albedo (dimensionless)');a.legend(fontsize=8,loc='lower right');a.grid(alpha=.2)
a=ax[1,1];d=z['recalculated_BD1500_2']-z['official_BD1500_2'];im=a.pcolormesh(x,y,np.ma.masked_where(~m,d),cmap='PuOr',norm=TwoSlopeNorm(vmin=-.02,vcenter=0,vmax=.02),shading='nearest');f.colorbar(im,ax=a,label='Recalculated minus official (dimensionless)');a.set(title='D. Formula/product difference; cause not established',xlabel='Mars east longitude (deg)',ylabel='Planetocentric latitude (deg)',xlim=(242,242.5),ylim=(57.5,58))
f.suptitle('MS-03: official-resource MRDR v4 evidence and remaining validation gaps\nIce presence / depth / content remain unknown',fontsize=17,y=.97)
f.text(.07,.15,'Source: NASA/MRO CRISM PDS MRDR v4 tileT1811; software1.03.94; product date2023-07-18.\n13,284 map centres have numeric values; 13,169 also have source DDR centres inside the fixed cell.\nNative map grid180.4662 m; sphere radius3,381,164.4 m from product labels (not Earth or a generic Mars radius).\nFive source observations span2006–2014; atmospheric/photometric/noise processing is documented, not a local cloud-free mask.\nRecalculation follows PDS July2026 multispectral reference pp1–2,5; product/reference processing differences remain unresolved.\nMissing/outside-source values are masked, not zero. Neither index values nor residuals are ice probabilities or depth measurements.',ha='left',va='top',fontsize=10)
f.savefig(O/'F-RES01_MRDR_quality_and_parameters.png',facecolor='white');plt.close(f)
