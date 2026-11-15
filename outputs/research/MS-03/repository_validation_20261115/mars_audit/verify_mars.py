"""Offline independent audit. Reads immutable checkout; writes only output directory.
No acquisition, reprojection, interpolation, sharpening, segmentation or inference of edges.
"""
from pathlib import Path
import json,csv,math,hashlib,gzip,re,subprocess,argparse
import numpy as np
from PIL import Image,ImageDraw
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);args=parser.parse_args();ROOT=args.repo.resolve();OUT=args.out.resolve();OUT.mkdir(parents=True,exist_ok=True)
SHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
R=3396190.; RAD=math.pi/180
LV=ROOT/'outputs/research/MS-03/local_validation'; MOR=ROOT/'outputs/research/MS-03/morphology'; GAP=LV/'gap_completion'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def area(b):return R*R*(b['east']-b['west'])*RAD*(math.sin(b['north']*RAD)-math.sin(b['south']*RAD))
roi={'west':242.,'east':242.5,'south':57.5,'north':58.};roi_area=area(roi)
rows=[]; hashes={};image_inventory=[]
obs=json.loads((LV/'ctx_observability.json').read_text()); old=json.loads((LV/'ctx_sample_manifest.json').read_text())
for s in obs['samples']:
 p=LV/s['image_file'];im=Image.open(p).convert('RGBA');a=np.asarray(im);b=dict(s['bounds_mars_east180_lat']);b['east']%=360;b['west']%=360
 pp=int((a[:,:,3]>0).sum());assert digest(p)==s['sha256']; assert pp==s['opaque_pixels']
 px=area(b)/a.shape[0]/a.shape[1]; y=R*(b['north']-b['south'])*RAD/a.shape[0];x=px/y
 rows.append(dict(window_id='CTX_'+s['sample_id'],source_sha=SHA,source_path=str(p.relative_to(ROOT)),west_E=b['west'],east_E=b['east'],south_N=b['south'],north_N=b['north'],width_px=im.width,height_px=im.height,nonzero_or_opaque_px=pp,map_spacing_m=f'{x:.12g};{y:.12g}',nominal_source_spacing_m=';'.join(map(str,s['native_ctX_nominal_m'])),optical_resolution_m='NA',observed_ground_area_km2=area(b)/1e6,in_roi_fraction=1.,acceptance='not_accepted',qualified_contours=0,polygon_width_m='NA',polygon_area_m2='NA',polygon_density_km2='NA',reason='Mottled/tonal surface; no two adjacent fully traceable closed units or repeatable three-junction contour; opaque display pixels are not sensor QA',limit='KML display derivative; geolocation uncertainty and PSF unknown; 8 samples necessary but not sufficient; no inferred edges'))
 hashes[str(p.relative_to(ROOT))]=digest(p)
# Crop retained in Git is masked RDR DN, not absent original IMG.
p=GAP/'MOC_S1700607_roi_native_DN.png';im=np.asarray(Image.open(p)); q=json.loads((GAP/'moc_summary.json').read_text());scale=float(q['map_grid_m']); r0,r1,c0,c1=q['roi_crop_0based_inclusive'];assert im.shape==(r1-r0+1,c1-c0+1)
# Repeat PDS pixel-centre inverse from independent retained label offsets.
label=(GAP/'sources/s1700607_na.lbl').read_text();fetch=lambda k:float(re.search(r'^'+k+r'\s*=\s*([-\d.]+)',label,re.M)[1]); so=fetch('SAMPLE_PROJECTION_OFFSET');lo=fetch('LINE_PROJECTION_OFFSET');l0=fetch('CENTER_LONGITUDE')
xs=(np.arange(c0,c1+1)-so)*scale
moc_count=0;ground_area=0.;ext=[90,-90,360,0]; maxoutside=0
for a0 in range(0,im.shape[0],256):
 a1=min(a0+256,im.shape[0]); yy=(lo-np.arange(r0+a0,r0+a1))*scale
 rho=np.hypot(xs[None,:],yy[:,None]); lat=90-np.degrees(2*np.arctan(rho/(2*R)));lon=(l0+np.degrees(np.arctan2(xs[None,:],-yy[:,None])))%360
 m=im[a0:a1]!=0; inside=(lat>=57.5)&(lat<=58)&(lon>=242)&(lon<=242.5);maxoutside+=int((m&~inside).sum());moc_count+=int(m.sum())
 # polar stereographic local conformal scale k=2/(1+sin(phi)); ground pixel area=map pixel area/k^2.
 ground_area+=float(np.sum((scale*(1+np.sin(np.radians(lat[m])))/2)**2))
 if m.any():ext=[min(ext[0],float(lat[m].min())),max(ext[1],float(lat[m].max())),min(ext[2],float(lon[m].min())),max(ext[3],float(lon[m].max()))]
