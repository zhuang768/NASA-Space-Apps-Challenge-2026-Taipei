"""Published AD1 geometric sampling-phase sensitivity. Not image detection.
See README.md for tested dependencies and reproducibility checks.
The fixed source shapefile is Ulrich et al. (2020), DOI 10.1594/PANGAEA.921087.
"""
import argparse,csv,hashlib,io,json,math,zipfile
from pathlib import Path
from datetime import datetime,timezone
import numpy as np, shapefile
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from rasterio.features import rasterize, shapes
from rasterio.transform import from_origin
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
SOURCE_SHA256 = 'c75e7568c9fbfc67898f64e9c18681e5dc7e24a1ec272ceafa12c51377b8054e'
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--repo', type=Path, default=Path.cwd(), help='Repository root (default: current directory)')
ap.add_argument('--source', type=Path, help='Override the tracked original AD1 shapefile ZIP')
ap.add_argument('--output-dir', required=True, type=Path, help='New output directory (must not exist)')
a=ap.parse_args()
started=datetime.now(timezone.utc).isoformat()
source=a.source if a.source is not None else a.repo/'outputs/research/MS-03/polygons_Act-IWS_source.zip'
if not source.is_file():
    ap.error(f'AD1 shapefile ZIP not found: {source}')
b=source.read_bytes()
if hashlib.sha256(b).hexdigest() != SOURCE_SHA256:
    ap.error('Source SHA-256 does not match the expected AD1 shapefile ZIP')
O=a.output_dir
if O.exists():
    ap.error('--output-dir already exists; choose a new directory')
O.mkdir(parents=True)
z=zipfile.ZipFile(io.BytesIO(b))
r=shapefile.Reader(shp=io.BytesIO(z.read('polygons_Act-IWS.shp')),dbf=io.BytesIO(z.read('polygons_Act-IWS.dbf')),shx=io.BytesIO(z.read('polygons_Act-IWS.shx')))
gs=[shape(x.__geo_interface__) for x in r.iterShapes()]
assert len(gs)==185 and all(g.is_valid for g in gs)
rows=[]
for res in [.5,1.,3.,6.11]:
 for i,g in enumerate(gs):
  xmin,ymin,xmax,ymax=g.bounds
  for px in [0.,.25,.5,.75]:
   for py in [0.,.25,.5,.75]:
    left=(math.floor(xmin/res)-1+px)*res;top=(math.ceil(ymax/res)+1+py)*res
    width=math.ceil((xmax-left)/res)+1;height=math.ceil((top-ymin)/res)+1
    t=from_origin(left,top,res,res)
    ar=rasterize([(g,1)],out_shape=(height,width),transform=t,fill=0,dtype='uint8',all_touched=False)
    vs=[shape(q) for q,v in shapes(ar,mask=ar>0,transform=t) if v==1]
    rr=unary_union(vs)
    intersection=g.intersection(rr).area;union=g.union(rr).area
    rows.append(dict(source_id=f'AD1-{i+1:03d}',grid_spacing_m=res,phase_x_pixel=px,phase_y_pixel=py,grid_left_UTM33N_m=left,grid_top_UTM33N_m=top,source_area_m2=g.area,raster_area_m2=rr.area,intersection_m2=intersection,union_m2=union,IoU=intersection/union,relative_area_error=rr.area/g.area-1,occupied_cells=int(ar.sum()),disconnected_parts=len(vs),measurement_type='computed_geometry_only'))
 with (O/'phase_results.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print('finished grid',res,flush=True)
summary=[];per=[]
for res in [.5,1.,3.,6.11]:
 sub=[x for x in rows if x['grid_spacing_m']==res]
 robust=[];span=[]
 for i in range(185):
  ss=[x for x in sub if x['source_id']==f'AD1-{i+1:03d}'];mi=min(x['IoU'] for x in ss);ma=max(x['IoU'] for x in ss);s=max(x['relative_area_error'] for x in ss)-min(x['relative_area_error'] for x in ss)
  robust.append(mi>=.8);span.append(s)
  per.append(dict(source_id=f'AD1-{i+1:03d}',grid_spacing_m=res,min_IoU_16phases=mi,max_IoU_16phases=ma,all16_IoU_ge_0p8=mi>=.8,area_error_phase_span=s))
 summary.append(dict(grid_spacing_m=res,polygons=185,phases=16,rows=len(sub),median_IoU_allphases=float(np.median([x['IoU'] for x in sub])),min_IoU_allphases=min(x['IoU'] for x in sub),max_IoU_allphases=max(x['IoU'] for x in sub),min_relative_area_error=min(x['relative_area_error'] for x in sub),max_relative_area_error=max(x['relative_area_error'] for x in sub),median_per_polygon_phase_area_error_span=float(np.median(span)),max_per_polygon_phase_area_error_span=max(span),all16_IoU_ge_0p8_count=sum(robust),n_polygons_IoU_crosses_0p8_by_phase=sum(x['min_IoU_16phases']<.8<=x['max_IoU_16phases'] for x in per if x['grid_spacing_m']==res)))
for name,rs in [('per_polygon_phase_summary.csv',per),('phase_summary.csv',summary)]:
 with (O/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
fig,ax=plt.subplots(figsize=(8,4.5));ax.boxplot([[r['IoU'] for r in rows if r['grid_spacing_m']==s] for s in [.5,1,3,6.11]],tick_labels=['0.5','1','3','6.11'],showfliers=False);ax.axhline(.8,color='darkred',linestyle='--',label='Exploratory geometry threshold0.80');ax.set(xlabel='Grid spacing (m)',ylabel='Geometric IoU',title='AD1: same 185 published polygons,16 grid phases each');ax.legend(fontsize=8);fig.tight_layout();fig.savefig(O/'phase_IoU.png',dpi=180);plt.close(fig)
receipt=dict(started_utc=started,completed_utc=datetime.now(timezone.utc).isoformat(),input_sha256=hashlib.sha256(b).hexdigest(),input_bytes=len(b),input_doi='10.1594/PANGAEA.921087',site='Adventdalen AD1, not Cape Blossom',rows=len(rows),original_polygons=185,summary=summary,limits='IoU measures digital geometry preservation, not crack visibility, not manual delineation accuracy; not Mars-Earth pairing.16 phases are deterministic, not independent data.')
(O/'execution.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
