from acquire_resources import fetch
import urllib.parse
root='https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/mrdr/mc03/'
for typ in ['al','su','de','wv']:
 stem='t1811_mrr'+typ+'_60n243_0327_4'
 for ext in (['lbl','tab'] if typ=='wv' else ['lbl','hdr']):fetch(root+stem+'.'+ext,stem+'.'+ext,max_bytes=2000000)
q=dict(target='mars',ihid='MRO',iid='CRISM',pt='MRDR4',minlat=57.5,maxlat=58,westernlon=242,easternlon=242.5,query='product',results='fmpc',output='JSON',limit=1000)
fetch('https://oderest.rsl.wustl.edu/live2/?'+urllib.parse.urlencode(q),'ode_MRDR4.json')
