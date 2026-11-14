"""Acquire bounded public imagery evidence;never download full CTX IMG.
Outputs include API responses, full author browse images, detached HiRISE label,
and an exact byte-range of CTX D01 native EDR rows. No radiometric calibration.
"""
from pathlib import Path
import urllib.request,json,hashlib,gzip
R=Path(__file__).resolve().parents[3];O=R/'outputs/research/MS-03/morphology';O.mkdir(exist_ok=True)
records=[]
def fetch(url,name,headers=None):
 req=urllib.request.Request(url,headers=headers or {})
 with urllib.request.urlopen(req,timeout=60) as response:
  b=response.read();status=response.status;content_range=response.headers.get('Content-Range')
 (O/name).write_bytes(b)
 records.append(dict(path=name,url=url,request_headers=headers or {},http_status=status,content_range=content_range,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 return b
for iid,pt in [('CTX','EDR'),('HIRISE','RDRV11'),('HIRISE','RDR')]:
 url=f'https://oderest.rsl.wustl.edu/live2/?target=mars&query=product&results=fmpc&output=JSON&ihid=MRO&iid={iid}&pt={pt}&minlat=57.5&maxlat=58&westernlon=242&easternlon=242.5&limit=1000'
 fetch(url,f'ode_{iid}_{pt}.json')
products=json.loads((O/'ode_CTX_EDR.json').read_text())['ODEResults']['Products']['Product']
assert len(products)==3 # stop for review if catalogue changes;do not silently change inputs
for p in products:
 f=next(x for x in p['Product_files']['Product_file'] if x['Description']=='BROWSE IMAGE')
 fetch(f['URL'],p['pdsid']+'_browse.jpg')
fetch('https://www.uahirise.org/PSP_006864_2380','hirise_page.html')
fetch('https://hirise-pds.lpl.arizona.edu/PDS/RDR/PSP/ORB_006800_006899/PSP_006864_2380/PSP_006864_2380_RED.LBL','PSP_006864_2380_RED.LBL')
fetch('https://planetarydata.jpl.nasa.gov/img/data/mro/ctx/mrox_1677/index/cumindex.lbl','CTX_cumindex.lbl')
p=next(x for x in products if x['pdsid']=='D01_027566_2370_XN_57N117W')
label=fetch(p['LabelURL'],'D01_label_record.bin',{'Range':'bytes=0-5055'})
assert len(label)==5056
(O/'D01_label.txt').write_bytes(label.split(b'\0')[0])
start=5056*(1+36000);end=5056*(1+37024)-1
b=fetch(p['LabelURL'],'D01_native_rows.bin',{'Range':f'bytes={start}-{end}'})
assert len(b)==5056*1024 and records[-1]['http_status']==206
assert records[-1]['content_range'].startswith(f'bytes {start}-{end}/')
(O/'D01_native_rows.bin.gz').write_bytes(gzip.compress(b,mtime=0));(O/'D01_native_rows.bin').unlink()
records[-1]['path']='D01_native_rows.bin.gz';records[-1]['sha256_uncompressed']=records[-1].pop('sha256');records[-1]['bytes_uncompressed']=records[-1].pop('bytes');records[-1]['sha256']=hashlib.sha256((O/'D01_native_rows.bin.gz').read_bytes()).hexdigest();records[-1]['bytes']=(O/'D01_native_rows.bin.gz').stat().st_size
(O/'acquisition_manifest.json').write_text(json.dumps(dict(start_sha='7b3c865e85ffeb4db81277ef34e9c3f4a318fc9f',review_date_taipei='2026-11-15',files=records,limitations=['ODE catalogue snapshot not completeness guarantee','USGS independent footprint query returned403','native D01 slice uncalibrated SQROOT DN;not orthorectified','native rows selected by approximate index corner locator,not precision camera model']),indent=2)+'\n')
