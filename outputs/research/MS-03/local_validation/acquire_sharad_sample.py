"""Bounded RDR geometry/record acquisition, NOT radar ice interpretation."""
import json,struct,math,hashlib
from pathlib import Path
from acquire import fetch,S
O=S.parent
pid='R_1768301_001_SS19_700_A'; url='https://pds-geosciences.wustl.edu/mro/mro-m-sharad-4-rdr-v1/MROSH_1001/data/rdr17xxx/rdr1768301/r_1768301_001_ss19_700_a.dat'
rowbytes=5822;nrows=150892
# Byte offsets validated from the acquired original RDR.FMT (PDS start bytes are one-based).
fmt=(S/'SHARAD_RDR.FMT').read_text();assert 'SUB_SC_PLANETOCENTRIC_LATITUDE' in fmt
checks=[]
def readrow(i):
 name=f'SHARAD_bisect_row_{i:06}.bin';start=i*rowbytes
 r=fetch(url,name,{'Range':f'bytes={start}-{start+rowbytes-1}','Cache-Control':'no-cache'},max_bytes=100000)
 assert r['status']=='acquired' and r['http_status']==206 and r['content_range'].startswith(f'bytes {start}-{start+rowbytes-1}/'),r
 b=(S/name).read_bytes();assert len(b)==rowbytes
 lon,lat=struct.unpack_from('<dd',b,5637);epoch=b[5570:5593].decode('ascii').strip()
 assert 0<=lon<=360 and -90<=lat<=90 and epoch.startswith('2010-')
 checks.append({'row_0based':i,'lon_east':lon,'lat_planetocentric':lat,'geometry_epoch':epoch,'source_range':r['content_range'],'sha256':r['sha256']})
 return lat
lo,hi=0,nrows-1
assert readrow(lo)>57.75>readrow(hi)
while hi-lo>1:
 mid=(lo+hi)//2
 if readrow(mid)>57.75:lo=mid
 else:hi=mid
centre=hi;startrow=centre-128;stoprow=centre+127;start=startrow*rowbytes;end=(stoprow+1)*rowbytes-1
r=fetch(url,'SHARAD_local_records.bin',{'Range':f'bytes={start}-{end}','Cache-Control':'no-cache'},max_bytes=2000000)
assert r['status']=='acquired' and r['http_status']==206 and r['content_range'].startswith(f'bytes {start}-{end}/'),r
b=(S/'SHARAD_local_records.bin').read_bytes();assert len(b)==256*rowbytes
rows=[]
for k in range(256):
 record=b[k*rowbytes:(k+1)*rowbytes];lon,lat=struct.unpack_from('<dd',record,5637)
 rows.append({'record_0based':startrow+k,'longitude_east_deg':lon,'latitude_planetocentric_deg':lat,'geometry_epoch_utc':record[5570:5593].decode().strip(),'inside_fixed_roi':242<=lon<=242.5 and 57.5<=lat<=58,'instrument_status_qa':'not evaluated','ice_reflector_identified':'unknown'})
import csv
with (O/'sharad_local_geometry.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
(O/'sharad_sample_qa.json').write_text(json.dumps({'product_id':pid,'source_url':url,'label':'sources/SHARAD_'+pid+'.LBL','format':'sources/SHARAD_RDR.FMT','row_bytes':rowbytes,'records_total':nrows,'binary_search_checks':checks,'sample_start_row':startrow,'sample_stop_row':stoprow,'sample_record_count':256,'sample_inside_roi':sum(r['inside_fixed_roi'] for r in rows),'coordinate_method':'little-endian 8-byte PC_REAL: SUB_SC_EAST_LONGITUDE at5638; SUB_SC_PLANETOCENTRIC_LATITUDE at5646; one-based byte labels','coordinate_convention':'IAU2000 planetocentric, east-positive sub-spacecraft points; NOT radar beam footprint','limits':['Geometry only validated; processed echoes retained without reflector picking or detection.','No clutter simulation, dielectric inversion, waveform QA, depth or ice content inference.','Bisection checks observed descending coordinates; no assumption of complete other-track coverage.']},indent=2))
print('Validated in-cell RDR rows',sum(r['inside_fixed_roi'] for r in rows),'of256')