assert maxoutside==0;assert moc_count==q['roi_valid_nonzero_pixel_centres']==9272742
hashes[str(p.relative_to(ROOT))]=digest(p)
for t in q['tiles']:
 p=GAP/f"MOC_detail_{t['id']}_native_DN.png";a=np.asarray(Image.open(p));rr0,rr1=t['source_rows_0based_inclusive'];cc0,cc1=t['source_columns_0based_inclusive'];assert np.array_equal(a,im[rr0-r0:rr1-r0+1,cc0-c0:cc1-c0+1])
 # full tile geolocation pixel centres and area
 xx=(np.arange(cc0,cc1+1)-so)*scale;yy=(lo-np.arange(rr0,rr1+1))*scale;lat=90-np.degrees(2*np.arctan(np.hypot(xx[None,:],yy[:,None])/(2*R)));lon=(l0+np.degrees(np.arctan2(xx[None,:],-yy[:,None])))%360
 m=a!=0; ar=float(np.sum((scale*(1+np.sin(np.radians(lat[m])))/2)**2));assert int(m.sum())==t['valid_roi_pixels']
 rows.append(dict(window_id=f"MOC_{t['id']}",source_sha=SHA,source_path=str(p.relative_to(ROOT)),west_E=float(lon.min()),east_E=float(lon.max()),south_N=float(lat.min()),north_N=float(lat.max()),width_px=a.shape[1],height_px=a.shape[0],nonzero_or_opaque_px=int(m.sum()),map_spacing_m=scale,nominal_source_spacing_m='NA;original3x3summed',optical_resolution_m='NA',observed_ground_area_km2=ar/1e6,in_roi_fraction=1.,acceptance='not_accepted',qualified_contours=0,polygon_width_m='NA',polygon_area_m2='NA',polygon_density_km2='NA',reason='Mottled fine texture and broad tonal contrasts; no two adjacent closed cells with independently repeatable junctions; no blind inter-rater test',limit='3.000339463m projected sampling is not optical resolution; retained masked crop verified, original IMG absent'))
 hashes[str(p.relative_to(ROOT))]=digest(p)
# Actual uncalibrated native CTX row bytes and exact pre-existing displayed crop.
b=gzip.decompress((MOR/'D01_native_rows.bin.gz').read_bytes());assert len(b)==5177344
assert hashlib.sha256(b).hexdigest()=='4ecf31416e3f76ce564dda7264d8ee0b8147d26f74ace17d5d2adf31d90aecae'
a=np.frombuffer(b,np.uint8).reshape(1024,5056);p=MOR/'D01_native_crop_DN.png';crop=np.asarray(Image.open(p));assert np.array_equal(crop,a[:,600:1624])
ctxraw=dict(source_path='outputs/research/MS-03/morphology/D01_native_rows.bin.gz',rows_0based=[36000,37023],samples=[0,5055],raw_byte_count=len(b),sha256_uncompressed=hashlib.sha256(b).hexdigest(),no_map_projection=True,precise_ground_area='NA',visual_crop_rows=[36000,37023],visual_crop_samples=[600,1623],visual_crop_pixels=int(crop.size),native_grid_m='6.089997 nominal source',verified_png_equal_retained_bytes=True,acceptance='not_accepted',reason='Uncalibrated/striped DN; approximate bilinear index locator only; no qualified adjacent closed network')
rows.append(dict(window_id='CTX_D01_native_supplement',source_sha=SHA,source_path=str(p.relative_to(ROOT)),west_E=242.201,east_E=242.423,south_N=57.664,north_N=57.779,width_px=crop.shape[1],height_px=crop.shape[0],nonzero_or_opaque_px=int(np.count_nonzero(crop)),map_spacing_m='NA;unprojected6.089997nominal',nominal_source_spacing_m=6.089997,optical_resolution_m='NA',observed_ground_area_km2='NA',in_roi_fraction='NA',acceptance='not_accepted',qualified_contours=0,polygon_width_m='NA',polygon_area_m2='NA',polygon_density_km2='NA',reason='Uncalibrated striped DN; no two adjacent complete closed contours; rows36000:37023 samples600:1623; unprojected',limit='Bounds are approximate four-corner bilinear locator from morphology README; not precision geolocation or actual ground area; nonzero DN not sensorQA'))
# all image-like tracked files in MS03; distinguishes source derivatives from raw products by path.
tree=subprocess.check_output(['git','ls-tree','-rl','HEAD','--','outputs/research/MS-03'],cwd=ROOT,text=True).splitlines()
for line in tree:
 meta,path=line.split('\t',1)
 if re.search(r'\.(png|jpg|jpeg|tif|tiff|jp2|img|imq|IMG|gz)$',path):
  parts=meta.split();image_inventory.append(dict(source_sha=SHA,path=path,git_blob=parts[2],bytes=int(parts[3]),classification='retained_file;see_extension_and_source_label;not_automatically_measurable'))
