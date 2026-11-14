"""Select actual USGEOM table rows in the fixed ROI; not an echo/ice analysis."""
from pathlib import Path
import csv,gzip,hashlib,json
HERE=Path(__file__).resolve().parent
raw=gzip.decompress((HERE/'inputs/s_01958801_geom.tab.gz').read_bytes())
assert len(raw)==5210*100
rows=[]
for line in raw.decode('ascii').splitlines():
    fields=next(csv.reader([line]));assert len(fields)==10
    col=int(fields[0]);lat=float(fields[2]);lon=float(fields[3])
    if 56.5<=lat<57 and 72.5<=lon<73:
        rows.append(dict(column_label=col,UTC=fields[1],latitude_n=lat,longitude_e=lon,
            Mars_radius_km=float(fields[4]),spacecraft_radius_km=float(fields[5]),SZA_deg=float(fields[8])))
assert rows and all(b['column_label']-a['column_label']==1 for a,b in zip(rows,rows[1:]))
with (HERE/'sharad_actual_geometry_rows.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
base='https://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v2/mrosh_2101/data/geom/s_0195xx/'
result=dict(product='S_01958801_GEOM',source_url=base+'s_01958801_geom.tab',label_url=base+'s_01958801_geom.lbl',
    source_sha256=hashlib.sha256(raw).hexdigest(),total_rows=5210,selected_rows=len(rows),first=rows[0],last=rows[-1],
    source_locator='LBL TABLE columns1–4:column/time/latitude/longitude;start_byte1/7/31/40;TAB100bytes×5210rows',
    coordinates='Planetocentric,east-positive per official USGEOM product description;degrees',
    method='Parse actual ASCII table;half-open fixedROI mask;no timing transfer to ItalianRDR processing',
    limits=['Locations refer to radargram columns,not echo picks,beam area,independent ice detections or depth',
            'No radargram IMG or calibrated DAT parsed;no clutter simulation or dielectric inversion',
            'USV2 and ItalianRDR times/column definitions differ;not joined by observation-prefix alone'])
(HERE/'sharad_actual_geometry.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(selected=len(rows),first=rows[0],last=rows[-1]),indent=2))
