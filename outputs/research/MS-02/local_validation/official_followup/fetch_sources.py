import urllib.request,urllib.parse,json,pathlib,hashlib,concurrent.futures,datetime
P=pathlib.Path(__file__).parent;S=P/'sources';S.mkdir(exist_ok=True)
queries={
'ctx_tile.html':'https://murray-lab.caltech.edu/CTX/V01/TilePages/E168_N52.html',
'swim2.html':'https://swim.psi.edu/SWIM2Products.php',
'crism_sis.htm':'https://pds-geosciences.wustl.edu/mro/mro-m-crism-2-edr-v1/mrocr_0001/document/crism_dpsis.htm',
'competition.html':'https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources',
'brighi_thesis.json':'https://api.archives-ouvertes.fr/search/?q=authFullName_t:%22Emile%20Brighi%22&fl=title_s,fileMain_s,uri_s,docType_s&rows=100&wt=json',
'ns_grs.html':'https://pds-geosciences.wustl.edu/missions/odyssey/grs.html'}
for inst,host,typ in [('CRISM','MRO','TRDR'),('CRISM','MRO','MRDR4'),('CRISM','MRO','VRDR'),('THEMIS','ODY','IRPBT2')]:
 q=dict(target='mars',ihid=host,iid=inst,pt=typ,query='PRODUCT',results='FMPC',output='JSON',westernlon=168,easternlon=168.5,minlat=52.5,maxlat=53,limit=1000)
 queries[inst+'_'+typ+'.json']='https://oderest.rsl.wustl.edu/live2/?'+urllib.parse.urlencode(q)
def get(item):
 name,url=item;out=dict(file=name,url=url,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  r=urllib.request.urlopen(url,timeout=25);b=r.read();(S/name).write_bytes(b);out.update(status=r.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:out['error']=str(e)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as ex:
 logs=list(ex.map(get,queries.items()))
for x in logs:print(x,flush=True)
(P/'retrievals_initial.json').write_text(json.dumps(logs,indent=2))
