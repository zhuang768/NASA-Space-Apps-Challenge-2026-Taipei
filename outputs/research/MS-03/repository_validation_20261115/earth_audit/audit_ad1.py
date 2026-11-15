"""Offline AD1 geometry remeasurement. No imagery/segmentation/independent annotation claims.
Run: NASA-Space-Apps-Challenge-2026-Taipei/.venv/bin/python audit_ad1.py --repo PATH --out PATH
Only tracked bytes from frozen main are used. Two candidate provenance checks are kept separate.
"""
import argparse,csv,hashlib,io,json,math,pathlib,zipfile,statistics,subprocess,warnings
import shapefile
from shapely.geometry import shape,mapping
from shapely.ops import unary_union,transform
from rasterio.warp import transform as crstransform
p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--out',required=True);a=p.parse_args();R=pathlib.Path(a.repo);O=pathlib.Path(a.out);O.mkdir(exist_ok=True)
sha=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip()
rel='outputs/research/MS-03/polygons_Act-IWS_source.zip';src=R/rel;z=zipfile.ZipFile(src)
r=shapefile.Reader(shp=io.BytesIO(z.read('polygons_Act-IWS.shp')),shx=io.BytesIO(z.read('polygons_Act-IWS.shx')),dbf=io.BytesIO(z.read('polygons_Act-IWS.dbf')))
geoms=[shape(s.__geo_interface__) for s in r.shapes()];records=[x.as_dict() for x in r.records()]
rows=[];features=[];numerical_warnings=[]
def xy(x,y,z=None):
 xx,yy=crstransform('EPSG:32633','EPSG:4326',list(x),list(y));return xx,yy
for i,(g,dbf) in enumerate(zip(geoms,records),1):
 hull=list(g.convex_hull.exterior.coords);spans=[]
 for p1,p2 in zip(hull[:-1],hull[1:]):
  dx=p2[0]-p1[0];dy=p2[1]-p1[1];L=math.hypot(dx,dy);projs=[(-dy*x+dx*y)/L for x,y in hull];spans.append(max(projs)-min(projs))
 with warnings.catch_warnings(record=True) as captured:
  warnings.simplefilter('always',RuntimeWarning)
  rect=g.minimum_rotated_rectangle
 for item in captured:numerical_warnings.append({'polygon_row_1based':i,'category':item.category.__name__,'message':str(item.message),'cause':'unknown;not_inferred_from_warning_alone'})
 pts=list(rect.exterior.coords);sides=[math.dist(x,y) for x,y in zip(pts[:-1],pts[1:])]
 assert all(math.isfinite(v) and v>0 for v in sides),f'Nonfinite/degenerate rectangle at source row{i}'
 row={'polygon_row_1based':i,'geometry_type':g.geom_type,'is_valid':g.is_valid,'is_closed':bool(g.exterior.is_closed),'ring_count':1+len(g.interiors),'area_m2':g.area,'perimeter_m':g.length,'equivalent_circle_diameter_m':math.sqrt(4*g.area/math.pi),'minimum_Feret_width_m':min(spans),'mrr_width_m':min(sides),'mrr_length_m':max(sides),'circularity_4piA_over_P2':4*math.pi*g.area/g.length**2,'published_dbf_area_m2':dbf.get('area'),'published_dbf_width_m':dbf.get('width'),'source_commit':sha,'source_path':rel}
 assert all(math.isfinite(row[k]) and row[k]>0 for k in ['area_m2','perimeter_m','equivalent_circle_diameter_m','minimum_Feret_width_m','mrr_width_m','mrr_length_m','circularity_4piA_over_P2']),f'Invalid metric at source row{i}'
 rows.append(row);features.append({'type':'Feature','id':i,'properties':row,'geometry':mapping(transform(xy,g))})
def write(name,rr):
 with (O/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rr[0]);w.writeheader();w.writerows(rr)
write('AD1_independent_geometry.csv',rows)
old=list(csv.DictReader((R/'outputs/research/MS-03/morphology/AD1_recomputed_geometry.csv').open()))
checks=[]
for field in ['area_m2','perimeter_m','equivalent_circle_diameter_m','mrr_width_m','mrr_length_m','circularity_4piA_over_P2']:
 diffs=[abs(float(n[field])-float(o[field])) for n,o in zip(rows,old)]
 checks.append({'field':field,'n':len(diffs),'max_abs_difference':max(diffs),'median_recomputed':statistics.median(x[field] for x in rows),'unit':'m2' if field=='area_m2' else ('1' if 'circularity' in field else 'm'),'source_commit':sha,'source_path':rel,'comparison_path':'outputs/research/MS-03/morphology/AD1_recomputed_geometry.csv'})
