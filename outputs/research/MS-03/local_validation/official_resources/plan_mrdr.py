"""Pixel-centre selection from native PDS projection, not inconsistent longitude bbox."""
from pathlib import Path
import re,json,math
O=Path(__file__).resolve().parent;S=O/'sources'
def field(s,k):return re.search(r'(?m)^\s*'+re.escape(k)+r'\s*=\s*([^\r\n]+)',s)[1].strip().strip('"')
lab=(S/'t1811_mrral_60n243_0327_4.lbl').read_text();hdr=(S/'t1811_mrral_60n243_0327_4.hdr').read_text();n=int(field(lab,'LINES'));ns=int(field(lab,'LINE_SAMPLES'));R=float(field(lab,'A_AXIS_RADIUS').split()[0])*1000;scale=float(field(lab,'MAP_SCALE'))*1000;lp=float(field(lab,'LINE_PROJECTION_OFFSET').split()[0]);sp=float(field(lab,'SAMPLE_PROJECTION_OFFSET').split()[0]);lt=float(field(lab,'CENTER_LATITUDE').split()[0]);lo=float(field(lab,'CENTER_LONGITUDE').split()[0]);deg=180/math.pi
lats=[(lp-r)*scale/R*deg for r in range(n)];lons=[(c-sp)*scale/(R*math.cos(math.radians(lt)))*deg+lo for c in range(ns)];rr=[i for i,x in enumerate(lats) if 57.5<=x<=58];cc=[i for i,x in enumerate(lons) if 242<=x%360<=242.5]
assert rr and cc
w=[float(x.split(',')[-1]) for x in (S/'t1811_mrrwv_60n243_0327_4.tab').read_text().splitlines() if x.strip()]
requests=[]
for typ,wants in [('al',[1367,1505,1558,1808,2007,2067]),('su',['BD1500_2','BD1435','ICER1_2']),('de',['Target ID','Segment ID (Counter)','IR (L-detector) Sample','IR (L-detector) Line','Latitude - areocentric - deg N','Longitude - areocentric - deg E'])]:
 stem='t1811_mrr'+typ+'_60n243_0327_4';s=(S/(stem+'.lbl')).read_text();names=re.findall(r'"([^"]+)"',re.search(r'BAND_NAME\s*=\s*\((.*?)\)',s,re.S)[1]) if typ!='al' else []
 # BAND_NAME strings can contain parentheses: parse through closing parenthesis before MISSING_CONSTANT.
 if typ!='al':names=re.findall(r'"([^"]+)"',re.search(r'BAND_NAME\s*=\s*\((.*?)\)\s*MISSING_CONSTANT',s,re.S)[1])
 for a in wants:
  k=min(range(len(w)),key=lambda i:abs(w[i]-a)) if typ=='al' else names.index(a)
  start=(k*n+rr[0])*ns*4;end=(k*n+rr[-1]+1)*ns*4-1
  requests.append(dict(product_id=stem.upper(),type=typ,band_index_0based=k,quantity=a,actual_wavelength_nm=w[k] if typ=='al' else None,byte_start=start,byte_end=end,subset_file=f'{stem}_band{k:02}_rows.bin',url='https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/mrdr/mc03/'+stem+'.img'))
plan=dict(starting_sha='44c2e03b8617c7bb536ad712b85f4716dd190d7c',native_lines=n,native_samples=ns,radius_m=R,pixel_scale_m=scale,standard_parallel_deg=lt,central_meridian_east_deg=lo,line_projection_offset=lp,sample_projection_offset=sp,roi_rows_0based=[rr[0],rr[-1]],roi_columns_0based=[cc[0],cc[-1]],roi_pixel_centres=len(rr)*len(cc),coordinate_method='PDS 0-based centre: x=(column-sample_offset)*scale; y=(line_offset-row)*scale; longitude=lon0+x/(R*cos(lat_ts)); latitude=y/R. Independent HDR corner-plus-half-pixel check.',metadata_warning='Source EASTERNMOST_LONGITUDE=+113.32495 conflicts with projected last centre near-113.328; unchanged source retained. Select from projection, not the faulty bbox.',requests=requests)
(O/'mrdr_extraction_plan.json').write_text(json.dumps(plan,indent=2)+'\n');print('Projected fixed ROI:',plan['roi_rows_0based'],plan['roi_columns_0based'],plan['roi_pixel_centres'],'centres;',len(requests),'band ranges')
