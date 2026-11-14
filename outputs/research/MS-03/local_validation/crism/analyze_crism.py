"""Local pixel/format QA only. No atmospheric correction or ice classification."""
from pathlib import Path
import numpy as np,json,csv,gzip,re,hashlib,warnings
O=Path(__file__).resolve().parent;S=O/'sources'
def field(s,k):return re.search(r'(?m)^\s*'+re.escape(k)+r'\s*=\s*([^\r\n]+)',s)[1].strip().strip('"')
def csvout(n,r):
 with (O/n).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=r[0].keys());w.writeheader();w.writerows(r)
plans=json.loads((O/'extraction_plan.json').read_text());summaries=[];channels=[];geometry=[];anchors=[];masks={}
with warnings.catch_warnings():
 warnings.simplefilter('ignore',RuntimeWarning)
 for p in plans:
  pid=p['product_id'];n=p['lines'];ns=p['samples'];nb=p['bands'];lab=(S/(pid+'.lbl')).read_text();dlab=(S/(p['ddr_id']+'.lbl')).read_text();wlab=(S/p['wavelength_file_label'].lower().replace('.img','.lbl')).read_text()
  assert field(lab,'SAMPLE_TYPE')==field(dlab,'SAMPLE_TYPE')==field(wlab,'SAMPLE_TYPE')=='PC_REAL'
  assert field(lab,'BAND_STORAGE_TYPE')=='LINE_INTERLEAVED' and field(dlab,'BAND_STORAGE_TYPE')=='BAND_SEQUENTIAL'
  db=(S/(p['ddr_id']+'.img')).read_bytes();d=np.frombuffer(db,dtype='<f4').reshape(14,n,ns);lat=d[3];lon=np.mod(d[4].astype(np.float64),360)
  # Retain original DDR bytes only for selected rows in each BSQ backplane.
  parts=[];segments=[]
  for band in range(14):
   start=(band*n+p['start_line_0based'])*ns*4;stop=(band*n+p['stop_line_0based']+1)*ns*4
   chunk=db[start:stop];parts.append(chunk);segments.append(dict(band_index_0based=band,original_byte_start=start,original_byte_end_inclusive=stop-1,bytes=len(chunk),sha256=hashlib.sha256(chunk).hexdigest()))
  (S/(p['ddr_id']+'_roi_bsq.bin')).write_bytes(b''.join(parts))
  (O/(p['ddr_id']+'_subset.json')).write_text(json.dumps(dict(source_file=p['ddr_id']+'.img',source_sha256=hashlib.sha256(db).hexdigest(),method='locally concatenate verbatim original band/row bytes after full original DDR acquisition; not a single original contiguous file or HTTP range',band_storage='BAND_SEQUENTIAL',lines=p['stop_line_0based']-p['start_line_0based']+1,samples=ns,segments=segments),indent=2)+'\n')
  geo=np.isfinite(lat)&np.isfinite(lon)&(lat>=57.5)&(lat<=58)&(lon>=242)&(lon<=242.5)
  rr,cc=np.where(geo);assert len(rr)==p['roi_pixel_centres'];l0=p['start_line_0based'];l1=p['stop_line_0based']
  b=(S/(pid+'_roi_rows.bin')).read_bytes();assert len(b)==(l1-l0+1)*ns*nb*4
  cube=np.frombuffer(b,dtype='<f4').reshape(l1-l0+1,nb,ns).transpose(0,2,1);spec=cube[rr-l0,cc].copy()
  wa=np.fromfile(S/p['wavelength_file_label'].lower(),dtype='<f4',count=nb*ns).reshape(nb,ns)
  trrows=np.fromfile(S/(pid+'_rownum.bin'),dtype='>u2')
  warows=np.fromfile(S/p['wavelength_file_label'].lower(),dtype='>u2',offset=nb*ns*4,count=nb)
  assert np.array_equal(trrows,warows) and len(trrows)==nb
  wave=wa[:,cc].T;cal=np.isfinite(wave)&(wave>0)&(wave!=65535)
  finite=np.isfinite(spec);notfill=finite&(spec!=65535);numeric=notfill&cal
  window=cal&(wave>=1300)&(wave<=2200)
  allwin=(window.sum(axis=1)>0)&((numeric|~window).all(axis=1))
  poswin=allwin&(((spec>0)|~window).all(axis=1))
  anchor_indices={};anchor_masks=[]
  for nm in [1367,1500,1525,1808,2000]:
   dist=np.where(cal,abs(wave-nm),np.inf);ind=np.argmin(dist,axis=1);idx=np.arange(len(rr));wv=wave[idx,ind];sv=spec[idx,ind];v=numeric[idx,ind]
   anchor_indices[nm]=ind
   if nm in [1367,1525,1808]:anchor_masks.append(v&(sv>0))
   anchors.append(dict(product_id=pid,requested_nm=nm,nearest_nm_min=float(wv[cal.any(axis=1)].min()),nearest_nm_median=float(np.median(wv[cal.any(axis=1)])),nearest_nm_max=float(wv[cal.any(axis=1)].max()),valid_numeric_pixels=int(v.sum()),positive_pixels=int((v&(sv>0)).sum()),IF_p05=float(np.percentile(sv[v],5)) if v.any() else '',IF_median=float(np.median(sv[v])) if v.any() else '',IF_p95=float(np.percentile(sv[v],95)) if v.any() else '',limits='Nearest sampled channel, not interpolation; uncorrected I/F; percentiles are spatial spread, not confidence'))
  trip=np.logical_and.reduce(anchor_masks);masks[pid]=trip
  for k in range(nb):
   valid=numeric[:,k];wv=wave[valid,k];val=spec[valid,k]
   channels.append(dict(product_id=pid,band_index_0based=k,detector_row_0based=int(trrows[k]),wavelength_nm_min=float(wv.min()) if len(wv) else '',wavelength_nm_median=float(np.median(wv)) if len(wv) else '',wavelength_nm_max=float(wv.max()) if len(wv) else '',roi_pixel_centres=len(rr),calibration_scene_pixels=int(cal[:,k].sum()),finite_not_fill_pixels=int(notfill[:,k].sum()),numeric_and_calibration_valid_pixels=int(valid.sum()),positive_pixels=int((valid&(spec[:,k]>0)).sum()),IF_p05=float(np.percentile(val,5)) if len(val) else '',IF_median=float(np.median(val)) if len(val) else '',IF_p95=float(np.percentile(val,95)) if len(val) else '',units='dimensionless uncorrected I/F',interval_meaning='spatial percentiles, not uncertainty or confidence'))
  for j,(r,c) in enumerate(zip(rr,cc)):
   row=dict(product_id=pid,line_0based=int(r),sample_0based=int(c),latitude_planetocentric_deg=float(lat[r,c]),longitude_raw_east_signed_deg=float(d[4,r,c]),longitude_east_0_360_deg=float(lon[r,c]),incidence_areoid_deg=float(d[0,r,c]),emission_areoid_deg=float(d[1,r,c]),phase_deg=float(d[2,r,c]),local_solar_time_h=float(d[12,r,c]),numerically_valid_1300_2200_nm=bool(allwin[j]),positive_1300_2200_nm=bool(poswin[j]),three_anchor_numeric_positive=bool(trip[j]),ice_classification='unknown')
   for nm in [1367,1525,1808,2000]:
    k=anchor_indices[nm][j];v=bool(numeric[j,k]);row[f'nearest_{nm}_nm']=float(wave[j,k]) if cal[j,k] else '';row[f'IF_nearest_{nm}']=float(spec[j,k]) if v else ''
   geometry.append(row)
  corrections={k:field(lab,'MRO:'+k) for k in ['ATMO_CORRECTION_FLAG','THERMAL_CORRECTION_MODE','PHOTOCLIN_CORRECTION_FLAG','SPECTRAL_RESAMPLING_FLAG']}
  width=[]
  for j in np.unique(rr):
   co=np.where(geo[j])[0]
   if len(co)>1:
    # Adjacent DDR-centre spacing, not PSF/resolution or polygon size.
    la=lat[j,co].astype(float);lo=lon[j,co].astype(float);da=np.diff(la)*np.pi/180;db=np.diff(lo)*np.pi/180;v=np.sin(da/2)**2+np.cos(la[:-1]*np.pi/180)*np.cos(la[1:]*np.pi/180)*np.sin(db/2)**2
    width.extend(2*3396190*np.arcsin(np.sqrt(v)))
  nearest1525=next(x for x in anchors if x['product_id']==pid and x['requested_nm']==1525)
  summaries.append(dict(product_id=pid,ddr_id=p['ddr_id'],UTC_start=field(lab,'START_TIME'),UTC_stop=field(lab,'STOP_TIME'),solar_longitude_deg=float(field(lab,'SOLAR_LONGITUDE')),lines_in_subset=l1-l0+1,roi_pixel_centres=len(rr),positive_triplet_pixels=int(trip.sum()),all_1300_2200_numeric_pixels=int(allwin.sum()),all_1300_2200_positive_pixels=int(poswin.sum()),calibration_non_scene_triplet_pixels=int((~cal[np.arange(len(rr)),anchor_indices[1525]]).sum()),median_adjacent_cross_track_centre_spacing_m=float(np.median(width)),native_support_note='10x spatial binning; actual DDR adjacent centre spacing, not validated PSF or crack resolution',correction_flags=corrections,detector_temperature_C=float(field(lab,'MRO:DETECTOR_TEMPERATURE')),wavelength_detector_rows_match=True,nearest_1525_nm=nearest1525['nearest_nm_median'],ice_presence='unknown',ice_depth_m='unknown',ice_content='unknown',surface_vs_cloud_or_seasonal_frost='unknown',full_cell_quality_coverage='not established',quality_status='numeric/calibration/geometry checks completed; atmospheric, cloud/frost and instrument residual validation incomplete',geolocation_limit='DDR IR geometry is representative near2300nm; wavelength-dependent keystone and absolute error not corrected, no guaranteed ice-band pixel-footprint coverage',roi_incidence_areoid_minmax_deg=[float(d[0][geo].min()),float(d[0][geo].max())],roi_emission_areoid_minmax_deg=[float(d[1][geo].min()),float(d[1][geo].max())],roi_LST_minmax_h=[float(d[12][geo].min()),float(d[12][geo].max())]))
  print(pid,len(rr),'triplet',trip.sum(),'window',allwin.sum(),poswin.sum(),flush=True)
csvout('channel_qa.csv',channels);csvout('anchor_channels.csv',anchors)
with gzip.open(O/'roi_pixels.csv.gz','wt',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=geometry[0].keys());w.writeheader();w.writerows(geometry)
(O/'qa.json').write_text(json.dumps({'starting_sha':'778af696c654a191fe2a720f24d9f30ebd7d247b','roi':{'latitude':[57.5,58.0],'longitude_east':[242,242.5]},'nodata':65535,'numeric_valid_definition':'finite I/F !=65535 AND finite positive non-sentinel WA wavelength; positive signal screened separately; neither is final scientific validity','products':summaries,'scope':'two deliberately selected lower-incidence northern summer mapping strips, not all12L-detector products','no_ice_index_calculated':'No standard index implemented: the hyperspectral 5/11/5 kernel was not applied as if these sparse mapping channels were contiguous. A documented mapping-mode version, corrections and detection validation would require separate work; no detection threshold is set.','no_absence_claim':True,'no_polygon_tracing':True,'no_clocks_aligned':True},indent=2)+'\n')
