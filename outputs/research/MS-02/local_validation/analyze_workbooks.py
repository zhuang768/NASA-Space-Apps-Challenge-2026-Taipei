"""Read every legacy workbook row; export independently located Wendt cores, no radar linkage."""
from pathlib import Path
import csv,json,zipfile,xml.etree.ElementTree as ET
import openpyxl
from pyproj import Transformer,Geod
P=Path(__file__).resolve().parent;repo=P.parents[3]
def write(name,heads,rows):
 with (P/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(heads);w.writerows(rows)
def main():
 f=repo/'outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx';w=openpyxl.load_workbook(f,read_only=True,data_only=True);inventory=[]
 for s in w:
  n=k=0
  for r in s.values:
   n+=any(x is not None for x in r);k+=any('MS-02' in str(x) for x in r)
  inventory.append([str(f.relative_to(repo)),s.title,n,k,'legacy context; no automatic transfer to fixed MS-02 ROI'])
 write('workbook_inventory.csv',['file','sheet','nonempty_rows','rows_mention_MS02','scope'],inventory)
 f=P/'sources/Adventdalen_data.xlsx';w=openpyxl.load_workbook(f,data_only=True)
 z=zipfile.ZipFile(f);txt=' '.join(ET.fromstring(z.read(n)).itertext() for n in []) if False else '\n'.join(' '.join(ET.fromstring(z.read(n)).itertext()) for n in z.namelist() if n.startswith('xl/drawings/') and n.endswith('.xml'))
 assert '33N' in txt and '1984' in txt
 t=Transformer.from_crs(32633,4326,always_xy=True);g=Geod(ellps='WGS84');out=[];qa=[]
 for r in list(w['Overview'].values)[1:]:
  if not r[0]:continue
  lon,lat=t.transform(r[1],r[2]);dcs=g.inv(lon,lat,15.840,78.201)[2]/1000;dade=g.inv(lon,lat,16.0613,78.1722)[2]/1000
  out.append([*r[:13],lat,lon,dcs,dade,'doi:10.5281/zenodo.11187360; Overview; README drawing WGS1984 UTM33N'])
 for s in w:
  if not s.title.startswith('Core_'):continue
  for ix,r in enumerate(list(s.values)[1:],2):
   if r[0] is None:continue
   for col,name in [(4,'VIC'),(5,'EIC'),(6,'PIC')]:
    v=r[col]
    if isinstance(v,(int,float)) and (v<0 or v>100):qa.append([s.title,ix,r[1],r[2],name,v,'vol%','outside physical 0–100 interval; preserved; do not clamp or transfer to Mars'])
 write('wendt_core_locations.csv',[*list(next(w['Overview'].values))[:13],'latitude','longitude','distance_CS1_km','distance_ADE_km','source'],out)
 write('wendt_quality_flags.csv',['sheet','excel_row','upper_cm','lower_cm','variable','value','unit','flag'],qa)
 print(json.dumps({'legacy_sheets':len(inventory),'cores':len(out),'out_of_range_fields':len(qa)}))
if __name__=='__main__':main()
