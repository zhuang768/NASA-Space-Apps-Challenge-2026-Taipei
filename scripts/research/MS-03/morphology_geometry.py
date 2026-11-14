"""Recompute AD1 planar metrics and Mars catalogue coverage; no image segmentation.
Dependencies: numpy, shapely>=2, pyproj, pyshp, matplotlib, pillow.
Only source polygons_Act-IWS are read; similarly named polylines are excluded.
"""
from pathlib import Path
import csv,hashlib,io,json,math,zipfile
import numpy as np
import shapefile
from shapely.geometry import shape,box,mapping
from shapely import wkt
from shapely.ops import transform,unary_union
from pyproj import CRS,Transformer
R=Path(__file__).resolve().parents[3];O=R/'outputs/research/MS-03/morphology'
def write(name,rows):
 with (O/name).open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
zpath=R/'outputs/research/MS-03/polygons_Act-IWS_source.zip'
assert hashlib.sha256(zpath.read_bytes()).hexdigest()=='c75e7568c9fbfc67898f64e9c18681e5dc7e24a1ec272ceafa12c51377b8054e'
z=zipfile.ZipFile(zpath);base='polygons_Act-IWS';crs=CRS.from_wkt(z.read(base+'.prj').decode());assert crs.to_epsg()==32633
r=shapefile.Reader(shp=io.BytesIO(z.read(base+'.shp')),shx=io.BytesIO(z.read(base+'.shx')),dbf=io.BytesIO(z.read(base+'.dbf')))
geoms=[shape(s.__geo_interface__) for s in r.shapes()];assert len(geoms)==185 and all(g.is_valid and g.area>0 for g in geoms)
rows=[]
for i,g in enumerate(geoms):
 rect=g.minimum_rotated_rectangle;c=list(rect.exterior.coords);sides=[math.dist(c[j],c[j+1]) for j in range(4)];length=max(sides);width=min(sides)
 rows.append(dict(polygon_row_1based=i+1,area_m2=g.area,perimeter_m=g.length,equivalent_circle_diameter_m=math.sqrt(4*g.area/math.pi),mrr_length_m=length,mrr_width_m=width,mrr_aspect_length_width=length/width,circularity_4piA_over_P2=4*math.pi*g.area/g.length**2))
write('AD1_recomputed_geometry.csv',rows)
metrics={k:dict(n=len(rows),min=float(min(x[k] for x in rows)),p25=float(np.percentile([x[k] for x in rows],25)),median=float(np.median([x[k] for x in rows])),p75=float(np.percentile([x[k] for x in rows],75)),max=float(max(x[k] for x in rows))) for k in list(rows[0])[1:]}
summary=dict(source_doi='10.1594/PANGAEA.921087',source_sha256=hashlib.sha256(zpath.read_bytes()).hexdigest(),source_crs='EPSG:32633;WGS84 UTM33N metres',n=185,invalid=0,method='Planar vector area/perimeter;equivalent diameter sqrt(4A/pi);minimum rotated rectangle edge lengths;4piA/P². No raster boundary re-digitization;not identical to paper largest/smallest diameters.',edge_status='All185 published polygons retained;original edge/truncation selection not re-audited;not a random regional sample',metrics=metrics)
(O/'AD1_geometry_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
roi=box(242,57.5,242.5,58)
# Mars spherical local LAEA for area ratios;planetocentric inputs;mean radius3389500m.
proj=Transformer.from_crs('+proj=longlat +R=3389500 +no_defs','+proj=laea +lat_0=57.75 +lon_0=242.25 +R=3389500 +units=m +no_defs',always_xy=True).transform
area=transform(proj,roi).area;products=json.loads((O/'ode_CTX_EDR.json').read_text())['ODEResults']['Products']['Product'];features=[];inventory=[];clips=[]
for p in products:
 g=wkt.loads(p['Footprint_geometry']);clip=g.intersection(roi);clips.append(clip)
 # Clip in lon/lat before projection;catalogue straight corner segments are an approximation.
 coverage=transform(proj,clip).area/area
 inventory.append(dict(product_id=p['pdsid'],instrument='CTX',utc_start=p['UTC_start_time'],utc_stop=p['UTC_stop_time'],nominal_pixel_m=float(p['Map_scale']),incidence_deg=float(p['Incidence_angle']),emission_deg=float(p['Emission_angle']),catalogue_quality='OK per archived index;not independent image-quality validation',roi_catalogue_area_fraction=coverage,footprint_wkt=p['Footprint_geometry'],footprint_source=p['Footprint_souce'],acquired_image_quality=({'G01':'505x5222 JPEG browse;approx10x downsample;not sufficient for AD1 boundaries','D01':'505x5222 browse plus native8bit EDR slice;tonal gradient and vertical striping;uncalibrated;limited patch only','V17':'5056x52224 JPEG browse;full dimensions but severe compression/block artifacts in inspected crop;not native radiometric quality'}[p['pdsid'].split('_')[0]]),product_url=p['ProductURL'],data_url=p['LabelURL']))
 features.append(dict(type='Feature',geometry=mapping(g),properties={'product_id':p['pdsid'],'roi_fraction':coverage}))
write('image_inventory.csv',inventory)
(O/'CTX_footprints_mars.json').write_text(json.dumps({'type':'FeatureCollection','name':'Mars_planetocentric_east_positive_NOT_Earth_WGS84','coordinate_note':'Mars planetocentric degrees;east0-360;do not import as Earth distances','features':features},indent=2)+'\n')
cover=dict(roi=[242,57.5,242.5,58],roi_area_km2_approx=area/1e6,mars_sphere_radius_m=3389500,union_catalogue_coverage_fraction=(1.0 if roi.difference(unary_union(clips)).area<1e-12 else transform(proj,unary_union(clips)).area/area),method='Intersect ODE corner footprints with ROI in lon/lat;area via local spherical Mars LAEA. Approximate catalogue support,not valid-pixel coverage or precision geolocation.',hirise_RDRV11_count=int(json.loads((O/'ode_HIRISE_RDRV11.json').read_text())['ODEResults']['Count']),hirise_RDR_count=int(json.loads((O/'ode_HIRISE_RDR.json').read_text())['ODEResults']['Count']),usgs_crosscheck='HTTP403;not an independent negative confirmation')
(O/'coverage_summary.json').write_text(json.dumps(cover,indent=2)+'\n')
print(json.dumps({'geometry':metrics,'coverage':cover},indent=2))
