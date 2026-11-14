"""Bounded public source acquisition; no science array is changed.

The frozen request_plan.json includes unsuccessful attempts. Run --replay-plan
to retry that plan; results append to retrievals.json instead of erasing history.
"""
from pathlib import Path
import urllib.request,datetime,json,hashlib,urllib.parse
O=Path(__file__).resolve().parent;S=O/'sources';S.mkdir(exist_ok=True)
def fetch(url,name,max_bytes=12000000,headers=None):
 row=dict(url=url,file='sources/'+name,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),request_headers=headers or {})
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Team-zasa-MS03-research/1.0',**(headers or {})}),timeout=40) as r:
   row.update(http_status=r.status,final_url=r.url,content_range=r.headers.get('Content-Range'),content_type=r.headers.get('Content-Type'));b=r.read(max_bytes+1);assert len(b)<=max_bytes,'bounded download exceeded'
  if headers and 'Range' in headers:assert row['http_status']==206 and row['content_range'],'range not honored'
  target=S/name;digest=hashlib.sha256(b).hexdigest()
  if target.exists() and target.read_bytes()!=b:
   target=target.with_name(target.stem+'_'+digest[:12]+target.suffix)
  target.write_bytes(b);row.update(file='sources/'+target.name,status='acquired',bytes=len(b),sha256=digest)
 except Exception as e:row.update(status='not_acquired',error=str(e))
 lp=O/'retrievals.json';a=json.loads(lp.read_text()) if lp.exists() else [];a.append(row);lp.write_text(json.dumps(a,indent=2)+'\n');print(name,row['status'],row.get('bytes'),row.get('error',''),flush=True);return row
if __name__=='__main__':
 import urllib.parse,sys
 if '--replay-plan' in sys.argv:
  for x in json.loads((O/'request_plan.json').read_text()):
   fetch(x['url'],Path(x['file']).name,max_bytes=x['max_bytes'])
  raise SystemExit
 root='https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/'
 for path,name in [('document/crism_dpsis.htm','official_dpsis.htm'),('aareadme.txt','volume_aareadme.txt'),('mrdr/mc03/t1811_mrral_60n243_0327_4.xml','T1811_AL_PDS4.xml'),('mrdr/mc03/t1811_mrrsu_60n243_0327_4.xml','T1811_SU_PDS4.xml')]:fetch(root+path,name,max_bytes=4500000)
 fetch('https://www.hou.usra.edu/meetings/lpsc2022/pdf/2361.pdf','author_lpsc2022_2361.pdf',max_bytes=3000000)
 url='https://web.archive.org/cdx/search/cdx?'+urllib.parse.urlencode({'url':root+'document/crism_dpsis.htm','from':'2022','to':'2023','output':'json','filter':'statuscode:200','collapse':'timestamp:4'})
 fetch(url,'wayback_dpsis_2022_2023.json',max_bytes=2000000)
 fetch('https://crism.jhuapl.edu/','author_crism_home.html',max_bytes=2500000)
