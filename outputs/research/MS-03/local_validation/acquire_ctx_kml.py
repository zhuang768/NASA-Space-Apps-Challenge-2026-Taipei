"""Follow only published KML links containing the fixed MS03 centre; no Google/Earth CRS."""
from pathlib import Path
import json,xml.etree.ElementTree as E,urllib.parse
from acquire import fetch,S
N={'k':'http://www.opengis.net/kml/2.2'}
url='https://murray-lab.caltech.edu/CTX/V01/kml/MurrayLab_GlobalCTXMosaic_V01/E-120_E-104_N56_N68/doc.kml'
lon,lat=-117.75,57.75;chain=[]
for i in range(15):
 name=f'ctx_centre_level_{i:02}.kml';r=fetch(url,name)
 if r['status']!='acquired':break
 root=E.fromstring((S/name).read_bytes());links=[]
 for n in root.findall('.//k:NetworkLink',N):
  b=n.find('.//k:LatLonAltBox',N)
  if b is None:continue
  v={x.tag.split('}')[-1]:float(x.text) for x in b if x.tag.split('}')[-1] in ['west','east','north','south']}
  if v['west']<=lon<=v['east'] and v['south']<=lat<=v['north']:
   h=n.find('.//k:href',N).text;links.append(urllib.parse.urljoin(url,h).replace('http:','https:'))
 overlays=[]
 for o in root.findall('.//k:GroundOverlay',N):
  b=o.find('k:LatLonBox',N);h=o.find('k:Icon/k:href',N)
  if b is not None and h is not None:
   v={x.tag.split('}')[-1]:float(x.text) for x in b};overlays.append({'url':urllib.parse.urljoin(url,h.text).replace('http:','https:'),'bounds':v})
 chain.append({'url':url,'source_file':name,'overlays':overlays,'next':links})
 if not links or (overlays and overlays[0]['bounds']['north']-overlays[0]['bounds']['south']<.05):
  if overlays:fetch(overlays[0]['url'],'CTX_mosaic_centre.png')
  break
 url=links[0]
(S.parent/'ctx_kml_chain.json').write_text(json.dumps(chain,indent=2))
