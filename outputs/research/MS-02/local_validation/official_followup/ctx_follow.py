import urllib.request,urllib.parse,xml.etree.ElementTree as E,pathlib,json
P=pathlib.Path(__file__).parent;S=P/'sources';N={'k':'http://www.opengis.net/kml/2.2'}
urls=['https://murray-lab.caltech.edu/CTX/V01/kml/MurrayLab_GlobalCTXMosaic_V01/doc.kml','https://murray-lab.caltech.edu/CTX/V01/kml/MurrayLab_GlobalCTXMosaic_V01/E160_E176_N44_N56/doc.kml']
chain=[]
for url in urls:
 try:
  b=urllib.request.urlopen(url,timeout=20).read();E.fromstring(b);break
 except Exception as e:print(url,str(e),flush=True)
else:raise SystemExit('no accessible KML')
for i in range(18):
 (S/f'ctx_{i:02}.kml').write_bytes(b);root=E.fromstring(b);links=[];over=[]
 for node in root.findall('.//k:NetworkLink',N):
  box=node.find('.//k:LatLonAltBox',N)
  if box is None:continue
  v={x.tag.split('}')[-1]:float(x.text)for x in box if x.tag.split('}')[-1]in['west','east','north','south']}
  if v['west']<=168.25<=v['east']and v['south']<=52.75<=v['north']:links.append(urllib.parse.urljoin(url,node.find('.//k:href',N).text).replace('http:','https:'))
 for node in root.findall('.//k:GroundOverlay',N):
  box=node.find('k:LatLonBox',N);href=node.find('k:Icon/k:href',N)
  if box is not None and href is not None:over.append(dict(url=urllib.parse.urljoin(url,href.text).replace('http:','https:'),bounds={x.tag.split('}')[-1]:float(x.text)for x in box}))
 chain.append(dict(url=url,overlays=over,next=links));print(i,url,flush=True)
 if not links or(over and over[0]['bounds']['north']-over[0]['bounds']['south']<.05):
  for j,x in enumerate(over):(S/f'ctx_centre_{j}.png').write_bytes(urllib.request.urlopen(x['url'],timeout=25).read())
  break
 url=links[0]
 try:b=urllib.request.urlopen(url,timeout=25).read()
 except Exception as e:chain.append(dict(url=url,error=str(e)));break
(P/'derived/ctx_kml_chain.json').write_text(json.dumps(chain,indent=2))
