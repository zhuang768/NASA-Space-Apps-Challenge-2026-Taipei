"""Validate this literature handoff; no global screening or new science analysis."""
from pathlib import Path
import csv,json,hashlib,math,subprocess,zipfile,io,struct
root=Path(__file__).resolve().parents[3];out=root/'outputs/research/MS-03'
def rows(name):
 with (out/name).open(newline='') as f:
  r=csv.DictReader(f);ret=list(r);assert None not in r.fieldnames and all(None not in x for x in ret);return ret
c=rows('candidates.csv');assert {r['candidate_id'] for r in c}=={'MS-03-E01','MS-03-E02'}
assert all(r['mars_id']=='MS-03' for r in c)
for r in c:
 assert -90<=float(r['latitude_deg'])<=90 and -180<=float(r['longitude_east_deg'])<=180
 json.loads(r['bounds_json'])
assert abs(-(77+51.729/60)-float(c[0]['latitude_deg']))<1e-10
assert abs(160+42.606/60-float(c[0]['longitude_east_deg']))<1e-10
assert 242.25-360==-117.75
s=json.loads((out/'sources.json').read_text());ev=rows('evidence.csv');prior=rows('prior_work.csv');log=rows('search_log.csv')
for table,idfield in [(ev,'evidence_id'),(prior,'prior_id'),(log,'search_id')]:assert len({r[idfield] for r in table})==len(table)
for r in ev+prior:assert r['source_id'] in s and r['source_url']==s[r['source_id']]['url']
for r in prior:assert r['classification'] in ['direct_precedent','partial_overlap','different_use','insufficient_evidence']
for cid in ['MS-03-E01','MS-03-E02']:
 assert {r['theme'] for r in ev if r['candidate_id']==cid}>={'terrain','temperature_thermal','water_ice','atmosphere_dust'}
reference=json.loads((out/'mars_reference.json').read_text())['record']
with (root/'outputs/research/mars_reselection_20261114/final_candidates.csv').open() as f:ms=next(r for r in csv.DictReader(f) if r['candidate_id']=='MS-03')
assert float(ms['TES_TI_mean'])==reference['tes_TI_native_excluding_infill']['mean']
assert int(ms['TES_TI_valid_cells'])==79 and reference['tes_mask_zero_native_cells']==21
assert float(ms['SWIM_0_1m_mean'])==reference['swim_0_1m_native']['mean']
assert reference['MCS_context']['paired_bins']==60 and reference['MCS_context']['selected_grid_coordinate']=={'lat':60.0,'lon':-120.0}
m=json.loads((out/'manifest.json').read_text())
for item in m['inputs']:assert hashlib.sha256((root/item['path']).read_bytes()).hexdigest()==item['sha256']
a=m['downloaded_earth_asset'];b=(root/a['path']).read_bytes();assert len(b)==a['bytes'] and hashlib.sha256(b).hexdigest()==a['sha256']
z=zipfile.ZipFile(io.BytesIO(b));assert z.testzip() is None
prj=z.read('polygons_Act-IWS.prj').decode();assert 'WGS_1984_UTM_Zone_33N' in prj
# DBF record count; do not compute morphology statistics.
assert struct.unpack('<I',z.read('polygons_Act-IWS.dbf')[4:8])[0]==185
for name in ['evidence.csv','candidates.csv','prior_work.csv','search_log.csv']:assert (out/name).stat().st_size>0
print('PASS: IDs;coordinates;4themes;source crossrefs;CSV/JSON;native-vs-finalMS03;input hashes;EarthGIS ZIP/CRS/185records.')
