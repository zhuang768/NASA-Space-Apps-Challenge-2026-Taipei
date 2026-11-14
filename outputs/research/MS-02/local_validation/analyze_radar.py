"""Extract observed SHARAD columns inside ROI; compare with archive clutter browse.
No reflector picking, dielectric inversion, or ice/no-ice classification.
"""
from pathlib import Path
import csv,re,json
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent; S=P/'sources/products'
def main():
 out=P/'radar_roi';out.mkdir(exist_ok=True);results=[]
 fig,axes=plt.subplots(3,2,figsize=(11,12))
 for k,oid in enumerate(['00464501','01983502','02004601']):
  prefix='s_'+oid
  label=(S/(prefix+'_rgram.lbl')).read_text();n=int(re.search(r'LINE_SAMPLES\s*=\s*(\d+)',label)[1]);m=int(re.search(r'LINES\s*=\s*(\d+)',label)[1])
  rows=list(csv.reader((S/(prefix+'_geom.tab')).open()));assert len(rows)==n
  nums=np.array([[float(r[i]) for i in [0,2,3,8,9]] for r in rows]);assert np.array_equal(nums[:,0],np.arange(1,n+1))
  sel=np.flatnonzero((nums[:,1]>=52.5)&(nums[:,1]<=53)&(nums[:,2]>=168)&(nums[:,2]<=168.5));assert len(sel)>0 and np.all(np.diff(sel)==1)
  raw=S/(prefix+'_rgram.img');assert raw.stat().st_size==m*n*4
  data=np.memmap(raw,dtype='<f4',mode='r',shape=(m,n));a=np.array(data[:,sel]);assert np.isfinite(a).all()
  np.savez_compressed(out/(prefix+'.npz'),power=a,source_columns_1based=sel+1,latitude=nums[sel,1],longitude=nums[sel,2])
  with (out/(prefix+'_geom.csv')).open('w',newline='') as f:
   w=csv.writer(f);w.writerow(['source_column_1based','utc','latitude','longitude','mars_radius_km','spacecraft_radius_km','radial_velocity_m_s','tangential_velocity_m_s','sza_deg','phase_per_1e16']);w.writerows([rows[i] for i in sel])
  # Row 1800 is AREOID, not surface. Display all delay rows; do not infer depth.
  sl=slice(0,m);db=10*np.log10(np.maximum(a[sl],np.finfo(np.float32).tiny));lo,hi=np.percentile(db,[5,99])
  axes[k,0].imshow(db,cmap='gray',aspect='auto',extent=[sel[0]+1,sel[-1]+1,m,0],vmin=lo,vmax=hi)
  axes[k,0].set_title(prefix+' observed power (display dB)')
  sim=Image.open(S/(prefix+'_browse_combined.tif'));assert sim.size==(n,m),sim.size
  simcrop=np.asarray(sim.crop((int(sel[0]),0,int(sel[-1]+1),m)))
  Image.fromarray(simcrop).save(out/(prefix+'_clutter_roi.png'))
  axes[k,1].imshow(simcrop,cmap='gray',aspect='auto',extent=[sel[0]+1,sel[-1]+1,m,0]);axes[k,1].set_title(prefix+' simulated surface clutter (browse)')
  for ax in axes[k]:ax.set_ylabel('Native radargram row (not depth)');ax.set_xlabel('Source column, 1-based')
  results.append(dict(orbit_segment=oid,columns=len(sel),column_first_1based=int(sel[0]+1),column_last_1based=int(sel[-1]+1),
   first_utc=rows[sel[0]][1],last_utc=rows[sel[-1]][1],latitude_min=float(nums[sel,1].min()),latitude_max=float(nums[sel,1].max()),
   longitude_min=float(nums[sel,2].min()),longitude_max=float(nums[sel,2].max()),finite_fraction=float(np.isfinite(a).mean()),
   zero_fraction=float((a==0).mean()),phase_per_1e16_min=float(nums[sel,4].min()),phase_per_1e16_max=float(nums[sel,4].max()),
   nominal_along_track_posting_m=460,delay_sample_us=0.0375,classification='unclassified; no accepted subsurface ice reflector',
   caveat='Posting is not independent resolution; sidelobes and surface clutter remain; browse amplitudes are not calibrated to observed power'))
 fig.tight_layout();fig.savefig(P/'fig_sharad_observed_clutter.png',dpi=160)
 (P/'radar_checks.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main()
