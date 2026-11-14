"""Read published USGS ZIP central directory and selected vector files via HTTP ranges."""
from pathlib import Path
import io,json,struct,zipfile,urllib.request
from acquire import fetch,S
url='https://pubs.usgs.gov/sim/3292/downloads/sim3292_database.zip'
b=(S/'usgs_geology_zip_eocd.bin').read_bytes();i=b.rfind(b'PK\x05\x06');e=struct.unpack('<4s4H2LH',b[i:i+22]);size,off=e[5:7]
print('central directory',size,off)
r=fetch(url,'usgs_geology_zip_cd.bin',{'Range':f'bytes={off}-{off+size-1}','Accept-Encoding':'identity'})
assert r['http_status']==206
cd=(S/'usgs_geology_zip_cd.bin').read_bytes();q=0;items=[]
while q<len(cd):
 h=struct.unpack('<4s6H3L5H2L',cd[q:q+46]);assert h[0]==b'PK\x01\x02'
 name=cd[q+46:q+46+h[10]].decode('utf-8');items.append({'name':name,'compressed_size':h[8],'uncompressed_size':h[9],'compression':h[4],'local_header_offset':h[16],'crc32':h[7]})
 q+=46+h[10]+h[11]+h[12]
(S/'usgs_geology_zip_members.json').write_text(json.dumps(items,indent=2))
print([(x['name'],x['compressed_size']) for x in items if 'Global_Geology' in x['name']])
# Download only the four necessary shapefile members, never the 809 MB package.
import zlib,hashlib,binascii
for it in items:
 if '/SIM3292_Shapefiles/SIM3292_Global_Geology.' not in it['name']:continue
 ext=it['name'].rsplit('.',1)[-1]
 if ext not in ['shp','shx','dbf','prj']:continue
 off=it['local_header_offset'];bn='usgs_geology_'+ext+'_header.bin'
 r=fetch(url,bn,{'Range':f'bytes={off}-{off+29}','Accept-Encoding':'identity'})
 assert r['http_status']==206
 h=struct.unpack('<4s5H3L2H',(S/bn).read_bytes());assert h[0]==b'PK\x03\x04'
 start=off+30+h[-2]+h[-1];end=start+it['compressed_size']-1
 fn='usgs_geology_'+ext+'_compressed.bin'
 r=fetch(url,fn,{'Range':f'bytes={start}-{end}','Accept-Encoding':'identity'},max_bytes=65000000)
 assert r.get('http_status')==206 and r['status']=='acquired'
 compressed=(S/fn).read_bytes();raw=zlib.decompress(compressed,-15) if it['compression']==8 else compressed
 assert len(raw)==it['uncompressed_size'] and (binascii.crc32(raw)&0xffffffff)==it['crc32']
 (S/('USGS_Global_Geology.'+ext)).write_bytes(raw)
 it.update(acquired_bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),crc32_verified=True)
 print('extracted',ext,len(raw),flush=True)
(S/'usgs_geology_selected_members.json').write_text(json.dumps([it for it in items if 'sha256' in it],indent=2))
