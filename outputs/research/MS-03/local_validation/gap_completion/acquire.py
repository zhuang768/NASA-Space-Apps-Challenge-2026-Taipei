"""Bounded public-source acquisition. Error/landing pages are never scientific data."""
from pathlib import Path
import datetime as dt
import hashlib,json,urllib.request,urllib.error,sys
O=Path(__file__).resolve().parent
S=O/'sources';S.mkdir(exist_ok=True)
def fetch(identifier,url,filename,basis,headers=None,max_bytes=20_000_000):
    row=dict(id=identifier,url=url,file='sources/'+filename,source_basis=basis,retrieved_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Team-zasa-public-research/1.0',**(headers or {})})
        with urllib.request.urlopen(req,timeout=45) as r:
            b=r.read(max_bytes+1);row.update(http_status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),content_range=r.headers.get('Content-Range'))
        if len(b)>max_bytes:row['status']='size_limit_not_retained'
        else:
            (S/filename).write_bytes(b);row.update(status='acquired_response_requires_content_validation',bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    except urllib.error.HTTPError as e:row.update(status='http_error_no_scientific_data',http_status=e.code,error=str(e))
    except Exception as e:row.update(status='transport_error',error=str(e))
    p=O/'retrievals.json';logs=json.loads(p.read_text()) if p.exists() else [];logs.append(row);p.write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
    print(identifier,row.get('http_status'),row.get('bytes'),row['status']);return row
if __name__=='__main__':
    for r in json.loads(Path(sys.argv[1]).read_text()):fetch(**r)
