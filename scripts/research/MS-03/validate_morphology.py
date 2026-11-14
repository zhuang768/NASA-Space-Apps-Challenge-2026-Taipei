"""Independent checks for bounded morphology delivery;no discovery certification."""
from pathlib import Path
import csv,gzip,hashlib,io,json,math,re,zipfile
import numpy as np
import shapefile
from shapely import wkt
from shapely.geometry import box
from shapely.ops import unary_union
from PIL import Image
R=Path(__file__).resolve().parents[3];O=R/'outputs/research/MS-03/morphology'
m=json.loads((O/'acquisition_manifest.json').read_text())
assert m['start_sha']=='7b3c865e85ffeb4db81277ef34e9c3f4a318fc9f'
for x in m['files']:
 b=(O/x['path']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
 if 'sha256_uncompressed'in x:assert hashlib.sha256(gzip.decompress(b)).hexdigest()==x['sha256_uncompressed']
for p in O.glob('*.json'):json.loads(p.read_text())
for p in O.glob('*.csv'):
 with p.open(newline='') as f:rows=list(csv.reader(f));assert all(len(r)==len(rows[0]) for r in rows)
for name in ['ode_HIRISE_RDRV11.json','ode_HIRISE_RDR.json']:
 q=json.loads((O/name).read_text())['ODEResults'];assert int(q['Count'])==0 and 'Error' not in q
ctx=json.loads((O/'ode_CTX_EDR.json').read_text())['ODEResults'];assert int(ctx['Count'])==3
roi=box(242,57.5,242.5,58);union=unary_union([wkt.loads(x['Footprint_geometry']) for x in ctx['Products']['Product']]);assert roi.difference(union).area<1e-12
lbl=(O/'PSP_006864_2380_RED.LBL').read_text();east=float(re.search(r'EASTERNMOST_LONGITUDE\s*=\s*([\d.]+)',lbl)[1]);assert east<242
z=zipfile.ZipFile(R/'outputs/research/MS-03/polygons_Act-IWS_source.zip');b='polygons_Act-IWS';r=shapefile.Reader(shp=io.BytesIO(z.read(b+'.shp')),shx=io.BytesIO(z.read(b+'.shx')),dbf=io.BytesIO(z.read(b+'.dbf')));assert r.shapeType==5 and len(r)==185
with (O/'AD1_recomputed_geometry.csv').open() as f:geo=list(csv.DictReader(f))
# Manual shoelace/perimeter for first source polygon;translate to avoid large-coordinate cancellation.
p=np.asarray(r.shape(0).points);p=p-p[0];manual_area=abs(sum(p[i,0]*p[i+1,1]-p[i+1,0]*p[i,1] for i in range(len(p)-1)))/2;manual_perim=sum(math.dist(p[i],p[i+1]) for i in range(len(p)-1))
assert math.isclose(manual_area,float(geo[0]['area_m2']),rel_tol=1e-9);assert math.isclose(manual_perim,float(geo[0]['perimeter_m']),rel_tol=1e-9)
assert len(geo)==185 and len({x['polygon_row_1based'] for x in geo})==185
assert all(0<float(x['circularity_4piA_over_P2'])<=1 and float(x['mrr_aspect_length_width'])>=1 for x in geo)
a=np.frombuffer(gzip.decompress((O/'D01_native_rows.bin.gz').read_bytes()),dtype='u1').reshape(1024,5056)[:,600:1624]
assert np.array_equal(a,np.asarray(Image.open(O/'D01_native_crop_DN.png')))
summary=json.loads((O/'AD1_geometry_summary.json').read_text());assert math.isclose(np.median([float(x['equivalent_circle_diameter_m']) for x in geo]),summary['metrics']['equivalent_circle_diameter_m']['median'])
for file in ['MS03_AD1_coverage_interpretation.png','MS03_AD1_coverage_interpretation.pdf']:assert (O/file).stat().st_size>1000
with (R/'outputs/research/MS-03/candidates.csv').open() as f:ad1=next(x for x in csv.DictReader(f) if x['candidate_id']=='MS-03-E02')
assert ad1['disposition']=='downgrade_general_method_reference_not_specific_MS03_pair'
print('PASS: acquisition hashes;JSON/CSV;185 polygon IDs;first polygon independent shoelace/perimeter;metric bounds;unmodified DN crop;ODE3CTX/0HiRISE responses;catalogue union;outside HiRISE label;AD1 downgrade;figure files.')
