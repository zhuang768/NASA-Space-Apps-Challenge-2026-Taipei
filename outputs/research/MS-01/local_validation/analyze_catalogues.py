"""Audit fixed-ROI ODE products without treating footprints as valid ice pixels.

Inputs: original JSON responses (optionally .gz) in --inputs.
Results write only this local_validation folder. No image reprojection/inversion.
"""
from pathlib import Path
import argparse,csv,gzip,hashlib,json,re,math
from shapely import wkt
from shapely.geometry import box,mapping
from shapely.ops import unary_union

HERE=Path(__file__).resolve().parent
ROI=box(72.5,56.5,73,57)
MARS_RADIUS=3396000.0

def ring_area(coords):
    # Integrate -sin(latitude)d(longitude) along straight lon/lat edges.
    result=0.0
    for (lon1,lat1),(lon2,lat2) in zip(coords,coords[1:]):
        x1,x2,y1,y2=map(math.radians,[lon1,lon2,lat1,lat2])
        mean_sin=math.sin(y1) if abs(y2-y1)<1e-12 else (math.cos(y1)-math.cos(y2))/(y2-y1)
        result-=(x2-x1)*mean_sin
    return abs(result)*MARS_RADIUS**2/1e6

def area_km2(geometry):
    if geometry.is_empty:return 0.0
    if geometry.geom_type not in ['Polygon','MultiPolygon','GeometryCollection']:return 0.0
    if hasattr(geometry,'geoms'):return sum(area_km2(g) for g in geometry.geoms)
    return ring_area(list(geometry.exterior.coords))-sum(ring_area(list(r.coords)) for r in geometry.interiors)

def line_km(g):
    if g is None or g.is_empty:return 0.0
    if hasattr(g,'geoms'):return sum(line_km(x) for x in g.geoms)
    if g.geom_type!='LineString':return 0.0
    total=0.
    for a,b in zip(list(g.coords),list(g.coords)[1:]):
        l1,p1,l2,p2=map(math.radians,[*a,*b]);h=math.sin((p2-p1)/2)**2+math.cos(p1)*math.cos(p2)*math.sin((l2-l1)/2)**2
        total+=2*MARS_RADIUS*math.asin(math.sqrt(min(1,h)))/1000
    return total

