import pathlib,csv,numpy as np
P=pathlib.Path(__file__).parent;O=P/'derived';rows=list(csv.DictReader(open(O/'thermal_epoch_qc.csv')));out=[]
# Grid shift of 0.001 degree is a conservative display-grid sensitivity, NOT a validated registration uncertainty.
for i,a in enumerate(rows):
 A=np.load(O/(a['product']+'.npy'))
 for b in rows[:i]:
  B=np.load(O/(b['product']+'.npy'));vals=[];ns=[]
  for dr in [-1,0,1]:
   for dc in [-1,0,1]:
    aa=A[1:499,1:499];bb=B[1+dr:499+dr,1+dc:499+dc];mask=np.isfinite(aa)&np.isfinite(bb)
    if mask.any():vals.append(float(np.median((aa-bb)[mask])));ns.append(int(mask.sum()))
  if vals:out.append(dict(a=b['product'],b=a['product'],shift_min_delta_K=min(vals),shift_max_delta_K=max(vals),common_grid_cells_min=min(ns),common_grid_cells_max=max(ns),perturbation='relative +/-0.001 degree in each geographic axis; nearest-neighbour display-grid sensitivity only'))
with(O/'thermal_grid_shift_sensitivity.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=out[0]);w.writeheader();w.writerows(out)
for x in out:
 if x['a']=='I54561019PBT'and x['b']=='I54586015PBT':print(x)
