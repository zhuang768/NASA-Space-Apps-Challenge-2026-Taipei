"""Update current acquisition status while retaining the previous catalogue-only records."""
from pathlib import Path
import csv,json
O=Path(__file__).resolve().parent;P=O.parent
q=json.loads((O/'qa.json').read_text());ps={x['product_id']:x for x in q['products']}
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);return list(r),r.fieldnames
def write(p,r,fields):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(r)
h=O/'previous_catalogue_status.json'
if not h.exists():
 a,_=read(P/'mars_ice_evidence.csv');b,_=read(P/'observation_inventory.csv');h.write_text(json.dumps({'starting_sha':'778af696c654a191fe2a720f24d9f30ebd7d247b','previous_ice_record':next(x for x in a if x['evidence_id']=='LV-ICE06'),'previous_observation_rows':[x for x in b if x['product_id'] in ps]},indent=2)+'\n')
a,f=read(P/'mars_ice_evidence.csv')
for x in a:
 if x['evidence_id']=='LV-ICE06':
  x.update(evidence_type='catalogue_plus_two_acquired_local_spectral_subsets',quantity='CRISM_products_catalogued_and_two_local_subsets_QA',value='168 catalogue products /44 observations;2LIF subsets;966 and8516 basic-valid pixel centres',units='product and pixel counts; no ice fraction or probability',product_id='HSP0002DE65_03_IF218L_TRR3;MSP00018FDA_01_IF214L_TRR3; matching DDR1/WA3',source_locator='TRR3 IMAGE/ROWNUM_TABLE; DDR IMAGE bands4/5; WA IMAGE in nm; PDS SIS §§3.2.1,3.4.1,3.9.1/Table3-3',period='2014-02-10T17:28:23.764 to17:31:23.693 and2010-05-25T09:48:43.578 to09:51:43.515; two observations only',depth_support='optical surface/atmosphere signal; no covered subsurface depth sensitivity demonstrated',resolution_or_scale='10x spatial binning; actual adjacent DDR centre spacing median187.80/187.44m; not PSF',effective_extent='fixed cell;1350/9056 DDR centres;966/8516 pass basic checks; not whole-cell quality coverage',ice_presence_assessment='unknown; uncorrected spectra do not establish surface or subsurface ice',assumptions='DDR near2300nm reference positions used; wavelength-dependent keystone uncorrected; native spectral samples retained',alternative_explanations='atmospheric gases/cloud, seasonal frost, mineral absorptions, illumination and instrument residuals',limits='Atmospheric/thermal/photometric corrections OFF; no validated cloud/frost mask or detection threshold; sparse mapping channels; no standard ice index or absence inference',evidence_path='crism/qa.json;crism/channel_qa.csv;crism/roi_pixels.csv.gz;crism/F-CRISM01_pixel_QA_spectra.png;crism/previous_catalogue_status.json')
write(P/'mars_ice_evidence.csv',a,f)
a,f=read(P/'observation_inventory.csv')
for x in a:
 if x['product_id'] in ps:
  x['science_pixels_downloaded']='partial: all64samples and allbands for documented ROI-intersecting rows; matching full DDR+WA acquired'
  x['quality_limit']='Basic numeric/calibration/geometry QA only; corrections OFF; cloud/frost/ice detection unknown; see crism/qa.json'
write(P/'observation_inventory.csv',a,f)
a,f=read(P/'search_log.csv');a=[x for x in a if not x['log_id'].startswith('LV-CRISM-')]
new=[]
for i,r in enumerate(json.loads((O/'retrievals.json').read_text())):
 new.append(dict(log_id=f'LV-CRISM-{i+1:03}',date_taipei='2026-11-15',platform='urllib public PDS/ODE; timestamp '+r['utc'],query_or_url=r['url'],status=r['status'],actual_read_scope='crism/'+r['file']+'; HTTP '+str(r.get('http_status','unknown'))+'; Range '+str(r['request_headers'].get('Range','none')),result=r.get('error','original bytes and SHA256 retained; content interpreted only within documented scope'),spatial_basis='DDR fixed-cell pixel-centre selection; access/SSL/404 failure is not zero coverage'))
a+=new;write(P/'search_log.csv',a,f)
print('Updated two acquired product statuses and LV-ICE06; retained previous records; appended',len(new),'request records')
