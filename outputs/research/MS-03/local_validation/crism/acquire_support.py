from acquire_crism import fetch,O,S
import json,urllib.parse
for pid in ['hsp0002de65_03_de218l_ddr1','msp00018fda_01_de214l_ddr1']:
 url='https://oderest.rsl.wustl.edu/live2/?'+urllib.parse.urlencode(dict(target='mars',query='product',pdsid=pid,results='fmpc',output='JSON'))
 r=fetch(url,pid+'_ode.json')
 if r['status']!='acquired':continue
 a=json.loads((S/(pid+'_ode.json')).read_text());print(str(a)[:300])
 try:products=a['ODEResults']['Products']['Product'];products=products if isinstance(products,list) else [products]
 except KeyError:continue
 for x in products:
  for f in x['Product_files']['Product_file']:
   if f['FileName'].lower().endswith(('.lbl','.img')):fetch(f['URL'],f['FileName'].lower(),max_bytes=25000000)
fetch('https://pds-geosciences.wustl.edu/mro/mro-m-crism-3-rdr-targeted-v1/mrocr_2108/cdr/','cdr_directory.html',max_bytes=3000000)