write('AD1_readback_comparison.csv',checks)
union=unary_union(geoms);bd=union.bounds
summary={'main_sha':sha,'source_path':rel,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_crs':'WGS84 UTM33N metres EPSG:32633 as .prj','feature_count':len(rows),'valid_count':sum(x['is_valid'] for x in rows),'closed_count':sum(x['is_closed'] for x in rows),'singlepart_count':sum(x['geometry_type']=='Polygon' for x in rows),'sum_source_polygon_area_m2':sum(g.area for g in geoms),'union_area_m2':union.area,'bounding_envelope_m':bd,'bounding_envelope_area_m2':(bd[2]-bd[0])*(bd[3]-bd[1]),'median_area_m2':statistics.median(x['area_m2'] for x in rows),'median_equivalent_diameter_m':statistics.median(x['equivalent_circle_diameter_m'] for x in rows),'median_minimum_Feret_m':statistics.median(x['minimum_Feret_width_m'] for x in rows),'raster_available':False,'two_independent_flights_available':False,'independent_ground_truth_annotation':False,'source_mapping_status':'Published closed vectors; full raster registration, completeness, positional error, inter-annotator or repeat-flight validation unavailable','xml_conflicting_bounds':'Source XML contains stale 16.365895 to16.411791E box and synchronized15.913665 to15.933937E box. Shape coordinates and EPSG32633 transformation select latter; stale XML not used.'}
summary['audited_branch_heads']=len(subprocess.check_output(['git','-C',str(R),'for-each-ref','--format=%(refname)','refs/remotes/audit'],text=True).splitlines())
summary['closed_single_ring_count']=sum(x['is_closed'] and x['ring_count']==1 for x in rows)
summary['feature_identity']='Source shapefile record order (1-based), source ZIP SHA256 and commit; no persistent FID in source DBF'
(O/'AD1_summary.json').write_text(json.dumps(summary,indent=2))
(O/'AD1_Earth_reference_contours.geojson').write_text(json.dumps({'type':'FeatureCollection','name':'AD1_published_Earth_contours_reencoded_no_new_digitization','source_commit':sha,'source_path':rel,'source_crs':'EPSG32633; transformed to EPSG4326 by PROJ via rasterio','warning':'Published reference vectors; no independent delineation validation; no Mars contours','features':features}))
# Size-only upper-bound test. Minimum Feret is not a narrow-neck proof, and no curve detectability is inferred.
scale=[]
for name,spacing in [('CTX_nominal',6.0),('MOC_ground_at_57_5N',3.000339463*(1+math.sin(math.radians(57.5)))/2),('MOC_ground_at_58N',3.000339463*(1+math.sin(math.radians(58)))/2)]:
 flags=[x['minimum_Feret_width_m']>=8*spacing for x in rows]
 scale.append({'sampling_case':name,'ground_sampling_m':spacing,'required_8_sample_width_m':8*spacing,'n_published_closed_earth_vectors':len(rows),'n_failing_minimum_Feret_upper_bound':sum(not f for f in flags),'n_not_excluded_by_size_only':sum(flags),'n_validated_for_Mars_comparison':'NA','median_samples_across_minimum_Feret':statistics.median(x['minimum_Feret_width_m']/spacing for x in rows),'origin_sensitivity':'not_applicable_to_analytic_width_bound','warning':'Minimum Feret is upper bound on narrowest local width; passing is not acceptance. No image raster, contrast, optical PSF, closed-edge identification or independent outlines tested. No recognition rate.','source_commit':sha,'source_path':rel})
write('AD1_sampling_upper_bound.csv',scale)
print(json.dumps(summary,indent=2));print(json.dumps(scale,indent=2))

(O/'geometry_warnings.json').write_text(json.dumps({'warnings':numerical_warnings,'nonfinite_metric_count':0,'all_output_metrics_finite_and_positive':True,'warning_root_cause':'unknown','scope':'Numeric QA only; independent mapping accuracy not established'},indent=2)+'\n')
