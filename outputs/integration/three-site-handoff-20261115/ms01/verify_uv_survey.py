#!/usr/bin/env python3
"""MS-01: pair map points with published University Valley depth survey, not logger records."""
import argparse, csv, hashlib, io, json, math, pathlib, urllib.request, zipfile
URL='https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S095410201200123X/resource/name/S095410201200123X.zip'
ENTRY='S095410201200123Xsup003.txt'
EXPECTED_SHA='773e68eb9fc63c4c1e7c771a057d2507ad0f2a237f4b1cb8f3b544bc32537517'
COORDS=[
    ('A',-(77+51.584/60),160+43.019/60,'D36','S8'),
    ('B',-(77+51.946/60),160+43.720/60,'S8','D36'),
    ('M',-(77+51.773/60),160+43.527/60,'M22','M22'),
    ('W',-(77+51.729/60),160+42.606/60,'','W42'),
]
def distance(a,b,c,d):
    a,b,c,d=map(math.radians,(a,b,c,d))
    h=math.sin((a-c)/2)**2+math.cos(a)*math.cos(c)*math.sin((b-d)/2)**2
    return 2*6371008.8*math.asin(math.sqrt(h))
def number(x):
    try:
        y=float(x)
        return y if y!=-999 and math.isfinite(y) else None
    except ValueError:
        return None
p=argparse.ArgumentParser(); p.add_argument('--archive',type=pathlib.Path,required=True)
p.add_argument('--output',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent)
a=p.parse_args()
if not a.archive.exists():
    with urllib.request.urlopen(URL,timeout=30) as r: a.archive.write_bytes(r.read())
b=a.archive.read_bytes()
assert hashlib.sha256(b).hexdigest()==EXPECTED_SHA
with zipfile.ZipFile(io.BytesIO(b)) as z:
    assert z.testzip() is None
    data=z.read(ENTRY)
rows=list(csv.reader(io.StringIO(data.decode())))
assert rows[0][0]=='DepthToPermafrost_UniversityValley_data'
assert rows[1][13]=='RawPitDepths[cm]'
points=[]
for i,row in enumerate(rows[2:],3):
    if len(row)<22 or number(row[0]) is None: continue
    a0,b0,h,s=map(number,(row[0],row[1],row[3],row[4]))
    raw=[number(val) for val in row[5:21]]
    finite=[x for x in raw if x is not None]
    notes=row[21].strip()
    lower='ice not reached' in notes.lower()
    assert abs(sum(finite)/len(finite)-h)<0.051
    points.append((i,a0,b0,h,s,lower,finite,notes))
assert len(points)==68
results=[]
for anchor,lat,lon,dep,paper in COORDS:
    ordered=sorted((distance(lat,lon,alat,alon),i,alat,alon,d,sd,lim,arr,notes)
                   for i,alat,alon,d,sd,lim,arr,notes in points)
    for rank,(r,i,alat,alon,d,sd,lim,arr,notes) in enumerate(ordered[:5],1):
        results.append(dict(anchor=anchor,deployment_2009=dep,paper_2022_2026=paper,anchor_lat=lat,anchor_lon=lon,
            neighbour_rank=rank,published_text_line=i,published_lat=alat,published_lon=alon,
            distance_m=round(r,3),same_coordinate_at_6_decimals=(round(lat,6)==alat and round(lon,6)==alon),
            ice_depth_published_cm=d,ice_depth_stddev_cm=sd,depth_is_lower_bound=lim,
            measured_depths_cm=';'.join(map(str,arr)),published_notes=notes))
assert [(r['published_text_line'],r['measured_depths_cm']) for r in results if r['same_coordinate_at_6_decimals']]==[(22,'40.0;44.0;44.0'),(14,'21.0;20.5;32.0;23.5;24.0')]
a.output.mkdir(parents=True,exist_ok=True)
with (a.output/'university_valley_coordinate_crosscheck.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(results[0])); w.writeheader(); w.writerows(results)
provenance={'publisher_zip_url':URL,'zip_sha256':EXPECTED_SHA,'zip_bytes':len(b),'entry':ENTRY,
    'entry_bytes':len(data),'entry_sha256':hashlib.sha256(data).hexdigest(),'entry_md5':hashlib.md5(data).hexdigest(),
    'source_rows':len(points),'censored_lower_bounds':sum(p[5] for p in points),'earth_radius_m':6371008.8,
    'source_note':'Publisher geometry cross-check, not GPS/serial attribution or proof of relocated sensor. Separate USAP-DC file advertises another MD5; bytes were not acquired, no byte-equivalence asserted.'}
(a.output/'university_valley_coordinate_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps(provenance,indent=2))
