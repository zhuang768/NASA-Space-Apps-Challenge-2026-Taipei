import urllib.request,pathlib,json,concurrent.futures,hashlib
P=pathlib.Path(__file__).parent;S=P/'sources'
u={'wisdom2026.pdf':json.load(open(S/'wisdom_hal.json'))['response']['docs'][0]['files_s'][0],'dsmap_snu_upper.cat':'https://static.mars.asu.edu/pds/ODTGEO_v2/catalog/DSMAP_SNU.CAT','pathare_mmc1.xlsx':'https://ars.els-cdn.com/content/image/1-s2.0-S0019103517303664-mmc1.xlsx','pathare_mmc2.xlsx':'https://ars.els-cdn.com/content/image/1-s2.0-S0019103517303664-mmc2.xlsx','pathare_mmc1.zip':'https://ars.els-cdn.com/content/image/1-s2.0-S0019103517303664-mmc1.zip','pathare_mmc1.pdf':'https://ars.els-cdn.com/content/image/1-s2.0-S0019103517303664-mmc1.pdf','pathare_elsevier.xml':'https://api.elsevier.com/content/article/PII:S0019103517303664?httpAccept=text/xml'}
def get(it):
 n,u=it;r=dict(file=n,url=u)
 try:
  with urllib.request.urlopen(u,timeout=30)as a:b=a.read();r.update(status=a.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest());(S/n).write_bytes(b)
 except Exception as e:r['error']=str(e)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=7)as ex:r=list(ex.map(get,u.items()))
(P/'retrievals_extra.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
