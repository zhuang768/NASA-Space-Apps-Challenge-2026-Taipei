"""Five predeclared in-cell samples from author KML; cache shared ancestors."""
from pathlib import Path
import json,xml.etree.ElementTree as E,urllib.parse
from acquire import fetch,S,LOG
N={'k':'http://www.opengis.net/kml/2.2'}
rooturl='https://murray-lab.caltech.edu/CTX/V01/kml/MurrayLab_GlobalCTXMosaic_V01/E-120_E-104_N56_N68/doc.kml'
points=[('C',-117.75,57.75),('NW',-117.875,57.875),('NE',-117.625,57.875),('SW',-117.875,57.625),('SE',-117.625,57.625)]
cache={r['url']:r['file'].removeprefix('sources/') for r in json.loads(LOG.read_text()) if r['status']=='acquired' and r['file'].endswith('.kml')};samples=[]
for key,lon,lat in points:
 url=rooturl;chain=[]
 for level in range(15):
  name=cache.get(url,f'CTX_{key}_kml_{level:02}.kml')
  if url not in cache:
   r=fetch(url,name)
   if r['status']!='acquired':break
   cache[url]=name
  root=E.fromstring((S/name).read_bytes());links=[];over=[]
  for node in root.findall('.//k:NetworkLink',N):
   b=node.find('.//k:LatLonAltBox',N)
   if b is None:continue
   v={x.tag.split('}')[-1]:float(x.text) for x in b if x.tag.split('}')[-1] in ['west','east','north','south']}
   if v['west']<=lon<=v['east'] and v['south']<=lat<=v['north']:
    links.append(urllib.parse.urljoin(url,node.find('.//k:href',N).text).replace('http:','https:'))
  for node in root.findall('.//k:GroundOverlay',N):
   b=node.find('k:LatLonBox',N);h=node.find('k:Icon/k:href',N)
   if b is not None and h is not None:over.append({'url':urllib.parse.urljoin(url,h.text).replace('http:','https:'),'bounds':{x.tag.split('}')[-1]:float(x.text) for x in b}})
  chain.append({'url':url,'source_file':name})
  if over and over[0]['bounds']['north']-over[0]['bounds']['south']<.025:
   image=f'CTX_sample_{key}.png';r=fetch(over[0]['url'],image)
   samples.append({'sample_id':key,'selection':'fixed centre and four quadrant centres, before pixel inspection','anchor_lon_east_180':lon,'anchor_lat_planetocentric':lat,'overlay':over[0],'image_file':'sources/'+image,'acquired':r['status']=='acquired','chain':chain});break
  if not links:break
  url=links[0]
(S.parent/'ctx_sample_manifest.json').write_text(json.dumps({'points_predeclared':points,'native_mosaic_m':5,'warning':'Web KML rendering with processing/registration; source CTX ~6 m. Display grid does not add information. Five partial patches, no whole-cell pixel-quality claim.','samples':samples},indent=2))
