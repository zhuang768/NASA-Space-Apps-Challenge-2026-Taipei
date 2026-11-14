"""Read three original IRPBT2 products; descriptive ROI brightness temperatures.

No atmospheric/emissivity correction, registration validation, ice inversion or
cross-scene daily-amplitude interpretation. Uses original SINUSOIDAL map labels.
"""
from pathlib import Path
import hashlib,json,re,csv,argparse
import numpy as np

HERE=Path(__file__).resolve().parent
ROI=dict(south=56.5,north=57.,west=72.5,east=73.)
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input-dir',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)

def get(text,key):
    m=re.search(r'^\s*'+re.escape(key)+r'\s*=\s*(.*?)\s*$',text,re.M)
    if not m:raise ValueError(key)
    return m[1].strip().strip('"')

def stats(a):
    if len(a)==0:return dict(n=0,min_K=None,p05_K=None,median_K=None,mean_K=None,p95_K=None,max_K=None,std_population_K=None)
    return dict(n=len(a),min_K=float(a.min()),p05_K=float(np.quantile(a,.05)),median_K=float(np.median(a)),mean_K=float(a.mean()),p95_K=float(np.quantile(a,.95)),max_K=float(a.max()),std_population_K=float(a.std()))

summaries=[];receipts=[];grid_records=[]
for p in sorted(a.input_dir.glob('*.IMG')):
    b=p.read_bytes();text=b[:10000].decode('ascii',errors='replace');record=int(get(text,'RECORD_BYTES'));pointer=int(get(text,'^IMAGE'));n=int(get(text,'LINES'));s=int(get(text,'LINE_SAMPLES'));offset=(pointer-1)*record
    assert get(text,'SAMPLE_TYPE')=='PC_REAL' and int(get(text,'SAMPLE_BITS'))==32
    assert len(b)-offset==n*s*4 and get(text,'MAP_PROJECTION_TYPE')=='SINUSOIDAL'
    payload=b[offset:];assert hashlib.md5(payload).hexdigest()==get(text,'MD5_CHECKSUM')
    arr=np.frombuffer(payload,dtype='<f4').reshape(n,s);scale=float(get(text,'SCALING_FACTOR'));add=float(get(text,'OFFSET'));null=float(get(text,'NULL_CONSTANT'))
    radius=float(get(text,'A_AXIS_RADIUS'));assert radius==float(get(text,'B_AXIS_RADIUS'))==float(get(text,'C_AXIS_RADIUS'))
    resolution=float(get(text,'MAP_SCALE'));spo=float(get(text,'SAMPLE_PROJECTION_OFFSET'));lpo=float(get(text,'LINE_PROJECTION_OFFSET'));lon0=float(get(text,'CENTER_LONGITUDE'))
    assert get(text,'COORDINATE_SYSTEM_NAME')=='PLANETOCENTRIC' and get(text,'POSITIVE_LONGITUDE_DIRECTION')=='EAST'
    row,col=np.indices((n,s));valid=np.isfinite(arr)&(arr!=null)
    temp=arr.astype(float)*scale+add
    # PDS sample/line equations expressed with zero-based NumPy centres.
    # This selected convention is retained explicitly and independently tested
    # below against both one-pixel shifts, not claimed as map registration proof.
    lat=np.degrees((lpo-row)*resolution/radius)
    lon=lon0+np.degrees((col-spo)*resolution/(radius*np.cos(np.radians(lat))))
    selection=(lat>=ROI['south'])&(lat<ROI['north'])&(lon>=ROI['west'])&(lon<ROI['east'])
    selected=selection&valid
    nominal=stats(temp[selected]);sens=[]
    for dl in [-1,0,1]:
        for ds in [-1,0,1]:
            ll=np.degrees((lpo-row+dl)*resolution/radius)
            oo=lon0+np.degrees((col-spo+ds)*resolution/(radius*np.cos(np.radians(ll))))
            mask=(ll>=56.5)&(ll<57)&(oo>=72.5)&(oo<73)&valid
            st=stats(temp[mask]);sens.append(dict(line_shift_px=dl,sample_shift_px=ds,**st))
    # Source-labelled image range is a footprint constraint, not a guarantee that
    # every projected rectangular image pixel is a non-null observation.
    labelled_bounds={k:float(get(text,k)) for k in ['MINIMUM_LATITUDE','MAXIMUM_LATITUDE','WESTERNMOST_LONGITUDE','EASTERNMOST_LONGITUDE']}
    centre_lat=56.75;centre_lon=72.75
    ic=int(round(lpo-np.radians(centre_lat)*radius/resolution));jc=int(round(spo+np.radians(centre_lon-lon0)*radius*np.cos(np.radians(centre_lat))/resolution))
    centre=dict(requested_latitude_n=centre_lat,requested_longitude_e=centre_lon,row_0based=ic,column_0based=jc,inside_array=bool(0<=ic<n and 0<=jc<s),valid=False,brightness_K=None)
    if centre['inside_array']:
        centre.update(valid=bool(valid[ic,jc]),brightness_K=float(temp[ic,jc]) if valid[ic,jc] else None,nearest_pixel_latitude_n=float(lat[ic,jc]),nearest_pixel_longitude_e=float(lon[ic,jc]))
    item=dict(product_id=get(text,'PRODUCT_ID'),filename=p.name,source_kind='PDS projected brightness-temperature product; this-run ROI selection and summaries',dataset_id=get(text,'DATA_SET_ID'),version=get(text,'PRODUCT_VERSION_ID'),UTC_start=get(text,'START_TIME'),UTC_stop=get(text,'STOP_TIME'),solar_longitude_deg=float(get(text,'SOLAR_LONGITUDE')),local_time_h=float(get(text,'LOCAL_TIME')),band_number=int(get(text,'BAND_NUMBER')),band_centre_micrometre=float(get(text,'BAND_CENTER').split()[0]),unit=get(text,'ODY:SAMPLE_UNIT'),image_shape=[n,s],image_offset_bytes=offset,payload_md5_matches_label=True,whole_image_valid_n=int(valid.sum()),whole_image_null_n=int((~valid).sum()),ROI_nominal_pixel_centres_n=int(selection.sum()),ROI_valid_n=int(selected.sum()),ROI_null_n=int((selection&~valid).sum()),ROI_valid_stats=nominal,ROI_selected_centre_bounds=dict(south=float(lat[selected].min()) if selected.any() else None,north=float(lat[selected].max()) if selected.any() else None,west=float(lon[selected].min()) if selected.any() else None,east=float(lon[selected].max()) if selected.any() else None),labelled_footprint_bounds=labelled_bounds,nearest_MS01_centre=centre,projection=dict(type='SINUSOIDAL',radius_km=radius,map_scale_km=resolution,centre_lon_e=lon0,sample_projection_offset=spo,line_projection_offset=lpo,formula_zero_based='lat=degrees((LPO-row)*MAP_SCALE/R);lon=LON0+degrees((col-SPO)*MAP_SCALE/(R*cos(lat)))',normative_convention_status='Pending source CAT reading; exact numeric convention is explicit; +/-1pixel sensitivity provided'),one_pixel_convention_sensitivity=sens)
    summaries.append(item)
    receipts.append(dict(filename=p.name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),payload_md5=hashlib.md5(payload).hexdigest(),label_md5=get(text,'MD5_CHECKSUM')))
    # Thin traceable sample rather than every ROI pixel (all full inputs retained).
    ii,jj=np.where(selected)
    for k in np.linspace(0,len(ii)-1,min(12,len(ii)),dtype=int):
        i,j=int(ii[k]),int(jj[k]);grid_records.append(dict(product_id=item['product_id'],row_0based=i,column_0based=j,latitude_n=float(lat[i,j]),longitude_e=float(lon[i,j]),brightness_K=float(temp[i,j]),image_byte_offset=offset+(i*s+j)*4))

