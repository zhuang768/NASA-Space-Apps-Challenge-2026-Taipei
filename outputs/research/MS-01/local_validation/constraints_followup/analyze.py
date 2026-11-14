"""Bounded material, same-location thermal sampling and radar/clutter QC.
Run: python analyze.py --raw-dir /tmp/ms01_constraints
No ice classifier, thermal inversion or depth transfer is performed.
"""
from pathlib import Path
import argparse,csv,gzip,hashlib,json,re,itertools
import numpy as np
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--raw-dir',type=Path,required=True);a=p.parse_args();raw=a.raw_dir
def dump(n,x):(HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def csvout(n,rows):
 with (HERE/n).open('w',newline='') as f:
  w=csv.DictWriter(f,list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def get(s,k):return re.search(r'^\s*'+re.escape(k)+r'\s*=\s*(.*?)\s*$',s,re.M)[1].strip().strip('"')
# Same requested geographic coordinates in every scene; not a registration test.
lat1=np.arange(56.5025,57,.005);lon1=np.arange(72.5045,73,.009)
lon,lat=np.meshgrid(lon1,lat1);vals=[];metadata=[]
for f in sorted(raw.glob('I*PBT.IMG')):
 b=f.read_bytes();s=b[:16384].decode('ascii','replace');n=int(get(s,'LINES'));m=int(get(s,'LINE_SAMPLES'));off=(int(get(s,'^IMAGE'))-1)*int(get(s,'RECORD_BYTES'))
 assert len(b)-off==n*m*4 and hashlib.md5(b[off:]).hexdigest()==get(s,'MD5_CHECKSUM')
 z=np.frombuffer(b,dtype='<f4',offset=off).reshape(n,m);R=float(get(s,'A_AXIS_RADIUS'));scale=float(get(s,'MAP_SCALE'));spo=float(get(s,'SAMPLE_PROJECTION_OFFSET'));lpo=float(get(s,'LINE_PROJECTION_OFFSET'));l0=float(get(s,'CENTER_LONGITUDE'));proj=get(s,'MAP_PROJECTION_TYPE')
 dl=np.radians(((lon-l0+180)%360)-180);phi=np.radians(lat)
 if proj=='SINUSOIDAL':x=R*dl*np.cos(phi);y=R*phi
 elif proj=='POLAR_STEREOGRAPHIC':
  assert float(get(s,'CENTER_LATITUDE'))==90
  rho=2*R*np.tan(np.pi/4-phi/2);x=rho*np.sin(dl);y=-rho*np.cos(dl)
 else:raise ValueError(proj)
 ii=np.rint(lpo-y/scale).astype(int);jj=np.rint(spo+x/scale).astype(int);inside=(ii>=0)&(ii<n)&(jj>=0)&(jj<m);v=np.full(lat.shape,np.nan);v[inside]=z[ii[inside],jj[inside]];v[v==0]=np.nan
 vals.append(v);item=dict(product=f.stem,UTC=get(s,'START_TIME'),Ls_deg=float(get(s,'SOLAR_LONGITUDE')),local_time_h=float(get(s,'LOCAL_TIME')),projection=proj,radius_km=R,scale_km=scale,valid_grid_nodes=int(np.isfinite(v).sum()),total_nodes=v.size,source_sha256=hashlib.sha256(b).hexdigest(),payload_md5=get(s,'MD5_CHECKSUM'),pixel_origin_status='explicit zero-based offset convention;normative CAT unresolved',period_support='label summary,not perROI-pixel LT')
 metadata.append(item)
 (HERE/(f.stem+'_header.lbl')).write_bytes(b[:off])
csvout('thermal_scene_qc.csv',metadata)
pairs=[]
for i,j in itertools.combinations(range(len(vals)),2):
 mask=np.isfinite(vals[i])&np.isfinite(vals[j]);n=int(mask.sum());dlst=abs(metadata[i]['local_time_h']-metadata[j]['local_time_h']);dlst=min(dlst,24-dlst);dls=abs(metadata[i]['Ls_deg']-metadata[j]['Ls_deg']);dls=min(dls,360-dls)
 diff=vals[j][mask]-vals[i][mask]
 pairs.append(dict(scene_A=metadata[i]['product'],scene_B=metadata[j]['product'],common_geographic_nodes=n,delta_LT_h=dlst,delta_Ls_deg=dls,median_B_minus_A_K=float(np.median(diff)) if n else None,p05_K=float(np.quantile(diff,.05)) if n else None,p95_K=float(np.quantile(diff,.95)) if n else None,interpretation='Same requested coordinates only;unequalUTC/Ls/LT/dust/emissivity;no causal ice attribution;projection convention provisional'))
csvout('thermal_pair_support.csv',pairs)
np.savez_compressed(HERE/'thermal_common_grid.npz',latitude_n=lat,longitude_e=lon,brightness_K=np.stack(vals),product=np.array([r['product'] for r in metadata]))
# Albedo: actual four complete rows acquired by HTTP Range. Global map edge
# definition gives 8ppd centre coordinates; one-based projection offset agrees.
al=np.fromfile(raw/'albedo_rows.bin',dtype='<f4').reshape(4,2880);ar=[]
for i in range(4):
 for j in range(2020,2024):
  ar.append(dict(row0=264+i,column0=j,latitude_n=90-(264+i+.5)/8,longitude_e=-180+(j+.5)/8,Lambert_albedo=float(al[i,j]),unit='1',source_url='http://tes.asu.edu/mineral_map/global_albedo_8ppd.img',locator='LBL IMAGE;8ppd;rows264–267cols2020–2023zero-based',period='exactsourceobservationperiodunknown;productcreation2002-10-25',depth='opticalsurface',resolution='0.125degree output;nativeTESsupportdifferent',support='fixedROI16outputcells',limit='Lambertvisiblebolometer0.3–2.9um;notcurrentBondalbedo,dustthickness,k,rho,Cp or ice proof'))
csvout('albedo_roi.csv',ar)
dump('albedo_summary.json',dict(n=16,min=min(x['Lambert_albedo'] for x in ar),max=max(x['Lambert_albedo'] for x in ar),mean=float(np.mean([x['Lambert_albedo'] for x in ar])),input_sha256=hashlib.sha256((raw/'albedo_rows.bin').read_bytes()).hexdigest(),source='http://tes.asu.edu/products/',geometry='90Nedge,-180Eedge;8ppd;pixelcentres;matchesLBLonebasedoffset720.5/1440.5',limits=['Not contemporaryforcing forTHEMIS2015/2018','No cellQA/uncertainty provided in downloadedLBL','Not independent proof ofice;noalbedo-to-temperatureconversion']))
# Source windows: rows1600:3000 of3600, columns1664:1727 label(1based).
r=np.fromfile(raw/'radar_window.bin','<f4').reshape(1400,5210)[:,1663:1727].copy();s=np.fromfile(raw/'sim_window.bin','<f4').reshape(1400,5210)[:,1663:1727].copy()
assert r.shape==s.shape==(1400,64) and np.all(np.isfinite(r)) and np.all(np.isfinite(s)) and np.all(r>=0) and np.all(s>=0)
np.savez_compressed(HERE/'radar_clutter_roi.npz',radar_power=r,combined_simulation=s,row0=np.arange(1600,3000),column1=np.arange(1664,1728))
pr=np.argmax(r,axis=0)+1600;ps=np.argmax(s,axis=0)+1600
csvout('radar_peak_diagnostic.csv',[dict(column1=i+1664,radar_max_row0=int(pr[i]),clutter_max_row0=int(ps[i]),difference_rows=int(pr[i]-ps[i]),scope='strongestsampleinwindow only;not a picked interface or subtraction') for i in range(64)])
dump('radar_qc.json',dict(shape=[1400,64],row0_support=[1600,2999],column1_support=[1664,1727],period_utc='2010-09-30T20:09:47.039–20:09:56.350',coordinates_source='../sharad_actual_geometry_rows.csv',radar_max_row_range=[int(pr.min()),int(pr.max())],clutter_max_row_range=[int(ps.min()),int(ps.max())],peak_row_difference_median=float(np.median(pr-ps)),data_kind='PDSderivedreceivedpower versus independenttopographiccluttersimulation;thisrunQC',radar_full_sha_unknown=True,window_sha256={n:hashlib.sha256((raw/n).read_bytes()).hexdigest() for n in ['radar_window.bin','sim_window.bin']},limits=['Full files not acquired;exactHTTPContent-Range preserved','Different arbitrary power scales;do notsubtractsimulationfromreceivedpower','Ionosphericregistration,offnadirsurface,sidelobes,noise and dielectriclayers remain alternatives','No identifieduniqueicehorizon/noicefractioninversion','SHARAD5–8mtypicalgeologicverticalresolutioncannotdirectlyresolve0.427mcover;not a noice test']))
dump('thermal_method.json',dict(grid_step_lat_deg=.005,grid_step_lon_deg=.009,method='Nearestnativepixelatidenticalrequestedcoordinates;notinterpolationorregistration',projection='Sphere3396.190km;sinusoidal or north-polarstereographic;zero-based offsets sameexplicitconventionaspreviousphase',limits=['Normativepixeloriginnotverified','Gridnodes are not independent observations','PBTbrightness not kinetictemperature','No same-season/LT pair accepted as controlled experiment']))
print(json.dumps(dict(scenes=len(metadata),pairs=len(pairs),albedo_mean=np.mean([x['Lambert_albedo'] for x in ar]),radar_peak_delta_median=np.median(pr-ps)),indent=2))
