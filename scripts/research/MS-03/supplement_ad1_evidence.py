"""Check independent mission RDR index and published AD1 rounded statistics.
Full index retained locally only;no claim of complete historical coverage.
Pass --index path to the downloaded table;source label is tracked.
"""
from pathlib import Path
import argparse,csv,hashlib,json,math,re,statistics
R=Path(__file__).resolve().parents[3];M=R/'outputs/research/MS-03/morphology';O=M/'evidence_followup';O.mkdir(exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--index',type=Path,required=True);a=p.parse_args()
label=M/'HiRISE_RDRCUMINDEX.LBL';s=label.read_text();cols={}
for b in re.findall(r'OBJECT\s*=\s*COLUMN\b(.*?)END_OBJECT',s,re.S):
 n=re.search(r'NAME\s*=\s*(\w+)',b)[1];start=int(re.search(r'START_BYTE\s*=\s*(\d+)',b)[1])-1;size=int(re.search(r'\bBYTES\s*=\s*(\d+)',b)[1]);cols[n]=(start,size)
def get(line,n):start,size=cols[n];return line[start:start+size].decode().strip().strip('"')
rows=valid=0;invalid=[];hits=[];prior=[];sha=hashlib.sha256()
with a.index.open('rb') as f:
 for i,line in enumerate(f,1):
  sha.update(line);rows+=1;assert len(line)==821
  lo,hi,west,east=[float(get(line,k)) for k in ['MINIMUM_LATITUDE','MAXIMUM_LATITUDE','MINIMUM_LONGITUDE','MAXIMUM_LONGITUDE']]
  entry={k:get(line,k) for k in ['OBSERVATION_ID','PRODUCT_ID','START_TIME','MINIMUM_LATITUDE','MAXIMUM_LATITUDE','MINIMUM_LONGITUDE','MAXIMUM_LONGITUDE','MAP_SCALE']};entry['source_line_1based']=i
  if entry['OBSERVATION_ID'] in ['PSP_001938_2265','PSP_002439_2265']:prior.append(entry)
  if not all(math.isfinite(x) for x in [lo,hi,west,east]) or not(-90<=lo<=hi<=90 and 0<=west<=360 and 0<=east<=360):invalid.append(entry);continue
  valid+=1;lon_overlap=(west<=242.5 and east>=242) if west<=east else (west<=242.5 or east>=242)
  if lo<=58 and hi>=57.5 and lon_overlap:hits.append(entry)
summary=dict(review_date_taipei='2026-11-15',source_url='https://hirise-pds.lpl.arizona.edu/PDS/INDEX/RDRCUMINDEX.TAB',index_bytes=a.index.stat().st_size,index_sha256=sha.hexdigest(),label_url='https://hirise-pds.lpl.arizona.edu/PDS/INDEX/RDRCUMINDEX.LBL',label_sha256=hashlib.sha256(label.read_bytes()).hexdigest(),label_declared_rows=int(re.search(r'\bROWS\s*=\s*(\d+)',s)[1]),actual_rows=rows,valid_bbox_rows=valid,invalid_bbox_rows=len(invalid),legacy_strict_flag_note='invalid_bbox_rows is failure of first-pass0to360 test,not proof of missing source geolocation;see index_anomalies/resolution_summary.json for followup',roi=[242,57.5,242.5,58],valid_bbox_intersection_count=len(hits),hits=hits,limits=['Only actually downloaded cumulative release;not all observations or future products','Invalid bbox rows not assigned to no-overlap','Label row count differs from actual table;schema821-byte lengths checked for every row but release consistency unresolved','Bounding rectangles used as conservative footprint screening;zero eligible bbox hits does not prove absence of surface features'])
(O/'HiRISE_independent_index_check.json').write_text(json.dumps(summary,indent=2)+'\n')
with (O/'HiRISE_invalid_bbox_rows.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(invalid[0]),lineterminator='\n');w.writeheader();w.writerows(invalid)
assert prior
with (O/'published_Mars_image_index_rows.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(prior[0]),lineterminator='\n');w.writeheader();w.writerows(prior)
# Published table4 rounded entries transcribed from original author PDF printed p204.
# Compare our vector statistics at the printed precision;MRR lengths explicitly excluded.
with (M/'AD1_recomputed_geometry.csv').open() as f:geo=list(csv.DictReader(f))
refs=[('area_m2','min',50.9,1),('area_m2','max',2029.0,1),('area_m2','mean',340.1,1),('area_m2','median',268.4,1),('perimeter_m','min',30.4,1),('perimeter_m','max',177.1,1),('perimeter_m','mean',69.8,1),('perimeter_m','median',65.0,1),('equivalent_circle_diameter_m','min',8.1,1),('equivalent_circle_diameter_m','max',50.8,1),('equivalent_circle_diameter_m','mean',19.7,1),('equivalent_circle_diameter_m','median',18.5,1),('circularity_4piA_over_P2','median',.81,2)]
checks=[]
for metric,stat,expected,precision in refs:
 vals=[float(x[metric]) for x in geo];value={'min':min,'max':max,'mean':statistics.fmean,'median':statistics.median}[stat](vals);ok=round(value,precision)==expected;assert ok,(metric,stat,value,expected)
 checks.append(dict(metric=metric,statistic=stat,recomputed=value,published_table4_AD1=expected,printed_decimals=precision,agreement_at_printed_precision=ok,source_locator='Ulrich et al2011 printed p204 Table4;PDFpage9'))
with (O/'AD1_published_table_crosscheck.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(checks[0]),lineterminator='\n');w.writeheader();w.writerows(checks)
print(f'PASS: {rows} actual index rows;{valid} valid bbox;{len(invalid)} invalid retained;{len(hits)} ROI bbox hits;13 published rounded statistics agree.')
