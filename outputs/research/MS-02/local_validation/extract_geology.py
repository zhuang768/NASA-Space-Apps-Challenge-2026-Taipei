"""Select all original SIM3292 polygons intersecting the unchanged ROI.
Usage: python extract_geology.py [path/to/sim3292_database.zip]
Without ZIP, uses locally extracted sources/usgs_geology shapefile.
"""
from pathlib import Path
import sys,json,zipfile,hashlib
import shapefile
from shapely.geometry import shape,box,mapping
P=Path(__file__).resolve().parent;S=P/'sources/usgs_geology'
if len(sys.argv)>1:
 zpath=Path(sys.argv[1]);z=zipfile.ZipFile(zpath);S.mkdir(parents=True,exist_ok=True)
 for n in z.namelist():
  if Path(n).name.startswith('SIM3292_Global_Geology.') and not n.endswith('/'):(S/Path(n).name).write_bytes(z.read(n))
 (P/'geology_archive_provenance.json').write_text(json.dumps(dict(url='https://pubs.usgs.gov/sim/3292/downloads/sim3292_database.zip',bytes=zpath.stat().st_size,sha256=hashlib.sha256(zpath.read_bytes()).hexdigest(),method='Extract original shapefile members; no reprojection before intersection'),indent=2)+'\n')
r=shapefile.Reader(str(S/'SIM3292_Global_Geology.shp'));roi=box(168,52.5,168.5,53);features=[]
for ix,sr in enumerate(r.iterShapeRecords()):
 g=shape(sr.shape.__geo_interface__)
 if g.intersects(roi):features.append(dict(type='Feature',geometry=mapping(g),properties=dict(source_record_zero_based=ix,**sr.record.as_dict())))
assert len(features)==1 and features[0]['properties']['Unit']=='mAl'
(P/'geology_roi_original.geojson').write_text(json.dumps(dict(type='FeatureCollection',features=features))+'\n')
print('Selected',len(features),'original polygons')
