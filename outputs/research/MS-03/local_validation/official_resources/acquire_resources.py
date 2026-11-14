"""Bounded public official-resource follow-up; no atmosphere model invented."""
from pathlib import Path
import urllib.request,datetime,json,hashlib,urllib.parse
O=Path(__file__).resolve().parent;S=O/'sources';S.mkdir(exist_ok=True)
def fetch(url,name,max_bytes=12000000,headers=None):
 row=dict(url=url,file='sources/'+name,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),request_headers=headers or {})
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Team-zasa-MS03-research/1.0',**(headers or {})}),timeout=40) as r:
   row.update(http_status=r.status,final_url=r.url,content_range=r.headers.get('Content-Range'),content_type=r.headers.get('Content-Type'));b=r.read(max_bytes+1);assert len(b)<=max_bytes,'bounded download exceeded'
  if headers and 'Range' in headers:assert row['http_status']==206 and row['content_range'],'range not honored'
  (S/name).write_bytes(b);row.update(status='acquired',bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:row.update(status='not_acquired',error=str(e))
 lp=O/'retrievals.json';a=json.loads(lp.read_text()) if lp.exists() else [];a.append(row);lp.write_text(json.dumps(a,indent=2)+'\n');print(name,row['status'],row.get('bytes'),row.get('error',''),flush=True);return row
if __name__=='__main__':
 for name,url in [('challenge_resources.html','https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources'),('challenge.html','https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/'),('pds_home.html','https://pds.nasa.gov/'),('pds_crism.html','https://pds-geosciences.wustl.edu/missions/mro/crism.htm')]:fetch(url,name)
 for pt in ['MRDR','TER','MTRDR']:
  q=dict(target='mars',ihid='MRO',iid='CRISM',pt=pt,minlat=57.5,maxlat=58,westernlon=242,easternlon=242.5,query='product',results='fmpc',output='JSON',limit=1000)
  fetch('https://oderest.rsl.wustl.edu/live2/?'+urllib.parse.urlencode(q),'ode_'+pt+'.json')
