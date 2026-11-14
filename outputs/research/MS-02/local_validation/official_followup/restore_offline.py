"""Restore retained source/download blocks and convenient epoch NPYs without network."""
from pathlib import Path
import zipfile
import numpy as np
P=Path(__file__).parent;S=P/'sources';O=P/'derived'
for archive,destination in [(S/'catalogues_and_themis_headers.zip',S),(O/'themis_source_row_blocks.zip',S)]:
 with zipfile.ZipFile(archive)as z:
  for name in z.namelist():
   if Path(name).name!=name:raise ValueError('unexpected archive member')
   (destination/name).write_bytes(z.read(name))
with np.load(O/'thermal_common_grid.npz')as z:
 for key in z.files:
  if key.startswith('I'):np.save(O/(key+'.npy'),z[key])
print('Retained catalogue/header/source blocks restored; nine epoch grids ready. No network used.')
