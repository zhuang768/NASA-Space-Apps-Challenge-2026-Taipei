"""Bounded check of current labels for nearby index candidates,not a complete search.
Select latitude-eligible rows whose bbox also overlaps237..247.5E (5deg margin).
Original MS03ROI unchanged;all source index products/path retained.
"""
from pathlib import Path
import argparse,csv,hashlib,json,re,urllib.request,concurrent.futures
R=Path(__file__).resolve().parents[3];M=R/'outputs/research/MS-03/morphology';O=M/'evidence_followup/index_handoff';O.mkdir(exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--index',type=Path,required=True);a=p.parse_args();source=a.index.read_bytes();assert hashlib.sha256(source).hexdigest()=='d58cf52657371f6a7e65ef4dc687fdd2f9c70e276f7755853e27971f17df4126'
s=(M/'HiRISE_RDRCUMINDEX.LBL').read_text();cols={}
for b in re.findall(r'OBJECT\s*=\s*COLUMN\b(.*?)END_OBJECT',s,re.S):
 n=re.search(r'NAME\s*=\s*(\w+)',b)[1];start=int(re.search(r'START_BYTE\s*=\s*(\d+)',b)[1])-1;size=int(re.search(r'\bBYTES\s*=\s*(\d+)',b)[1]);cols[n]=(start,size)
def get(line,n):start,size=cols[n];return line[start:start+size].decode().strip().strip('"')
selected=[]
for i,line in enumerate(source.splitlines(keepends=True),1):
 lo,hi,west,east=[float(get(line,k)) for k in ['MINIMUM_LATITUDE','MAXIMUM_LATITUDE','MINIMUM_LONGITUDE','MAXIMUM_LONGITUDE']]
 if lo<=58 and hi>=57.5 and 0<=west<=east<=360 and west<=247.5 and east>=237:
  selected.append(dict(source_line_1based=i,product_id=get(line,'PRODUCT_ID'),path=get(line,'FILE_NAME_SPECIFICATION'),index_bbox=[west,lo,east,hi]))
assert len(selected)==10

def fetch(x):
 u='https://hirise-pds.lpl.arizona.edu/PDS/'+x['path'].removesuffix('.JP2')+'.LBL';p=O/(x['product_id']+'.LBL');result=dict(x,url=u)
 try:
  with urllib.request.urlopen(u,timeout=30) as response:b=response.read();status=response.status
  p.write_bytes(b);t=b.decode();v={}
  for k in ['MINIMUM_LATITUDE','MAXIMUM_LATITUDE','WESTERNMOST_LONGITUDE','EASTERNMOST_LONGITUDE']:
   v[k]=float(re.search(r'^\s*'+k+r'\s*=\s*([-\d.]+)',t,re.M)[1])
  lo,hi,west,east=[v[k] for k in ['MINIMUM_LATITUDE','MAXIMUM_LATITUDE','WESTERNMOST_LONGITUDE','EASTERNMOST_LONGITUDE']]
  overlap=lo<=58 and hi>=57.5 and ((west<=242.5 and east>=242) if west<=east else (west<=242.5 or east>=242))
  result.update(status=status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),source_label_bbox=[west,lo,east,hi],source_label_roi_overlap=overlap,source_label_file=p.name)
 except Exception as e:result.update(status='unavailable',error=str(e),source_label_roi_overlap=None)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(fetch,selected))
summary=dict(date='2026-11-15',basis_commit='c6f9b93aa9ff5a471a8f67fbdf40f0922e508b84',source_index_sha256=hashlib.sha256(source).hexdigest(),original_roi=[242,57.5,242.5,58],selection_rule='Index latitude overlaps57.5..58N and non-wrapping longitude bbox overlaps237..247.5E;5degree analyst buffer solely for bounded label crosscheck',selected_products=len(results),observations=len({x['product_id'].rsplit('_',1)[0] for x in results}),downloaded=sum(x['status']==200 for x in results),overlap_true=sum(x['source_label_roi_overlap'] is True for x in results),unavailable=sum(x['source_label_roi_overlap'] is None for x in results),records=results,limits=['Not all205302unique product labels','Not a search of unlisted or unreleased observations','Source labels are metadata,not independent geodetic ground truth','5degree margin is a design sampling rule,not guaranteed maximum geolocation error'])
(O/'neighbour_label_check.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:summary[k] for k in ['selected_products','observations','downloaded','overlap_true','unavailable']},indent=2))
