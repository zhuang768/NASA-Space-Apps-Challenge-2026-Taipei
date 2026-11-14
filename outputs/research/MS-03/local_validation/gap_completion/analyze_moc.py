"""PDS MOC RDR native pixel-centre ROI mask; no tracing, interpolation or ice inference."""
from pathlib import Path
import numpy as np,json,hashlib,re
from PIL import Image
O=Path(__file__).resolve().parent;S=O/'sources'
b=(S/'s1700607_na.img').read_bytes();label=(S/'s1700607_na.lbl').read_text()
assert len(b)==10568*2728
im=np.frombuffer(b,dtype=np.uint8,offset=8184).reshape(10565,2728)
assert int(im.sum(dtype=np.uint64))==1590142434
# PDS one-based sample/line centres. DSMAP polar stereographic, spherical R and pole.
R=3396190.;scale=3.000339463;so=-2906.;lo=-646450.;lon0=242.
xs=(np.arange(im.shape[1])+1-so-1)*scale
valid_count=0;bounds=[];tiles=[];extrema=[90.,-90.,360.,0.]
for r0 in range(0,len(im),256):
 r1=min(r0+256,len(im));y=(lo-(np.arange(r0,r1)+1)+1)*scale
 rho=np.hypot(xs[None,:],y[:,None]);lat=90-np.degrees(2*np.arctan(rho/(2*R)));lon=(lon0+np.degrees(np.arctan2(xs[None,:],-y[:,None])))%360
 v=im[r0:r1]!=0
 for k,a,op in [(0,lat,np.min),(1,lat,np.max),(2,lon,np.min),(3,lon,np.max)]:
  if op is np.min:extrema[k]=min(extrema[k],float(op(a[v])))
  else:extrema[k]=max(extrema[k],float(op(a[v])))
 m=v&(lat>=57.5)&(lat<=58)&(lon>=242)&(lon<=242.5)
 valid_count+=int(m.sum())
 rr,cc=np.where(m)
 if len(rr):bounds.append([r0+int(rr.min()),r0+int(rr.max()),int(cc.min()),int(cc.max())])
# Check valid pixel centres lie inside separately reported footprint bounds.
# Footprint bounds include zero-valued padding: equality is neither expected nor assumed.
label_ext=[float(re.search(r'^'+k+r'\s*=\s*([\d.]+)',label,re.M)[1]) for k in ['MINIMUM_LATITUDE','MAXIMUM_LATITUDE','WESTERNMOST_LONGITUDE','EASTERNMOST_LONGITUDE']]
assert extrema[0]>=label_ext[0]-.0001 and extrema[1]<=label_ext[1]+.0001
assert extrema[2]>=label_ext[2]-.0001 and extrema[3]<=label_ext[3]+.0001
r0=min(x[0] for x in bounds);r1=max(x[1] for x in bounds)+1;c0=min(x[2] for x in bounds);c1=max(x[3] for x in bounds)+1
# Retain exact source-DN ROI bounding crop with unknown/outside pixels masked zero.
x=xs[c0:c1];y=(lo-(np.arange(r0,r1)+1)+1)*scale
lat=90-np.degrees(2*np.arctan(np.hypot(x[None,:],y[:,None])/(2*R)));lon=(lon0+np.degrees(np.arctan2(x[None,:],-y[:,None])))%360
m=(im[r0:r1,c0:c1]!=0)&(lat>=57.5)&(lat<=58)&(lon>=242)&(lon<=242.5)
crop=np.where(m,im[r0:r1,c0:c1],0).astype('uint8')
Image.fromarray(crop).save(O/'MOC_S1700607_roi_native_DN.png')
# Three fixed nearest-valid centres at southern/middle/northern available strip; no feature-selected tiles.
for i,quant in enumerate([.15,.5,.85],1):
 rr=int(r0+(r1-r0-1)*quant);cols=np.where(m[rr-r0])[0];cc=c0+int(np.median(cols))
 a=max(rr-256,r0);d=min(a+512,r1);a=d-512
 f=max(cc-256,c0);g=min(f+512,c1);f=g-512
 tile=crop[a-r0:d-r0,f-c0:g-c0];Image.fromarray(tile).save(O/f'MOC_detail_{i}_native_DN.png')
 tiles.append(dict(id=i,source_rows_0based_inclusive=[a,d-1],source_columns_0based_inclusive=[f,g-1],latitude_deg_N=float(lat[rr-r0,cc-c0]),longitude_deg_E=float(lon[rr-r0,cc-c0]),selection='fixed along-strip fraction; nearest valid centre, not feature-based',valid_roi_pixels=int(np.count_nonzero(tile)),display='native 8-bit source DN; zero is masked outside-ROI/no-data'))
q=dict(product_id='S1700607_NA',raw_product_id='S17/00607',source_sha256=hashlib.sha256(b).hexdigest(),source_label_sha256=hashlib.sha256((S/'s1700607_na.lbl').read_bytes()).hexdigest(),utc_start='2006-04-08T00:22:40.473',utc_stop='2006-04-08T00:22:50.285',projection='spherical north polar stereographic',radius_m=R,centre_longitude_deg_E=lon0,map_grid_m=scale,native_downtrack_summing=3,native_crosstrack_summing=3,map_grid_is_effective_resolution=False,latitude_convention='planetocentric',longitude_convention='east-positive',producer_quality_id='1000000000',producer_quality_interpretation='complete C-kernel; no extraction error or repair reported; not proof of feature detectability',original_dimensions=[10565,2728],roi_valid_nonzero_pixel_centres=valid_count,source_valid_pixel_coordinate_extrema=extrema,label_coordinate_extrema=label_ext,roi_crop_0based_inclusive=[r0,r1-1,c0,c1-1],tiles=tiles,geometry_measurement='not performed: no validated closed polygon boundaries',morphology='unknown; no automated morphology classification; separate visual-review record required',ice_presence='unknown',processing='Original RDR is destriped, histogram-scaled and map-projected. This script masks and crops only; it does not enhance or add spatial detail.')
(O/'moc_summary.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