result=dict(task='MS01 projected THEMIS brightness-temperature ROI audit',ROI=ROI,selection='Half-open latitude/longitude pixel-centre mask;finite and non-null only;no interpolation',products=summaries,source_receipts=receipts,limits=['Brightness temperature at band9,not emissivity/atmosphere-corrected kinetic ground temperature','Individual scene subsets have unequal coverage;not the wholeROI mean','Different UTC,Ls and local times are not a same-sol day/night pair,season-controlled experiment or causal ice test','No product per-pixel calibration uncertainty or cloud/dust QA has been independently validated here','Sinusoidal sphere uses label3396.190km,not commonMars3396.000km','Projection offset source CAT pending reading; +/-1pixel convention sensitivity is not geographic accuracy or confidence interval','No ice-depth,ice-abundance or Earth-to-Mars thermal-parameter inference'])
(a.output_dir/'projected_temperature_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
with (a.output_dir/'ROI_pixel_samples.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,list(grid_records[0]));w.writeheader();w.writerows(grid_records)
with (a.output_dir/'temperature_summary.csv').open('w',newline='') as f:
    rr=[dict(product_id=s['product_id'],UTC_start=s['UTC_start'],solar_longitude_deg=s['solar_longitude_deg'],local_time_h=s['local_time_h'],ROI_nominal_n=s['ROI_nominal_pixel_centres_n'],ROI_valid_n=s['ROI_valid_n'],ROI_null_n=s['ROI_null_n'],**s['ROI_valid_stats']) for s in summaries];w=csv.DictWriter(f,list(rr[0]));w.writeheader();w.writerows(rr)
print(json.dumps([dict(id=s['product_id'],valid=s['ROI_valid_n'],null=s['ROI_null_n'],stats=s['ROI_valid_stats'],centre=s['nearest_MS01_centre'],sensitivity_median_min=min(v['median_K'] for v in s['one_pixel_convention_sensitivity'] if v['median_K'] is not None),sensitivity_median_max=max(v['median_K'] for v in s['one_pixel_convention_sensitivity'] if v['median_K'] is not None)) for s in summaries],indent=2))
