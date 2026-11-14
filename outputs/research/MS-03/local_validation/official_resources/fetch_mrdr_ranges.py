from acquire_resources import fetch,O
import json
for x in json.loads((O/'mrdr_extraction_plan.json').read_text())['requests']:
 fetch(x['url'],x['subset_file'],headers={'Range':f"bytes={x['byte_start']}-{x['byte_end']}"},max_bytes=1500000)
