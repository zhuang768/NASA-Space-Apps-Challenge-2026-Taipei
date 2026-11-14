"""Fixed-MS03 data validation/extraction. No Mars boundary tracing or clock alignment."""
from pathlib import Path
import argparse,csv,json,hashlib,math,re,zipfile
import numpy as np
import shapefile,rasterio
from rasterio.windows import Window
from shapely.geometry import shape,box,Point,mapping
from shapely import wkt
from PIL import Image
O=Path(__file__).resolve().parent;S=O/'sources';ROOT=O.parents[3]
ROI=box(242,57.5,242.5,58);ROI_NEG=box(-118,57.5,-117.5,58)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def writecsv(name,rows):
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def dump(name,obj):(O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
parser=argparse.ArgumentParser();parser.add_argument('--mars-raw-dir',required=True);args=parser.parse_args()
# CaltechDATA v1: verify provider MD5, coordinate axes, matrix shape and native cell match.
rec=json.loads((S/'piqueux_record.json').read_text());checks=[]
for name,f in rec['files']['entries'].items():
 p=S/('piqueux_'+name)
 assert p.exists() and p.stat().st_size==f['size']
 assert hashlib.md5(p.read_bytes()).hexdigest()==f['checksum'].split(':')[1]
 checks.append({'file':name,'bytes':p.stat().st_size,'provider_checksum':f['checksum'],'provider_checksum_verified':True,'sha256':h(p),'content_url':f['links']['content']})
lat=np.loadtxt(S/'piqueux_Lat.ascii');lon=np.loadtxt(S/'piqueux_Lon.ascii');dep=np.loadtxt(S/'piqueux_d_m.ascii');ti=np.loadtxt(S/'piqueux_TI_SI.ascii')
assert dep.shape==ti.shape==(len(lat),len(lon))==(360,720)
assert np.allclose(np.diff(lat),-.5) and np.allclose(np.diff(lon),.5)
rs=np.where((lat>57.5)&(lat<58))[0];cs=np.where((lon>242)&(lon<242.5))[0];assert len(rs)==len(cs)==1
r,c=int(rs[0]),int(cs[0]);assert (lat[r],lon[c])==(57.75,242.25)
assert dep[r,c]!=-32768 and ti[r,c]!=-32768 and dep[r,c]>0
row={'candidate_id':'MS-03','dataset_doi':'10.22002/D1.1316','record':'ym7fc-x0r93','version':'1.0 (2019-11-27)','row_0based':r,'column_0based':c,'latitude_planetocentric_deg':float(lat[r]),'longitude_east_deg':float(lon[c]),'lat_min':57.5,'lat_max':58,'lon_min':242,'lon_max':242.5,'model_ice_depth_m_raw':float(dep[r,c]),'model_upper_regolith_TI':float(ti[r,c]),'TI_units':'J m^-2 K^-1 s^-1/2','actual_ice_depth_m':'unknown','ice_volume_or_mass_fraction':'unknown','evidence_type':'published model estimate, locally extracted; NOT direct measurement','nodata_code':-32768}
writecsv('piqueux_native_cell.csv',[row])
dump('piqueux_qa.json',{'files':checks,'actual_matrix_shape_lat_lon':[360,720],'row_index':r,'column_index':c,'valid_cells_in_fixed_roi':1,'product_grid_degrees':.5,'deposited_ppd':2,'paper_reports_ppd':3,'grid_note':'Use deposited 2 ppd coordinates; conversion from paper 3 ppd to deposited 2 ppd undocumented in retrieved notes. Do not imply 3 ppd data were extracted.','metadata_dimension_note':'Notes lists 720x360; actual ASCII matrix is360 latitude rows x720 longitude columns, independently resolved by coordinate-file lengths.','raw_depth_m':float(dep[r,c]),'display_depth_m':'~0.10 (conditional model)','upper_material_ti':float(ti[r,c]),'ti_unit_note':'Physical SI J m^-2 K^-1 s^-1/2 from paper; Notes renders m^2 (unit typography not used to redefine TI).','limits':['Two-layer thermal model assumes ice as the lower material; no unique material separation or independent local ice truth.','Lookup depths discrete, raw decimals not measurement precision.','Cannot distinguish massive from pore ice; local fraction remains unknown.','Published MCS native support ~7 km; deposited cell ~30x16 km. No sub-cell variability resolved.','MCS/THEMIS overlap other thermal evidence; no independent-truth count.','Exact per-cell observation times and QA not provided in the deposited grids.']})
# Original USGS shapefile, acquired via zip member ranges + CRC check, not the initial mirror.
rdr=shapefile.Reader(str(S/'USGS_Global_Geology'));units=[]
for sr in rdr.iterShapeRecords(bbox=(-118,57.5,-117.5,58)):
 g=shape(sr.shape.__geo_interface__)
 assert g.is_valid,'Stop for topology review; do not silently repair.'
 if g.intersects(ROI_NEG):units.append({'attributes':sr.record.as_dict(),'source_shape_id':sr.shape.oid,'geometry_valid':True,'covers_fixed_roi':g.covers(ROI_NEG),'contains_center':g.covers(Point(-117.75,57.75)),'clipped_geometry':mapping(g.intersection(ROI_NEG))})
assert len(units)==1 and units[0]['attributes']['Unit']=='AHv' and units[0]['covers_fixed_roi']
dump('geology_query.json',{'dataset':'USGS SIM3292, original official ZIP','map_scale':'1:20,000,000','crs_wkt':(S/'USGS_Global_Geology.prj').read_text(),'query_bounds':[-118,57.5,-117.5,58],'units':units,'limits':'Mapped regional volcanic substrate; no local soil, mantle, mineral assay, ice proof or map-contact accuracy claim.'})
# SWIM baseline recheck from read-only local raw GeoTIFFs, matching pinned source hashes.
baseline=json.loads((ROOT/'outputs/research/mars_reselection_20261114/candidate_native_evidence.json').read_text());pixels=[];sw=[]
for file in ['SWIM2_c0_1.tif','SWIM2_c1_5.tif']:
 path=Path(args.mars_raw_dir)/file;srcmeta=next(x for x in baseline['sources'] if x['path'].endswith('/'+file));assert h(path)==srcmeta['sha256']
 with rasterio.open(path) as ds:
  pr=ds.crs.to_dict();assert pr['proj']=='eqc' and all(pr.get(k,0)==0 for k in ['lat_ts','lat_0','lon_0','x_0','y_0'])
  R=pr['R'];tr=ds.transform;assert tr.b==tr.d==0
  xs=tr.c+(np.arange(ds.width)+.5)*tr.a;ys=tr.f+(np.arange(ds.height)+.5)*tr.e
  lo=(np.rad2deg(xs/R)%360);la=np.rad2deg(ys/R)
  rr=np.where((la>57.5)&(la<58))[0];cc=np.where((lo>242)&(lo<242.5))[0];a=ds.read(1,window=Window(int(cc.min()),int(rr.min()),len(cc),len(rr)))
  valid=np.isfinite(a)&(a>=-1)&(a<=1)&(a!=ds.nodata)
  wt=np.cos(np.deg2rad(la[rr]))[:,None]*np.ones_like(a);mean=float(np.sum(a[valid]*wt[valid])/np.sum(wt[valid]))
  sw.append({'product':file,'source_url':srcmeta['url'],'sha256':h(path),'radius_m':R,'source_crs_wkt':ds.crs.to_wkt(),'source_grid_m':[tr.a,abs(tr.e)],'selected_cells':int(a.size),'valid_cells':int(valid.sum()),'weighted_mean':mean,'min':float(a[valid].min()),'max':float(a[valid].max()),'source_resolution_note':'~0.05 deg output, not independent instrument footprint','interpretation':'consistency, not probability, fraction or ice-layer depth','new_result':False})
  for i,ri in enumerate(rr):
   for j,ci in enumerate(cc):pixels.append({'product':file,'source_row_0based':int(ri),'source_column_0based':int(ci),'lat_planetocentric_deg':float(la[ri]),'lon_east_deg':float(lo[ci]),'consistency':float(a[i,j]) if valid[i,j] else '','valid':bool(valid[i,j])})
assert all(x['valid_cells']==100 for x in sw)
assert abs(sw[0]['weighted_mean']-.9109040236)<1e-7 and abs(sw[1]['weighted_mean']-.5099723018)<1e-7
writecsv('swim_native_cells.csv',pixels);dump('swim_recheck.json',{'status':'existing-result reproduction, not new observation','products':sw})
# ODE geometries: distinguish lines, polygons, product counts and independent acquisition IDs.
obs=[];catalogues=[];tracks=[]
for fn,inst in [('ode_CRISM_TRDR_expanded.json','CRISM'),('ode_THEMIS_IRBTR_local.json','THEMIS'),('ode_SHARAD_RDR_expanded.json','SHARAD')]:
 j=json.loads((S/fn).read_text())['ODEResults'];assert 'Error' not in j
 ps=j.get('Products',{}).get('Product',[]);ps=ps if isinstance(ps,list) else [ps];inside=0
 for p in ps:
  geom=p.get('Footprint_geometry') or p.get('Footprint_GL_geometry');g=wkt.loads(geom)
  if not g.is_valid:status='unknown_invalid_geometry';cut=None
  else:
   cut=g.intersection(ROI);hit=(not cut.is_empty) and (cut.length>0 if 'Line' in g.geom_type else cut.area>0)
   status='intersects_fixed_roi' if hit else 'outside_fixed_roi';inside+=int(hit)
  if inst=='SHARAD' and status=='intersects_fixed_roi':tracks.append({'type':'Feature','geometry':mapping(cut),'properties':{'product_id':p['pdsid'],'source':'ODE sampled sub-spacecraft track from Geom product; NOT radar beam footprint','date':p.get('UTC_start_time','')}})
  obs.append({'instrument':inst,'product_id':p['pdsid'],'observation_id':(p.get('Observation_id') or (p['pdsid'].split('_')[1] if inst=='SHARAD' else p['pdsid'].split('_')[0])),'product_url':p['ProductURL'],'dataset_id':p.get('Data_Set_Id',''),'utc_start':p.get('UTC_start_time',''),'utc_stop':p.get('UTC_stop_time',''),'solar_longitude_deg':p.get('Solar_longitude',''),'solar_time_as_reported':p.get('Solar_time',''),'geometry_type':g.geom_type,'geometry_source':p.get('Footprint_souce',''),'roi_relation':status,'footprint_wkt':geom,'science_pixels_downloaded':'selected SHARAD256 records only' if inst=='SHARAD' and '1768301' in p['pdsid'] else 'no','ice_signature':'unknown','quality_limit':'Footprint/date metadata alone; detector and scientific-pixel QA not established'})
 catalogues.append({'instrument':inst,'response_file':'sources/'+fn,'returned_records':len(ps),'count_field':int(j['Count']),'valid_geometry_intersections':inside,'unique_observation_identifiers':len(set((p.get('Observation_id') or (p['pdsid'].split('_')[1] if inst=='SHARAD' else p['pdsid'].split('_')[0])) for p in ps)),'limit':1000 if inst=='CRISM' else (100 if inst=='SHARAD' else 50),'complete_catalogue_claim':False})
writecsv('observation_inventory.csv',obs);dump('catalogue_qa.json',{'catalogues':catalogues,'CRISM_if_products':sum('_if' in r['product_id'].lower() for r in obs if r['instrument']=='CRISM'),'CRISM_l_if_products':sum('_if' in r['product_id'].lower() and 'l_trr' in r['product_id'].lower() for r in obs if r['instrument']=='CRISM'),'invalid_usrdr_query_note':'USRDR was an invalid IIPT, not zero coverage; valid RDR request subsequently returned six actual intersecting lines.'});dump('sharad_tracks.geojson',{'type':'FeatureCollection','name':'Mars planetocentric / east-positive degrees, NOT Earth CRS','features':tracks})
# Exact named source-image footprints for the Alba Patera example, not a centre-distance exclusion.
gregg=[]
for f in S.glob('gregg_*.json'):
 j=json.loads(f.read_text())['ODEResults'];ps=j['Products']['Product'];ps=ps if isinstance(ps,list) else [ps]
 for p in ps:
  g=wkt.loads(p.get('Footprint_geometry') or p['Footprint_GL_geometry']);assert g.is_valid
  gregg.append({'product_id':p['pdsid'],'footprint_wkt':g.wkt,'intersects_ms03':g.intersects(ROI),'geometry_source':p.get('Footprint_souce'),'utc_start':p.get('UTC_start_time'),'source_url':p.get('ProductURL')})
assert len(gregg)==2 and not any(x['intersects_ms03'] for x in gregg);dump('gregg_named_image_scope.json',gregg)
# Read published CTX mosaic seam maps and check each five patch's support, not just the centre.
with zipfile.ZipFile(S/'CTX_E-120_N56_seams.zip') as z:
 z.extractall(S/'ctx_seams')
sp=next((S/'ctx_seams').glob('*.shp'));sm=shapefile.Reader(str(sp));proj=sp.with_suffix('.prj').read_text();assert '3396190' in proj and 'Ocentric' in proj
R=3396190.;toeq=lambda b:box(*[math.radians(x)*R for x in b])
seams=[];invalid_seams=0
for sr in sm.iterShapeRecords():
 g=shape(sr.shape.__geo_interface__)
 if not g.is_valid:invalid_seams+=1;continue
 if g.intersects(toeq([-118,57.5,-117.5,58])):seams.append((g,sr.record.as_dict()))
samples=json.loads((O/'ctx_sample_manifest.json').read_text());qa=[]
for sample in samples['samples']:
 assert sample['acquired'];b=sample['overlay']['bounds'];assert -118<=b['west']<b['east']<=-117.5 and 57.5<=b['south']<b['north']<=58
 im=np.array(Image.open(O/sample['image_file']));assert im.shape==(256,256,2)
 qbox=toeq([b['west'],b['south'],b['east'],b['north']]);assigned=[a for g,a in seams if g.intersects(qbox)]
 latitude=(b['north']+b['south'])/2
 dx=R*math.radians(b['east']-b['west'])*math.cos(math.radians(latitude))/256;dy=R*math.radians(b['north']-b['south'])/256
 qa.append({'sample_id':sample['sample_id'],'image_file':sample['image_file'],'bytes':(O/sample['image_file']).stat().st_size,'sha256':h(O/sample['image_file']),'bounds_mars_east180_lat':b,'width_px':256,'height_px':256,'opaque_pixels':int((im[:,:,1]==255).sum()),'total_pixels':65536,'luminance_min':int(im[:,:,0].min()),'luminance_max':int(im[:,:,0].max()),'display_spacing_approx_m':[dx,dy],'source_product_ids':sorted(set(a['PRODUCT_ID'] for a in assigned)),'source_dates':sorted(set(a['IMAGE_TIME'] for a in assigned)),'native_ctX_nominal_m':sorted(set(float(a['PX_WIDTH']) for a in assigned)),'pixel_validity_limit':'Opaque/nonempty display pixels only, not sensor quality, frost/cloud QA or validated crack-detection resolution. Geolocation uncertainty not given.'})
assert len(qa)==5
writecsv('ctx_pixel_qa.csv',[{k:(json.dumps(v) if isinstance(v,(dict,list)) else v) for k,v in r.items()} for r in qa]);dump('ctx_observability.json',{'samples':qa,'invalid_seam_geometries':invalid_seams,'seam_products_in_roi':sorted(set(a['PRODUCT_ID'] for _,a in seams)),'source_prj':proj,'projection_method':'Mars ocentric eqc x=R*lon_rad, y=R*lat_rad, R3396190; no Earth CRS','morphology':'unknown; no reliable closed boundaries digitized','morphology_is_absent':False,'geometric_comparison_with_ad1_enabled':False,'coverage_limit':'Five deterministic local display patches only; not whole-cell quality coverage.'})
# QA/captcha distinction for acquired HTTP-200 publisher response.
html=(S/'courville_2026_article.html').read_text();assert 'Captcha' in html
dump('content_validation.json',{'courville_journal_response':{'file':'sources/courville_2026_article.html','http_status':200,'title':'Radware Bot Manager Captcha','usable_as_article':False,'full_journal_article_read':False,'alternative_read':'LPSC2026 abstract1792 pp1–2 via web PDF and author university abstract; not journal full text'},'notes':['No CAPTCHA bypass or credential access attempted.','Failed ScienceBase/table access is not an empty inventory.','Source publication grid and deposited grid differ; retain both conventions.']})
dump('analysis_summary.json',{'roi':[242,57.5,242.5,58],'starting_sha':'8fa07afac4a98096958880f6a5ece16f35abc4db','geology':'AHv; original USGS polygon covers nominal ROI','piqueux_depth_model_m':row['model_ice_depth_m_raw'],'actual_depth_m':None,'actual_ice_fraction':None,'independent_local_ice_confirmation':False,'morphology':'unknown','ad1_disposition':'general_method_reference_not_specific_pair','uv_disposition':'known_interface_method_and_quality_reference_only','campbell_hobo_alignment_performed':False,'new_physical_measurements':False,'new_model_fit':False,'new_data_extractions':['one deposited thermal-model cell','original geology ROI membership','five georeferenced mosaic display samples','three other-instrument catalogue spatial checks','one SHARAD RDR256-row geometry sample']})
print('PASS: fixed cell, five provider MD5s, original geology, two SWIM rechecks, exact product footprints, five CTX patches; all claims remain scoped.')
