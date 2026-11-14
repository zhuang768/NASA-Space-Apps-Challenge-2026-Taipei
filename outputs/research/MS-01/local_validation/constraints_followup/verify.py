"""Check derived data against retained source windows and provider labels."""
from pathlib import Path
import argparse,csv,hashlib,json
import numpy as np
p=Path(__file__).resolve().parent
a=argparse.ArgumentParser();a.add_argument('--raw-dir',type=Path,required=True);raw=a.parse_args().raw_dir
scenes=list(csv.DictReader((p/'thermal_scene_qc.csv').open()))
for s in scenes:assert hashlib.sha256((raw/(s['product']+'.IMG')).read_bytes()).hexdigest()==s['source_sha256']
for s in json.loads((p/'source_hashes.json').read_text()):
 if s['filename'] in ['radar_window.bin','sim_window.bin','albedo_rows.bin']:
  assert hashlib.sha256((raw/s['filename']).read_bytes()).hexdigest()==s['sha256']
z=np.load(p/'radar_clutter_roi.npz')
for key,name in [('radar_power','radar_window.bin'),('combined_simulation','sim_window.bin')]:
 expected=np.fromfile(raw/name,'<f4').reshape(1400,5210)[:,1663:1727]
 assert np.array_equal(z[key],expected)
al=list(csv.DictReader((p/'albedo_roi.csv').open()));source=np.fromfile(raw/'albedo_rows.bin','<f4').reshape(4,2880)
for r in al:assert float(r['Lambert_albedo'])==float(source[int(r['row0'])-264,int(r['column0'])])
t=np.load(p/'thermal_common_grid.npz');pairs=list(csv.DictReader((p/'thermal_pair_support.csv').open()));names=t['product'].tolist()
for r in pairs:
 x,y=t['brightness_K'][names.index(r['scene_A'])],t['brightness_K'][names.index(r['scene_B'])];m=np.isfinite(x)&np.isfinite(y)
 assert int(m.sum())==int(r['common_geographic_nodes'])
 if m.any():assert float(np.median(y[m]-x[m]))==float(r['median_B_minus_A_K'])
print('PASS:6 source hashes;3 Range hashes;radar/simulation byte slices;16 albedo values;15 pair summaries. Not physical truth validation.')
