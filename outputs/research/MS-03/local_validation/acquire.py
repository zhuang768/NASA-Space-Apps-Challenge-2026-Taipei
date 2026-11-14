"""Bounded public-source acquisition. Failures are evidence of access, not absence."""
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,urllib.error,urllib.parse,json,hashlib,sys
O=Path(__file__).resolve().parent;S=O/'sources';S.mkdir(exist_ok=True)
LOG=O/'retrievals.json'
def fetch(url,name,headers=None,max_bytes=12000000):
 row={'retrieved_utc':datetime.now(timezone.utc).isoformat(),'url':url,'file':'sources/'+name,'request_headers':headers or {}}
 try:
  q=urllib.request.Request(url,headers={'User-Agent':'Team-zasa-MS03-public-research/1.0',**(headers or {})})
  with urllib.request.urlopen(q,timeout=25) as r:
   row.update(http_status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),content_range=r.headers.get('Content-Range'),last_modified=r.headers.get('Last-Modified'))
   b=r.read(max_bytes+1)
   if len(b)>max_bytes:raise ValueError('response exceeds bounded byte budget; not retained')
  (S/name).write_bytes(b);row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),status='acquired')
 except Exception as e:row.update(status='not_acquired',error=str(e))
 rows=json.loads(LOG.read_text()) if LOG.exists() else [];rows.append(row);LOG.write_text(json.dumps(rows,indent=2)+'\n')
 print(name,row['status'],row.get('http_status'),row.get('bytes'),row.get('error',''),flush=True)
 return row
if __name__=='__main__':fetch(sys.argv[1],sys.argv[2])
