from pathlib import Path
import csv,json
O=Path(__file__).resolve().parent;P=O.parent

def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);return list(r),r.fieldnames

def write(p,a,fields):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(a)
a,f=read(P/'mars_ice_evidence.csv');a=[x for x in a if x['evidence_id']!='LV-ICE12'];x={k:'' for k in f};x.update({k:a[0][k] for k in ['candidate_id','roi','date_checked_taipei']});x.update(evidence_id='LV-ICE12',evidence_type='published_corrected_MRDR_product_plus_local_QA_not_ice_detection',quantity='official_BD1500_2_and_acquisition_support',value='13284 map centres numeric;13169 source centres in ROI;5source observations',units='dimensionless parameter; centre counts not area/probability',url_or_doi='https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources ; https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/ ; https://pds-geosciences.wustl.edu/missions/mro/crism_summary_parameter_reference.pdf',product_id='T1811_MRRAL/MRRSU/MRRDE_60N243_0327_4; software1.03.94',source_locator='PDS IMAGE bands, IMAGE_MAP_PROJECTION; official reference July2026 pp1–2,5; catalogue processing sections; exact byte ranges in extraction plan',period='5source dates2006-12-01 to2014-07-26; product creation2023-07-18 is NOT observation date',depth_support='optical surface/atmosphere sensitivity; no covered subsurface depth truth',resolution_or_scale='native MRDR grid180.4662m; product sphere3381164.4m; resampling not native optical PSF',effective_extent='fixed ROI grid centres;115 boundary remaps excluded from strict-source mask; not validated complete optical footprint',ice_presence_assessment='unknown; official negative parameters are not ice-absence or detection bounds',actual_ice_depth_m='unknown',ice_content_fraction='unknown',dependencies_json=json.dumps(['CRISM observations reused; not independent of LV-ICE06','MRDR v4 radiative transfer/volcano scan','MARCI/opacity and strip normalization assumptions']),assumptions='native PDS projection independently HDR-checked; official processing documented but not reproduced end-to-end; labels commented flags not per-pixel QA',alternative_explanations='cloud/frost,aerosol/mineral/instrument residuals and strip normalization; current formula differs from official summary for unproven reasons',limits='source bbox east longitude inconsistent; no validated local cloud mask or detection threshold; calculated-minus-official maxabs~0.01935 retained; ice/depth/content unknown',evidence_path='official_resources/README.md;official_resources/mrdr_qa.json;official_resources/source_observations.csv;official_resources/F-RES01_MRDR_quality_and_parameters.png');a.append(x);write(P/'mars_ice_evidence.csv',a,f)
a,f=read(P/'search_log.csv');a=[x for x in a if not x['log_id'].startswith('LV-RES-')]
for i,r in enumerate(json.loads((O/'retrievals.json').read_text())):
 status=r['status'];result=r.get('error','original bytes/SHA retained; source-specific read scope in official_resources/README.md');path=O/r['file']
 if path.suffix=='.json' and path.exists():
  try:
   data=json.loads(path.read_text()).get('ODEResults',{})
   if data.get('Status')=='ERROR':status='invalid_query_not_zero_coverage';result=data.get('Error','API error')
   elif 'Count' in data:result='API Count='+str(data['Count'])+'; metadata/index response, not ice detection; source bbox caveats apply'
  except (ValueError,AttributeError):pass
 a.append(dict(log_id=f'LV-RES-{i+1:03}',date_taipei='2026-11-15',platform='public HTTP; acquired UTC '+r['utc'],query_or_url=r['url'],status=status,actual_read_scope='official_resources/'+r['file']+'; HTTP '+str(r.get('http_status','unknown'))+'; Range '+str(r.get('request_headers',{}).get('Range','none')),result=result,spatial_basis='fixed ROI native projection; in-map and in-source support separated; metadata bbox not assumed true coverage'))
write(P/'search_log.csv',a,f);print('LV-ICE12 added/updated; acquisition log appended; previous rows retained')
