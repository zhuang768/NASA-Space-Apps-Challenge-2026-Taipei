"""Recompute fixed-ROI spatial checks and published thermal-grid extraction.
Python: numpy, shapely, pyproj, pyshp, matplotlib. No geologic inference from colour.
"""
import csv,json,re,hashlib
from pathlib import Path
import numpy as np
from shapely.geometry import box,shape,mapping,Point
from shapely import wkt
from shapely.ops import transform,unary_union
from pyproj import Transformer,Geod
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent; S=P/'sources'; ROI=box(168,52.5,168.5,53)
R=3396190.0
PROJECT=Transformer.from_crs(f'+proj=longlat +R={R}',f'+proj=laea +lat_0=52.75 +lon_0=168.25 +R={R}',always_xy=True).transform
AREA=transform(PROJECT,ROI).area
def dump(name,x): (P/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def table(name,rows):
    if not rows:return
    with (P/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def products(name):
    d=json.loads((S/'catalog'/f'{name}.json').read_text())['ODEResults']
    if d['Status'].lower()!='success':return None
    v=d.get('Products');p=v.get('Product',[]) if isinstance(v,dict) else []
    if isinstance(p,dict):p=[p]
    assert int(d.get('Count',len(p)))==len(p),'Pagination required'
    return p
def main():
    lat=np.loadtxt(S/'piqueux/Lat.ascii');lon=np.loadtxt(S/'piqueux/Lon.ascii')
    d=np.loadtxt(S/'piqueux/d_m.ascii');ti=np.loadtxt(S/'piqueux/TI_SI.ascii')
    assert d.shape==ti.shape==(len(lat),len(lon))==(360,720)
    assert np.allclose(np.diff(lon),0.5) and np.allclose(np.diff(lat),-0.5)
    x=np.flatnonzero((lon>=168)&(lon<168.5));y=np.flatnonzero((lat>=52.5)&(lat<53))
    assert x.tolist()==[336] and y.tolist()==[74]
    assert d[74,336]!=-32768 and ti[74,336]!=-32768
    thermal=dict(source_doi='10.22002/D1.1316',array_shape=list(d.shape),row_zero_based=74,column_zero_based=336,
        latitude=float(lat[74]),longitude=float(lon[336]),depth_m=float(d[74,336]),dry_regolith_TI=float(ti[74,336]),
        pixel_bounds=[168,52.5,168.5,53],grid_spacing_deg=0.5,area_km2=AREA/1e6,
        evidence_type='published model estimate; not an in-situ depth or ice fraction',
        missing_value=-32768,uncertainty='Paper says ~20% best-case discretization floor; no local residual or confidence interval in archive; no ±20% local confidence claim',
        resolution_discrepancy='Downloaded archive is 2 ppd; paper text says observations binned at 3 ppd. Export spacing verified; cause of difference undocumented.')
    dump('thermal_pixel.json',thermal)
    table('thermal_neighborhood.csv',[dict(row_zero_based=i,col_zero_based=j,latitude=lat[i],longitude=lon[j],d_m=d[i,j] if d[i,j]!=-32768 else '',TI_SI=ti[i,j] if ti[i,j]!=-32768 else '') for i in range(72,77) for j in range(334,339)])
    ws=re.findall(r'MULTIPOLYGON \(.*',(S/'arcadia348.html').read_text())
    old=wkt.loads(ws[0]);new=wkt.loads(ws[2]);assert new.is_valid
    geo=json.loads((P/'geology_roi_original.geojson').read_text())['features']; assert len(geo)==1
    g=shape(geo[0]['geometry']);assert g.is_valid and g.covers(ROI)
    geography=dict(coordinate_system='planetocentric, east positive; Mars sphere R=3396190 m',
        quadrangle='MC-7 Cebrenia; I-1140 map states 30-65N,180-240W (=120-180E)',
        unit=geo[0]['properties'],unit_roi_area_fraction=transform(PROJECT,g.intersection(ROI)).area/AREA,
        arcadia_MDIM20_bbox_intersects=old.intersects(ROI),arcadia_MDIM21_polygon_intersects=new.intersects(ROI),
        arcadia_boundary_approximate=True,arcadia_MDIM21_min_projected_gap_km=transform(PROJECT,new).distance(transform(PROJECT,ROI))/1000,
        limitation='Gazetteer outlines approximate; global geologic map 1:20,000,000 cannot supply local mineralogy or cover thickness')
    dump('geography_check.json',geography)
    rows=[];unions={}; fig,axes=plt.subplots(1,2,figsize=(12,6))
    ax=axes[0]; gx,gy=g.exterior.xy;ax.fill(gx,gy,color='#d7e7a7',alpha=.8,label='mAl, SIM 3292')
    for poly in new.geoms: ax.plot(*poly.exterior.xy,color='#9e621d',label='Gazetteer MDIM 2.1' if poly==list(new.geoms)[0] else None)
    ax.plot(*ROI.exterior.xy,color='red',linewidth=2,label='Fixed MS-02 ROI');ax.set(xlim=(166.5,170),ylim=(51.5,54),title='Unit and approximate named-feature boundary')
    ax.legend(fontsize=8);ax=axes[1]
    for cat in ['CTX_EDR','SHARAD_USRDRV2','CRISM_TRDR','HIRISE_RDR4','HIRISE_EDR','CRISM_MTRDR']:
        ps=products(cat); geometries=[]
        if ps is None:
            unions[cat]=dict(status='query unsupported; not zero coverage',catalog_records=None);continue
        for x in ps:
            geom=wkt.loads(x['Footprint_geometry']);assert geom.is_valid,(cat,x['pdsid'])
            inter=geom.intersection(ROI);frac=transform(PROJECT,inter).area/AREA if geom.geom_type.endswith('Polygon') else None
            isscience=cat!='CRISM_TRDR' or '_if' in x['pdsid']
            if not inter.is_empty and isscience:geometries.append(geom)
            rows.append(dict(catalog=cat,product_id=x['pdsid'],is_reflectance_or_primary_science=isscience,
                footprint_type=geom.geom_type,intersects_roi=not inter.is_empty,roi_area_fraction=frac if frac is not None else '',
                utc_start=x.get('UTC_start_time',''),utc_stop=x.get('UTC_stop_time',''),map_scale_m_px=x.get('Map_scale',''),
                solar_longitude_deg=x.get('Solar_longitude',''),incidence_deg=x.get('Incidence_angle',''),
                source_url=x.get('LabelURL',''),footprint_wkt=x['Footprint_geometry'],quality='footprint support only; not all pixels validated'))
            if cat=='CTX_EDR': ax.plot(*geom.exterior.xy,alpha=.65,label=x['pdsid'][:3])
            if cat=='SHARAD_USRDRV2':
                lines=list(inter.geoms) if hasattr(inter,'geoms') else [inter]
                for line in lines:
                    if not line.is_empty:ax.plot(*line.xy,color='#771777',linewidth=2)
        union=unary_union(geometries)
        unions[cat]=dict(catalog_records=len(ps),science_records=sum(r['is_reflectance_or_primary_science'] for r in rows if r['catalog']==cat),
            intersecting_science_records=len(geometries),union_roi_fraction=transform(PROJECT,union.intersection(ROI)).area/AREA if 'SHARAD' not in cat else None)
    table('product_footprints.csv',rows);dump('catalog_summary.json',unions)
    ax.plot(*ROI.exterior.xy,color='red',linewidth=2);ax.set(xlim=(167.8,168.7),ylim=(52.3,53.2),title='CTX outlines and SHARAD ground tracks');ax.legend(fontsize=8)
    for ax in axes:ax.set_xlabel('East longitude (degrees)');ax.set_ylabel('Planetocentric latitude (degrees)');ax.grid(alpha=.2)
    fig.tight_layout();fig.savefig(P/'fig_verified_footprints.png',dpi=180);plt.close(fig)
    print(json.dumps(dict(thermal=thermal,geography=geography,catalog=unions),indent=2))
if __name__=='__main__':main()
