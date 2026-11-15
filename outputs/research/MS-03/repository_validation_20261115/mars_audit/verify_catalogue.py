from pathlib import Path
import csv,json,math,argparse
from shapely import wkt
from shapely.geometry import box
from shapely.ops import unary_union,transform
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);args=parser.parse_args();R=args.repo.resolve();O=args.out.resolve();O.mkdir(parents=True,exist_ok=True);d=R/'outputs/research/MS-03/morphology';roi=box(242,57.5,242.5,58)
def laea(lon,lat,z=None):
 lon0=math.radians(242.25);p0=math.radians(57.75);l=math.radians(lon);p=math.radians(lat);k=math.sqrt(2/(1+math.sin(p0)*math.sin(p)+math.cos(p0)*math.cos(p)*math.cos(l-lon0)));return (3389500*k*math.cos(p)*math.sin(l-lon0),3389500*k*(math.cos(p0)*math.sin(p)-math.sin(p0)*math.cos(p)*math.cos(l-lon0)))
proj_roi=transform(laea,roi)
rows=list(csv.DictReader((d/'image_inventory.csv').open())); out=[];polys=[]
for s in rows:
 g=wkt.loads(s['footprint_wkt']);cl=g.intersection(roi);polys.append(cl);v=cl.area/roi.area
 out.append(dict(product_id=s['product_id'],source_sha='07dbe29203504ba0ccde5e379f42ecc16e4b1b4f',source_path='outputs/research/MS-03/morphology/image_inventory.csv',source_field='footprint_wkt',date_UTC=s['utc_start'],nominal_pixel_m=s['nominal_pixel_m'],catalogue_rect_or_corner_intersection_fraction_deg2=v,stored_value=float(s['roi_catalogue_area_fraction']),difference=v-float(s['roi_catalogue_area_fraction']),LAEA_clip_before_project_fraction=transform(laea,cl).area/proj_roi.area,LAEA_project_corner_chords_before_clip_fraction=transform(laea,g).intersection(proj_roi).area/proj_roi.area,actual_valid_pixel_fraction='NA',optical_resolution_m='NA',limits='ODE planetocentric four-corner polygon; planar degree-area fraction only; no full native valid pixel mask; no full-image QA'))
with (O/'catalogue_footprints.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
# Existing retained extracted index rows, no repetition of original index generator search.
p=d/'evidence_followup/index_anomalies/latitude_eligible_rows.csv'; rs=list(csv.DictReader(p.open()));hits=[]
for s in rs:
 if float(s['min_lat'])<=58 and float(s['max_lat'])>=57.5 and float(s['min_lon'])<=242.5 and float(s['max_lon'])>=242:hits.append(s['product_id'])
#615flagged rows: excludes by latitude before longitude normalization.
p2=d/'evidence_followup/HiRISE_invalid_bbox_rows.csv'; invalid=list(csv.DictReader(p2.open()));print('invalid keys',invalid[0].keys())
latkeys=[k for k in invalid[0] if 'lat' in k.lower()]
flagged_lat_hits=[s['PRODUCT_ID'] for s in invalid if float(s['MINIMUM_LATITUDE'])<=58 and float(s['MAXIMUM_LATITUDE'])>=57.5]
q=dict(CTX_nominal_union_degree_area_fraction=unary_union(polys).area/roi.area,HiRISE_retained_latitude_eligible_rows=len(rs),HiRISE_retained_latitude_eligible_bbox_hits=hits,HiRISE_retained_flagged_rows=len(invalid),HiRISE_retained_flagged_latitude_hits=flagged_lat_hits,full_cumulative_index_present=any(R.rglob('RDRCUMINDEX.TAB')),interpretation='Retained index extract/catalogue calculations, not a fresh full cumulative index run or observation absence proof',CTX_geometric_fraction_note='Both independent degree-square and README-specified LAEA calculations reported. LAEA uses R3389500m at57.75N242.25E; nominal geometric support only.')
(O/'catalogue_summary.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