for name,data in [('windows.csv',rows),('retained_image_inventory.csv',image_inventory)]:
 with (OUT/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
summary=dict(source_sha=SHA,roi_area_spherical_km2=roi_area/1e6,roi_area_radius_m=R,ctx_five_window_area_km2=sum(x['observed_ground_area_km2'] for x in rows[:5]),ctx_five_window_fraction_of_roi=sum(x['observed_ground_area_km2'] for x in rows[:5])/(roi_area/1e6),ctx_opaque_px=sum(x['nonzero_or_opaque_px'] for x in rows[:5]),moc_retained_valid_pixels=moc_count,moc_retained_valid_area_km2=ground_area/1e6,moc_retained_valid_fraction_of_roi=ground_area/roi_area,moc_nonzero_outside_roi=maxoutside,moc_valid_pixel_centre_extrema=ext,moc_three_reviewed_windows_area_km2=sum(x['observed_ground_area_km2'] for x in rows if x['window_id'].startswith('MOC_')),moc_three_reviewed_windows_fraction_of_roi=sum(x['observed_ground_area_km2'] for x in rows if x['window_id'].startswith('MOC_'))/(roi_area/1e6),fixed_review_window_count=8,supplemental_window_count=1,qualified_contour_count=0,morphology='unknown',original_moc_IMG_present=(GAP/'sources/s1700607_na.img').exists(),moc_full_original_rebuild='not_executed;original IMG absent;masked PNG/count/geolocation and retained fixed tiles tested',ctx_native_rows=ctxraw,nonzero_is_not_quality_qualification=True,ground_area_method='Mars spherical pixel-centre approximation; polar map area corrected by k^-2; areas are observation support, not qualified polygon area',overlap_limit='CTX and MOC supports overlap; do not sum them as unique coverage',figure_limit='No source-corner footprint interpreted as valid-pixel mask; no optical resolution asserted')
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(OUT/'input_hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
# Native pixel contact sheet: no scientific changes; individual originals remain listed.
canvas=Image.new('RGB',(1590,970),'white');d=ImageDraw.Draw(canvas)
d.text((20,8),'MS-03 fixed-window audit: native samples only; no qualified complete closed contour set',(0,0,0))
for i,t in enumerate(q['tiles']):
 img=Image.open(GAP/f"MOC_detail_{t['id']}_native_DN.png").convert('RGB');x=20+i*525;y=52
 canvas.paste(img,(x,y));d.text((x,y-20),f'MOC {t["id"]}: full512x512;3.000339463m map grid;2006-04-08',(0,0,0))
for i,s in enumerate(obs['samples']):
 x=20+i*310;y=645;img=Image.open(LV/s['image_file']).convert('RGB');canvas.paste(img,(x,y));d.text((x,y-36),f'CTX {s["sample_id"]}: full256x256',(0,0,0));d.text((x,y-20),'2010/2012 KML mosaic;~5.4m display',(0,0,0))
d.text((20,930),'No enhancement/resampling. Map sampling differs from optical resolution. SHA '+SHA+'.',(0,0,0));d.text((20,950),'Source paths/window bounds: windows.csv. These8windows are a bounded sample, not proof of morphology absence.',(0,0,0));canvas.save(OUT/'native_review_contact_sheet.png')
print(json.dumps(summary,indent=2))
