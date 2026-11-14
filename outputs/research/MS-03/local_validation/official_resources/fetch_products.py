from acquire_resources import fetch,O,S
fetch('https://oderest.rsl.wustl.edu/live2/?query=iipt&target=mars&output=JSON','ode_iipt.json')
root='https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/'
for f in ['mrdr/','index/','aareadme.txt','errata.txt']:
 fetch(root+f,'mrdr_'+f.replace('/','_').replace('.txt','')+'.txt',max_bytes=2000000)
fetch('https://pds-geosciences.wustl.edu/missions/mro/crism_summary_parameter_reference.pdf','crism_summary_parameter_reference.pdf',max_bytes=2000000)
fetch('https://pds-geosciences.wustl.edu/missions/mro/CAT74_release.txt','CAT74_release.txt')
