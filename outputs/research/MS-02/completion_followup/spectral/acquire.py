"""Try exact public source products with per-request wall-clock and size bounds."""
from pathlib import Path
import urllib.request, datetime, hashlib, json, signal
P=Path(__file__).resolve().parent; S=P/'sources';S.mkdir(exist_ok=True)
targets=[
 ('https://pds-geosciences.wustl.edu/mro/mro-m-crism-2-edr-v1/mrocr_0001/cdr/wa/cdr450924300802_wa0300010l_3.lbl','cdr450924300802_wa0300010l_3.lbl',100000),
 ('https://pds-geosciences.wustl.edu/mro/mro-m-crism-2-edr-v1/mrocr_0001/cdr/wa/cdr450924300802_wa0300010l_3.img','cdr450924300802_wa0300010l_3.img',3000000),
 ('https://pds-geosciences.wustl.edu/mro/mro-m-crism-3-rdr-targeted-v1/mrocr_2104/trdr/2010/2010_008/msp0001565d/msp0001565d_01_if213l_trr3.img','msp0001565d_01_if213l_trr3.img',13000000),
 ('https://pds-geosciences.wustl.edu/mro/mro-m-crism-6-ddr-v1/mrocr_1002/ddr/2010/2010_008/msp0001565d/msp0001565d_01_de213l_ddr1.img','msp0001565d_01_de213l_ddr1.img',4000000)]
def alarm(*args):raise TimeoutError('wall-clock budget12s reached')
signal.signal(signal.SIGALRM,alarm)
receipts=[]
for url,name,bound in targets:
 row=dict(url=url,file='sources/'+name,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),request_timeout_s=8,wall_budget_s=12)
 try:
  signal.alarm(12)
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Team-zasa-MS02-research/1.0'}),timeout=8) as r:
   row.update(http_status=r.status,content_type=r.headers.get('Content-Type'),last_modified=r.headers.get('Last-Modified'))
   b=r.read(bound+1)
  if len(b)>bound:raise ValueError('response exceeded size bound')
  (S/name).write_bytes(b)
  row.update(status='acquired',bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:row.update(status='not_acquired',error=str(e))
 finally:signal.alarm(0)
 receipts.append(row);print(name,row['status'],row.get('error',''),flush=True)
 (P/'retrievals.json').write_text(json.dumps(receipts,indent=2)+'\n')
