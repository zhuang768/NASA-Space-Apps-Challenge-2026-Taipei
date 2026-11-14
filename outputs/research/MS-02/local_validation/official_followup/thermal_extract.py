import pathlib,json,re,urllib.request,concurrent.futures,hashlib,csv
import numpy as np
P=pathlib.Path(__file__).parent;S=P/'sources';O=P/'derived';O.mkdir(exist_ok=True)
products=json.loads((S/'THEMIS_IRPBT2.json').read_text())['ODEResults']['Products']['Product']
def run(p):
 id=p['pdsid'];h=(S/(id.lower()+'.img.header')).read_bytes().split(b'END\r\n')[0].decode('ascii',errors='ignore')
 def val(k):return re.search(r'^\s*'+re.escape(k)+r'\s*=\s*([^\r\n]+)',h,re.M).group(1).strip().strip('"')
 n,m=int(val('LINES')),int(val('LINE_SAMPLES'));off=(int(val('^IMAGE'))-1)*int(val('RECORD_BYTES'));url=next(x['URL']for x in p['Product_files']['Product_file']if x['FileName'].lower().endswith('.img')and x['Type']=='Product')
 # PDS pixel centres: x=(sample-offset-1)*scale; y=(line_offset-line+1)*scale.
 R=float(val('A_AXIS_RADIUS'));sc=float(val('MAP_SCALE'));lo=float(val('CENTER_LONGITUDE'));so=float(val('SAMPLE_PROJECTION_OFFSET'));li=float(val('LINE_PROJECTION_OFFSET'))
 lat=np.arange(52.5005,53,.001);lon=np.arange(168.0005,168.5,.001);lat,lon=np.meshgrid(lat,lon,indexing='ij');row=np.rint(li-R*np.deg2rad(lat)/sc).astype(int);col=np.rint(so+R*np.deg2rad(lon-lo)*np.cos(np.deg2rad(lat))/sc).astype(int);inside=(row>=0)&(row<n)&(col>=0)&(col<m)
 rows=row[inside];a,b=rows.min(),rows.max();start=off+a*m*4;end=off+(b+1)*m*4-1
 req=urllib.request.Request(url,headers={'Range':f'bytes={start}-{end}'})
 with urllib.request.urlopen(req,timeout=60)as r:
  data=r.read();assert r.status==206 and len(data)==end-start+1
 image=np.frombuffer(data,dtype='<f4').reshape(b-a+1,m);out=np.full(lat.shape,np.nan,dtype='f4');out[inside]=image[row[inside]-a,col[inside]];out[(out<=0)|(~np.isfinite(out))]=np.nan
 np.save(O/(id+'.npy'),out);(S/(id+'.roi_rows.bin')).write_bytes(data)
 return dict(product=id,start_time=val('START_TIME'),Ls_deg=val('SOLAR_LONGITUDE'),local_time_h=val('LOCAL_TIME'),incidence_deg=val('INCIDENCE_ANGLE'),valid_grid_cells=int(np.isfinite(out).sum()),grid_cells=out.size,median_K=float(np.nanmedian(out)),min_K=float(np.nanmin(out)),max_K=float(np.nanmax(out)),url=url,byte_start=int(start),byte_end=int(end),sha256=hashlib.sha256(data).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as ex:results=list(ex.map(run,products))
with(O/'thermal_epoch_qc.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=results[0]);w.writeheader();w.writerows(results)
arrays=[np.load(O/(x['product']+'.npy'))for x in results];pairs=[]
for i,a in enumerate(arrays):
 for j in range(i):
  mask=np.isfinite(a)&np.isfinite(arrays[j]);pairs.append(dict(a=results[j]['product'],b=results[i]['product'],common_cells=int(mask.sum()),median_delta_K=float(np.median((a-arrays[j])[mask]))if mask.any()else None,interpretation='brightness temperature difference; Ls/local time/confounders not normalized'))
with(O/'thermal_pairs.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=pairs[0]);w.writeheader();w.writerows(pairs)
print(json.dumps(results,indent=2));print('pairs with overlap',sum(x['common_cells']>0 for x in pairs))
