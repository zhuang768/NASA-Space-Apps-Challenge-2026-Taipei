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
# Optional W follow-up: independent checks on serialized delivery and summary.
uv=out/'uv_w'
if (uv/'qa.json').exists():
 import gzip,statistics,datetime as D
 q=json.loads((uv/'qa.json').read_text());d=json.loads((uv/'download_manifest.json').read_text())
 assert d['record_id']==10553882 and d['license']['id']=='cc-zero' and len(d['files'])==6
 with gzip.open(uv/'hobo_W_temperatures.csv.gz','rt',newline='') as f:rr=list(csv.DictReader(f))
 assert len(rr)==27553 and len({r['time_naive'] for r in rr})==len(rr)
 assert all(r['time_label'].startswith('GMT+13:00') for r in rr)
 assert rr[0]['T20_C']=='-8.530' and rr[0]['T42_C']=='-13.352'
 assert rr[-1]['T20_C']=='-11.831' and rr[-1]['T42_C']=='-12.602'
 window=[r for r in rr if '2010-01-01T00:00:00'<=r['time_naive']<'2011-01-01T00:00:00'];assert len(window)==8760
 paired=[float(r['T20_C'])-float(r['T42_C']) for r in window if r['T20_C'] and r['T42_C']];assert len(paired)==8759
 with (uv/'earth_only_2010_summary.csv').open() as f:summary={r['metric']:r for r in csv.DictReader(f)}
 assert math.isclose(statistics.fmean(paired),float(summary['T20_minus_T42_C']['mean']),abs_tol=1e-12)
 assert int(summary['T42_C']['finite_n'])==8759
 assert q['records']['Campbell']['decimal_day_minus_timestamp_regimes'][-1]['offset_hours_decimal_minus_timestamp']==-5
 assert q['records']['HOBO']['gaps']==[]
 for f in d['files']:
  raw=Path(d['raw_directory'])/f['filename']
  if raw.exists():assert hashlib.md5(raw.read_bytes()).hexdigest()==f['md5'] and hashlib.sha256(raw.read_bytes()).hexdigest()==f['sha256']
 print('PASS: W pinned6source hashes where local;header mapping first/last samples;27553rows;2010window8760;8759pairs;summary reproduction;clock limits retained.')
