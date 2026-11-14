"""Resolve legacy strict-longitude flags and count mismatch for pinned HiRISE index.
Uses latitude first to avoid assuming a longitude-wrap fix;does not alter raw index.
"""
from pathlib import Path
import argparse,csv,collections,datetime as dt,hashlib,json,math,re
R=Path(__file__).resolve().parents[3];M=R/'outputs/research/MS-03/morphology';O=M/'evidence_followup/index_anomalies'
p=argparse.ArgumentParser();p.add_argument('--index',type=Path,required=True);a=p.parse_args();O.mkdir(exist_ok=True)
s=(M/'HiRISE_RDRCUMINDEX.LBL').read_text();cols={}
for b in re.findall(r'OBJECT\s*=\s*COLUMN\b(.*?)END_OBJECT',s,re.S):
 n=re.search(r'NAME\s*=\s*(\w+)',b)[1];start=int(re.search(r'START_BYTE\s*=\s*(\d+)',b)[1])-1;size=int(re.search(r'\bBYTES\s*=\s*(\d+)',b)[1]);cols[n]=(start,size)
def get(line,n):start,size=cols[n];return line[start:start+size].decode().strip().strip('"')
def csvout(name,rows):
 with (O/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
groups=collections.defaultdict(list);flagged=[];lat_candidates=[];sha=hashlib.sha256();total=0
with a.index.open('rb') as f:
 for i,line in enumerate(f,1):
  assert len(line)==821;sha.update(line);total+=1;pid=get(line,'PRODUCT_ID');groups[pid].append((i,line))
  lo,hi,west,east=[float(get(line,k)) for k in ['MINIMUM_LATITUDE','MAXIMUM_LATITUDE','MINIMUM_LONGITUDE','MAXIMUM_LONGITUDE']]
  assert all(math.isfinite(v) for v in [lo,hi,west,east]) and -90<=lo<=hi<=90
  overlap=lo<=58 and hi>=57.5
  if overlap:lat_candidates.append((i,line,west,east))
  if not(0<=west<=360 and 0<=east<=360):
   assert west<0 and -180<=west<=east<=360
   flagged.append(dict(product_id=pid,observation_id=get(line,'OBSERVATION_ID'),source_line_1based=i,target=get(line,'TARGET_NAME'),min_lat=lo,max_lat=hi,min_lon_raw=west,max_lon_raw=east,original_flag='strict0to360failed;not missing latitude',category='both_negative_longitudes' if east<0 else 'crosses_zero_raw',lat_overlaps_MS03=overlap,latitude_gap_deg=max(57.5-hi,lo-58,0),resolution='exclude from MS03 by valid latitude alone;no longitude normalization required'))
assert sha.hexdigest()=='d58cf52657371f6a7e65ef4dc687fdd2f9c70e276f7755853e27971f17df4126'
assert len(flagged)==615 and not any(r['lat_overlaps_MS03'] for r in flagged)
# Inspect every latitude-eligible raw row,never truncating at the label ROWS value.
latrows=[]
for i,line,west,east in lat_candidates:
 assert 0<=west<=360 and 0<=east<=360
 overlap=(west<=242.5 and east>=242) if west<=east else (west<=242.5 or east>=242)
 latrows.append(dict(source_line_1based=i,product_id=get(line,'PRODUCT_ID'),min_lat=get(line,'MINIMUM_LATITUDE'),max_lat=get(line,'MAXIMUM_LATITUDE'),min_lon=west,max_lon=east,roi_bbox_overlap=overlap))
assert not any(x['roi_bbox_overlap'] for x in latrows)
duplicates=[];patterns=collections.Counter();deltas=collections.Counter()
for pid,vv in groups.items():
 if len(vv)==1:continue
 assert len(vv)==2
 diff=[n for n in cols if len({get(line,n) for _,line in vv})>1];assert diff==['OBSERVATION_START_TIME'];patterns.update(diff)
 times=[get(line,'OBSERVATION_START_TIME') for _,line in vv];delta=(dt.datetime.fromisoformat(times[1])-dt.datetime.fromisoformat(times[0])).total_seconds();deltas[delta]+=1
 duplicates.append(dict(product_id=pid,source_line1=vv[0][0],source_line2=vv[1][0],changed_fields_json=json.dumps(diff),time1=times[0],time2=times[1],delta_second_minus_first_seconds=delta,spatial_fields_identical=True,file_path_identical=True,index_path=get(vv[0][1],'FILE_NAME_SPECIFICATION')))
assert total-len(groups)==len(duplicates)==149
csvout('negative_longitude_reclassification.csv',flagged);csvout('duplicate_product_audit.csv',duplicates);csvout('latitude_eligible_rows.csv',latrows)
# Read only downloaded label samples;do not infer all615 were individually verified.
label_checks=[]
for label in sorted(O.glob('*RED.LBL')):
 t=label.read_text();vals={}
 for key in ['MINIMUM_LATITUDE','MAXIMUM_LATITUDE','WESTERNMOST_LONGITUDE','EASTERNMOST_LONGITUDE']:
  vals[key]=float(re.search(r'^\s*'+key+r'\s*=\s*([-\d.]+)',t,re.M)[1])
 assert vals['MAXIMUM_LATITUDE']<57.5 or vals['MINIMUM_LATITUDE']>58
 label_checks.append(dict(file=label.name,values=vals,lat_excludes_MS03=True))
result=dict(date_taipei='2026-11-15',starting_commit='115576b51e1a7c89d2d9cd75ae667d4da4ad96c0',source_index_sha256=sha.hexdigest(),physical_rows=total,label_declared_rows=int(re.search(r'\bROWS\s*=\s*(\d+)',s)[1]),unique_product_ids=len(groups),duplicated_product_groups=len(duplicates),extra_rows=total-len(groups),duplicate_changed_fields=dict(patterns),duplicate_observation_start_time_delta_counts={str(k):v for k,v in sorted(deltas.items())},legacy_flagged_rows=len(flagged),negative_longitude_categories=dict(collections.Counter(r['category'] for r in flagged)),flagged_target_counts=dict(collections.Counter(r['target'] for r in flagged)),flagged_latitude_intersections=0,min_flagged_latitude_gap_deg=min(r['latitude_gap_deg'] for r in flagged),all_rows_latitudes_valid=True,latitude_eligible_rows=len(latrows),all_raw_rows_roi_bbox_intersections=0,source_label_samples=label_checks,upstream_duplicate_generation_reason='unknown;count arithmetic and changed fields established,but no producer generation code/explanation acquired',label_count_interpretation='physical ROWS mismatch remains;declared value equals unique IDs,which is not proof of producer counting implementation',decision='These615flags and149extra rows do not hide a bbox match in the actual downloaded index. This does not exclude unreleased/noncatalogued images or erroneous source geometries. AD1 downgrade retained;Mars morphology unknown.',raw_index_modified=False,clock_alignment=False)
(O/'resolution_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['physical_rows','unique_product_ids','duplicated_product_groups','legacy_flagged_rows','flagged_latitude_intersections','latitude_eligible_rows','all_raw_rows_roi_bbox_intersections']},indent=2))
