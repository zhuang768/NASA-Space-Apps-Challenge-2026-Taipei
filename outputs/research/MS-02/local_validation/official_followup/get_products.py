import json,pathlib,urllib.request,hashlib,concurrent.futures,datetime
P=pathlib.Path(__file__).parent;S=P/'sources';queries={}
for catalog in ['CRISM_MRDR4','CRISM_VRDR']:
 a=json.loads((S/(catalog+'.json')).read_text())['ODEResults']['Products']['Product']
 for x in a:
  if '55n170' not in x['pdsid']:continue
  for f in x.get('Product_files',{}).get('Product_file',[]):
   if f.get('Type')=='Product'and f['FileName'].lower().endswith(('.lbl','.hdr')):queries[f['FileName'].lower()]=(f['URL'],None)
a=json.loads((S/'THEMIS_IRPBT2.json').read_text())['ODEResults']['Products']['Product']
for x in a:
 for f in x.get('Product_files',{}).get('Product_file',[]):
  if f.get('Type')=='Product'and f['FileName'].lower().endswith('.img'):queries[f['FileName'].lower()+'.header']=(f['URL'],'bytes=0-65535')
queries.update({'ctx_tile_retry.html':('https://murray-lab.caltech.edu/CTX/V01/TilePages/E168_N52.html',None),'ctx_index.html':('https://murray-lab.caltech.edu/CTX/',None),'swim2_http.html':('http://swim.psi.edu/SWIM2Products.php',None),'grs_special.html':('https://pds-geosciences.wustl.edu/missions/odyssey/grsspecial.html',None),'brighi_thesis.pdf':('https://theses.hal.science/tel-04953869/document',None),'pathare_paper.pdf':('https://www.psi.edu/wp-content/uploads/Pathare-2018-Driven-by-excess-Climatic-implications-of-new-global-mapping-of-near-surface-water-equivalent-hydrogen-on-Mars.pdf',None)})
def get(item):
 n,(u,rg)=item;o=dict(file=n,url=u,range=rg,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  req=urllib.request.Request(u,headers={'Range':rg}if rg else{});r=urllib.request.urlopen(req,timeout=35);b=r.read();(S/n).write_bytes(b);o.update(status=r.status,content_range=r.headers.get('Content-Range'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:o['error']=str(e)
 return o
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as ex:
 logs=list(ex.map(get,queries.items()))
(P/'retrievals_products.json').write_text(json.dumps(logs,indent=2))
for x in logs:print(x,flush=True)
