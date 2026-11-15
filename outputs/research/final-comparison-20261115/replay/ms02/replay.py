"""MS-02 reproducibility from pinned repository inputs. No downloads or source edits."""
from pathlib import Path
from itertools import combinations
import argparse, csv, hashlib, json, math
import numpy as np
parser = argparse.ArgumentParser(description='Recompute selected MS-02 SHARAD and Adventdalen results.')
parser.add_argument('--repo', type=Path, required=True, help='Checkout containing the pinned MS-02 inputs')
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
ROOT = args.out.resolve()
ROOT.mkdir(parents=True, exist_ok=True)
RESEARCH = args.repo.resolve() / 'outputs' / 'research'
LOCAL = RESEARCH / 'MS-02' / 'local_validation'
RADAR = LOCAL / 'radar_roi'
CORES = LOCAL / 'official_followup' / 'derived'
MARS = RESEARCH / 'mars_reselection_20261114' / 'final_candidates.csv'
def rows(p):
 with p.open(newline='') as f: return list(csv.DictReader(f))
def export(name, result):
 with (ROOT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,result[0].keys());w.writeheader();w.writerows(result)
def stats(x):
 return dict(count=len(x),min=float(np.min(x)),median=float(np.median(x)),max=float(np.max(x)))
pins={'00464501':'4d08b6b9083e19a9cac7fde6415d99291fbd720df444388eff91c8d227c92608','01983502':'198ba059c4b3c379bfeb7f492ad381461c192edc74a12c7791b60c1aedf2d90c','02004601':'7a3332adfadaecbe1b7273881157b99ed8162396d2b19315f0cdb3b137fb2132'}
# Independent declared rule: max of linear power, nearest contiguous crossing of
# half that peak on both sides; linearly interpolate in linear (not dB) power.
# Also show sensitivity to dB interpolation and subtracting a local noise proxy.
def width(a, pk, cut, db=False):
 l,r=pk,pk
 while l>0 and a[l-1]>=cut:l-=1
 while r<len(a)-1 and a[r+1]>=cut:r+=1
 if l==0 or r==len(a)-1:return float('nan')
 if db:a=np.log(a);cut=np.log(cut)
 lo=l-(a[l]-cut)/(a[l]-a[l-1])
 hi=r+(a[r]-cut)/(a[r]-a[r+1])
 return hi-lo
def arc(lon,lat):
 u=np.radians(lat);v=np.radians(lon)
 h=np.sin(np.diff(u)/2)**2+np.cos(u[:-1])*np.cos(u[1:])*np.sin(np.diff(v)/2)**2
 return 3396000*2*np.arcsin(np.sqrt(h))
echo=[]; posting={}
for n,h in pins.items():
 p=RADAR/f's_{n}.npz'; 
 if hashlib.sha256(p.read_bytes()).hexdigest()!=h:
  raise ValueError(f'Unexpected SHARAD input digest: {p.name}')
 z=np.load(p);power=z['power'].astype(float)
 posting[n]=stats(arc(z['longitude'],z['latitude']))
 for j,a in enumerate(power.T):
  pk=int(a.argmax()); cut=a[pk]/2
  bas=float(np.median(a[200:1000]))
  echo.append(dict(orbit=n,column_source_1based=int(z['source_columns_1based'][j]),peak_row_zero_based=pk,
    fwhm_samples=width(a,pk,cut),fwhm_db_interp_samples=width(a,pk,cut,True),
    fwhm_baseline_adjusted_samples=width(a,pk,(a[pk]+bas)/2)))
assert len(echo)==194
export('sharad_echo_fwhm.csv',echo)
other_expected={
 CORES/'adventdalen_2023_core_overview.csv':'61fa1977395a200365535c297b1b7330f4583abd35a48af22b7b5d434bca6fa6',
 CORES/'adventdalen_2023_core_samples.csv':'6784303d853429b7b304d48f60d771d5064bb41e739b0ede490c424af17eca15',
 MARS:'83a03d1f4273fa7c45c0d22b5c29a8b8cfc0544e481d5f2bbca2c85812534c4e',
}
for path,expected in other_expected.items():
 if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
  raise ValueError(f'Unexpected input digest: {path.relative_to(RESEARCH)}')
overview=rows(CORES/'adventdalen_2023_core_overview.csv');samples=rows(CORES/'adventdalen_2023_core_samples.csv')
def eic(s):
 try:return float(s['EIC_vol_percent'])
 except ValueError:return float('nan')
