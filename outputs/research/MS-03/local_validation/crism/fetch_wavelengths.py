from acquire_crism import fetch,O,S
import json
for p in json.loads((O/'extraction_plan.json').read_text()):
 a=json.loads((S/(p['product_id']+'_WA_ode.json')).read_text())['ODEResults']['Products']['Product']
 for f in a['Product_files']['Product_file']:
  fetch(f['URL'],f['FileName'].lower(),max_bytes=3000000)
# Formal product-specific quality fields are in the TRDR index; acquire the accompanying HK labels only if needed later.
