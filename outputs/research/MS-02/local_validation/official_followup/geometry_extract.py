import pathlib,json,re,urllib.request,concurrent.futures,csv,hashlib
import numpy as np
P=pathlib.Path(__file__).parent;S=P/'sources';O=P/'derived';d=json.load(open(O/'mrdr4_roi_metadata.json'));a,z=d['rows_0based'];c,e=d['columns_0based'];n,m=1636,1252;id='t1746_mrrde_55n170_0327_4';hdr=(S/(id+'.hdr')).read_text();names=[x.strip()for x in re.search(r'band names = \{(.*?)\}',hdr,re.S).group(1).split(',')];url=d['url'].replace('mrral','mrrde')
def get(k):
 st=(k*n*m+a*m)*4;end=(k*n*m+(z+1)*m)*4-1
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':f'bytes={st}-{end}'}),timeout=50)as r:b=r.read();assert r.status==206 and len(b)==end-st+1
 x=np.frombuffer(b,dtype='<f4').reshape(z-a+1,m)[:,c:e+1].copy();x[(x==65535)|~np.isfinite(x)]=np.nan
 return x,dict(band_1based=k+1,name=names[k],n_valid=int(np.isfinite(x).sum()),min=float(np.nanmin(x)),max=float(np.nanmax(x)),median=float(np.nanmedian(x)),download_sha256=hashlib.sha256(b).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=10)as ex:r=list(ex.map(get,range(19)))
x=np.stack([i[0]for i in r]);np.savez_compressed(O/'mrdr4_geometry_roi.npz',geometry=x,band_names=names)
with(O/'mrdr4_geometry_qc.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=r[0][1]);w.writeheader();w.writerows(i[1]for i in r)
npz=np.load(O/'mrdr4_roi.npz');lat=npz['latitude'][:,None];lon=npz['longitude'][None,:];q=np.isfinite(x[9])&np.isfinite(x[10]);valid=q&(x[9]>=52.5)&(x[9]<=53)&(x[10]>=168)&(x[10]<=168.5)&(x[11]<80)&(x[12]<30)
alb=npz['albedo'];stats=dict(geometry_valid=int(q.sum()),geometry_filter_valid=int(valid.sum()),roi_pixels=int(valid.size),lat_residual_deg_median=float(np.nanmedian(x[9]-lat)),lon_residual_deg_median=float(np.nanmedian(x[10]-lon)),warning='Geometry coordinates are source observation centres; source pixel vs mosaic centre residual includes mapping/resampling. TI and albedo are supporting inputs, not independent mineral/ice evidence.')
with(O/'mrdr4_filtered_spectrum.csv').open('w')as f:
 w=csv.writer(f);w.writerow(['wavelength_nm','valid_after_geometry','median_albedo','negative_after_geometry'])
 for k,wv in enumerate(npz['wavelength_nm']):
  v=alb[k][valid];v=v[np.isfinite(v)];w.writerow([wv,len(v),float(np.median(v))if len(v)else None,int((v<0).sum())])
(O/'mrdr4_geometry_filter.json').write_text(json.dumps(stats,indent=2));print(stats)
