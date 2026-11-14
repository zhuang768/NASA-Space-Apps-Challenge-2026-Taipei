"""Public PDS requests, bounded size and original byte preservation; no credentials."""
from pathlib import Path
import urllib.request,datetime,json,hashlib
O=Path(__file__).resolve().parent;S=O/'sources';S.mkdir(exist_ok=True)
def fetch(url,name,max_bytes=16000000,headers=None):
 row=dict(url=url,file='sources/'+name,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),request_headers=headers or {})
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Team-zasa-MS03-research/1.0',**(headers or {})}),timeout=45) as r:
   row.update(http_status=r.status,content_range=r.headers.get('Content-Range'),content_type=r.headers.get('Content-Type'),last_modified=r.headers.get('Last-Modified'))
   b=r.read(max_bytes+1)
   if len(b)>max_bytes:raise ValueError('bounded response too large')
  if headers and 'Range' in headers:
   assert row['http_status']==206 and row['content_range'],'requested range not honored'
  (S/name).write_bytes(b);row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),status='acquired')
 except Exception as e:row.update(status='not_acquired',error=str(e))
 p=O/'retrievals.json';a=json.loads(p.read_text()) if p.exists() else [];a.append(row);p.write_text(json.dumps(a,indent=2)+'\n');print(name,row['status'],row.get('bytes'),row.get('error',''),flush=True);return row
if __name__=='__main__':
 import sys
 for pid in ['hsp0002de65_03_if218l_trr3','msp00018fda_01_if214l_trr3']:
  src=next(x for x in json.loads((O/'candidate_products.json').read_text()) if x['pdsid']==pid)
  lbl=next(x['URL'] for x in src['Product_files']['Product_file'] if x['FileName'].endswith('.LBL'))
  fetch(lbl,pid+'.lbl')
 fetch('https://pds-geosciences.wustl.edu/mro/mro-m-crism-3-rdr-targeted-v1/mrocr_2110/document/crism_dpsis.htm','crism_dpsis.htm',max_bytes=6000000)
