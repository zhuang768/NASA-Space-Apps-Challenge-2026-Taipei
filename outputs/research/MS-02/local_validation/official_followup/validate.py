from pathlib import Path
import hashlib,json,csv,zipfile,io
import numpy as np
P=Path(__file__).parent;O=P/'derived';checks=[]
def check(name,cond):
 checks.append(dict(check=name,passed=bool(cond)))
 if not cond:raise AssertionError(name)
rows=list(csv.DictReader(open(O/'thermal_epoch_qc.csv')));check('nine THEMIS epochs with distinct product IDs',len(rows)==len({x['product']for x in rows})==9)
with zipfile.ZipFile(O/'themis_source_row_blocks.zip')as z:
 for r in rows:check('retained source bytes '+r['product'],hashlib.sha256(z.read(r['product']+'.roi_rows.bin')).hexdigest()==r['sha256'])
t=np.load(O/'thermal_common_grid.npz');check('fixed common grid coordinate shape',t['latitude'].shape==(500,)and t['longitude'].shape==(500,));check('fixed ROI unchanged',np.isclose(t['latitude'][0],52.5005)and np.isclose(t['longitude'][-1],168.4995))
for r in rows:check('numeric coverage '+r['product'],np.isfinite(t[r['product']]).sum()==int(r['valid_grid_cells']))
x=np.load(O/'mrdr4_roi.npz');check('CRISM cube shape',x['albedo'].shape==(72,163,93));check('72 explicit wavelengths',len(x['wavelength_nm'])==72);check('missingness retained',np.isnan(x['albedo']).any())
a=list(csv.DictReader(open(P/'sources/gtnp1505/alt_dataset_1505_alt_grid-transect.csv')));check('UNISCALM 968 source records',len(a)==968);check('UNISCALM 121-node grid on 8 dates',len(set(x['date']for x in a))==8 and all(sum(y['date']==d for y in a)==121 for d in set(x['date']for x in a)))
a=list(csv.DictReader(open(O/'adventdalen_2023_core_samples.csv')));check('269 source core intervals',len(a)==269);check('source VIC outlier retained and flagged',sum(x['flag_VIC_outside_0_100']=='True'for x in a)==1)
a=list(csv.DictReader(open(O/'crism_trdr_inventory.csv')));check('177 unique explicit TRDR IDs',len(a)==len(set(x['product_id']for x in a))==177)
n=0
for id in ['00464501','01983502','02004601']:
 r=list(csv.DictReader(open(O/f's_{id}_surface_picks.csv')));n+=len(r);check('radar picks within fixed ROI '+id,all(52.5<=float(x['latitude'])<=53 and 168<=float(x['longitude'])<=168.5 for x in r))
check('194 radar postings',n==194)
for f in json.load(open(P/'manifest.json'))['files']:
 p=P.parents[4]/f['path']
 check('file hash '+f['path'],p.exists()and hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'])
(P/'validation.json').write_text(json.dumps(dict(passed=all(x['passed']for x in checks),checks=checks),indent=2));print(len(checks),'checks passed')
