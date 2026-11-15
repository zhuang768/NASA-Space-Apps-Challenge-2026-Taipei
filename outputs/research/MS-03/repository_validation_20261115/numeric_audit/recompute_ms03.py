"""Offline independent MS-03 numeric audit. Inputs are exact Git blobs, not DOI downloads."""
from pathlib import Path
import csv, json, subprocess, hashlib, re, math, argparse
import numpy as np
import pandas as pd
import rasterio
import xarray as xr
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo',type=Path,required=True)
parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent)
args=parser.parse_args()
ROOT=args.repo.resolve()
OUT=args.out.resolve();OUT.mkdir(parents=True,exist_ok=True)
RAW=OUT/'github_inputs'; RAW.mkdir(exist_ok=True)
MAIN='07dbe29203504ba0ccde5e379f42ecc16e4b1b4f'
ARCHIVE='8f666d878fe0a3d97e41daa64fab43660174652f'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==MAIN,'Checkout must be pinned to frozen main'
SOURCE=ROOT/'outputs/research/mars_reselection_20261114'
manifest=json.load(open(ROOT/'config/raw_inputs_manifest.json'))
receipt=[]
for spec in manifest['files']:
 p=RAW/Path(spec['path']).name
 if not p.exists():
  with p.open('wb') as f:subprocess.run(['git','show',f"{ARCHIVE}:{spec['path']}"],cwd=ROOT,stdout=f,check=True)
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 assert digest==spec['sha256'] and p.stat().st_size==spec['bytes'],spec['path']
 receipt.append(dict(commit=ARCHIVE,path=spec['path'],git_blob=subprocess.check_output(['git','rev-parse',f"{ARCHIVE}:{spec['path']}"],cwd=ROOT,text=True).strip(),sha256=digest,bytes=p.stat().st_size,manifest_sha256_match=True))
