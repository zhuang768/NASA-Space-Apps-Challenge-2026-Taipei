from acquire import fetch,O
import json
P=O.parent/'official_resources';p=json.loads((P/'mrdr_extraction_plan.json').read_text());r0,r1=p['roi_rows_0based'];c0,c1=p['roi_columns_0based'];requests=[]
for r,c in [(r0,c0),((r0+r1)//2,(c0+c1)//2),(r1,c1)]:
 for typ,qty in [('su','BD1500_2'),('al',1505)]:
  x=next(x for x in p['requests'] if x['type']==typ and x['quantity']==qty);offset=(x['band_index_0based']*p['native_lines']*p['native_samples']+r*p['native_samples']+c)*4;name=f'point_{typ}_r{r}_c{c}.bin';fetch(x['url'],name,max_bytes=4,headers={'Range':f'bytes={offset}-{offset+3}'});requests.append(dict(original_product=x['product_id'],original_url=x['url'],map_row_0based=r,map_col_0based=c,original_byte_offset=offset,source_band=x['band_index_0based'],file='sources/'+name,compare_range_file='../official_resources/sources/'+x['subset_file']))
(O/'point_checks.json').write_text(json.dumps(requests,indent=2)+'\n')
fetch('https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/document/','production_document_directory.html',max_bytes=2000000)
