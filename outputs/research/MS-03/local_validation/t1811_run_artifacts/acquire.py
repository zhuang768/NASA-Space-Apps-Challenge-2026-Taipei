"""Bounded public source acquisition; no science array is changed.

Run this script to retry the frozen request_plan.json. Results append to
retrievals.json instead of erasing history; earlier source bytes are preserved.
"""
from pathlib import Path
import urllib.request,datetime,json,hashlib,urllib.parse
O=Path(__file__).resolve().parent;S=O/'sources';S.mkdir(exist_ok=True)
def fetch(url,name,max_bytes=12000000,headers=None):
 row=dict(url=url,file='sources/'+name,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),request_headers=headers or {})
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Team-zasa-MS03-research/1.0',**(headers or {})}),timeout=40) as r:
   final_url=r.url
   if 'X-Amz-' in final_url:
    final_url=final_url.split('?')[0];row['temporary_redirect_query_omitted']=True
   row.update(http_status=r.status,final_url=final_url,content_range=r.headers.get('Content-Range'),content_type=r.headers.get('Content-Type'));b=r.read(max_bytes+1);assert len(b)<=max_bytes,'bounded download exceeded'
  if headers and 'Range' in headers:assert row['http_status']==206 and row['content_range'],'range not honored'
  target=S/name;digest=hashlib.sha256(b).hexdigest()
  if target.exists() and target.read_bytes()!=b:
   target=target.with_name(target.stem+'_'+digest[:12]+target.suffix)
  target.write_bytes(b);row.update(file='sources/'+target.name,status='acquired',bytes=len(b),sha256=digest)
 except Exception as e:row.update(status='not_acquired',error=str(e))
 lp=O/'retrievals.json';a=json.loads(lp.read_text()) if lp.exists() else [];a.append(row);lp.write_text(json.dumps(a,indent=2)+'\n');print(name,row['status'],row.get('bytes'),row.get('error',''),flush=True);return row
if __name__=='__main__':
 for x in json.loads((O/'request_plan.json').read_text()):
  fetch(x['url'],Path(x['file']).name,max_bytes=x.get('max_bytes',3000000))
