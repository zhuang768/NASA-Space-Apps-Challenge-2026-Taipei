import urllib.request,json,pathlib,concurrent.futures,hashlib,math
from PIL import Image
import numpy as np
P=pathlib.Path(__file__).parent;S=P/'sources';O=P/'derived';base='https://astro.arcgis.com/arcgis/rest/services/OnMars/CTX1/MapServer';meta=json.load(open(S/'ctx_esri.json'));res=next(x['resolution']for x in meta['tileInfo']['lods']if x['level']==12);step=512*res
points=[('C',168.25,52.75),('NW',168.125,52.875),('NE',168.375,52.875),('SW',168.125,52.625),('SE',168.375,52.625)]
def get(t):
 key,lon,lat=t;col=math.floor((lon+180)/step);row=math.floor((90-lat)/step);url=f'{base}/tile/12/{row}/{col}'
 b=urllib.request.urlopen(url,timeout=30).read();p=S/f'ctx_{key}_L12.png';p.write_bytes(b);im=Image.open(p);im.load();a=np.array(im.convert('L'));bounds=dict(west=-180+col*step,east=-180+(col+1)*step,north=90-row*step,south=90-(row+1)*step)
 return dict(sample=key,anchor_lon=lon,anchor_lat=lat,url=url,bounds=bounds,sha256=hashlib.sha256(b).hexdigest(),size=list(im.size),min=int(a.min()),max=int(a.max()),std=float(a.std()),deg_per_pixel=res,nominal_m_N_S=3396190*np.pi/180*res,nominal_m_E_W=3396190*np.pi/180*res*np.cos(np.deg2rad(lat)),caveat='Georeferenced Esri beta01 uncontrolled Murray rendering, lossy JPEG source; no proven absolute registration, no whole-ROI morphology or ice claim')
with concurrent.futures.ThreadPoolExecutor(max_workers=5)as ex:r=list(ex.map(get,points))
(O/'ctx_sample_metadata.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
