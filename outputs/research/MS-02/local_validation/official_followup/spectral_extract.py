import pathlib,re,json,urllib.request,concurrent.futures,hashlib,csv
import numpy as np
P=pathlib.Path(__file__).parent;S=P/'sources';O=P/'derived';O.mkdir(exist_ok=True)
id='t1746_mrral_55n170_0327_4';label=(S/(id+'.lbl')).read_text();hdr=(S/(id+'.hdr')).read_text()
def val(k):return float(re.search(r'^\s*'+k+r'\s*=\s*([\d.]+)',label,re.M).group(1))
n,m,bands=int(val('LINES')),int(val('LINE_SAMPLES')),int(val('BANDS'));R=val('A_AXIS_RADIUS');sc=val('MAP_SCALE');li=val('LINE_PROJECTION_OFFSET');so=val('SAMPLE_PROJECTION_OFFSET')
y=np.arange(n);x=np.arange(m);lat=np.rad2deg((li-y)*sc/R);lon=170+np.rad2deg((x-so)*sc/(R*np.cos(np.deg2rad(55))));ri=np.where((lat>=52.5)&(lat<=53))[0];ci=np.where((lon>=168)&(lon<=168.5))[0];a,z=ri.min(),ri.max();c,d=ci.min(),ci.max();wv=np.array([float(x)for x in re.search(r'wavelength = \{(.*?)\}',hdr,re.S).group(1).split(',')]);url='https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/mrdr/mc07/'+id+'.img'
def get(k):
 start=(k*n*m+a*m)*4;end=(k*n*m+(z+1)*m)*4-1
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':f'bytes={start}-{end}'}),timeout=60)as r:
  raw=r.read();assert r.status==206 and len(raw)==end-start+1
 arr=np.frombuffer(raw,dtype='<f4').reshape(z-a+1,m)[:,c:d+1].copy();arr[(arr==65535)|(~np.isfinite(arr))]=np.nan
 return arr,dict(band_1based=k+1,wavelength_nm=wv[k],valid_pixels=int(np.isfinite(arr).sum()),roi_pixels=arr.size,negative_pixels=int((arr<0).sum()),median_Lambert_albedo=float(np.nanmedian(arr))if np.isfinite(arr).any()else None,byte_start=start,byte_end=end,download_sha256=hashlib.sha256(raw).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=12)as ex:res=list(ex.map(get,range(bands)))
cube=np.stack([x[0]for x in res]);np.savez_compressed(O/'mrdr4_roi.npz',albedo=cube,latitude=lat[ri],longitude=lon[ci],wavelength_nm=wv)
with(O/'mrdr4_band_qc.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=res[0][1]);w.writeheader();w.writerows(x[1]for x in res)
(O/'mrdr4_roi_metadata.json').write_text(json.dumps(dict(product=id,url=url,rows_0based=[int(a),int(z)],columns_0based=[int(c),int(d)],shape=list(cube.shape),valid_fraction=float(np.isfinite(cube).mean()),caveat='PDS delivered Lambert albedo; numeric coverage is not mineral identification or validated water ice'),indent=2))
print((O/'mrdr4_roi_metadata.json').read_text())