(OUT/'input_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
row=pd.read_csv(SOURCE/'final_candidates.csv').set_index('candidate_id').loc['MS-03']
checks=[]
def ck(field,value,unit='',src='',loc='',atol=1e-10):
 expected=float(row[field]); val=float(value)
 checks.append(dict(candidate_id='MS-03',field=field,recomputed=val,retained=expected,absolute_difference=abs(val-expected),atol=atol,pass_check=abs(val-expected)<=atol,unit=unit,source_commit=ARCHIVE if src.startswith('data/') else MAIN,source_path=src,source_locator=loc,target_commit=MAIN,target_path='outputs/research/mars_reselection_20261114/final_candidates.csv',target_row='candidate_id=MS-03'))
ck('lon_east_0_360',(-117.75)%360,'degree','config/raw_inputs_manifest.json','longitude normalization')
ck('north_south_km',math.radians(.5)*3396000/1000,'km',src='outputs/research/mars_reselection_20261114/candidate_native_evidence.json',loc='units_periods_and_support.coordinate_model')
ck('east_west_km',math.radians(.5)*3396000*math.cos(math.radians(57.75))/1000,'km',src='outputs/research/mars_reselection_20261114/candidate_native_evidence.json',loc='units_periods_and_support.coordinate_model')
# Parse original PDS detached labels independently of the repository reader.
def pds(name):
 label=(RAW/(name+'.lbl')).read_text()
 def val(k):return re.search(r'^\s*'+re.escape(k)+r'\s*=\s*(.*)$',label,re.M).group(1).strip().split()[0].strip('"')
 shape=(int(val('LINES')),int(val('LINE_SAMPLES')));bits=int(val('SAMPLE_BITS'))
 dtype={8:'u1',16:'>i2'}[bits]
 arr=np.memmap(RAW/(name+'.img'),mode='r',dtype=dtype,shape=shape)
 ppd=float(val('MAP_RESOLUTION')); north=float(val('MAXIMUM_LATITUDE'));west=float(val('WESTERNMOST_LONGITUDE'))
 lat=north-(np.arange(shape[0])+.5)/ppd;lon=(west+(np.arange(shape[1])+.5)/ppd)%360
 yi=np.where((lat>=57.5)&(lat<58))[0];xi=np.where((lon>=242)&(lon<242.5))[0]
 return arr,lat,lon,yi,xi,label

def stats(prefix,values,lats,src,unit):
 a=np.asarray(values,dtype=float);ok=np.isfinite(a);w=np.broadcast_to(np.cos(np.deg2rad(lats))[:,None],a.shape)
 d={'native_cells':a.size,'valid_cells':ok.sum(),'valid_fraction':ok.mean(),'mean':np.average(a[ok],weights=w[ok]),'median':np.median(a[ok]),'min':a[ok].min(),'max':a[ok].max(),'std_population':a[ok].std()}
 for k,v in d.items(): ck(prefix+'_'+k,v,unit if k not in ['native_cells','valid_cells','valid_fraction'] else 'count' if 'cells' in k else 'fraction',src,'native centres:57.5<=lat<58;242<=lon<242.5')
 return d
mola,lat,lon,yy,xx,label=pds('megt90n000eb')
z=np.asarray(mola[np.ix_(yy,xx)],float)
stats('mola_elevation_m',z,lat[yy],'data/raw/mars/megt90n000eb.img','m above areoid')
ck('mola_relief_m',z.max()-z.min(),'m','data/raw/mars/megt90n000eb.img','max-min of64in-boxnativecentres')
delta=math.radians(1/16)
# Independent explicit centred differences, with one-cell halo; does not invoke analog.terrain.
dy=(np.asarray(mola[np.ix_(yy+1,xx)],float)-np.asarray(mola[np.ix_(yy-1,xx)],float))/(2*3396000*delta)
dx=(np.asarray(mola[np.ix_(yy,xx+1)],float)-np.asarray(mola[np.ix_(yy,xx-1)],float))/(2*3396000*delta*np.cos(np.deg2rad(lat[yy]))[:,None])
slope=np.rad2deg(np.arctan(np.sqrt(dx*dx+dy*dy)))
stats('mola_slope_deg',slope,lat[yy],'data/raw/mars/megt90n000eb.img','degree;centred differencebaseline')
ti,tlat,tlon,ty,tx,_=pds('global_ti_night_2007')
mask,*_=pds('global_ti_msk_night_2007')
values=np.asarray(ti[np.ix_(ty,tx)],float);m=np.asarray(mask[np.ix_(ty,tx)])
values[(values<5)|(values>5000)|(m==0)]=np.nan
stats('TES_TI',values,tlat[ty],'data/raw/mars/global_ti_night_2007.img','J m-2 K-1 s-0.5')
ck('tes_mask_zero_cells',(m==0).sum(),'count','data/raw/mars/global_ti_msk_night_2007.img','100in-boxnativecentres')
for fname,prefix in [('SWIM2_c0_1.tif','SWIM_0_1m'),('SWIM2_c1_5.tif','SWIM_1_5m')]:
 with rasterio.open(RAW/fname) as ds:
  info={'crs_wkt':ds.crs.to_wkt(),'transform':list(ds.transform),'width':ds.width,'height':ds.height,'nodata':ds.nodata}
  radius=float(re.search(r'SPHEROID\["[^"]*",\s*([\d.]+)',ds.crs.to_wkt()).group(1))
  lons=((ds.transform.c+(np.arange(ds.width)+.5)*ds.transform.a)*180/(np.pi*radius))%360
  lats=(ds.transform.f+(np.arange(ds.height)+.5)*ds.transform.e)*180/(np.pi*radius)
  sy=np.where((lats>=57.5)&(lats<58))[0];sx=np.where((lons>=242)&(lons<242.5))[0]
  a=ds.read(1,window=rasterio.windows.Window(sx.min(),sy.min(),len(sx),len(sy))).astype(float)
  a[(a==ds.nodata)|(a<-1)|(a>1)]=np.nan
  stats(prefix,a,lats[sy],'data/raw/mars/'+fname,'dimensionlessconsistency')
  ck(prefix+'_positive_cells',(a>0).sum(),'count','data/raw/mars/'+fname,'validvalue>0')
  ck(prefix+'_positive_fraction_of_valid',(a[np.isfinite(a)]>0).mean(),'fraction','data/raw/mars/'+fname,'validvalue>0')
  (OUT/(fname+'.metadata.json')).write_text(json.dumps(info,indent=2)+'\n')
# Independently reselect nearest native cells in original dust/MCS GitHub files.
for my in [34,35]:
 with xr.open_dataset(RAW/f'dustscenario_MY{my}_v2-5.nc') as ds:
  iy=int(abs(ds.latitude-57.75).argmin());ix=int(abs((ds.longitude-242.25+180)%360-180).argmin())
  sub=ds.isel(latitude=iy,longitude=ix);a=np.asarray(sub.cdodtot.values,float);valid=np.isfinite(a)&(a>=0);aa=a[valid]
  vals={'mean_cdodtot':aa.mean(),'p95_cdodtot':np.quantile(aa,.95),'max_cdodtot':aa.max(),'valid_reconstructed_sols':len(aa),'native_cell_lat':float(sub.latitude),'native_cell_lon':float(sub.longitude)}
  for k,v in vals.items():ck(f'dust_my{my}_'+k,v,'dimensionlessorcount/degree','data/raw/mars/'+f'dustscenario_MY{my}_v2-5.nc',f'nearestcelliy={iy};ix={ix};validnonnegative')
with xr.open_dataset(RAW/'MCS_tsurf_corrected.nc') as ds:
 iy=int(abs(ds.Lat-57.75).argmin());ix=int(abs((ds.Lon-242.25+180)%360-180).argmin())
 s=ds.tsurf_correct.sel(MY=slice(29,36)).isel(Lat=iy,Lon=ix)
 night=np.asarray(s.sel(ltst=3).values,float);day=np.asarray(s.sel(ltst=15).values,float)
 night[(night<=0)|~np.isfinite(night)]=np.nan;day[(day<=0)|~np.isfinite(day)]=np.nan
 pair=np.isfinite(day)&np.isfinite(night)
 vals={'valid_day_bins':np.isfinite(day).sum(),'valid_night_bins':np.isfinite(night).sum(),'paired_bins':pair.sum(),'expected_year_season_pairs':day.size,'paired_contrast_median_K':np.median((day-night)[pair]),'native_lat':float(ds.Lat[iy]),'native_lon':float(ds.Lon[ix]),'populated_night_median_K':np.nanmedian(night),'populated_day_median_K':np.nanmedian(day)}
 for k,v in vals.items():ck('MCS_'+k,v,'K/count/degree','data/raw/mars/temperature/mcs_corrected/MCS_tsurf_corrected.nc',f'nearestiy={iy};ix={ix};MY29-36;pairedbyMY,Ls')
pd.DataFrame(checks).to_csv(OUT/'ms03_numeric_checks.csv',index=False)
assert all(x['pass_check'] for x in checks),[x for x in checks if not x['pass_check']]
summary={'checks':len(checks),'passed':sum(x['pass_check'] for x in checks),'main':MAIN,'raw_source_commit':ARCHIVE,'raw_originals_github_available':len(receipt),'scope':'Only MS-03 native values, coordinate and retained-series checks; no new candidate selection, polygon detection or ice validation','original_global_validation_not_rerun':True}
(OUT/'results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
