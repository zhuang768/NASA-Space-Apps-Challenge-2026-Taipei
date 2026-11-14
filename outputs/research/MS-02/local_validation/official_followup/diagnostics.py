import pathlib,csv,json,itertools
import numpy as np
from scipy.signal import find_peaks
P=pathlib.Path(__file__).parent;S=P/'sources';O=P/'derived';ids=['00464501','01983502','02004601'];candidates=[];tracks={}
for id in ids:
 a=np.load((S/f's_{id}.npz') if (S/f's_{id}.npz').exists() else P.parent/'radar_roi'/f's_{id}.npz');obs=a['power'];sim=np.load(O/f's_{id}_numeric_clutter_roi.npz')['power'];picks=list(csv.DictReader(open(O/f's_{id}_surface_picks.csv')));tracks[id]=a
 for j,p in enumerate(picks):
  pick=int(p['observed_peak_row_0based']);pred=int(p['predicted_nadir_row_0based']);noise=float(p['local_noise_power']);speak=np.argmax(sim[max(0,pred-40):min(3600,pred+41),j])+max(0,pred-40)
  db=10*np.log10(np.maximum(obs[:,j],1e-30)/max(noise,1e-30));peaks,_=find_peaks(db[pick+30:pick+201],height=6,prominence=3,distance=3)
  sp,_=find_peaks(sim[:,j],prominence=max(float(sim[:,j].max())*.01,1e-30),distance=2)
  for rel in peaks+30:
   row=pick+rel;clut=bool(np.any(abs((sp-speak)-rel)<=3))
   candidates.append(dict(track=id,column_1based=p['column_1based'],relative_delay_samples=int(rel),relative_delay_us=float(rel*.0375),peak_noise_dB=float(db[row]),numerical_clutter_peak_within_3_samples=clut,classification='unvalidated peak; clutter-compatible'if clut else'unvalidated peak; sidelobes and cross-track agreement unresolved',accepted_ice_reflector=False))
if candidates:
 with(O/'radar_candidate_screen.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=candidates[0]);w.writeheader();w.writerows(candidates)
pairs=[]
for i,j in itertools.combinations(ids,2):
 a,b=tracks[i],tracks[j];la=np.deg2rad(a['latitude'])[:,None];lb=np.deg2rad(b['latitude'])[None,:];dl=np.deg2rad(a['longitude'][:,None]-b['longitude'][None,:]);h=np.sin((la-lb)/2)**2+np.cos(la)*np.cos(lb)*np.sin(dl/2)**2;dist=3396190*2*np.arcsin(np.sqrt(h));mn=np.unravel_index(np.argmin(dist),dist.shape)
 pairs.append(dict(track_a=i,track_b=j,min_posting_separation_m=float(dist[mn]),a_column_1based=int(a['source_columns_1based'][mn[0]]),b_column_1based=int(b['source_columns_1based'][mn[1]]),same_ground_point_proven=False))
with(O/'radar_cross_track_geometry.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=pairs[0]);w.writeheader();w.writerows(pairs)
# authoritative reproducible catalogue inventory, preserving legacy discrepancy
products=json.load(open(S/'CRISM_TRDR.json'))['ODEResults']['Products']['Product'];rows=[dict(product_id=x['pdsid'],ode_id=x.get('ode_id'),source='PDS ODE REST fixed bounding query',access_date_utc='2026-11-14')for x in products]
with(O/'crism_trdr_inventory.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
(O/'catalog_reconciliation.json').write_text(json.dumps(dict(rest_entries=len(rows),unique_product_ids=len(set(x['product_id']for x in rows)),legacy_browser_claim=180,legacy_180_id_manifest_available=False,operational_decision='Use explicit 177-ID REST inventory for this release; do not add three invented observations. Historical browser difference remains unexplained.'),indent=2))
print('candidate peaks',len(candidates),'clutter compatible',sum(x['numerical_clutter_peak_within_3_samples']for x in candidates));print(pairs)
