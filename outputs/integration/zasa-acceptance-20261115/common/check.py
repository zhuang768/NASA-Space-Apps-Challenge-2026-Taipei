import math,json,csv
from pathlib import Path
out=Path(__file__).parent
R=3389.5
boxes={'MS01':(56.5,57,72.5,73),'MS02':(52.5,53,168,168.5),'MS03':(57.5,58,242,242.5)}
obs=[('Phoenix',68.219,234.249,'Excavated ice; mechanical, spectral and chemical confirmation','https://doi.org/10.1029/2009JE003417'),('Dundas2021_Table1_A',46.35,176.89,'Impact site with icy color; morphology depths not direct ice abundance','https://doi.org/10.1029/2020JE006617'),('Dundas2021_Table1_B',44.22,164.20,'Impact site with icy color; morphology depths not direct ice abundance','https://doi.org/10.1029/2020JE006617'),('Dundas2021_Table1_C',50.51,265.2,'Impact site with icy color; morphology depths not direct ice abundance','https://doi.org/10.1029/2020JE006617'),('Dundas2021_Table1_D',39.11,190.25,'Impact site with icy color; morphology depths not direct ice abundance','https://doi.org/10.1029/2020JE006617'),('Dundas2021_Table1_E',47.43,112.01,'Impact site with icy color; morphology depths not direct ice abundance','https://doi.org/10.1029/2020JE006617'),('Dundas2021_Fig14a',41.4,48.8,'Ice-exposing impact in lineated valley fill ESP_046707_2220','https://doi.org/10.1029/2020JE006617'),('Dundas2021_Fig14b',41.9,36.4,'Ice-exposing impact in lineated valley fill ESP_046747_2220','https://doi.org/10.1029/2020JE006617')]
def dist(a,b):
 a1,o1,a2,o2=map(math.radians,(*a,*b));return 2*R*math.asin(math.sqrt(math.sin((a2-a1)/2)**2+math.cos(a1)*math.cos(a2)*math.sin((o2-o1)/2)**2))
with (out/'observations.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['observation','latitude_planetocentric_N','longitude_E','type','source','inside_MS01','inside_MS02','inside_MS03','distance_to_MS01_center_km','distance_to_MS02_center_km','distance_to_MS03_center_km'])
 for name,lat,lon,kind,url in obs:
  w.writerow([name,lat,lon,kind,url,*[lo<=lat<=hi and west<=lon<=east for lo,hi,west,east in boxes.values()],*[round(dist((lat,lon),((lo+hi)/2,(west+east)/2)),1) for lo,hi,west,east in boxes.values()]])
print((out/'observations.csv').read_text())
