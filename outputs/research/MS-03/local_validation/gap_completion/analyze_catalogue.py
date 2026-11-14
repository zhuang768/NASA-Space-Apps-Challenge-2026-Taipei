"""Original author XLSX cached cells -> reproducible, bounded point membership.
No workbook editing. No imputation of uncatalogued impact or ice absence.
"""
from pathlib import Path
import csv,json,hashlib,zipfile,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent
p=O/'sources/Daubar_2022_catalog_tableS1.xlsx';raw=p.read_bytes()
assert hashlib.md5(raw).hexdigest()=='4d1b49c2e62785a1b4efb73b2040de4d'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(p) as z:
    strings=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        strings=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
    rows=[]
    for r in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('m:sheetData/m:row',ns):
        d={}
        for c in r.findall('m:c',ns):
            v=c.find('m:v',ns);t=c.get('t');s=v.text if v is not None else ''
            if t=='s':s=strings[int(s)]
            elif t=='inlineStr':s=''.join(c.find('m:is',ns).itertext())
            d[''.join(x for x in c.get('r') if x.isalpha())]=s
        rows.append((int(r.get('r')),d))
header=rows[0][1];data=[]
for rn,d in rows[1:]:
    lat=float(d['B']);lon=float(d['C'])
    assert -90<=lat<=90 and 0<=lon<360
    inside=57.5<=lat<=58 and 242<=lon<=242.5
    data.append(dict(source_excel_row=rn,HiRISE_observation_id=d.get('A',''),latitude_deg_planetocentric=lat,longitude_deg_east=lon,ice_exposing_flag_original=d.get('H',''),reference_original=d.get('T',''),inside_fixed_roi=str(inside).lower(),scope='catalogued impact point; not image footprint'))
with (O/'daubar2022_membership.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=data[0]);w.writeheader();w.writerows(data)
hits=[x for x in data if x['inside_fixed_roi']=='true']
flags={x:sum(r['ice_exposing_flag_original']==x for r in data) for x in sorted(set(r['ice_exposing_flag_original'] for r in data))}
q=dict(source_doi='10.5281/zenodo.6604912',paper_doi='10.1029/2021JE007145',source_sha256=hashlib.sha256(raw).hexdigest(),license='CC-BY-4.0 per author record metadata',original_headers=header,original_header_issue='B has Latitude (deg E, centric), C has Longitude (deg N): parenthetical cardinal-unit labels conflict with variable names. Coordinates read by variable name and independently checked against official HiRISE product PSP_007561_1290; original labels preserved.',rows=len(data),point_hits=len(hits),hits=hits,original_ice_flag_counts=flags,interpretation='No catalogued point in this bounded source is not no ice, no crater, no study, or no overlapping image.',selection_limit='Paper sections2–2.1: dated new impacts with before/after constraints and crater-resolving HiRISE confirmation; not equivalent to Dundas2021 TableS4 selection.',Dundas_TableS4_replacement=False,ice_presence='unknown',ice_depth_m=None,ice_fraction=None)
(O/'daubar2022_summary.json').write_text(json.dumps(q,indent=2)+'\n')
print(json.dumps(q,indent=2))
