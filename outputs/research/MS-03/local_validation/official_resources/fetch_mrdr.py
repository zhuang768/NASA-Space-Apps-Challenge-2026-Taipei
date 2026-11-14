from acquire_resources import fetch
root='https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/'
for f in ['mrdr/mc03/','index/index.lbl','index/index.tab','catalog/mrdr_ds.cat','catalog/mrr_polar_map.cat']:
 fetch(root+f,'mrdr_'+f.replace('/','_'),max_bytes=6500000)
