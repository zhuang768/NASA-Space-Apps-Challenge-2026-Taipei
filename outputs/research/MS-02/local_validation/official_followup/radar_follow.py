import pathlib,json,urllib.request,xml.etree.ElementTree as E,concurrent.futures,csv,hashlib
import numpy as np
from scipy.signal import find_peaks
P=pathlib.Path(__file__).parent;S=P/'sources';O=P/'derived'
def run(id):
 old=np.load((S/f's_{id}.npz') if (S/f's_{id}.npz').exists() else P.parent/'radar_roi'/f's_{id}.npz');power=old['power'];cols=old['source_columns_1based'].astype(int)-1;n=len(list(csv.DictReader((S/f's_{id}_rtrn.csv').open())));root=E.parse(S/f's_{id}_sim.xml');ns={'p':'http://pds.nasa.gov/pds4/pds/v1'};arrs=root.findall('.//p:Array_2D_Image',ns);off=int(arrs[-1].find('p:offset',ns).text);size=3600*n*4;url=f'https://pds-geosciences.wustl.edu/mro/urn-nasa-pds-mro_sharad_simulations/data/s_{id[:4]}xx/s_{id}/s_{id}_sim.img'
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':f'bytes={off}-{off+size-1}'}),timeout=120)as r:
  raw=r.read();assert r.status==206 and len(raw)==size
 sim=np.frombuffer(raw,dtype='<f4').reshape(3600,n)[:,cols].copy();np.savez_compressed(O/f's_{id}_numeric_clutter_roi.npz',power=sim,source_columns_1based=cols+1)
 geom=list(csv.DictReader((S/f's_{id}_rtrn.csv').open()));records=[];aligned=np.full((401,len(cols)),np.nan,dtype='f4')
 for j,c in enumerate(cols):
  pred=int(geom[c]['NadirLine'])-1;lo=max(0,pred-40);hi=min(3600,pred+41);pick=lo+np.argmax(power[lo:hi,j]);noise=float(np.median(power[max(0,pick-400):max(1,pick-100),j]));snr=10*np.log10(power[pick,j]/max(noise,1e-30));ind=pick+np.arange(-100,301);ok=(ind>=0)&(ind<3600);aligned[ok,j]=power[ind[ok],j]
  records.append(dict(track=id,column_1based=int(c+1),latitude=float(old['latitude'][j]),longitude=float(old['longitude'][j]),predicted_nadir_row_0based=pred,observed_peak_row_0based=int(pick),peak_offset_samples=int(pick-pred),local_noise_power=noise,surface_peak_to_noise_dB=float(snr),surface_pick_method='maximum within +-40 samples of simulated nadir; provisional; not an accepted subsurface reflector'))
 np.savez_compressed(O/f's_{id}_surface_aligned.npz',observed_power=aligned,relative_delay_samples=np.arange(-100,301),latitude=old['latitude'],longitude=old['longitude'])
 with(O/f's_{id}_surface_picks.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
 # amplitude-normalized numerical clutter compared only for timing, not reflectivity
 return dict(track=id,ncols=len(cols),numeric_clutter_url=url,range_start=off,range_end=off+size-1,download_sha256=hashlib.sha256(raw).hexdigest(),median_surface_peak_offset_samples=float(np.median([x['peak_offset_samples']for x in records])),median_peak_noise_dB=float(np.median([x['surface_peak_to_noise_dB']for x in records])),accepted_ice_reflectors=0,caveat='zero accepted is not evidence of no ice; clutter matching, sidelobes and dielectric assumptions limit classification')
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as ex:r=list(ex.map(run,['00464501','01983502','02004601']))
(O/'radar_followup_qc.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
