"""Retrieve public source bytes and append auditable request metadata. No credentials."""
import sys, json, hashlib, datetime, urllib.request, urllib.error, urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def fetch(name,url):
    dest=ROOT/'sources'/name; dest.parent.mkdir(parents=True,exist_ok=True)
    row={'name':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'MS02-research/1.0'})
        with urllib.request.urlopen(req,timeout=55) as r:
            data=r.read(); final=r.url
            if 'X-Amz-' in final: final=final.split('?')[0]
            row.update(status=r.status,final_url=final,content_type=r.headers.get('Content-Type'))
        dest.write_bytes(data)
        row.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e: row.update(error=str(e))
    with (ROOT/'acquisition_log.jsonl').open('a') as f: f.write(json.dumps(row,ensure_ascii=False)+'\n')
    print(json.dumps(row,ensure_ascii=False),flush=True)
if __name__=='__main__': fetch(*sys.argv[1:])