def write_csv(path,rows):
    if not rows:return
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,list(dict.fromkeys(k for r in rows for k in r)),lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,required=True);a=p.parse_args()
    products=[];summary=[];features=[]
    files=sorted(a.inputs.glob('ode_*.json'))+sorted(a.inputs.glob('ode_*.json.gz'))
    for path in files:
        raw=gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()
        doc=json.loads(raw);d=doc['ODEResults'];q=d.get('QuerySummary',{})
        # Missing/changed query support must not silently become zero coverage.
        dataset=path.name.replace('ode_','').replace('.json.gz','').replace('.json','')
        if d['Status']!='Success':
            summary.append(dict(dataset=dataset,query_status=d['Status'],query_error=d.get('Error','unknown; see raw response'),query_count=None,
                records_parsed=None,source_file=path.name,source_sha256=hashlib.sha256(raw).hexdigest(),interpretation='Query error; coverage and observation count unknown, not zero.'))
            continue
        for name,value in [('minlat',56.5),('maxlat',57),('westernlon',72.5),('easternlon',73)]:assert float(q[name])==value,(path,name)
        container=d.get('Products',{})
        if not isinstance(container,dict):
            assert int(d['Count'])==0 and container in ['',None,'No Products Found'],(path,'unexpected products container')
            ps=[]
        else:ps=container.get('Product',[])
        ps=[ps] if isinstance(ps,dict) else ps
        assert len(ps)==int(d['Count']),(path,'pagination/incomplete response')
        clipped=[];obs=set();IF_obs=set();IF_L=[];IF_S=[];invalid=0;intersecting=0;line_intersections=0
        for r in ps:
            product=r['pdsid']
            group=product.split('_')[0] if dataset.startswith('CRISM') else product[:9] if dataset.startswith('THEMIS') else product
            if dataset.startswith('SHARAD'):
                group=str(int(re.search(r'^[rRsS]_0*(\d+)',product).group(1)))
            obs.add(group)
            is_IF=bool(re.search(r'_if\d+[ls]_trr3$',product))
            if is_IF:IF_obs.add(product.split('_')[0])
            if re.search(r'_if\d+l_trr3$',product):IF_L.append(product)
            if re.search(r'_if\d+s_trr3$',product):IF_S.append(product)
            geom_text=r.get('Footprint_geometry','');g=None;inter=None;status='missing_geometry'
            try:
                g=wkt.loads(geom_text)
                if not g.is_valid:status='invalid_geometry';invalid+=1
                else:
                    inter=g.intersection(ROI);status='positive_area_intersection' if inter.area>0 else 'no_positive_area_intersection'
                    if g.geom_type in ['LineString','MultiLineString']:
                        status='positive_line_intersection' if line_km(inter)>0 else 'no_line_intersection'
                        if line_km(inter)>0:line_intersections+=1
                    if inter.area>0:clipped.append(inter);intersecting+=1
            except Exception:status='unreadable_geometry';invalid+=1
            center_inside=None
            try:center_inside=72.5<=float(r['Center_longitude'])<=73 and 56.5<=float(r['Center_latitude'])<=57
            except (KeyError,ValueError):pass
            row=dict(dataset=dataset,product_id=product,observation_group=group,
                     observation_start_utc=r.get('UTC_start_time','unknown'),observation_stop_utc=r.get('UTC_stop_time','unknown'),
                     solar_longitude_deg=r.get('Solar_longitude','unknown'),local_solar_time_hours=r.get('Solar_time','unknown'),
                     incidence_deg=r.get('Incidence_angle','unknown'),map_scale_m_per_pixel=r.get('Map_scale','unknown'),
                     centre_latitude=r.get('Center_latitude','unknown'),centre_longitude=r.get('Center_longitude','unknown'),centre_inside_roi=center_inside,
                     geometry_type=g.geom_type if g is not None else 'unknown',polygon_status=status,nominal_intersection_km2=area_km2(inter) if inter is not None and inter.area>0 else None,
                     nominal_line_intersection_km=line_km(inter) if g is not None and g.geom_type in ['LineString','MultiLineString'] else None,
                     footprint_source=r.get('Footprint_souce','unknown'),footprint_wkt=geom_text,
                     product_url=r.get('ProductURL','unknown'),label_url=r.get('LabelURL','unknown'),
                     radiance_factor_cube=is_IF,source_file=path.name,source_sha256=hashlib.sha256(raw).hexdigest(),
                     support_limit='Nominal catalogue geometry only;not valid-pixel QA,ice detection,independent observation count or complete archive guarantee')
            products.append(row)
            if inter is not None and inter.area>0 and dataset=='CTX_EDR':features.append(dict(type='Feature',properties={k:v for k,v in row.items() if k!='footprint_wkt'},geometry=mapping(inter)))
        union=unary_union(clipped) if clipped else None
        fraction=area_km2(union)/area_km2(ROI) if union is not None else 0.0
        assert -1e-9<=fraction<=1+1e-9,(dataset,'non-numerical coverage excess',fraction)
        fraction=min(1.0,max(0.0,fraction))
        summary.append(dict(dataset=dataset,query_status='Success',query_error='',query_count=int(d['Count']),records_parsed=len(ps),positive_area_intersections=intersecting,positive_line_intersections=line_intersections,invalid_or_unreadable_geometry=invalid,
                            grouped_observations=len(obs),IF_cubes=len(IF_L)+len(IF_S),IF_observation_groups=len(IF_obs),IF_L_cubes=len(IF_L),IF_S_cubes=len(IF_S),
                            nominal_union_area_km2=area_km2(union) if union is not None else 0,
                            nominal_roi_area_km2=area_km2(ROI),nominal_roi_coverage_fraction=fraction,
                            query_url='https://oderest.rsl.wustl.edu/live2/?'+'&'.join(k+'='+str(q[k]) for k in sorted(q) if k not in ['Date','Query_Elapsed_Time']),
                            provider_query_date=q.get('Date','unknown'),source_file=path.name,source_sha256=hashlib.sha256(raw).hexdigest(),
                            interpretation='0 means this query returned0,not all observations absent;nonzero footprint coverage is not usable pixels or ice evidence'))
    assert files,'No input catalogues'
    write_csv(HERE/'product_inventory.csv',products)
    write_csv(HERE/'catalogue_summary.csv',summary)
    (HERE/'ctx_nominal_intersections.geojson').write_text(json.dumps(dict(type='FeatureCollection',roi=mapping(ROI),coordinate_definition='Marsplanetocentric east-positive;nominal catalogue polygon clipping',features=features),ensure_ascii=False,indent=2)+'\n')
    global_groups={instrument:len({r['observation_group'] for r in products if r['dataset'].startswith(instrument)}) for instrument in ['CTX','CRISM','THEMIS','SHARAD']}
    result=dict(roi=[72.5,56.5,73,57],Mars_sphere_radius_m=MARS_RADIUS,method='WKT validity then planar lonlat polygon clipping;spherical area integral along straight lonlat edges;no geometry repair,great-circle reprojection or calibrated pixel geolocation',summary=summary,grouped_observations_across_queried_product_types=global_groups,
                limits=['Catalogue count can include wavelengths/radiance/housekeeping versions of one observation','IF observations grouped by leading CRISM mode+observationID;not all archive products checked','Catalogue footprint union is geometric support,not image usability or detection completeness','No spectrum,temperature,ice depth or abundance derived by this script'])
    (HERE/'catalogue_analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([{k:r.get(k) for k in ['dataset','query_status','query_count','positive_area_intersections','positive_line_intersections','grouped_observations','IF_L_cubes','IF_S_cubes','nominal_roi_coverage_fraction']} for r in summary],indent=2))
if __name__=='__main__':main()
