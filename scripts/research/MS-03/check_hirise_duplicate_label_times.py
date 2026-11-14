"""Compare all149duplicate product metadata pairs with public archived labels.
Does not select/correct a timestamp or infer production SQL. Downloads labels only.
"""
from pathlib import Path
import argparse,csv,concurrent.futures,datetime as dt,hashlib,json,re,urllib.request,zipfile
R=Path(__file__).resolve().parents[3];M=R/'outputs/research/MS-03/morphology';O=M/'evidence_followup/generator_followup';O.mkdir(exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--cache-dir',type=Path,required=True);a=p.parse_args();a.cache_dir.mkdir(parents=True,exist_ok=True)
with (M/'evidence_followup/index_anomalies/duplicate_product_audit.csv').open() as f:rows=list(csv.DictReader(f))
assert len(rows)==149

def param(text,name):
 m=re.search(r'^\s*'+re.escape(name)+r'\s*=\s*([^\r\n]+)',text,re.M)
 return m[1].strip().strip('"') if m else None

def fetch(x):
 url='https://hirise-pds.lpl.arizona.edu/PDS/'+x['index_path'].removesuffix('.JP2')+'.LBL';f=a.cache_dir/(x['product_id']+'.LBL');r=dict(product_id=x['product_id'],url=url,index_time1=x['time1'],index_time2=x['time2'],source_line1=x['source_line1'],source_line2=x['source_line2'])
 try:
  if not f.exists():
   with urllib.request.urlopen(url,timeout=25) as response:b=response.read();assert response.status==200
   assert b.startswith(b'PDS_VERSION_ID');f.write_bytes(b)
  b=f.read_bytes();s=b.decode();precise=param(s,'MRO:OBSERVATION_START_TIME');start=param(s,'START_TIME')
  if precise is None:raise ValueError('No MRO:OBSERVATION_START_TIME;do not substitute START_TIME')
  t=dt.datetime.fromisoformat(precise);t1=dt.datetime.fromisoformat(x['time1']);t2=dt.datetime.fromisoformat(x['time2'])
  floor=t.replace(microsecond=0);ceil=floor+(dt.timedelta(seconds=1) if t.microsecond else dt.timedelta())
  both_on_floorceil=t1 in [floor,ceil] and t2 in [floor,ceil]
  r.update(status='read',bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),label_observation_start_time=precise,label_first_line_start_time=start,label_product_creation_time=param(s,'PRODUCT_CREATION_TIME'),index_time1_minus_label_seconds=(t1-t).total_seconds(),index_time2_minus_label_seconds=(t2-t).total_seconds(),both_index_values_floor_or_ceil_of_label=both_on_floorceil,index_times_separation_seconds=abs((t2-t1).total_seconds()),compatible_with_current_label_rounding_not_causal=both_on_floorceil)
 except Exception as e:r.update(status='unavailable',error=str(e))
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 results=[]
 for i,r in enumerate(ex.map(fetch,rows),1):
  results.append(r)
  if i%30==0:print('labels checked',i,flush=True)
fields=list(dict.fromkeys(k for x in results for k in x))
with (O/'duplicate_label_time_comparison.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(results)
with zipfile.ZipFile(O/'duplicate_source_labels.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for x in results:
  if x['status']=='read':z.write(a.cache_dir/(x['product_id']+'.LBL'),x['product_id']+'.LBL')
valid=[x for x in results if x['status']=='read'];summary=dict(date_taipei='2026-11-15',basis_commit='3321765dc0cd24316e7e12d30b4ade803fa67fcd',duplicate_products_requested=149,labels_read=len(valid),unavailable=len(results)-len(valid),pairs_both_floor_or_ceil_of_current_label=sum(x['both_index_values_floor_or_ceil_of_label'] for x in valid),pairs_not_both_floor_or_ceil=sum(not x['both_index_values_floor_or_ceil_of_label'] for x in valid),pairs_over_one_second=sum(x['index_times_separation_seconds']>1 for x in valid),no_timestamp_changed=True,causal_interpretation='Pairwise compatibility with current label rounding is a diagnostic only;does not identify executed2026code,SQL or source of duplicated rows. Do not assume current product-label version equals index-generation input version.',hypothesis_rule='If both values come only from floor/ceil/nearest rounding of one instant to integer seconds,their separation cannot exceed1second. >1second rejects that restricted sole-cause hypothesis;does not rule out rounding as one stage.',zip_sha256=hashlib.sha256((O/'duplicate_source_labels.zip').read_bytes()).hexdigest())
(O/'duplicate_label_time_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
