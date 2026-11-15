#!/usr/bin/env python3
"""Read the USGS 79-feature DBF/SHP without GIS dependencies; select exact ID.
Usage: python3 recompute_gis.py INPUT_ROOT OUTPUT_DIR
Only supports public release's PolyLine/PolyLineZ geometry. CRS: EPSG:32628.
"""
from pathlib import Path
import struct,json,sys,math,hashlib
B=Path(sys.argv[1]);O=Path(sys.argv[2]);O.mkdir(parents=True,exist_ok=True)
p=B/'GPR_Locations_2019_2021_shp/GPR_Locations_2019_2021_Askja_Vikrahraun'
b=p.with_suffix('.dbf').read_bytes();n=struct.unpack_from('<I',b,4)[0];h,rs=struct.unpack_from('<HH',b,8);fields=[];k=32
while b[k]!=13:
 x=b[k:k+32];fields.append((x[:11].split(b'\0')[0].decode(),chr(x[11]),x[16]));k+=32
s=p.with_suffix('.shp').read_bytes();shapes=[];k=100
while k<len(s):
 ix,ln=struct.unpack_from('>II',s,k);z=s[k+8:k+8+2*ln];st=struct.unpack_from('<I',z,0)[0]
 assert st in [3,13]
 np,nv=struct.unpack_from('<II',z,36);parts=[struct.unpack_from('<I',z,44+4*j)[0] for j in range(np)]+[nv];pts=[struct.unpack_from('<dd',z,44+4*np+16*j) for j in range(nv)];shapes.append((parts,pts));k+=8+2*ln
out=[]
assert len(shapes)==n
for i in range(n):
 rec=b[h+i*rs:h+(i+1)*rs];offset=1;r={}
 for name,typ,le in fields:r[name]=rec[offset:offset+le].decode(errors='replace').strip();offset+=le
 if r.get('GPR_ID')=='ICE192__030':
  parts,pts=shapes[i];length=sum(math.dist(pts[j],pts[j+1]) for a,e in zip(parts,parts[1:]) for j in range(a,e-1))
  out.append(dict(record_zero_based=i,attributes=r,crs='EPSG:32628',vertex_count=len(pts),length_m=length,parts=parts,points=pts,control_points='NA: cannot identify B7 from line geometry alone',borehole_registration_rmse_m='NA',tolerance_m='NA'))
assert len(out)==1
(O/'gis_exact_ID_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
