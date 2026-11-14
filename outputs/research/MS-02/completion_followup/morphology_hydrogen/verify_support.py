"""Independent midpoint-integration check of catalogue footprint intersections.

Uses vectorized half-plane point tests, not polygon clipping or inclusion/exclusion.
Run with Python and numpy. Scientific completeness is explicitly separate from QA.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import analyze_support as a

H=Path(__file__).resolve().parent
rows=a.read_ctx()
s=json.loads((H/'support_summary.json').read_text())
N=1000
lon,lat=np.meshgrid(168+(np.arange(N)+0.5)*0.5/N,52.5+(np.arange(N)+0.5)*0.5/N)
weights=np.cos(np.radians(lat))
masks=[]
for r in rows:
    p=r['poly']; mask=np.ones(lon.shape,dtype=bool)
    for u,v in zip(p,p[1:]+p[:1]):
        mask &= (v[0]-u[0])*(lat-u[1])-(v[1]-u[1])*(lon-u[0]) >= 0
    masks.append(mask)
total=weights.sum()
checks=[]
def check(name,ok,**detail):
    checks.append(dict(check=name,passed=bool(ok),**detail))
check('pinned_source_sha256',hashlib.sha256(a.SOURCE.read_bytes()).hexdigest()==s['source_sha256'])
check('legacy_spatial_reproduction',s['maximum_legacy_fraction_error']<1e-10,error=s['maximum_legacy_fraction_error'])
grid_counts=np.sum(masks,axis=0)
mult=list(csv.DictReader((H/'ctx_coverage_multiplicity.csv').open()))
for r in mult:
    k=int(r['number_of_epochs'])
    observed=float(weights[grid_counts>=k].sum()/total)
    analytic=float(r['at_least_roi_fraction'])
    check(f'independent_grid_at_least_{k}',abs(observed-analytic)<0.001,
          grid_fraction=observed,analytic_fraction=analytic,tolerance=0.001)
pairs=list(csv.DictReader((H/'ctx_pair_support.csv').open()))
ids=[r['product_id'] for r in rows]
for r in pairs:
    i,j=ids.index(r['product_a']),ids.index(r['product_b'])
    observed=float(weights[masks[i]&masks[j]].sum()/total)
    analytic=float(r['common_nominal_roi_fraction'])
    check(f"independent_grid_{i}_{j}",abs(observed-analytic)<0.001,
          grid_fraction=observed,analytic_fraction=analytic,tolerance=0.001)
check('no_unmeasured_change_or_weh',all(s[k] is None for k in
      ['actual_valid_image_fraction','actual_change_rate','hydrogen_weh_wt_percent']))
check('all_science_status_unclosed','remain unclosed' in s['scientific_status'])
check('roi_not_earth_radius',a.RADIUS_M==3396190)
out=dict(verification_scope='numerical nominal footprint/time geometry only; not scientific gap closure',
         checks=checks,all_passed=all(c['passed'] for c in checks),
         independent_method='1000x1000 midpoint samples; cosine-latitude area weights; direct polygon half-plane tests',
         check_count=len(checks))
(H/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(all_passed=out['all_passed'],check_count=len(checks)),indent=2))
assert out['all_passed']
