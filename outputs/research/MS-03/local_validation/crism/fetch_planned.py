from acquire_crism import fetch,O,S
import json,urllib.parse
for p in json.loads((O/'extraction_plan.json').read_text()):
 src=next(x for x in json.loads((O/'candidate_products.json').read_text()) if x['pdsid']==p['product_id']);url=next(x['URL'] for x in src['Product_files']['Product_file'] if x['FileName'].lower().endswith('.img'))
 fetch(url,p['product_id']+'_roi_rows.bin',headers={'Range':f"bytes={p['byte_start']}-{p['byte_end']}"})
 fetch(url,p['product_id']+'_rownum.bin',headers={'Range':f"bytes={p['rownum_byte_start']}-{p['rownum_byte_start']+p['bands']*2-1}"})
 q='https://oderest.rsl.wustl.edu/live2/?'+urllib.parse.urlencode(dict(target='mars',query='product',pdsid=p['wavelength_file_label'][:-4],results='fmpc',output='JSON'))
 fetch(q,p['product_id']+'_WA_ode.json')
fetch('https://pds-geosciences.wustl.edu/missions/mro/crism.htm','official_crism_page.html',max_bytes=2000000)
