#!/usr/bin/env python3
"""Recompute scale and documented PQ19-only thermal transfer, not ice truth."""
from pathlib import Path
import csv, hashlib, json, math
root=Path(__file__).resolve().parent
R=3396.19
def read_csv(n):
    with (root/n).open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))
def deg_dist(lat1,lon1,lat2,lon2):
    p,x,q,y=map(math.radians,(lat1,lon1,lat2,lon2))
    h=math.sin((q-p)/2)**2+math.cos(p)*math.cos(q)*math.sin((y-x)/2)**2
    return 2*R*math.asin(math.sqrt(min(h,1)))
def area(s,n,w,e):
    s,n,w,e=map(math.radians,(s,n,w,e))
    return R**2*(math.sin(n)-math.sin(s))*(e-w)
def fmt(v): return f"{v:.6f}"
def clamp(v): return max(0,min(1,v))
models={r['site']:r for r in read_csv('model_source.csv')}
metrics={r['candidate_id']:r for r in read_csv('candidates_source.csv')}
sites=json.loads((root/'targets_source.json').read_text())['sites']
assert set(models)==set(metrics)=={s['id'] for s in sites}
rows=[]
for site in sites:
    i=site['id']; model=models[i]; met=metrics[i]
    lat=site['center']['lat']; lon=site['lon_east_0_360']
    assert lat==float(model['latitude_deg_N'])==float(met['lat'])
    assert lon==float(model['longitude_deg_E'])==float(met['lon_east_0_360'])
    s,n,w,e=(site['bounds'][q] for q in ('south','north','west','east'))
    assert (s,n,w%360,e%360)==tuple(float(model[k]) for k in ('south_deg_N','north_deg_N','west_deg_E','east_deg_E'))
    a=area(s,n,w,e)
    dp=float(model['conditional_depth_m'])
    assert 0<=dp<=.5
    pq=clamp((.50-dp)/.20)
    lo=clamp((.50-(dp+.05))/.20); hi=clamp((.50-(dp-.05))/.20)
    mlat,mlon=map(float,(met['MCS_native_lat'],met['MCS_native_lon']))
    dlat,dlon=map(float,(met['dust_my34_native_cell_lat'],met['dust_my34_native_cell_lon']))
    count=int(met['MCS_paired_bins']); den=int(met['MCS_expected_year_season_pairs'])
    rows.append({
      'site':i, 'lat_deg_N':lat, 'lon_deg_E':lon, 'box_area_km2':fmt(a),
      'TES_valid_cells':met['TES_TI_valid_cells'], 'TES_nominal_cells':met['TES_TI_native_cells'],
      'MCS_nearest_grid_center_distance_km':fmt(deg_dist(lat,lon,mlat,mlon)),
      'MY34_dust_nearest_grid_center_distance_km':fmt(deg_dist(lat,lon,dlat,dlon)),
      'MCS_paired_bins':count, 'MCS_expected_pairs':den, 'MCS_paired_fraction':fmt(count/den),
      'PQ19_conditional_model_depth_m':f'{dp:.10g}',
      'PQ19_only_consistency_arithmetic':fmt(pq),
      'PQ19_only_if_depth_plus_0p05m':fmt(lo),
      'PQ19_only_if_depth_minus_0p05m':fmt(hi),
      'nominal_shallow_composite_term_if_all_factors_present':fmt(pq/(3*2.4)),
      'nominal_term_change_if_depth_plus_0p05m':fmt((lo-pq)/(3*2.4)),
      'nominal_term_change_if_depth_minus_0p05m':fmt((hi-pq)/(3*2.4)),
      'nominal_1to5m_PQ19_direct_weight':'0',
    })
with (root/'cross_site_checks.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
for name in ['targets_source.json','candidates_source.csv','model_source.csv','cross_site_checks.csv']:
    b=(root/name).read_bytes();print(hashlib.sha256(b).hexdigest(),name)