core=[]
for r in overview:
 n=r['Core']; full=[s for s in samples if s['core']==n]
 # Do not silently treat a disturbed sample as a measured intact layer, or a
 # missing value as zero. Overlaps disallow unique contiguous group membership.
 g=sorted([s for s in full if s['sample_type']=='Core'],key=lambda s:float(s['upper_depth_cm']))
 first=next((j for j,s in enumerate(g) if eic(s)>0),None)
 lo=hi=None
 if first is not None:
  lo=float(g[first]['upper_depth_cm']);hi=float(g[first]['lower_depth_cm'])
  for s in g[first+1:]:
   if not (float(s['upper_depth_cm'])==hi and eic(s)>0):break
   hi=float(s['lower_depth_cm'])
 core.append(dict(core=n,ALT_cm=float(r['ALT (cm)']),X_UTM_m=int(r['UTM X']),Y_UTM_m=int(r['UTM Y']),
   sample_count_all=len(full),intact_count=len(g),intact_eic_positive_count=sum(eic(s)>0 for s in g),
   all_eic_positive_count=sum(eic(s)>0 for s in full),first_intact_EIC_positive_upper_cm=lo,
   first_contiguous_intact_positive_interval_cm=hi-lo if lo is not None else None))
export('adventdalen_core_ice_replay.csv',core)
pairs=sorted((math.hypot(a['X_UTM_m']-b['X_UTM_m'],a['Y_UTM_m']-b['Y_UTM_m']),a['core'],b['core']) for a,b in combinations(core,2))
cand=[r for r in rows(MARS) if r['candidate_id']=='MS-02']
assert len(cand)==1
row=cand[0]
keys=['lat','lon_east_0_360','north_south_km','east_west_km','mola_elevation_m_mean','mola_elevation_m_median','mola_relief_m','mola_slope_deg_median','TES_TI_valid_cells','TES_TI_native_cells',*[f'SWIM_{d}_{k}' for d in ('0_1m','1_5m') for k in ('mean','median','min','max','valid_cells','native_cells')]]
native={k:float(row[k]) for k in keys}
assert math.isclose(native['north_south_km'],3396*math.radians(.5))
assert math.isclose(native['east_west_km'],3396*math.cos(math.radians(native['lat']))*math.radians(.5))
export('mars_cell_pinned_extraction.csv',[native])
C=299792458.; d=.45; dt=37.5e-9; b=10e6
sc=[]
for e in [2,3.15,6,9,40]:
 t=2*d*math.sqrt(e)/C
 sc.append(dict(epsilon=e,sharad_045_delay_ns=t*1e9,sharad_045_delay_samples=t/dt,
  sharad_nominal_resolution_m=C/(2*b*math.sqrt(e)),depth_of_19_3ns_m=C*19.3e-9/(2*math.sqrt(e))))
export('modeled_velocity_and_orbital_scale.csv',sc)
out={'observed_posting_m':posting,'echo':{k:stats([x[k] for x in echo]) for k in list(echo[0])[3:]},
 'cores':{'ALT_cm':stats([x['ALT_cm'] for x in core]),'intact_positive_cores_count':sum(x['intact_eic_positive_count']>0 for x in core),
 'first_intact_positive_upper_cm':stats([x['first_intact_EIC_positive_upper_cm'] for x in core if x['first_intact_EIC_positive_upper_cm'] is not None]),
 'first_contiguous_intact_positive_cm':stats([x['first_contiguous_intact_positive_interval_cm'] for x in core if x['first_contiguous_intact_positive_interval_cm'] is not None]),'closest_pair':pairs[0]},
 'mars_geometry_km':{'north_south':3396*math.radians(.5),'east_west_at_center':3396*math.cos(math.radians(52.75))*math.radians(.5)},
 'hann_assumed_FWHM_samples':1.44/(b*dt),
 'median_echo_FWHM_us':np.median([x['fwhm_samples'] for x in echo])*dt*1e6,
 'median_echo_FWHM_in_ice_m':np.median([x['fwhm_samples'] for x in echo])*dt*C/(2*math.sqrt(3.15)),
 'WISDOM_assumed_resolution_cm_range':[100*C/(2*2.5e9*math.sqrt(7)),100*C/(2*.5e9*math.sqrt(3.2))]}
(ROOT/'replay_summary.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
