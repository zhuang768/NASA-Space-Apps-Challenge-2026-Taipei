"""Offline extraction planning from acquired DDR; use fetch_planned.py for network requests."""
from acquire_crism import O,S
import numpy as np,re,json,urllib.parse
plans=[]
for pid in ['hsp0002de65_03_if218l_trr3','msp00018fda_01_if214l_trr3']:
 d=pid.replace('_if','_de').replace('_trr3','_ddr1');lab=(S/(d+'.lbl')).read_text()
 n=int(re.search(r'LINES\s*=\s*(\d+)',lab)[1]);ns=int(re.search(r'LINE_SAMPLES\s*=\s*(\d+)',lab)[1])
 a=np.fromfile(S/(d+'.img'),dtype='<f4').reshape(14,n,ns);lon=np.mod(a[4].astype(np.float64),360);m=np.isfinite(a[3])&np.isfinite(a[4])&(a[3]>=57.5)&(a[3]<=58)&(lon>=242)&(lon<=242.5);rr,cc=np.where(m)
 print(pid,'ROI pixel centres',len(rr),'lines',int(rr.min()),int(rr.max()),flush=True)
 lbl=(S/(pid+'.lbl')).read_text();nb=int(re.search(r'BANDS\s*=\s*(\d+)',lbl)[1]);rowbytes=ns*nb*4;l0=int(rr.min());l1=int(rr.max());start=l0*rowbytes;end=(l1+1)*rowbytes-1
 product=next(x for x in json.loads((O/'candidate_products.json').read_text()) if x['pdsid']==pid);url=next(x['URL'] for x in product['Product_files']['Product_file'] if x['FileName'].lower().endswith('.img'))
 rec=int(re.search(r'RECORD_BYTES\s*=\s*(\d+)',lbl)[1]);ptr=int(re.search(r'\^ROWNUM_TABLE\s*=\s*\("[^"]+",\s*(\d+)',lbl)[1]);rs=(ptr-1)*rec
 wave=re.search(r'MRO:WAVELENGTH_FILE_NAME\s*=\s*"([^"]+)"',lbl)[1]
 plans.append(dict(product_id=pid,ddr_id=d,lines=n,samples=ns,bands=nb,roi_pixel_centres=int(len(rr)),start_line_0based=l0,stop_line_0based=l1,row_bytes=rowbytes,byte_start=start,byte_end=end,rownum_byte_start=rs,wavelength_file_label=wave))
(O/'extraction_plan.json').write_text(json.dumps(plans,indent=2)+'\n')
